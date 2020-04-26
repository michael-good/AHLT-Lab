def number_entities(tree, start_e1, end_e1, start_e2, end_e2, check=False):
    '''
    returns the node number of the entities
    '''
    number_node_e1 = None
    number_node_e2 = None

    for i in range(1, len(tree.nodes)):
        node = tree.nodes[i]
        # it's not a bracket
        if 'start' in node:
            if ((start_e1 >= node["start"] and start_e1 <= node["end"] and number_node_e1 is None) or
                    (end_e1 >= node["start"] and end_e1 <= node["end"] and number_node_e1 is None)):
                number_node_e1 = i

            if ((start_e2 >= node["start"] and start_e2 <= node["end"] and number_node_e2 is None) or
                    (end_e2 >= node["start"] and end_e2 <= node["end"] and number_node_e2 is None)):
                number_node_e2 = i

    return number_node_e1, number_node_e2


def indexin(el, list):
    '''
    returns if an element appears inside a list
    '''
    for ind in range(len(list)):
        if el == list[ind]:
            return True
    return False


def extract_features(tree, entities, e1, e2):
    features = []  # where the list of features of all the sentence will be

    # ignore multi formed words that result in span of [34, 43;70 ,85] for example
    if len(entities[e1]) == 2 and len(entities[e2]) == 2:
        # offsets of e1 and e2
        start_e1 = int(entities[e1][0])
        end_e1 = int(entities[e1][1])
        start_e2 = int(entities[e2][0])
        end_e2 = int(entities[e2][1])

        number_node_e1, number_node_e2 = number_entities(tree, start_e1, end_e1, start_e2, end_e2)
        node_e1 = tree.nodes[number_node_e1]
        deps_e1 = node_e1["deps"]
        node_e2 = tree.nodes[number_node_e2]
        deps_e2 = node_e2["deps"]

        # Get the path from element 1/2 to the origin 0
        path_e1 = [number_node_e1]
        head1 = number_node_e1
        while head1 != 0:
            node1 = tree.nodes[head1]
            head1 = node1["head"]
            path_e1.append(head1)

        path_e2 = [number_node_e2]
        head2 = number_node_e2
        while head2 != 0:
            node2 = tree.nodes[head2]
            head2 = node2["head"]
            path_e2.append(head2)

        # (9) Indicates if there is an 'interaction' within the sentence
        for i in range(1, len(tree.nodes)):
            node = tree.nodes[i]
            if node["rel"] != 'punct':  # if it's not a punctuation
                if 'interact' in node["lemma"]:
                    features.append('interact_appears')

        # (2) check who is under who (direct child case) and the distance
        direct_child = False
        dist_e1 = 0
        for nod in path_e1:
            if nod == number_node_e2:
                features.append('1under2-d' + str(dist_e1))
                direct_child = True
                break
            dist_e1 += 1

        dist_e2 = 0
        for nod in path_e2:
            if nod == number_node_e1:
                features.append('2under1-d' + str(dist_e2))
                direct_child = True
                break
            dist_e2 += 1

        # (3) check the common point (same parent case) and the distance
        if direct_child == False:
            dist_e1 = 0
            for ind in range(len(path_e1)):
                if not indexin(path_e1[ind], path_e2):
                    dist_e1 += 1
                else:
                    features.append('common_word=' + tree.nodes[path_e1[ind]]["lemma"])
                    features.append('common_word_type=' + tree.nodes[path_e1[ind]]["tag"])
                    break
            features.append('common_point_e1:d' + str(dist_e1))

            dist_e2 = 0
            for ind in range(len(path_e2)):
                if not indexin(path_e2[ind], path_e1):
                    dist_e2 += 1
                else:
                    break
            features.append('common_point_e2:d' + str(dist_e2))

        # (5) return the relations/words between the e1/e2 and the path until the common element between them
        rel_e1 = []
        words_e1 = [tree.nodes[number_node_e1]["lemma"]]
        # get the path of relations/words until the common element of the entity 1
        for p in path_e1:
            if not indexin(p, path_e2):
                actual_node = tree.nodes[p]
                rel_e1.append(actual_node["rel"])
                words_e1.append(tree.nodes[actual_node["head"]]["lemma"])
            else:
                break
        # print the feature of the path of relations/words
        for i, rel in enumerate(rel_e1):
            if i == 0:
                sentence_rel = 'rel_e1=' + rel
            else:
                sentence_rel = sentence_rel + '<' + rel
            features.append(sentence_rel)

        for i, wor in enumerate(words_e1):
            if i == 0:
                sentence_words = 'words_e1=' + wor
            else:
                sentence_words = sentence_words + '<' + wor
            features.append(sentence_words)

        # get the path of relations/words until the common element of the entity 2
        rel_e2 = []
        words_e2 = [tree.nodes[number_node_e2]["lemma"]]
        for p in path_e2:
            if not indexin(p, path_e1):
                actual_node = tree.nodes[p]
                rel_e2.append(actual_node["rel"])
                words_e2.append(tree.nodes[actual_node["head"]]["lemma"])
            else:
                break
        # print the feature of the path of relations/words
        for i, rel in enumerate(rel_e2):
            if i == 0:
                sentence_rel = 'rel_e2=' + rel
            else:
                sentence_rel = sentence_rel + '<' + rel
            features.append(sentence_rel)

        for i, wor in enumerate(words_e2):
            if i == 0:
                sentence_words = 'words_e2=' + wor
            else:
                sentence_words = sentence_words + '<' + wor
            features.append(sentence_words)

        # (6) verbs inbetween the two entities on the tree structure
        for p in path_e1:
            if not indexin(p, path_e2):
                actual_node = tree.nodes[p]
                if 'V' in actual_node["tag"]:
                    features.append('verb_between_tree=' + actual_node["lemma"] + '/' + actual_node["tag"])
            else:
                break
        for p in path_e2:
            if not indexin(p, path_e1):
                actual_node = tree.nodes[p]
                if 'V' in actual_node["tag"]:
                    features.append('verb_between_tree=' + actual_node["lemma"] + '/' + actual_node["tag"])
            else:
                break
        # (7) verbs inbetween the two entities on the sentence structure
        for i in range(1, len(tree.nodes)):
            node = tree.nodes[i]
            if 'V' in node["tag"]:
                if 'start' in node:
                    start = node["start"]
                    end = node["end"]
                    if start >= start_e1 and end <= end_e2:
                        features.append('verb_between_sentence=' + node["lemma"] + '/' + node["tag"])

        found = False
        for i in range(1, len(tree.nodes)):
            node = tree.nodes[i]
            if node["rel"] != 'punct':  # if it's not a punctuation
                if 'start' in node:
                    offset_start = node["start"]
                    offset_end = node["end"]
                    # it's not one of the entities we are featuring
                    if i != number_node_e1 and i != number_node_e2:

                        # (1) get the position relative to the entities of each word, not if it's a punctuation
                        # lb1 = lemma before 1
                        # la2 = lemma after 2
                        # lib = lemma in between
                        if start_e1 < offset_start < start_e2:
                            features.append('lib=' + node["lemma"])
                        else:
                            if offset_start < start_e1:
                                features.append('lb1=' + node["lemma"])

                            if offset_start > start_e2:
                                features.append('la2=' + node["lemma"])

            # (8) return the sentence inbetween
            if node["rel"] != 'punct':
                if 'start' in node:
                    offset_start = node["start"]
                    offset_end = node["end"]
                    if end_e1 < offset_start < start_e2:
                        if found == False:
                            sentence = 'sentence_between=' + node["lemma"]
                            found = True
                        else:
                            sentence = sentence + '<' + node["lemma"]
        if found:
            features.append(sentence)

    # if they are a multi-segmented element, we return only one feature
    else:
        features.append('multiple_length')

    return features
