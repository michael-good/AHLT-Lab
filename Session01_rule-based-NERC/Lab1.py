from xml.dom.minidom import parse
from nltk.tokenize import TreebankWordTokenizer as twt
import os
from rules import return_type


def parse_xml(file, inputdir):
    dom = parse(inputdir + file)
    return dom.getElementsByTagName("sentence")


def get_sentence_info(sentence):
    return sentence.getAttribute("id"), sentence.getAttribute("text")


def tokenize(text):
    span_generator = twt().span_tokenize(text)
    tokens = []
    for s in span_generator:
        tokens.append((text[s[0]:s[1]], s[0], s[1] - 1))
    return tokens


def extract_entities(token_list):
    list_entities = []
    previous_type = 'n'
    name_group = ''
    type_aux = 'n'
    type_aux_saved = False
    for index, element in enumerate(token_list):
        type_element, aux = return_type(element[0], index, token_list)
        if isinstance(type_element, int) and type_element != 1:
            off = str(element[1])
            name_group = name_group + ' ' + element[0]
            previous_type = type_element - 1
            if not type_aux_saved:
                type_aux = aux
                type_aux_saved = True
        elif isinstance(previous_type, int) and previous_type != 1:
            name_group = name_group + ' ' + element[0]
            previous_type -= 1
        elif isinstance(previous_type, int) and previous_type == 1:
            entity = {"name": name_group + ' ' + element[0],
                      "offset": off + "-" + str(element[2]),
                      "type": type_aux
                      }
            name_group = ''
            previous_type = 'n'
            type_aux_saved = False
            list_entities.append(entity)

        elif type_element != "other":
            entity = {"name": element[0],
                      "offset": str(element[1]) + "-" + str(element[2]),
                      "type": type_element
                      }
            list_entities.append(entity)

    return list_entities


def output_entities(id_, entities, output):
    for element in entities:
        output.write(id_ + '|' + element["offset"] + '|' + element["name"] + '|' + element["type"] + '\n')


def evaluate(input_dir, output_file):
    os.system("java -jar eval/evaluateNER.jar " + input_dir + " " + output_file)


def nerc(input_dir, output_file):
    if os.path.exists(input_dir):
        input_files = os.listdir(input_dir)
    if os.path.exists(output_file):
        os.remove(output_file)
    f = open(output_file, "a")
    for file in input_files:
        tree = parse_xml(file, input_dir)
        for sentence in tree:
            (id_, text) = get_sentence_info(sentence)
            token_list = tokenize(text)
            entities = extract_entities(token_list)
            output_entities(id_, entities, f)
    f.close()
    evaluate(input_dir, output_file)


def main():
    input_dir = "./data/Devel/"
    output_file = "./task9.1_lluis_5.txt"
    nerc(input_dir, output_file)


if __name__ == "__main__":
    main()
