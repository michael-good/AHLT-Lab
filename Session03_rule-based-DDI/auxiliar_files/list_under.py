#!/usr/bin/python3

import sys
# prints the number of times a verb appears in each type
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def main():

    verb_search = sys.argv[1]

    feat_file_effects=open('under_effects.txt', 'r')
    line = feat_file_effects.readline()
    dict_eff = {}
    #elements in general
    for line in feat_file_effects:
        if not is_number(line):
            verb = line.split()[0][:-1]
            type_verb = line.split()[1]
            if verb == verb_search:
                if type_verb in dict_eff:
                    dict_eff[type_verb]+=1
                else:
                    dict_eff[type_verb]=1
    feat_file_effects.close()

    feat_file_mechanism=open('under_mechanism.txt', 'r')
    line = feat_file_mechanism.readline()
    dict_mecha = {}
    #elements in general
    for line in feat_file_mechanism:
        if not is_number(line):
            verb = line.split()[0][:-1]
            type_verb = line.split()[1]
            if verb == verb_search:
                if type_verb in dict_mecha:
                    dict_mecha[type_verb]+=1
                else:
                    dict_mecha[type_verb]=1
    feat_file_mechanism.close()

    feat_file_int=open('under_int.txt', 'r')
    line = feat_file_int.readline()
    dict_int = {}
    #elements in general
    for line in feat_file_int:
        if not is_number(line):
            verb = line.split()[0][:-1]
            type_verb = line.split()[1]
            if verb == verb_search:
                if type_verb in dict_int:
                    dict_int[type_verb]+=1
                else:
                    dict_int[type_verb]=1
    feat_file_int.close()

    feat_file_advise=open('under_advise.txt', 'r')
    line = feat_file_advise.readline()
    dict_adv = {}
    #elements in general
    for line in feat_file_advise:
        if not is_number(line):
            verb = line.split()[0][:-1]
            type_verb = line.split()[1]
            if verb == verb_search:
                if type_verb in dict_adv:
                    dict_adv[type_verb]+=1
                else:
                    dict_adv[type_verb]=1
    feat_file_advise.close()

    feat_file_null=open('under_null.txt', 'r')
    line = feat_file_null.readline()
    dict_null = {}
    #elements in general
    for line in feat_file_null:
        if not is_number(line):
            verb = line.split()[0][:-1]
            type_verb = line.split()[1]
            if verb == verb_search:
                if type_verb in dict_null:
                    dict_null[type_verb]+=1
                else:
                    dict_null[type_verb]=1
    feat_file_null.close()



    print('verb '+verb_search+' ---------')
    output_effect = 'effect \t'
    for key in dict_eff:
        output_effect = output_effect +'\t'+ key+ ': '+ str(dict_eff[key])
    print(output_effect)

    output_mechanism = 'mechanism '
    for key in dict_mecha:
        output_mechanism = output_mechanism +'\t'+ key +': '+ str(dict_mecha[key])
    print(output_mechanism)

    output_advise = 'advise \t'
    for key in dict_adv:
        output_advise = output_advise +'\t'+ key +': '+ str(dict_adv[key])
    print(output_advise)

    output_int = 'int \t'
    for key in dict_int:
        output_int = output_int +'\t'+ key +': '+ str(dict_int[key])
    print(output_int)

    output_null = 'null \t'
    for key in dict_null:
        output_null = output_null +'\t'+ key +': '+ str(dict_null[key])
    print(output_null)


if __name__ == '__main__':
    main()
