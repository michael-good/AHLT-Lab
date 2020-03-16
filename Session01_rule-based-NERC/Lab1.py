from xml.dom.minidom import parse
from nltk.tokenize import TreebankWordTokenizer as twt
import os
from rules import return_type

def parseXML(file, inputdir):
    dom = parse(inputdir + file)
    return dom.getElementsByTagName("sentence")


def get_sentence_info(sentence):
    return sentence.getAttribute("id"), sentence.getAttribute("text")


def tokenize(text):
    span_generator = twt().span_tokenize(text)
    tokens = []
    for s in span_generator:
        tokens.append((text[s[0]:s[1]], s[0], s[1]-1))
    return tokens

def extract_entities(token_list):
    previous = False
    list_entities = []
    #demands as implementation first
    previoustype = 'n'
    namegroup = ''

    for index, element in enumerate(token_list):
        typeel = return_type(element[0], index, token_list)

        #to return groups of words
        if isinstance(typeel, int) and typeel!=1 :
            off = str(element[1])
            namegroup = namegroup+' '+element[0]
            previoustype = typeel-1
        elif isinstance(previoustype, int) and previoustype!=1 :
            namegroup = namegroup+' '+element[0]
            previoustype-=1
        elif isinstance(previoustype, int) and previoustype == 1:
            entity = {"name": namegroup+' '+element[0],
                      "offset": off + "-" + str(element[2]),
                      "type": 'group'
                      }
            # print(entity)
            namegroup = ''
            previoustype = 'n'
            list_entities.append(entity)

        elif typeel != "other":
            entity = {"name": element[0],
                      "offset": str(element[1]) + "-" + str(element[2]),
                      "type": typeel
                      }
            list_entities.append(entity)

    return list_entities


def output_entities(id, entities, output):
    for element in entities:
        output.write(id+'|'+element["offset"]+'|'+element["name"]+'|'+element["type"]+'\n')


def evaluate(inputdir, outputfile):
    os.system("java -jar eval/evaluateNER.jar " + inputdir + " " + outputfile)


def nerc(inputdir, outputfile):
    if os.path.exists(inputdir):
        inputfiles = os.listdir(inputdir)
    if os.path.exists(outputfile):
        os.remove(outputfile)
    f = open(outputfile, "a")
    for file in inputfiles:
        tree = parseXML(file, inputdir)
        for sentence in tree:
            (id, text) = get_sentence_info(sentence)
            token_list = tokenize(text)
            entities = extract_entities(token_list)
            output_entities(id, entities, f)
    f.close()
    evaluate(inputdir, outputfile)


def main():
    inputdir = "./data/Train/"
    outputfile = "./task9.1_lluis_5.txt"
    nerc(inputdir, outputfile)


if __name__ == "__main__":
    main()
