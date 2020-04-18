#!/usr/bin/python3

import sys
# prints the number of times a relation between the entities appears in each type
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def main():

    feat_file_effects=open('type_relations_effect.txt', 'r')
    line = feat_file_effects.readline()
    dict_eff = {}
    #elements in general
    for line in feat_file_effects:
        if not is_number(line):
            type_i = line.split()[0]
            if type_i in dict_eff:
                dict_eff[type_i]+=1
            else:
                dict_eff[type_i]=1
    feat_file_effects.close()

    feat_file_mechanism=open('type_relations_mechanism.txt', 'r')
    line = feat_file_mechanism.readline()
    dict_mecha = {}
    #elements in general
    for line in feat_file_mechanism:
        if not is_number(line):
            type_i = line.split()[0]
            if type_i in dict_mecha:
                dict_mecha[type_i]+=1
            else:
                dict_mecha[type_i]=1
    feat_file_mechanism.close()

    feat_file_int=open('type_relations_int.txt', 'r')
    line = feat_file_int.readline()
    dict_int = {}
    #elements in general
    for line in feat_file_int:
        if not is_number(line):
            type_i = line.split()[0]
            if type_i in dict_int:
                dict_int[type_i]+=1
            else:
                dict_int[type_i]=1
    feat_file_int.close()

    feat_file_advise=open('type_relations_advise.txt', 'r')
    line = feat_file_advise.readline()
    dict_adv = {}
    #elements in general
    for line in feat_file_advise:
        if not is_number(line):
            type_i = line.split()[0]
            if type_i in dict_adv:
                dict_adv[type_i]+=1
            else:
                dict_adv[type_i]=1
    feat_file_advise.close()

    feat_file_null=open('type_relations_null.txt', 'r')
    line = feat_file_null.readline()
    dict_null = {}
    #elements in general
    for line in feat_file_null:
        if not is_number(line):
            type_i = line.split()[0]
            if type_i in dict_null:
                dict_null[type_i]+=1
            else:
                dict_null[type_i]=1
    feat_file_null.close()



    print('interactions ----------------')
    print('effect')
    for key in ['drug-drug','drug-drug_n','drug-group','drug-band','drug_n-drug','drug_n-drug_n','drug_n-group','grup_n-band','group-drug','group-drug_n','group-group','group-band','band-drug','band-drug_n','band-group','band-band']:
        if key in dict_eff:
            print('\t'+ key+ ': '+ str(dict_eff[key]))

    print('mechanism')
    for key in ['drug-drug','drug-drug_n','drug-group','drug-band','drug_n-drug','drug_n-drug_n','drug_n-group','grup_n-band','group-drug','group-drug_n','group-group','group-band','band-drug','band-drug_n','band-group','band-band']:
        if key in dict_mecha:
            print('\t'+ key+ ': '+ str(dict_mecha[key]))

    print('advise')
    for key in ['drug-drug','drug-drug_n','drug-group','drug-band','drug_n-drug','drug_n-drug_n','drug_n-group','grup_n-band','group-drug','group-drug_n','group-group','group-band','band-drug','band-drug_n','band-group','band-band']:
        if key in dict_adv:
            print('\t'+ key+ ': '+ str(dict_adv[key]))

    print('int')
    for key in ['drug-drug','drug-drug_n','drug-group','drug-band','drug_n-drug','drug_n-drug_n','drug_n-group','grup_n-band','group-drug','group-drug_n','group-group','group-band','band-drug','band-drug_n','band-group','band-band']:
        if key in dict_int:
            print('\t'+ key+ ': '+ str(dict_int[key]))

    print('null')
    for key in ['drug-drug','drug-drug_n','drug-group','drug-band','drug_n-drug','drug_n-drug_n','drug_n-group','grup_n-band','group-drug','group-drug_n','group-group','group-band','band-drug','band-drug_n','band-group','band-band']:
        if key in dict_null:
            print('\t'+ key+ ': '+ str(dict_null[key]))


if __name__ == '__main__':
    main()
