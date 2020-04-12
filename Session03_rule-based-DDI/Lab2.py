import os
import pycrfsuite
from nltk.tokenize import TreebankWordTokenizer as twt
from xml.etree import ElementTree
from extract_featuresL2 import extract_features

# True will obtain features from the external files too (goal5)
# If false will not obtain them (goal4)
USE_EXTERNAL_RESOURCES = True


def parseXML(file, inputdir):
    tree = ElementTree.parse(inputdir + file)
    return tree.getroot()


def get_sentence_info(sentence):
    return sentence.attrib["id"], sentence.attrib["text"]


def tokenize(text):
    span_generator = twt().span_tokenize(text)
    tokens = []
    for s in span_generator:
        tokens.append((text[s[0]:s[1]], s[0], s[1] - 1))
    return tokens


def get_ground_truth_label(token_list, sentence):
    """
        Only used for the training part
        The idea is to return collect the ground truth of the sentence in a list
        separating the words grouped by the spacebar, go word by word looking if they appear in the list
        and if they appear look in which position from the separation, if they don't appear it's assigned the O
    """
    list_ofset = []
    entities = sentence.getchildren()
    if len(entities) != 0:
        for entity in entities:
            if entity.tag == 'entity':
                list_ofset.append(entity.attrib['text'].split(' '))
    ground = []
    for token in token_list:
        g = 'O'
        for ind, off in enumerate(list_ofset):
            if token[0] in off:
                if len(off) > 1 and token[0] not in off[0]:
                    g = 'I-' + entities[ind].attrib['type']
                else:
                    g = 'B-' + entities[ind].attrib['type']
        ground.append(g)

    return ground


def get_external_resources():
    filename_hsdb = './resources/HSDB.txt'
    filename_drug_bank = './resources/DrugBank_partial.txt'

    with open(filename_hsdb, 'r') as f:
        drugs_data = f.readlines()
    hsdb_list = []
    for element in drugs_data:
        hsdb_list.append(element.lower().rstrip())

    with open(filename_drug_bank, 'r', encoding="utf8") as g:
        data = g.readlines()

    drug_bank = {}
    for sentence in data:
        split_sentence = sentence.rsplit('|', 1)
        drug_bank[split_sentence[0]] = split_sentence[-1].rstrip()

    return hsdb_list, drug_bank


def output_features(id, s, ents, gold_class):
    for ind, token in enumerate(s):
        sentence_features = id + '\t' + token[0] + '\t' + str(token[1]) + '\t' + str(token[2]) + '\t' + gold_class[ind]
        for feat in ents[ind]:
            sentence_features = sentence_features + '\t' + str(feat)
        sentence_features = sentence_features + '\n'
        # sys.stdout.write(sentence_features)


def train(traindata, labels):
    trainer = pycrfsuite.Trainer(verbose=False)
    for xseq, yseq in zip(traindata, labels):
        trainer.append(xseq, yseq)

    trainer.set_params({
        'c1': 0.2,  # coefficient for L1 penalty
        'c2': 1e-3,  # coefficient for L2 penalty
        # as we have a considerable quantity of features to train from
        # the training should be longer
        'max_iterations': 200,
        # include transitions that are possible, but not observed
        'feature.possible_transitions': True
    })

    if USE_EXTERNAL_RESOURCES:
        trainer.train('model_trained_goal5.crfsuite')
    else:
        trainer.train('model_trained_goal4.crfsuite')
    print(trainer.logparser.last_iteration)


def predict(feat):
    # predicts the tag for the word given the features
    predictor = pycrfsuite.Tagger()
    if USE_EXTERNAL_RESOURCES:
        predictor.open('model_trained_goal5.crfsuite')
    else:
        predictor.open('model_trained_goal4.crfsuite')

    return predictor.tag(feat)


