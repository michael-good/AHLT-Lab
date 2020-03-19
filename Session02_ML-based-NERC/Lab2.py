import os, sys
import pycrfsuite
from nltk.tokenize import TreebankWordTokenizer as twt
from IPython import embed
from xml.etree import ElementTree

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

def extract_features(s):
    features = []
    for ind, word in enumerate(s):
        feat = []
        # word itself
        feat.append('form='+ word[0])

        # last 4 letters
        if len(word[0])>4:
            feat.append('suf4='+ word[0][-4:])
        else:
            feat.append('suf4='+ word[0])

        # next word
        if ind==len(s)-1:
            feat.append('next=_EoS_')
        else:
            feat.append('next='+ s[ind+1][0])

        # previous word
        if ind==0:
            feat.append('prev=_BoS_')
        else:
            feat.append('prev='+ s[ind-1][0])

        # if punctuation
        if (not word[0].isalpha() and not word[0].isdigit()):
            feat.append('punct')

        # length of the word
        feat.append('len='+ str(word[2]-word[1]))

        #if capitalized or all capitalized
        upper=0
        letter=0
        for let in word[0]:
            if let.isalpha():
                letter+=1
            if let.isupper():
                upper+=1
        if upper > 0:
            if upper == letter:
                feat.append('allCapitalized')
            else:
                feat.append('capitalized')

        features.append(feat)

    return features

def get_ground_truth_label(token_list, sentence):
    list_ofset = []
    entities = sentence.getchildren()
    if len(entities)!=0:
        for entity in entities:
            if entity.tag=='entity':
                list_ofset.append(entity.attrib['charOffset'].split('-'))

    ground = []
    for token in token_list:
        g='O'
        for ind, off in enumerate(list_ofset):
            if len(off[1].split(';'))==1:
                if token[1]>=int(off[0]) and token[2]<=int(off[1]):
                    g=entities[ind].attrib['type']

            else:
                sep_off = [off[0], off[1].split(';')[0], off[1].split(';')[1], off[2]]
                if token[1]>=int(sep_off[0]) and token[2]<=int(sep_off[1]):
                    g=entities[ind].attrib['type']
                if token[1]>=int(sep_off[2]) and token[2]<=int(sep_off[3]):
                    g=entities[ind].attrib['type']

        ground.append(g)
    return ground

def output_features(id, s, ents, gold_class):
    for ind, token in enumerate(s):
        sys.stdout.write( id +'\t'+ token[0] +'\t'+ str(token[1]) +'\t'+ str(token[2]) +'\t'+ gold_class[ind])
        for feat in ents[ind]:
            sys.stdout.write('\t'+ str(feat))
        sys.stdout.write('\n')

def train(traindata, labels):
    trainer = pycrfsuite.Trainer(verbose=False)
    i=0
    for xseq, yseq in zip(traindata, labels):
        trainer.append(xseq, yseq)

    trainer.set_params({
        'c1': 1.0,   # coefficient for L1 penalty
        'c2': 1e-3,  # coefficient for L2 penalty
        'max_iterations': 50,  # stop earlier
        # include transitions that are possible, but not observed
        'feature.possible_transitions': True
    })

    trainer.train('model_trainedL2.crfsuite')
    print(trainer.logparser.last_iteration)


def main():
    # TRAIN
    traindir = "./data/Train/"
    if os.path.exists(traindir):
        trainfiles = os.listdir(traindir)
    traindata = [] #where all the features are saved
    labels = [] #where the ground truth of the train data labels will be
    for file in trainfiles:
        # print(traindir+file)
        root = parseXML(file, traindir)

        for sentence in root:
            (id, text) = get_sentence_info(sentence)
            token_list = tokenize(text)
            features = extract_features(token_list)
            type_ground = get_ground_truth_label(token_list, sentence)
            traindata.append(features)
            labels.append(type_ground)
            # output_features(id, token_list, features, type_ground)
    train(traindata, labels)

    # #PREDICT
    # testdir = "./data/Devel/"
    # outputfile = "./task9.2_lluis_1.txt"
    # if os.path.exists(testdir):
    #     testfiles = os.listdir(testdir)
    # f = open(outputfile, "a")
    # for file in testfiles:
    #     print(testdir+file)
    #     tree = parseXML(file, testdir)
    #     for sentence in tree:
    #         (id, text) = get_sentence_info(sentence)
    #         token_list = tokenize(text)
    #         features = extract_features(token_list)
    #         y_pred = crf.predict(features)
    #         output_entities(id, token_list, y_pred, f)
    # f.close()
    # evaluate(testdir, outputfile)

if __name__ == "__main__":
    main()
