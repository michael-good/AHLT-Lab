import os
import time
from xml.dom.minidom import parse
from extract_featuresL4 import extract_features
# import nltk CoreNLP module (just once)
from nltk.parse.corenlp import CoreNLPDependencyParser

# connect to your CoreNLP server (just once)
my_parser = CoreNLPDependencyParser(url="http://localhost:9000")


# nltk.config_megam('C:/Users/Lluis/Desktop/MATT/AHLT/AHLT-Lab/Session04_ML-based-DDI/megam_0.92/megam.exe')


def parse_xml(file):
    """
        Parses given XML file

        Parameters:
            file: name of the file to parse
        Returns:
            Data structure holding 'file' data in a readable way
    """
    return parse(file)


def get_offsets(sentence, word, starting_point):
    """
        Retrieves the position of word within sentence at character level

        Parameters:
            sentence: information held by 'sentence' tag structure in XML file
            word: string of a word that belongs to the provided sentence
        Returns:
            Start and end index of the position of word within sentence at character level
    """
    start_index = sentence[starting_point:].find(word) + starting_point
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
    starting_point = 0
    for e in range(1, len(tree.nodes)):
        node = tree.nodes[e]
        word = node['word']
        start_off, end_off = get_offsets(sentence, word, starting_point)
        # returns start_off=-1 if didn't find the word in the sentence
        if start_off != -1:
            node['start'] = start_off
            node['end'] = end_off
            starting_point = end_off
        else:
            # for now we will not touch the the braquets which are represented by
            # -lrb- and -rrb-, but then on the feature_extractor we will ignore
            # them as if they are not needed for the features
            pass
            # print(node)
    return tree


def output_features(id_, e1, e2, gold_class, features, fout, fout2):
    """
        Prints to stdout the feature vector in the specified format

        Parameters:
            id_: sentence identifier
            e1: name of first entity
            e2: name of second entity
            gold_class: classification type
            features: list of features
            fout: output txt file
    """

    feat_megam = ''
    sentence_features = id_ + '\t' + e1 + '\t' + e2 + '\t' + gold_class
    for feat in features:
        sentence_features = sentence_features + '\t' + str(feat)
        feat_megam = feat_megam + str(feat) + ' '

    sentence_features = sentence_features + '\n'
    feat_megam = feat_megam + '\n'
    # print in the terminal
    # sys.stdout.write(sentence_features)
    # print in a file
    fout.write(sentence_features)
    fout2.write(feat_megam)


def output_ddi(id_, e1, e2, ddi_type, fout):
    """
        Prints on fout the interactions between two given entities in the right format

        Parameters:
            id_: sentence identifier
            e1: name of first entity
            e2: name of second entity
            ddi_type: interaction type
            fout: output txt file
    """
    if ddi_type == 'null':
        ddi = 0
    else:
        ddi = 1
    sentence_features = id_ + '|' + e1 + '|' + e2 + '|' + str(ddi) + '|' + ddi_type + '\n'
    # print in a file
    fout.write(sentence_features)


def evaluate(input_dir, output_file):
    """
        Evaluates the performance of the classifier by means of different metrics such as
        precision, recall and f-score

        Parameters:
            input_dir: path to output_file
            output_file: txt file holding entities data
    """
    os.system("java -jar eval/evaluateDDI.jar " + input_dir + " " + output_file)


def predict(feat_test, classifier):
    # create a dictionary with the binary of the feat that appears
    feat_test_dict = {}
    for feat in feat_test:
        feat_test_dict[feat] = 1;

    # save to a file
    t_test = open('test_features.txt', 'w')
    t_test.write(str(feat_test_dict))
    t_test.close()

    # pred = classifier.classify_many(test)
    pred = classifier.classify(feat_test_dict)
    return pred


