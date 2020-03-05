from xml.dom.minidom import parse
from nltk.tokenize import WhitespaceTokenizer
import os


def parseXML(file, inputdir):
    dom = parse(inputdir + file)
    return dom.getElementsByTagName("entity")


def get_sentence_info(sentence):
    return sentence.getAttribute("type"), sentence.getAttribute("text")


def nerc(inputdir):
    inputfiles = os.listdir(inputdir)
    outputfile_1 = "./ground_truth_drug.txt"
    outputfile_2 = "./ground_truth_brand.txt"
    outputfile_3 = "./ground_truth_group.txt"
    outputfile_4 = "./ground_truth_drug-n.txt"
    file_1 = open(outputfile_1, "w")
    file_2 = open(outputfile_2, "w")
    file_3 = open(outputfile_3, "w")
    file_4 = open(outputfile_4, "w")
    for file in inputfiles:
        tree = parseXML(file, inputdir)
        for sentence in tree:
            (type, text) = get_sentence_info(sentence)
            if type == "drug":
                file_1.write(text + " | " + type + "\n")
            elif type == "brand":
                file_2.write(text + " | " + type + "\n")
            elif type == "group":
                file_3.write(text + " | " + type + "\n")
            elif type == "drug_n":
                file_4.write(text + " | " + type + "\n")
    file_1.close()
    file_2.close()
    file_3.close()
    file_4.close()


def main():
    inputdir = "./data/Train/"
    nerc(inputdir)


if __name__ == "__main__":
    main()