from xml.dom.minidom import parse
from nltk.tokenize import WhitespaceTokenizer
import os, sys
from random import random, seed



def parseXML(file, inputdir):
    dom = parse(inputdir + file)
    return dom.getElementsByTagName("sentence")

def get_sentence_info(sentence):
    return sentence.getAttribute("id"), sentence.getAttribute("text")

def tokenize(text):
    span_generator = WhitespaceTokenizer().span_tokenize(text)
    token_generator = WhitespaceTokenizer().tokenize(text)

    tokens = [(token, span[0], span[1]) for token, span in zip(token_generator, span_generator)]

    return tokens

def extract_features(s):
    features = []
    for word in s:
        #extract features
        #for now will put random to 0 or 1
        f1 = round(random())
        f2 = round(random())
        f3 = round(random())
        features.append([f1, f2, f3])

    return features

def output_features(id, s, ents):
    #type of element, for now all B-drug
    elem = 'B-drug'
    for ind, token in enumerate(s):
        sys.stdout.write( id +'\t'+ token[0] +'\t'+ str(token[1]) +'\t'+ str(token[2]) +'\t'+ elem)
        for feat in ents[ind]:
            sys.stdout.write('\t'+ str(feat))
        sys.stdout.write('\n')

def main():
    seed(1)
    inputdir = "./data/Train/"
    # outputfile = "./task9.1_lluis_3.txt"
    if os.path.exists(inputdir):
        inputfiles = os.listdir(inputdir)
    # f = open(outputfile, "a")
    for file in inputfiles:
        tree = parseXML(file, inputdir)
        for sentence in tree:
            (id, text) = get_sentence_info(sentence)
            token_list = tokenize(text)
            features = extract_features(token_list)
            output_features(id, token_list, features)
    # f.close()
    # evaluate(inputdir, outputfile)

if __name__ == "__main__":
    main()
