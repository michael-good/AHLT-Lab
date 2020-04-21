def check_interaction(analysis, entities, id_e1, id_e2):
    """
        Given two entities that belong to a sentence, check_interaction tries to find the type
        of interaction between them if any

        Parameters:
            analysis: Grammar dependency tree
            entities: List of all entities of the current sentence
            id_e1: Entity of the sentence number 1 to compare
            id_e2: Entity of the sentence number 2 to compare
        Returns:
            Whether there is interaction or not between two entities and its type
    """
    found_e1 = False
    found_e2 = False

    # check they aren't multielements (that one word is used for more than one)
    if len(entities[id_e1]) == 2 and len(entities[id_e2]) == 2:
        start_e1 = int(entities[id_e1][0])
        end_e1 = int(entities[id_e1][1])
        start_e2 = int(entities[id_e2][0])
        end_e2 = int(entities[id_e2][1])

        # get info of the two entities
        for e in range(1, len(analysis.nodes)):
            node = analysis.nodes[e]
            if 'start' in node:
                start = node["start"]
                end = node["end"]

                if start >= start_e1 and end <= end_e1:
                    found_e1 = True
                    node_entity1 = node
                elif start >= start_e2 and end <= end_e2:
                    found_e2 = True
                    node_entity2 = node

        # (2) check if same parent
        # check if 1under2 or 2under1 (1) has been analyzed but doesn't add anything
        if found_e1 and found_e2:
            if node_entity1["head"] == node_entity2["head"]:
                if node_entity1["rel"] == 'conj' and node_entity2["rel"] == 'conj':
                    return 0, 'null'

        # (3) look for the verbs between the two entities
        for e in range(1, len(analysis.nodes)):
            node = analysis.nodes[e]
            if 'start' in node:
                start = node["start"]
                end = node["end"]
                if start >= start_e1 and end <= end_e2:
                    if 'V' in node["tag"]:
                        if (
                         'VB' == node["tag"] and node["lemma"] == 'increase' or
                         'V' in node["tag"] and node["lemma"] == 'decrease' or
                         'V' in node["tag"] and node["lemma"] == 'interfere' or
                         'V' in node["tag"] and node["lemma"] == 'inhibit' or
                         'V' in node["tag"] and node["lemma"] == 'alter' or
                         'VB' == node["tag"] and node["lemma"] == 'cause' or
                         'V' in node["tag"] and node["lemma"] == 'delay' or
                         'V' in node["tag"] and node["lemma"] == 'raise'):
                            return 1, 'mechanism'

                        elif (
                         'VBP' == node["tag"] and node["lemma"] == 'include' or
                         'V' in node["tag"] and node["lemma"] == 'potentiate' or
                         'VB' == node["tag"] and node["lemma"] == 'enhance' or
                         'VB' == node["tag"] and node["lemma"] == 'reduce' or
                         'VBZ' in node["tag"] and node["lemma"] == 'produce' or
                         'V' in node["tag"] and node["lemma"] == 'antagonize'):
                            return 1, 'effect'

                        elif (
                         'V' in node["tag"] and node["lemma"] == 'tell' or
                         'VBN' == node["tag"] and node["lemma"] == 'administer' or
                         'V' in node["tag"] and node["lemma"] == 'take' or
                         'V' in node["tag"] and node["lemma"] == 'exceed'):
                            return 1, 'advise'

                        elif (
                         'VBZ' == node["tag"] and node["lemma"] == 'suggest' or
                         'V' in node["tag"] and node["lemma"] == 'interact'):
                            return 1, 'int'

                        else:
                            return 0, 'null'

    return 0, 'null'
