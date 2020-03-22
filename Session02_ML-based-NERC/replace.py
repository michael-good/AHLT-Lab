import random

"""
This file processes DrugBank.txt and creates a new document DrugBank_partial.txt 
with a reduced size so that Lab2.py processing time is not so long
"""

outputfile = './resources/DrugBank_partial.txt'

filename_drug_bank = './resources/DrugBank.txt'

with open(filename_drug_bank, 'r',  encoding="utf8") as g:
    data = g.readlines()

drug_bank = {}
for sentence in data:
    split_sentence = sentence.rsplit('|', 1)
    drug_bank[split_sentence[0]] = split_sentence[-1].rstrip()

partial = {}
portion = 0.01 #1% of 100.000 (1.000)
# portion = 0.1 #10% (10.000)
for key, value in drug_bank.items():
    rnd = random.uniform(0, 1)
    if rnd < portion:
        partial.update({key:value})

f = open(outputfile, "w", encoding="utf8")
for key, value in partial.items():
    f.write(key+', '+value+'\n')
    # print(key, value)
f.close()
