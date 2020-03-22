import os
import pycrfsuite
from nltk.tokenize import TreebankWordTokenizer as twt
from xml.etree import ElementTree
from extract_featuresL2 import extract_features

# True will obtain features from the external files too (goal5)
# If false will not obtain them (goal4)
EXTERNAL_FILE = False

def parseXML(file, inputdir):
    tree = ElementTree.parse(inputdir+file)
    return tree.getroot()

def get_sentence_info(sentence):
    return sentence.attrib["id"], sentence.attrib["text"]

def tokenize(text):
    span_generator = twt().span_tokenize(text)
    tokens = []
    for s in span_generator:
        tokens.append((text[s[0]:s[1]], s[0], s[1]-1))
    return tokens

def get_ground_truth_label(token_list, sentence):
    #return the supposed label for each detected element (not O) of the sentence
    #only used for the training part
    list_ofset = []
    entities = sentence.getchildren()
    if len(entities)!=0:
        for entity in entities:
            if entity.tag=='entity':
                list_ofset.append(entity.attrib['charOffset'].split('-'))

    ground = []
    previous=0
    for ind2, token in enumerate(token_list):
        g='O' #assign O first, if it's any kind of drug it will stay like this
        for ind, off in enumerate(list_ofset):
            if len(off[1].split(';'))==1:
                if token[1]>=int(off[0]) and token[2]<=int(off[1]):
                    g=entities[ind].attrib['type']
                    previous+=1
                else:
                    previous=0
            else:   # there are some elements assigned to more than one
                    # to these elements only assign the last tag that have appeared
                sep_off = [off[0], off[1].split(';')[0], off[1].split(';')[1], off[2]]
                if token[1]>=int(sep_off[0]) and token[2]<=int(sep_off[1]):
                    g=entities[ind].attrib['type']
                    previous+=1
                elif token[1]>=int(sep_off[2]) and token[2]<=int(sep_off[3]):
                    g=entities[ind].attrib['type']
                    previous+=1
                else:
                    previous=0

        # add the BI tags
        if g != 'O':
            if previous == 1:
                g='B-'+g
            else:
                g='I-'+g
        ground.append(g)

    return ground


def output_features(id, s, ents, gold_class, trainfile):
    for ind, token in enumerate(s):
        sentence_features = id +'\t'+ token[0] +'\t'+ str(token[1]) +' '+ str(token[2]) +'\t'+ gold_class[ind] +'\t'
        for feat in ents[ind]:
            sentence_features = sentence_features+' '+ str(feat)
        sentence_features = sentence_features+'\n'
        trainfile.write(sentence_features)


def train(traindata, labels):
    trainer = pycrfsuite.Trainer(verbose=False)
    for xseq, yseq in zip(traindata, labels):
        trainer.append(xseq, yseq)

    trainer.set_params({
        'c1': 1.0,   # coefficient for L1 penalty
        'c2': 1e-3,  # coefficient for L2 penalty
        # as we have a considerable quantity of features to train from
        # the training should be longer
        'max_iterations': 3000,
        # include transitions that are possible, but not observed
        'feature.possible_transitions': True
    })

    trainer.train('model_trained_goal4.crfsuite')
    print(trainer.logparser.last_iteration)

def predict(feat):
    # predicts the tag for the word given the features
    predictor = pycrfsuite.Tagger()
    predictor.open('model_trained_goal4.crfsuite')
    return predictor.tag(feat)


def output_entities(id_, token_list, pred, foutput):
    # if it's not waiting will print the BI elements without the marks
    wait = False #while it's waiting will not print the elements
    name = ''
    off_start = '0'
    element = {'name':'', 'offset':'', 'type':''}
    for ind, token in enumerate(token_list):
        if pred[ind]=='O': #if it's a O element, we do nothing
            wait = True
        elif ind == len(token_list)-1: #if it's the last element of the sentence
            if pred[ind].startswith('B'):
                element = {'name': token[0],
                          'offset': str(token[1]) + '-' + str(token[2]),
                          'type': pred[ind].split('-')[1] #without B or I
                          }
            elif pred[ind].startswith('I'):
                element = {'name': name+' '+token[0],
                          'offset': off_start + '-' + str(token[2]),
                          'type': pred[ind].split('-')[1]
                          }
            else: #only to check
                print('There\'s something wrong')
            wait = False

        else:
            if( (pred[ind].startswith('B') and pred[ind+1].startswith('O')) or
                    (pred[ind].startswith('B') and pred[ind+1].startswith('B')) ):
                element = {'name': token[0],
                          'offset': str(token[1]) + '-' + str(token[2]),
                          'type': pred[ind].split('-')[1] #without B or I
                          }
                wait = False
            elif pred[ind].startswith('B') and pred[ind+1].startswith('I'):
                name = token[0]
                off_start = str(token[1])
                wait = True
            elif( (pred[ind].startswith('I') and pred[ind+1].startswith('O')) or
                (pred[ind].startswith('I') and pred[ind+1].startswith('B')) ):
                element = {'name': name+' '+token[0],
                          'offset': off_start + '-' + str(token[2]),
                          'type': pred[ind].split('-')[1]
                          }
                if pred[ind-1]=='O':
                    element["name"]=token[0]
                wait = False
            elif pred[ind].startswith('I') and pred[ind+1].startswith('I'):
                name = name+' '+token[0]
                wait = True
            else: #only to check
                print('There\'s something wrong2')

        if not wait:
            foutput.write(id_ + '|' + element['offset'] + '|' + element['name'] + '|' + element['type'] + '\n')


def evaluate(input_dir, output_file):
    os.system('java -jar eval/evaluateNER.jar ' + input_dir + ' ' + output_file)


def main():
    # TRAIN
    traindir = "./data/Train/"
    if EXTERNAL_FILE:
        trainfile = "./train_elements_9.5_lluis_1.txt"
    else:
        trainfile = "./train_elements_9.5_lluis_1.txt"
    if os.path.exists(traindir):
        trainfiles = os.listdir(traindir)
    traindata = [] #where all the features are saved
    labels = [] #where the ground truth of the train data labels will be
    t = open(trainfile, "a")
    for file in trainfiles:
        root = parseXML(file, traindir)
        for sentence in root:
            (id, text) = get_sentence_info(sentence)
            token_list = tokenize(text)
            features = extract_features(token_list, EXTERNAL_FILE)
            traindata.append(features)
            type_ground = get_ground_truth_label(token_list, sentence)
            labels.append(type_ground)
            output_features(id, token_list, features, type_ground, t)
    train(traindata, labels)
    t.close()

    for n in range(6):
        # PREDICT
        #two different files for the two goals of the lab2
        if EXTERNAL_FILE:
            output = "./task9.5_lluis_1"
        else:
            output = "./task9.4_lluis_1"
        # for test in ["Devel", "Test-NER", "Test-DDI"]:
        for test in ["Devel"]:
            outputfile = output+'_'+test+'.txt'
            f = open(outputfile, "a")
            testdir = "./data/"+test+"/"
            if os.path.exists(testdir):
                testfiles = os.listdir(testdir)
            testdata = [] #where all the features are saved
            for file in testfiles:
                root = parseXML(file, testdir)
                for sentence in root:
                    (id, text) = get_sentence_info(sentence)
                    token_list = tokenize(text)
                    features = extract_features(token_list, EXTERNAL_FILE)
                    y_pred = predict(features)
                    output_entities(id, token_list, y_pred, f)
            f.close()
            evaluate(testdir, outputfile)

if __name__ == "__main__":
    main()
