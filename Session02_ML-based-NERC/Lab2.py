from xml.dom.minidom import parse
from nltk.tokenize import WhitespaceTokenizer
import os, sys

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

def extract_features(s):
    features = []
    for ind, word in enumerate(s):
        feat = []
        # word itself
        feat.append('form='+ word[0])

        # last 4 letters
        if len(word[0])>4:
            feat.append('suf4='+ word[0][-4:])
        else:
            feat.append('suf4='+ word[0])

        # next word
        if ind==len(s)-1:
            feat.append('next=_EoS_')
        else:
            feat.append('next='+ s[ind+1][0])

        # previous word
        if ind==0:
            feat.append('prev=_BoS_')
        else:
            feat.append('prev='+ s[ind-1][0])

        # if punctuation
        if (not word[0].isalpha() and not word[0].isdigit()):
            feat.append('punct')

        # length of the word
        feat.append('len='+ str(word[2]-word[1]))

        #if capitalized or all capitalized
        upper=0
        letter=0
        for let in word[0]:
            if let.isalpha():
                letter+=1
            if let.isupper():
                upper+=1
        if upper > 0:
            if upper == letter:
                feat.append('allCapitalized')
            else:
                feat.append('capitalized')

        features.append(feat)


    return features

def output_features(id, s, ents):
    #type of element, for now all B-drug
    elem = 'B-drug'
    for ind, token in enumerate(s):
        sys.stdout.write( id +'\t'+ token[0] +'\t'+ str(token[1]) +'\t'+ str(token[2]) +'\t'+ elem)
        for feat in ents[ind]:
            sys.stdout.write('\t'+ str(feat))
        sys.stdout.write('\n')

def main():
    inputdir = "./data/Train/"
    # outputfile = "./task9.1_lluis_3.txt"
    if os.path.exists(inputdir):
        inputfiles = os.listdir(inputdir)
    # f = open(outputfile, "a")
    for file in inputfiles:
        tree = parseXML(file, inputdir)
        for sentence in tree:
            (id, text) = get_sentence_info(sentence)
            token_list = tokenize(text)
            features = extract_features(token_list)
            output_features(id, token_list, features)
    # f.close()
    # evaluate(inputdir, outputfile)

if __name__ == "__main__":
    main()