def main():
    mode = 'train_feat' # train_feat, train_model or eval
    os_version = 'linux'  # windows or linux
    megam_v = 'exe'  # nltk or exe

    start_time = time.time()
    if mode == 'train_feat':
        ###############################
        ###          TRAIN          ###
        ###############################
        train_dir = './data/Train'

        train_file = 'train_features_output.txt'
        if os.path.exists(train_file):
            os.remove(train_file)
        if os.path.exists('megam.dat'):
            os.remove('megam.dat')
        foutput = open(train_file, "a")
        foutput2 = open('megam.dat', "a")

        null = 0
        mechanism = 0
        effect = 0
        advise = 0
        int_ = 0
        # process each file in directory
        for number_files, f in enumerate(os.listdir(train_dir)):
            # parse XML file, obtaining a DOM tree1
            tree = parse(train_dir + "/" + f)
            # process each sentence in the file
            sentences = tree.getElementsByTagName("sentence")
            for number_sentences, s in enumerate(sentences):
                sid = s.attributes["id"].value  # get sentence id
                stext = s.attributes["text"].value  # get sentence text
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
                    for i, p in enumerate(pairs):
                        id_e1 = p.attributes["e1"].value
                        id_e2 = p.attributes["e2"].value
                        features = extract_features(analysis, entities, id_e1, id_e2, i)
                        i += 1
                        # get ground truth
                        is_ddi = p.attributes["ddi"].value
                        if is_ddi == "true" and 'type' in p.attributes:
                            type_ = p.attributes["type"].value
                        else:
                            type_ = "null"

                        output_features(sid, id_e1, id_e2, type_, features, foutput, foutput2)
            print('{:2.2f}'.format(number_files / len(os.listdir(train_dir)) * 100))
        foutput.close()
        foutput2.close()
        if mode == 'train_model' and megam_v == 'exe':
            if os_version == 'windows':
                os.system('C:/Users/Lluis/Desktop/MATT/AHLT/AHLT-Lab/Session04_ML-based-DDI/megam_0.92/megam.exe -quiet -nc -nobias multiclass megam.dat > me_model.dat')
            elif os_version == 'linux':
                os.system('./megam_i686.opt -quiet -nc -nobias multiclass megam.dat > me_model.dat')

        print("null: " + str(null))
        print("mechanism: " + str(mechanism))
        print("advise: " + str(advise))
        print("effect: " + str(effect))
        print("int: " + str(int_))

        print("--- %s seconds ---" % (time.time() - start_time))

    if (mode == 'train_model' or mode == 'eval') and megam_v == 'nltk':
        read_train_examples = open("train_features_output.txt", "r")
        # create a dictionary with the binary of the feat that appears
        # and append together with its label
        feat_train_dict = {}
        train = []
        for ind, x in enumerate(read_train_examples):
            if ind in range(2000):
                label_train = x.split()[3]
                feat_train = x.split()[4:]

                for feat in feat_train:
                    feat_train_dict[feat] = 1;
                train.append((feat_train_dict, label_train))
        read_train_examples.close()

        try:
            # classifier = nltk.classify.MaxentClassifier.train(train, 'MEGAM', trace=0, max_iter=1000)
            classifier = nltk.classify.MaxentClassifier.train(train, 'MEGAM')
        except Exception as e:
            print('Error: %r' % e)
        print(sorted(classifier.labels()))
        #
        # # THIS ONE
        # # https://stackoverflow.com/questions/12606543/nltk-megam-max-ent-algorithms-on-windows
        #

    if mode == 'eval':
        ###############################
        ###          TEST           ###
        ###############################

        output = 'task9.6_lluis_2'

        # for test in ["Devel", "Test-NER", "Test-DDI"]:
        for test in ["Devel"]:

            output_file = output + '_' + test + '_results.txt'
            outf = open(output_file, "w")
            test_dir = "./data/" + test + "/"

            test_file = 'test_features_output.txt'
            if os.path.exists(test_file):
                os.remove(test_file)
                os.remove('megam_test.dat')
            foutput = open(test_file, "a")
            foutput2 = open('megam_test.dat', "a")

            # process each file in directory
            for f in os.listdir(test_dir):
                # parse XML file, obtaining a DOM tree
                tree = parse(test_dir + "/" + f)
                # process each sentence in the file
                sentences = tree.getElementsByTagName("sentence")
                for s in sentences:
                    sid = s.attributes["id"].value  # get sentence id
                    stext = s.attributes["text"].value  # get sentence text
                    # it gives an error on the raw_parser if the sentence is empty ("")
                    if stext != "":
                        # print('stext')
                        # print(stext)

                        # load sentence entities into a dictionary
                        entities = {}
                        sentence_entities = s.getElementsByTagName("entity")
                        for e in sentence_entities:
                            id = e.attributes["id"].value
                            offset = e.attributes["charOffset"].value.split("-")
                            entities[id] = offset
                        # Tokenize, tag, and parse sentence
                        analysis = analyze(stext)
                        # print(analysis)

                        # for each pair in the sentence, decide whether it is DDI and its type
                        pairs = s.getElementsByTagName("pair")
                        for p in pairs:
                            id_e1 = p.attributes["e1"].value
                            id_e2 = p.attributes["e2"].value
                            features = extract_features(analysis, entities, id_e1, id_e2)
                            # print(features)
                            output_features(sid, id_e1, id_e2, '', features, foutput, foutput2)
                            if megam_v == 'nltk':
                                prediction = predict(features, classifier)
                                output_ddi(sid, id_e1, id_e2, prediction, outf)
                print('{:2.2f}'.format(number_files / len(os.listdir(test_dir)) * 100))
        foutput.close()
        foutput2.close()
        print('MEGAM Test...')
        if megam_v == 'exe':
            if os_version == 'windows':
                os.system(
                    'C:/Users/Lluis/Desktop/MATT/AHLT/AHLT-Lab/Session04_ML-based-DDI/megam_0.92/megam.exe -nc -nobias -predict me_model.dat multiclass  megam_test.dat')
            elif os_version == 'linux':
                os.system('./megam_i686.opt -nc -nobias -predict me_model.dat multiclass  megam_test.dat > output.txt')
        with open("output.txt", "r") as f:
            lines = f.readlines()
        with open("output.txt", "w") as f:
            for line in lines:
                for i, char in enumerate(line):
                    if char == '\t':
                        f.write(line[:i] + '\n')
                        break
        with open("output.txt", "r") as f:
            type_ = [x.strip() for x in f.readlines()]
        with open("test_features_output.txt", "r") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            x = line.split('\t')
            sentence = x[0]
            e1 = x[1]
            e2 = x[2]
            if len(x) == 3:
                type_ddi = 'null'
            else:
                type_ddi = type_[i]
            output_ddi(sentence, e1, e2, type_ddi, outf)
        outf.close()
        # get performance score
        evaluate(test_dir, output_file)
        print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
