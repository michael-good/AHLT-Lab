def number_entities(tree, start_e1, end_e1, start_e2, end_e2):
    number_node_e1 = None
    number_node_e2 = None

    # get the element number of the entities
    for i in range(1, len(tree.nodes)):
        node = tree.nodes[i]
        # it's not a bracket
        if 'start' in node:
            if node["start"] >= start_e1 and node["end"] <= end_e1 and number_node_e1 is None:
                number_node_e1 = i
            elif node["start"] >= start_e2 and node["end"] <= end_e2 and number_node_e2 is None:
                number_node_e2 = i
    return number_node_e1, number_node_e2


def extract_features(tree, entities, e1, e2):
    features = []  # where the list of features of all the sentence will be

    # print(len(entities[e1]), len(entities[e2]), entities[e1], entities[e2])
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

        # (2) check who is under who (direct child case)
        # look if in the dependencies of one of the entities appears the other
        if node_e1["head"] == number_node_e2:
            features.append('1under2')
            features.append('rel='+ str(node_e1["rel"]))

        elif node_e2["head"] == number_node_e1:
            features.append('2under1')
            features.append('rel='+ str(node_e2["rel"]))

        # (3) check who is under who (same parent case)
        # look if in the dependencies of the actual element appear both entities as childs
        elif node_e1["head"] == node_e2["head"]:
            features.append('same_father')
            features.append('rel='+str(node_e1["rel"]) +'-'+ str(node_e2["rel"]))

        for i in range(1, len(tree.nodes)):
            node = tree.nodes[i]
            # print(node)
            # it's not a bracket
            if 'start' in node:
                offset_start = node["start"]
                offset_end = node["end"]
                # it's not one of the entities we are featuring
                if i != number_node_e1 and i != number_node_e2:
                    # (1) get the position relative to the entities of each word
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

                # (4) return the verbs of the sentence
                if 'VB' in node["tag"]:
                    features.append('verb=' + node["lemma"])

    return features
