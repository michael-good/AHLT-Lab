from xml.dom.minidom import parse
import sys, os
from extract_featuresL4 import extract_features
# import nltk CoreNLP module (just once)
from nltk.parse.corenlp import CoreNLPDependencyParser
# connect to your CoreNLP server (just once)
my_parser = CoreNLPDependencyParser(url="http://localhost:9000")
from nltk.classify import megam
import nltk
nltk.config_megam('C:/Users/Lluis/Desktop/MATT/AHLT/AHLT-Lab/Session04_ML-based-DDI/megam_0.92/megam.exe')

def parse_xml(file):
    return parse(file)

def getOffsets(sentence, word):
    start_index = sentence.find(word)
    end_index = start_index + len(word) -1 # if the start_index is not -1
    return start_index, end_index

def analyze(sentence):
    # parse text (as many times as needed)
    # print(sentence)
    mytree, = my_parser.raw_parse(sentence)
    # print(mytree)
    # enrich the NLPDepencyGraph with the start and end offset
    for e in range(1, len(mytree.nodes)):
        node = mytree.nodes[e]
        word = node['word']
        start_off, end_off = getOffsets(sentence, word)
        # returns start_off=-1 if didn't find the word in the sentence
        # SHOULD LOOK IF THERE'S , OR . FOR NOW ONLY RETURNS THE SPAN OF THE FIRST APPEARED
        if start_off != -1:
            node['start'] = start_off
            node['end'] = end_off
        else:
            # for now we will not touch the the braquets which are represented by
            # -lrb- and -rrb-, but then on the feature_extractor we will ignore
            # them as if they are not needed for the features
            pass
            # print(node)

    return mytree

def output_features(id, e1, e2, gold_class, features, fout):
    sentence_features = id + '\t' + e1 + '\t' + e2 + '\t' + gold_class
    for feat in features:
        sentence_features = sentence_features + '\t' + str(feat)
    sentence_features = sentence_features + '\n'
    # sys.stdout.write(sentence_features) # print in the terminal
    fout.write(sentence_features) # print in a file

def output_ddi(id, e1, e2, ddi_type, fout):
    if ddi_type == 'null':
        ddi=0
    else:
        ddi=1

    sentence_features = id + '|' + e1 + '|' + e2 + '|' + str(ddi) + '|' + ddi_type +'\n'
    fout.write(sentence_features) # print in a file

def evaluate(inputdir, outputfile):
    os.system("java -jar eval/evaluateDDI.jar " + inputdir + " " + outputfile)

import time
def predict(feat_dict, feat_test, classifier):

    # create a dictionary with the binary of the feat that appears
    feat_test_dict = {}
    for feat in feat_test:
        feat_test_dict[feat]=1;

    # save to a file
    t_test = open('te_onlyUnder.txt','w')
    t_test.write(str(feat_test_dict))
    t_test.close()

    # pred = classifier.classify_many(test)
    pred = classifier.classify(feat_test_dict)
    return pred

