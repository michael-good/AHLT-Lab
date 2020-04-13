def extract_features(tree, entities, e1, e2, hsdb_list=None, drug_bank=None):
    features = []  # where the list of features of all the sentence will be
    # print('extract featureeeees')
    # print('tree')
    # print(tree)
    # print(entities)
    # print(e1, entities[e1], e2, entities[e2])

    # ignore multi formed words
    # (that result in span of [34, 43;70 ,85] for example)
    if len(entities[e1])==2 and len(entities[e2])==2:

        # 1st feature: if it's before after or inbetween the entities ------
        starte1 = int(entities[e1][0])
        ende1 = int(entities[e1][1])
        starte2 = int(entities[e2][0])
        ende2 = int(entities[e2][1])

        for e in range(1, len(tree.nodes)):
            node = tree.nodes[e]
            # print(node)
            # it's not a bracket
            if 'start' in node:
                start = node["start"]
                # it's not one of the entities we are featuring
                if start != starte1 and start != starte2:
                    # print('start e1', starte1, 'start e2', starte2, 'start', start)
                    if start < starte1:
                        features.append('lb1='+ node["lemma"])
                    elif start > starte1 and start < starte2:
                        features.append('b12='+ node["lemma"])
                    elif start > starte2:
                        features.append('lib='+ node["lemma"])


        # word = node['word']
        # start_off, end_off = getOffsets(sentence, word)
        # # returns start_off=-1 if didn't find the word in the sentence
        # if start_off != -1:
        #     node['start'] = start_off
        #     node['end'] = end_off


    # for ind, word in enumerate(s):
    #     feat = []  # where list of features for that word will be saved
    #
    #     # word itself
    #     feat.append('form=' + word[0])
    #
    #     # looking at external resources
    #     if not (hsdb_list is None and drug_bank is None):
    #         if word[0].lower() in hsdb_list:
    #             feat.append('hsdb_drug')
    #         for key, value in drug_bank.items():
    #             if word[0].lower() == key.lower():
    #                 feat.append('drug_bank_' + value)
    #
    #     # last [1,..,5] letters
    #     for sufix in [1, 2, 3, 4, 5]:
    #         if len(word[0]) >= sufix:
    #             feat.append('suf' + str(sufix) + '=' + word[0][(-sufix):])
    #         else:
    #             feat.append('suf' + str(sufix) + '=' + word[0])
    #
    #     # first [1,..,5] letters
    #     for prefix in [1, 2, 3, 4, 5]:
    #         if len(word[0]) >= prefix:
    #             feat.append('pref' + str(prefix) + '=' + word[0][:prefix])
    #         else:
    #             feat.append('pref' + str(prefix) + '=' + word[0])
    #
    #     # next [1, .., 3] words
    #     for next in [1, 2, 3]:
    #         if ind >= len(s) - next:
    #             feat.append('next' + str(next) + '=_EoS_')
    #         else:
    #             feat.append('next' + str(next) + '=' + s[ind + next][0])
    #
    #     # previous [1,..,3] words
    #     for prev in [1, 2, 3]:
    #         if ind <= prev:
    #             feat.append('prev' + str(prev) + '=_BoS_')
    #         else:
    #             feat.append('prev' + str(prev) + '=' + s[ind - prev][0])
    #
    #     # length of the word
    #     feat.append('len=' + str(word[2] - word[1]))
    #
    #     # if punctuation
    #     if (not word[0].isalpha() and not word[0].isdigit()):
    #         feat.append('punct')
    #
    #     # if capitalized or all capitalized (without counting the numbers or punctuation)
    #     upper = 0
    #     letter = 0
    #     for let in word[0]:
    #         if let.isalpha():
    #             letter += 1
    #         if let.isupper():
    #             upper += 1
    #     if upper > 0:
    #         if upper == letter:
    #             feat.append('allCapitalized')
    #         else:
    #             feat.append('capitalized')
    #
    #     # how many numbers
    #     number = 0
    #     for let in word[0]:
    #         if let.isdigit():
    #             number += 1
    #     feat.append('numbers=' + str(number))
    #
    #     # features from rules from lab1
    #     if ('MHD' in word[0] or
    #             'NaC' in word[0] or
    #             'MC' in word[0] or
    #             'gaine' in word[0] or
    #             word[0].lower().startswith('bombe') or
    #             word[0].lower().startswith('contor') or
    #             word[0].lower().startswith('dmp') or
    #             word[0].lower().startswith('egf') or
    #             word[0].lower().startswith('ginse') or
    #             word[0].lower().startswith('hero') or
    #             word[0].lower().startswith('ibo') or
    #             word[0].lower().startswith('jac') or
    #             'PTX' in word[0] or
    #             'PCP' in word[0]):
    #         feat.append('rules_drug_n')
    #     if (word[0].endswith('zides') or
    #             word[0].startswith('sali') or
    #             'ids' in word[0] or
    #             'urea' in word[0].lower() or
    #             word[0].lower().startswith('sali') or
    #             word[0].lower().startswith('ssri') or
    #             word[0].lower().startswith('cepha') or
    #             word[0].lower().startswith('sulfo') or
    #             word[0].startswith('TCA') or
    #             word[0].lower().startswith('thiaz') or
    #             word[0].lower().startswith('benzo') or
    #             word[0].lower().startswith('barb') or
    #             word[0].lower().startswith('contracept') or
    #             word[0].lower().startswith('cortico') or
    #             word[0].lower().startswith('digitalis') or
    #             word[0].lower().startswith('diu')):
    #         feat.append('rules_group')
    #     if (word[0].isupper() or
    #             word[0].startswith('SPR') or
    #             word[0].startswith('Acc') or
    #             word[0].lower().startswith('equ') or
    #             'aspirin' in word[0].lower() or
    #             'PEGA' in word[0] or
    #             'XX' in word[0] or
    #             'IVA' in word[0]):
    #         feat.append('rules_brand')
    #     if (word[0].endswith('azole') or
    #             word[0].endswith('ine') or
    #             word[0].endswith('amine') or
    #             word[0].endswith('mycin') or
    #             word[0].endswith('avir') or
    #             word[0].endswith('ide') or
    #             word[0].endswith('olam') or
    #             word[0].endswith('il') or
    #             word[0].endswith('pril') or
    #             word[0].lower().endswith('cin') or
    #             word[0].lower().endswith('tin') or
    #             word[0].startswith('z') or
    #             word[0].startswith('cef') or
    #             word[0].startswith('amph') or
    #             word[0].lower().startswith('epin') or
    #             word[0].lower().startswith('eryth') or
    #             word[0].lower().startswith('theo') or
    #             'hydr' in word[0] or
    #             'cyclo' in word[0] or
    #             'ole' in word[0] or
    #             'ano' in word[0] or
    #             'ium' in word[0] or
    #             'phen' in word[0] or
    #             'yl' in word[0] or
    #             'hol' in word[0] or
    #             'carb' in word[0].lower() or
    #             'chlor' in word[0].lower() or
    #             'ofen' in word[0].lower() or
    #             'efav' in word[0].lower() or
    #             'theophy' in word[0].lower()):
    #         feat.append('rules_drugs')
    #
    #     features.append(feat)
    return features
