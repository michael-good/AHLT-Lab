from xml.dom.minidom import parse
from nltk.tokenize import TreebankWordTokenizer as twt
import os
from rules import return_type

USE_EXTERNAL_RESOURCES = False


def parse_xml(file, input_dir):
    dom = parse(input_dir + file)
    return dom.getElementsByTagName('sentence')


def get_sentence_info(sentence):
    return sentence.getAttribute('id'), sentence.getAttribute('text')


def tokenize(text):
    span_generator = twt().span_tokenize(text)
    tokens = []
    for s in span_generator:
        tokens.append((text[s[0]:s[1]], s[0], s[1] - 1))
    return tokens


def extract_entities(token_list, hsdb_list, drug_bank):
    list_entities = []
    previous_type = 'n'
    name_group = ''
    type_aux = 'n'
    type_aux_saved = False
    for index, element in enumerate(token_list):
        type_element, aux = return_type(element[0], index, token_list, hsdb_list, drug_bank)
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
            entity = {'name': name_group + ' ' + element[0],
                      'offset': off + '-' + str(element[2]),
                      'type': type_aux
                      }
            name_group = ''
            previous_type = 'n'
            type_aux_saved = False
            list_entities.append(entity)

        elif type_element != 'other':
            entity = {'name': element[0],
                      'offset': str(element[1]) + '-' + str(element[2]),
                      'type': type_element
                      }
            list_entities.append(entity)

    return list_entities


def output_entities(id_, entities, output):
    for element in entities:
        output.write(id_ + '|' + element['offset'] + '|' + element['name'] + '|' + element['type'] + '\n')


def evaluate(input_dir, output_file):
    os.system('java -jar eval/evaluateNER.jar ' + input_dir + ' ' + output_file)


def get_external_resources():
    filename_hsdb = './resources/HSDB.txt'
    filename_drug_bank = './resources/DrugBank.txt'

    with open(filename_hsdb, 'r') as f:
        drugs_data = f.readlines()
    hsdb_list = []
    for element in drugs_data:
        hsdb_list.append(element.lower().rstrip())

    with open(filename_drug_bank, 'r') as g:
        data = g.readlines()

    drug_bank = {}
    for sentence in data:
        split_sentence = sentence.rsplit('|', 1)
        drug_bank[split_sentence[0]] = split_sentence[-1].rstrip()

    return hsdb_list, drug_bank


def nerc(input_dir, output_file):
    if os.path.exists(input_dir):
        input_files = os.listdir(input_dir)
    if os.path.exists(output_file):
        os.remove(output_file)
    f = open(output_file, 'w')
    hsdb_list = None
    drug_bank = None
    if USE_EXTERNAL_RESOURCES:
        hsdb_list, drug_bank = get_external_resources()
    i = 0
    for file in input_files:
        tree = parse_xml(file, input_dir)
        for sentence in tree:
            (id_, text) = get_sentence_info(sentence)
            token_list = tokenize(text)
            entities = extract_entities(token_list, hsdb_list, drug_bank)
            output_entities(id_, entities, f)
        i += 1
        print("{0:.2f}%".format(i / len(input_files) * 100))
    f.close()
    evaluate(input_dir, output_file)


def main():
    input_dir = './data/Devel/'
    output_file = './task9.1_lluis_5.txt'
    nerc(input_dir, output_file)


if __name__ == '__main__':
    main()