def output_entities(id_, token_list, pred, foutput):
    # if it's not waiting will print the BI elements without the marks
    # in order to not print the O's or print together the BI
    wait = False  # while it's waiting will not print the elements
    name = ''
    off_start = '0'
    element = {'name': '', 'offset': '', 'type': ''}
    for ind, token in enumerate(token_list):
        if pred[ind] == 'O':  # if it's a O element, we do nothing
            wait = True
        elif ind == len(token_list) - 1:  # if it's the last element of the sentence
            if pred[ind].startswith('B'):
                element = {'name': token[0],
                           'offset': str(token[1]) + '-' + str(token[2]),
                           'type': pred[ind].split('-')[1]  # without B or I
                           }
            elif pred[ind].startswith('I'):
                element = {'name': name + ' ' + token[0],
                           'offset': off_start + '-' + str(token[2]),
                           'type': pred[ind].split('-')[1]
                           }
                if name == '' and ind != len(token_list) - 1:
                    element["name"] = token[0]
                wait = False
            else:  # only to check
                print('There\'s something wrong')
            wait = False

        else:
            if ((pred[ind].startswith('B') and pred[ind + 1].startswith('O')) or
                    (pred[ind].startswith('B') and pred[ind + 1].startswith('B'))):
                element = {'name': token[0],
                           'offset': str(token[1]) + '-' + str(token[2]),
                           'type': pred[ind].split('-')[1]  # without B or I
                           }
                wait = False
            elif pred[ind].startswith('B') and pred[ind + 1].startswith('I'):
                name = token[0]
                off_start = str(token[1])
                wait = True
            elif ((pred[ind].startswith('I') and pred[ind + 1].startswith('O')) or
                  (pred[ind].startswith('I') and pred[ind + 1].startswith('B'))):
                element = {'name': name + ' ' + token[0],
                           'offset': off_start + '-' + str(token[2]),
                           'type': pred[ind].split('-')[1]
                           }
                if name == '':
                    element["name"] = token[0]
                wait = False
            elif pred[ind].startswith('I') and pred[ind + 1].startswith('I'):
                if name == '':
                    name = token[0]
                else:
                    name = name + ' ' + token[0]
                wait = True
            else:  # only to check
                print('There\'s something wrong2')

        if not wait:
            foutput.write(id_ + '|' + element['offset'] + '|' + element['name'] + '|' + element['type'] + '\n')


def evaluate(input_dir, output_file):
    os.system('java -jar eval/evaluateNER.jar ' + input_dir + ' ' + output_file)


def main():
    # TRAIN
    traindir = "./data/Train/"
    if os.path.exists(traindir):
        trainfiles = os.listdir(traindir)
    traindata = []  # where all the features are saved
    labels = []  # where the ground truth of the train data labels will be
    # extracts elements from external resources
    hsdb_list = None
    drug_bank = None
    if USE_EXTERNAL_RESOURCES:
        hsdb_list, drug_bank = get_external_resources()
    for file in trainfiles:
        root = parseXML(file, traindir)
        for sentence in root:
            (id, text) = get_sentence_info(sentence)
            token_list = tokenize(text)
            features = extract_features(token_list, hsdb_list, drug_bank)
            traindata.append(features)
            type_ground = get_ground_truth_label(token_list, sentence)
            labels.append(type_ground)
            output_features(id, token_list, features, type_ground)
    train(traindata, labels)

    # PREDICT
    # three different files for the two goals of the lab2
    if USE_EXTERNAL_RESOURCES:
        output = "./task9.5_lluis_1"
    else:
        output = "./task9.4_lluis_1"
    for test in ["Devel", "Test-NER", "Test-DDI"]:
        outputfile = output + '_' + test + '.txt'
        f = open(outputfile, "w")
        testdir = "./data/" + test + "/"
        if os.path.exists(testdir):
            testfiles = os.listdir(testdir)
        for file in testfiles:
            root = parseXML(file, testdir)
            for sentence in root:
                (id, text) = get_sentence_info(sentence)
                token_list = tokenize(text)
                features = extract_features(token_list, hsdb_list, drug_bank)
                y_pred = predict(features)
                output_entities(id, token_list, y_pred, f)
        f.close()
        evaluate(testdir, outputfile)


if __name__ == "__main__":
    main()
