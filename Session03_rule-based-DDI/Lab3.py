import os
import time
from xml.dom.minidom import parse
from interactions import check_interaction
# import nltk CoreNLP module (just once)
from nltk.parse.corenlp import CoreNLPDependencyParser
# connect to your CoreNLP server (just once)
my_parser = CoreNLPDependencyParser(url="http://localhost:9000")


def parse_xml(file):
    """
        Parses given XML file

        Parameters:
            file: name of the file to parse
        Returns:
            Data structure holding 'file' data in a readable way
    """
    return parse(file)


def get_offsets(sentence, word):
    """
        Retrieves the position of word within sentence at character level

        Parameters:
            sentence: information held by 'sentence' tag structure in XML file
            word: string of a word that belongs to the provided sentence
        Returns:
            Start and end index of the position of word within sentence at character level
    """
    start_index = sentence.find(word)
    # if the start_index is not -1
    end_index = start_index + len(word) - 1
    return start_index, end_index


def analyze(sentence):
    """
        Generates a grammar dependency tree of all the words within the sentence

        Parameters:
            sentence: information held by 'sentence' tag structure in XML file
        Returns:
            A grammar dependency tree
    """
    # parse text (as many times as needed)
    tree, = my_parser.raw_parse(sentence)

    # enrich the NLPDepencyGraph with the start and end offset
    for e in range(1, len(tree.nodes)):
        node = tree.nodes[e]
        word = node['word']
        start_off, end_off = get_offsets(sentence, word)
        # returns start_off=-1 if didn't find the word in the sentence
        if start_off != -1:
            node['start'] = start_off
            node['end'] = end_off

    return tree


def evaluate(input_dir, output_file):
    """
        Evaluates the performance of the classifier by means of different metrics such as
        precision, recall and f-score

        Parameters:
            input_dir: path to output_file
            output_file: txt file holding entities data
    """
    os.system("java -jar eval/evaluateDDI.jar " + input_dir + " " + output_file)


def main():
    start = time.time()

    # input_dir = './data/Devel'
    # output_file = 'task9.2_lluis_Devel.txt'

    input_dir = './data/Test-DDI'
    output_file = 'task9.2_lluis_TestDDI.txt'

    foutput = open(output_file, "w")

    # process each file in directory
    for f in os.listdir(input_dir):
        # parse XML file, obtaining a DOM tree
        tree = parse(input_dir + "/" + f)
        # process each sentence in the file
        sentences = tree.getElementsByTagName("sentence")
        for s in sentences:
            # get sentence id
            sid = s.attributes["id"].value
            # get sentence text
            stext = s.attributes["text"].value
            # it gives an error on the raw_parser if the sentence is empty ("")
            if stext != "":
                # load sentence entities into a dictionary
                entities = {}
                sentence_entities = s.getElementsByTagName("entity")
                for e in sentence_entities:
                    id_ = e.attributes["id"].value
                    offset = e.attributes["charOffset"].value.split("-")
                    entities[id_] = offset

                # Tokenize, tag, and parse sentence
                analysis = analyze(stext)

                # for each pair in the sentence, decide whether it is DDI and its type
                pairs = s.getElementsByTagName("pair")
                for p in pairs:
                    id_e1 = p.attributes["e1"].value
                    id_e2 = p.attributes["e2"].value

                    (is_ddi, ddi_type) = check_interaction(analysis, entities, id_e1, id_e2)
                    foutput.write("|".join([sid, id_e1, id_e2, str(is_ddi), ddi_type]))
                    foutput.write("\n")
    foutput.close()

    # get performance score
    evaluate(input_dir, output_file)


if __name__ == '__main__':
    main()