import numpy as np
def main():

    i=0


    # TRAIN
    traindir = './data/Train'

    train_file = 'train_features_output_onlyUnder.txt'
    if os.path.exists(train_file):
        os.remove(train_file)
    foutput = open(train_file, "a")

    # process each file in directory
    for f in os.listdir(traindir) :
        print(f)
        # parse XML file, obtaining a DOM tree
        tree = parse(traindir + "/" + f)
        # process each sentence in the file
        sentences = tree.getElementsByTagName("sentence")
        for s in sentences :
            sid = s.attributes["id"].value # get sentence id
            stext = s.attributes["text"].value # get sentence text
            # it gives an error on the raw_parser if the sentence is empty ("")
            if stext != "":
                # print('stext')
                # print(stext)

                # load sentence entities into a dictionary
                entities = {}
                ents = s.getElementsByTagName("entity")
                for e in ents :
                    id = e.attributes["id"].value
                    offs = e.attributes["charOffset"].value.split("-")
                    entities[id] = offs
                # Tokenize, tag, and parse sentence
                analysis = analyze(stext)
                # print(analysis)

                # for each pair in the sentence, decide whether it is DDI and its type
                pairs = s.getElementsByTagName("pair")
                for p in pairs:
                    id_e1 = p.attributes["e1"].value
                    id_e2 = p.attributes["e2"].value
                    features = extract_features(analysis, entities, id_e1, id_e2, i)
                    # print(features)
                    is_ddi = p.attributes["ddi"].value #get ground truth
                    if is_ddi=="true" and 'type' in p.attributes:
                        type = p.attributes["type"].value
                    else:
                        type = "null"

                    output_features(sid, id_e1, id_e2, type, features, foutput)
                    i=i+1

    os.system('cat '+train_file+'  | cut -f4- > megam.dat')
    foutput.close()

    #
    # start = time.time()
    # read_train_examples = open("megam.dat", "r")
    # # create a dictionary with the binary of the feat that appears
    # # and append together with its label
    # train = []
    # feat_train_dict = {}
    # count_null=0
    # count_notnull=0
    # for ind, x in enumerate(read_train_examples):
    #     # if ind in range(2000):
    #         label_train = x.split()[0]
    #         feat_train = x.split()[1:]
    #         # feat_train_dict = feat_dict
    #         if label_train!="null" or True: # if its not a null
    #             for feat in feat_train:
    #                 feat_train_dict[feat]=1;
    #             train.append((feat_train_dict, label_train))
    #             # count_notnull+=1
    #
    #             #for all
    #             if label_train!="null":
    #                 count_notnull+=1
    #             else:
    #                 count_null+=1
    #         else:
    #             count_null+=1
    # # save to a file
    # t_train = open('t_onlyUnder.txt','w')
    # t_train.write(str(train))
    # t_train.close()
    # print('count null-notnull', count_null, count_notnull)
    #
    #
    # # classifier = nltk.classify.NaiveBayesClassifier.train(train)
    # # print(sorted(classifier.labels()))
    # try:
    #     # classifier = nltk.classify.MaxentClassifier.train(train, 'MEGAM', trace=0, max_iter=1000)
    #     classifier = nltk.classify.MaxentClassifier.train(train, 'MEGAM')
    # except Exception as e:
    #     print('Error: %r' % e)
    # end=time.time()
    # print('time_train', end-start)
    # print(sorted(classifier.labels()))
    #
    # # THIS ONE
    # # https://stackoverflow.com/questions/12606543/nltk-megam-max-ent-algorithms-on-windows
    #
    # # PREDICT
    # output = 'task9.6_lluis_onlyUnder'
    #
    # start = time.time()
    # feat_dict = {}
    #
    # # for test in ["Devel", "Test-NER", "Test-DDI"]:
    # for test in ["Devel", "Test-DDI"]:
    #     outputfile = output + '_' + test + '_results.txt'
    #     outf = open(outputfile, "w")
    #     testdir = "./data/" + test + "/"
    #
    #     # process each file in directory
    #     for f in os.listdir(testdir) :
    #         # parse XML file, obtaining a DOM tree
    #         tree = parse(testdir + "/" + f)
    #         # process each sentence in the file
    #         sentences = tree.getElementsByTagName("sentence")
    #         for s in sentences :
    #             sid = s.attributes["id"].value # get sentence id
    #             stext = s.attributes["text"].value # get sentence text
    #             # it gives an error on the raw_parser if the sentence is empty ("")
    #             if stext != "":
    #                 # print('stext')
    #                 # print(stext)
    #
    #                 # load sentence entities into a dictionary
    #                 entities = {}
    #                 ents = s.getElementsByTagName("entity")
    #                 for e in ents :
    #                     id = e.attributes["id"].value
    #                     offs = e.attributes["charOffset"].value.split("-")
    #                     entities[id] = offs
    #                 # Tokenize, tag, and parse sentence
    #                 analysis = analyze(stext)
    #                 # print(analysis)
    #
    #                 # for each pair in the sentence, decide whether it is DDI and its type
    #                 pairs = s.getElementsByTagName("pair")
    #                 for p in pairs:
    #                     id_e1 = p.attributes["e1"].value
    #                     id_e2 = p.attributes["e2"].value
    #                     features = extract_features(analysis, entities, id_e1, id_e2)
    #                     # print(features)
    #                     prediction = predict(feat_dict, features, classifier)
    #                     # prediction = 'null' #predict
    #
    #                     output_ddi(sid, id_e1, id_e2, prediction, outf);
    #
    #     outf.close()
    #     # get performance score
    #     end=time.time()
    #     print('time_test', end-start)
    #     evaluate(testdir,outputfile)


if __name__ == '__main__':
    main()
