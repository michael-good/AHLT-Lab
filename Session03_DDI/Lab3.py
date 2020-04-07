from xml.dom.minidom import parse
import os
# import nltk CoreNLP module (just once)
from nltk.parse.corenlp import CoreNLPDependencyParser
# connect to your CoreNLP server (just once)
my_parser = CoreNLPDependencyParser(url="http://localhost:9000")

def parse_xml(file):
    return parse(file)

def getOffsets(sentence, word):
    start_index = sentence.find(word)
    print(start_index)
    end_index = start_index + len(word) # if the start_index is not -1
    return start_index, end_index

def analyze(sentence):
    # parse text (as many times as needed)
    mytree, = my_parser.raw_parse(sentence)
    print(mytree)
    word = 'knkds'
    start_off, end_off = getOffsets(sentence, word)
    print(sentence)
    print(word, start_off, end_off)

    return None

def main():
    inputdir = './data/Train'

    # process each file in directory
    for f in os.listdir(inputdir) :
        print(f)
        # parse XML file, obtaining a DOM tree
        tree = parse(inputdir + "/" + f)
        # process each sentence in the file
        sentences = tree.getElementsByTagName("sentence")
        for s in sentences :
            sid = s.attributes["id"].value # get sentence id
            stext = s.attributes["text"].value # get sentence text
            # load sentence entities into a dictionary
            entities = {}
            ents = s.getElementsByTagName("entity")
            for e in ents :
                id = e.attributes["id"].value
                offs = e.attributes["charOffset"].value.split("-")
                entities[id] = offs
            # Tokenize, tag, and parse sentence
            analysis = analyze(stext)
    #         # for each pair in the sentence, decide whether it is DDI and its type
    #         pairs = s.getElementsByTagName("pair")
    #         for p in pairs:
    #             id e1 = p.attributes["e1"].value
    #             id e2 = p.attributes["e2"].value
    #             (is ddi,ddi type) = check interaction(analysis, entities, id e1, id e2)
    #             print("|".join([sid, id e1 id e2, is ddi, ddi type]), file=outf)
    # # get performance score
    # evaluate(inputdir,outputfile)

if __name__ == '__main__':
    main()
