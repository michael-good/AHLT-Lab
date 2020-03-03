from xml.dom.minidom import parse
from nltk.tokenize import WhitespaceTokenizer
import os


def parseXML(file):
    # path = "/home/miguel/University/AHLT/Lab/labAHLT/data/Train/"
    path = "C:/Users/Lluis/Desktop/MATT/AHLT/LaboratoryAHLT/Lab1/data/Train/"

    dom = parse(path + file)
    return dom.getElementsByTagName("sentence")


def get_sentence_info(sentence):
    return sentence.getAttribute("id"), sentence.getAttribute("text")


def tokenize(text):
    span_generator = WhitespaceTokenizer().span_tokenize(text)
    token_generator = WhitespaceTokenizer().tokenize(text)
    for token, span in zip(token_generator, span_generator):
        if token!=text[span[0]:span[1]]:
            print('Falseee')

    tokens = [(token, span[0], span[1]) for token, span in zip(token_generator, span_generator)]

    return tokens


def extract_entities(token_list):
    list_entities = []
    for element in token_list:
        type = "drug"
        entity = {"name": element[0],
                "offset": str(element[1]) + "-" + str(element[2]),
                "type": type
                }
        list_entities.append(entity)
    return list_entities


def evaluate(inputdir, outputfile):
    os.system("java -jar eval/evaluateNER.jar " + inputdir + " " + outputfile)

def output_entities(id, entities, output):
    for element in entities:
        output.write(id+'|'+element["offset"]+'|'+element["name"]+'|'+element["type"]+'\n')

def nerc(inputdir, outputfile):
    if os.path.exists(inputdir):
        inputfiles = os.listdir(inputdir)
    if os.path.exists(outputfile):
        os.remove(outputfile)
    f = open(outputfile, "a")
    for file in inputfiles:
        tree = parseXML(file)
        for sentence in tree:
            (id, text) = get_sentence_info(sentence)
            token_list = tokenize(text)
            entities = extract_entities(token_list)
            # print(entities)
            output_entities(id, entities, f)
    f.close()
    evaluate(inputdir, outputfile)


def main():
    # inputdir = os.listdir("/home/miguel/University/AHLT/Lab/labAHLT/data/Train/")
    inputdir = "C:/Users/Lluis/Desktop/MATT/AHLT/LaboratoryAHLT/Lab1/data/Train/"
    outputfile = "./task9.1_lluis_1.txt"
    nerc(inputdir, outputfile)


if __name__ == "__main__":
    main()
