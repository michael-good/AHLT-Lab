from xml.dom.minidom import parse
from nltk.tokenize import TreebankWordTokenizer as twt
import os
from rules import return_type

# If the flag is set to True, external resources will be used
USE_EXTERNAL_RESOURCES = True


def parse_xml(file, input_dir):
    """
    Parses given XML file and retrieves the elements with tag 'sentence'

    Parameters:
        file: name of the file to parse
        input_dir: path to the file to parse
    Returns:
        A list of 'sentence' elements contained within file
    """
    dom = parse(input_dir + file)
    return dom.getElementsByTagName('sentence')


def get_sentence_info(sentence):
    """
        Given an element sentence from an XML file, extracts 'id' and 'text' data from it

        Parameters:
            sentence: 'sentence' element from XML file
        Returns:
            'id' and 'text' information fields contained in sentence
    """
    return sentence.getAttribute('id'), sentence.getAttribute('text')


def tokenize(text):
    """
        Splits input text into words

        Parameters:
            text: group of words to split
        Returns:
            A list of tokens. Each token is made of a tuple that contains a word and its position in
            the original text in the following form: ("word", initial_offset, end_offset)
    """
    span_generator = twt().span_tokenize(text)
    tokens = []
    for s in span_generator:
        tokens.append((text[s[0]:s[1]], s[0], s[1] - 1))
    return tokens


def extract_entities(token_list, hsdb_list, drug_bank):
    """
        Given a list of word tokens, decides which class represents each one of them thanks to
        a defined set of rules. External resources can be used as well if desired.

        Parameters:
            token_list: list of tokens of a 'sentence'
            hsdb_list: list of drugs. Only available when external resources activated
            drug_bank: drug_bank: list of possible sentences and their corresponding label
                       Only available when external resources activated
        Returns:
            list_entities: For each token, a dictionary that stores information about its value,
                           position in the original text and its class
    """
    list_entities = []
    previous_type = None
    name_group = ''
    type_first_element_group = None
    offset = None
    for index, element in enumerate(token_list):
        # return_type classifies the current token. If there is a relationship between such token and other
        # tokens in the sentence, current token type is stored in aux and type_element is given a number
        # that determines the number of possible tokens in the list that may be part of the same type
        type_element, type_group = return_type(element[0], index, token_list, hsdb_list, drug_bank)
        # If there are more than one word that could have the same type of the current token, store the last
        # into the name_group variable so that it can be properly classified together with the former in the future
        if isinstance(type_element, int) and type_element != 1:
            offset = str(element[1])
            name_group = name_group + ' ' + element[0]
            previous_type = type_element - 1
            if type_first_element_group is None:
                type_first_element_group = type_group
        # Keep adding tokens to the name_group variable if they are related
        elif isinstance(previous_type, int) and previous_type != 1:
            name_group = name_group + ' ' + element[0]
            previous_type -= 1
        # Once we get to the final element of the related tokens of the token list, create an entity with the
        # information stored in name_group
        elif isinstance(previous_type, int) and previous_type == 1:
            entity = {'name': name_group + ' ' + element[0],
                      'offset': offset + '-' + str(element[2]),
                      'type': type_first_element_group
                      }
            name_group = ''
            previous_type = None
            type_first_element_group = None
            list_entities.append(entity)
        # If there are no related tokens to the current one in the sentence and a type has been detected
        elif type_element != 'other':
            entity = {'name': element[0],
                      'offset': str(element[1]) + '-' + str(element[2]),
                      'type': type_element
                      }
            list_entities.append(entity)

    return list_entities


def output_entities(id_, entities, output):
    """
        Stores entities data into output txt file in a readable format

        Parameters:
            id_: identifier of the 'sentence' element
            entities: list of extracted entities
            output: txt file
    """
    for element in entities:
        output.write(id_ + '|' + element['offset'] + '|' + element['name'] + '|' + element['type'] + '\n')


def evaluate(input_dir, output_file):
    """
        Evaluates the performance of the classifier by means of different metrics such as
        precision, recall and f-score

        Parameters:
            input_dir: path to output_file
            output_file: txt file holding entities data
    """
    os.system('java -jar eval/evaluateNER.jar ' + input_dir + ' ' + output_file)


def get_external_resources():
    """
        Gets external resources data and processes them for future use in the program

        Returns:
            hsdb_list: list of drugs
            drug_bank: list of possible sentences and their corresponding label
    """
    filename_hsdb = './resources/HSDB.txt'
    filename_drug_bank = './resources/DrugBank.txt'

    # Load HSDB.txt data
    with open(filename_hsdb, 'r', encoding='utf8') as f:
        drugs_data = f.readlines()
    # Get rid of carriage return at the end of each line and convert all words to lowercase
    hsdb_list = []
    for element in drugs_data:
        hsdb_list.append(element.lower().rstrip())

    # Load DrugBank.txt data
    with open(filename_drug_bank, 'r', encoding='utf8') as g:
        data = g.readlines()

    # Store DrugBank.txt data into a dictionary where keys correspond to possible sentence's text and
    # values are their class
    drug_bank = {}
    for sentence in data:
        split_sentence = sentence.rsplit('|', 1)
        drug_bank[split_sentence[0]] = split_sentence[-1].rstrip()

    return hsdb_list, drug_bank


def nerc(input_dir, output_file):
    """
        Extracts entities datasets and decides what class they belong to. Moreover, it stores
        all the information into an output file that is then evaluated by means of statistical metrics

        Parameters:
            input_dir: path to datasets
            output_file: path to desired location of output txt file
        """
    # Set input_files variable if given paths exists and removes previously created output files
    input_files = os.listdir(input_dir)
    if os.path.exists(output_file):
        os.remove(output_file)
    f = open(output_file, 'w')

    # If use of external resources is desired necessary data is loaded
    hsdb_list = None
    drug_bank = None
    if USE_EXTERNAL_RESOURCES:
        hsdb_list, drug_bank = get_external_resources()

    # Loops over each file in the folder 'input_dir' and makes a classification of each word token
    # in every sentence element of the datasets
    i = 0
    for file in input_files:
        tree = parse_xml(file, input_dir)
        for sentence in tree:
            (id_, text) = get_sentence_info(sentence)
            token_list = tokenize(text)
            entities = extract_entities(token_list, hsdb_list, drug_bank)
            output_entities(id_, entities, f)
        i += 1
        # Prints the percentage of completion of the main task
        print("{0:.2f}%".format(i / len(input_files) * 100))
    f.close()
    evaluate(input_dir, output_file)


def main():
    input_folder = ['Devel', 'Test-NER', 'Test-DDI']
    for element in input_folder:
        input_dir = './data/' + element + '/'
        if USE_EXTERNAL_RESOURCES:
            output_file = './task9.2_lluis_9_' + element + '.txt'
        else:
            output_file = './task9.1_lluis_9_' + element + '.txt'
        nerc(input_dir, output_file)


if __name__ == '__main__':
    main()
