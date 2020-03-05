from xml.dom.minidom import parse
from nltk.tokenize import WhitespaceTokenizer
import os


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


def return_type(previous, text):
    type = "other"

    if (text.isupper() or "aspirin" in text.lower() or "PEGA" in text or text.startswith("SP") or "XX" in text or
        "IVA" in text):
        type = "brand"

    elif text.endswith('phane') or text[0].isdigit() or "MC" in text or "gain" in text:
        type = "drug_n"

    elif "thiazide" in text or text.startswith("anti") or "cont" in text or "ure" in text or "ids" in text:
        type = "group"

    elif (text.endswith('azole') or text.endswith('ine') or text.endswith('amine') or
          text.endswith('mycin') or text.endswith('avir') or text.endswith('ide') or text.endswith('olam') or
          "hydr" in text or "in" in text or text.startswith("amph") or "cyclo" in text or "ole" in text or
          "ano" in text or "ium" in text):
        type = "drug"

    if len(text) <= 4:
        type = "other"

    return type


def extract_entities(token_list):
    previous = ""
    list_entities = []
    for index, element in enumerate(token_list):
        type = return_type(previous, element[0])
        if type != "other":
            entity = {"name": element[0],
                      "offset": str(element[1]) + "-" + str(element[2]),
                      "type": type
                      }
            list_entities.append(entity)
        previous = type
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
    outputfile = "./task9.1_lluis_1.txt"
    nerc(inputdir, outputfile)


if __name__ == "__main__":
    main()
