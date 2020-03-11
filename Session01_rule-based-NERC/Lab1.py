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


def return_type(text, prev):
    type = "other"

    if (text.isupper() or text.startswith("SP") or text.startswith('Acc')
        or "aspirin" in text.lower() or "PEGA" in text or "XX" in text or "IVA" in text ):
        type = "brand"

    elif (text.endswith('phane') or "MC" in text or "gaine" in text or
           (len(text)>16 and ((text[0].isdigit() and text[1]=='-') or (text[0].isdigit() and text[1].isdigit() and text[2]=='-'))) or #1- or 16-
           (len(text)>10 and ((text[0].isdigit() and text[1]==',' and text[2].isdigit()))) ): #1,3
        type = "drug_n"

    elif (text.startswith("anti") or text.startswith('beta-block') or
         text.startswith('Beta-block') or text.startswith('Beta-Block') or
         "thiazide" in text or "cont" in text or "ure" in text or "ids" in text ):
        type = "group"

    elif (text.endswith('azole') or text.endswith('ine') or text.endswith('amine') or
          text.endswith('mycin') or text.endswith('avir') or text.endswith('ide') or text.endswith('olam') or
          text.endswith('il') or text.lower().endswith('cin') or text.lower().endswith('tin') or
          text.startswith('z') or text.startswith('cef') or text.startswith("amph") or
          "hydr" in text or  "cyclo" in text or "ole" in text or "ano" in text or
          "ium" in text or 'phen' in text or 'yl' in text or 'hol' in text or
          'carb' in text.lower() or 'chlor' in text.lower() or 'ofen' in text.lower() ):
        type = "drug"

    # if it has the prefix word, it returns a special case
    elif text.startswith('beta') or text.startswith('Beta') :
        type = 'previous'

    elif text.startswith('agent') or text.startswith('Agent'):
        type = 'future'

    if len(text) <= 4:
        type = "other"

    return type

def check_edges_letter(element):
    type(element)
    if len(element)>1:
        if not str(element[-1]).isdigit():
          if not str(element[-1]).isalpha(): #check if last item is a letter or number
            if not str(element[-1]) == '%':
                return 'end'
        elif str(element[-1]) == ']' or str(element[-1]) == ')':
                return 'end'
        elif not str(element[0]).isdigit():
          if not str(element[0]).isalpha(): #check if last item is a letter or number
            if not str(element[-1]) == '-':
                return 'start'
        elif str(element[0]) == '[' or str(element[0]) == '(':
                return 'start'
    return 'none'

def extract_entities(token_list):
    previous = False
    list_entities = []
    #demands as implementation first
    auxiliar = {"name": '',
              "offset": str(0),
              "type": ''
              }
    for index, element in enumerate(token_list):

        modified=False
        # check if last letter is a number or alphabet
        while check_edges_letter(element[0]) == 'end':
            y = list(element) #convert to a list
            y[0] = y[0][0:-1] #change value since tuple are immutable
            element = tuple(y) #convert back to tuple
        while check_edges_letter(element[0]) == 'start':
            y = list(element)
            y[0] = y[0][1:]
            element = tuple(y)

        type = return_type(element[0], previous)

        if previous == True or type=='future': #the revious word was type='previous'
            entity = {"name": auxiliar['name']+' '+element[0],
                      "offset": auxiliar['offset'] + "-" + str(element[2]),
                      "type": 'group'
                      }
            list_entities.append(entity)
            previous = False

        elif type == 'previous': #if it's the previous word, we will only set the flag
            previous = True

        elif type != "other":
            entity = {"name": element[0],
                      "offset": str(element[1]) + "-" + str(element[2]),
                      "type": type
                      }
            list_entities.append(entity)
        # auxiliar element to get previous and future words
        auxiliar = {"name": element[0],
                  "offset": str(element[1]),
                  "type": type
                  }
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
    outputfile = "./task9.1_lluis_3.txt"
    nerc(inputdir, outputfile)


if __name__ == "__main__":
    main()
