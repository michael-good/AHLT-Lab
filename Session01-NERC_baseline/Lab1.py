from xml.dom.minidom import parse
from nltk.tokenize import WhitespaceTokenizer
import os


def parseXML(file):
    path = "/home/miguel/University/AHLT/Lab/labAHLT/data/Train/"
    dom = parse(path + file)
    return dom.getElementsByTagName("sentence")


def get_sentence_info(sentence):
    return sentence.getAttribute("id"), sentence.getAttribute("text")


def tokenize(text):
    span_generator = WhitespaceTokenizer().span_tokenize(text)
    token_generator = WhitespaceTokenizer().tokenize(text)

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


def evaluate(inputdir, outputdir):
    os.system("java -jar eval/evaluateNER.jar " + inputdir + " " + outputfile)


def nerc(inputdir, outputfile):
    for file in inputdir:
        tree = parseXML(file)
        for sentence in tree:
            (id, text) = get_sentence_info(sentence)
            token_list = tokenize(text)
            entities = extract_entities(token_list)
            print(entities)
            """
            output_entities(id, entities, outputfile)
    evaluate(inputdir, outpufile)
    """


def main():
    inputdir = os.listdir("/home/miguel/University/AHLT/Lab/labAHLT/data/Train/")
    outputfile = "./output.txt"
    nerc(inputdir, outputfile)


if __name__ == "__main__":
    main()