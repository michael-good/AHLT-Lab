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
    end_index = start_index + len(word) -1 # if the start_index is not -1
    return start_index, end_index

def analyze(sentence):
    # parse text (as many times as needed)
    # print(sentence)
    mytree, = my_parser.raw_parse(sentence)
    # print('parsed')

    # enrich the NLPDepencyGraph with the start and end offset
    for e in range(1, len(mytree.nodes)):
        node = mytree.nodes[e]
        word = node['word']
        start_off, end_off = getOffsets(sentence, word)
        # returns start_off=-1 if didn't find the word in the sentence
        if start_off != -1:
            node['start'] = start_off
            node['end'] = end_off

    return mytree

import random
def check_interaction(analysis, entities, id_e1, id_e2):
    exist = random.randint(0,1)
    if exist==0:
        typeel = 'null'
    else:
        typeel = random.choice(['mechanism', 'effect', 'advise', 'int'])

    return exist, typeel

def evaluate(inputdir,outputfile):
    os.system("java -jar eval/evaluateDDI.jar " + inputdir + " " + outputfile)

def main():
    inputdir = './data/Train'
    outputfile = 'task9.2_lluis_5.txt'

    # i = 0
    # printed=True

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
            # it gives an error on the raw_parser if the sentence is empty ("")
            if stext != "":
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
                    (is_ddi,ddi_type) = check_interaction(analysis, entities, id_e1, id_e2)

                    foutput = open(outputfile, "a")
                    foutput.write("|".join([sid, id_e1, id_e2, str(is_ddi), ddi_type]))
                    foutput.write("\n")
                    foutput.close()

                    # print("|".join([sid, id_e1, id_e2, str(is_ddi), ddi_type]), file=outputfile)
    # get performance score
    evaluate(inputdir,outputfile)

if __name__ == '__main__':
    main()
