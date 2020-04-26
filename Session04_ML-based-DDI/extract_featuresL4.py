def number_entities(tree, start_e1, end_e1, start_e2, end_e2, check=False):
    number_node_e1 = None
    number_node_e2 = None
    if check:
        print('inside number entities function')

    # get the element number of the entities
    for i in range(1, len(tree.nodes)):
        node = tree.nodes[i]
        # it's not a bracket
        if 'start' in node:
            if check and number_node_e1==None:
                print('e1: ', start_e1, end_e1)
                # print('e1 '+str(i)+': ', node["start"], node["start"] >= start_e1, node["end"], node["end"] <= end_e1)
                # print('e1 '+str(i)+': ', node["start"], node["start"] <= start_e1, node["end"], node["end"] >= end_e1)
                print('e1 '+str(i)+': ', node["start"], node["start"] >= start_e1, node["start"] <= end_e1)
                print('e1 '+str(i)+': ', node["end"], node["end"] <= start_e1, node["end"] >= end_e1)
            if check and number_node_e2==None:
                print('e2: ', start_e2, end_e2)
                # print('e2 '+str(i)+': ', node["start"], node["start"] >= start_e2, node["end"], node["end"] <= end_e2)
                # print('e2 '+str(i)+': ', node["start"], node["start"] >= start_e2, node["end"], node["end"] >= end_e2)
                print('e2 '+str(i)+': ', node["start"], node["start"] >= start_e2, node["start"] <= end_e2)
                print('e2 '+str(i)+': ', node["end"], node["end"] >= start_e2, node["end"] >= end_e2)
            # if ((start_e1 >= node["start"] and node["end"] <= end_e1 and number_node_e1 is None) or
            #     (node["start"] <= start_e1 and node["end"] >= end_e1 and number_node_e1 is None) ):
            if ((start_e1 >= node["start"] and start_e1 <= node["end"] and number_node_e1 is None) or
                (end_e1 >= node["start"] and end_e1 <= node["end"] and number_node_e1 is None) ):
                if check:
                    print('found e1')
                number_node_e1 = i
            # elif ((node["start"] >= start_e2 and node["end"] <= end_e2 and number_node_e2 is None) or
            #     (node["start"] <= start_e2 and node["end"] >= end_e2 and number_node_e2 is None) ):
            if ((start_e2 >= node["start"] and start_e2 <= node["end"] and number_node_e2 is None) or
                (end_e2 >= node["start"] and end_e2 <= node["end"] and number_node_e2 is None) ):
                if check:
                    print('found e2')
                number_node_e2 = i
    return number_node_e1, number_node_e2

def indexin(el, list):
    '''
    returns if an element appears inside a list
    '''
    for ind in range(len(list)):
        if el==list[ind]:
            return True
    return False

def extract_features(tree, entities, e1, e2, i):
        features = []  # where the list of features of all the sentence will be
    # if i < 1 :
        # print(i, tree)
        # print(len(entities[e1]), len(entities[e2]), entities[e1], entities[e2])
        # ignore multi formed words that result in span of [34, 43;70 ,85] for example
        if len(entities[e1]) == 2 and len(entities[e2]) == 2:
            # print('\n neww entitiees')
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
            # print('entities1', number_node_e1, start_e1, end_e1)
            # print('entities2', number_node_e2, start_e2, end_e2)
            # print('entities', number_node_e1, number_node_e2)
            if number_node_e1==None or number_node_e2==None:
                print('Nooooooooooooooooooooooooooooooooooone')
                number_node_e1, number_node_e2 = number_entities(tree, start_e1, end_e1, start_e2, end_e2, True)
                print(tree)
                entotis = entotis-3
                #
                # print(start_e1, end_e1)
                # print(start_e2, end_e2)

            # we will get the path from the element 1 to the origin (0)
            path_e1 = [number_node_e1]
            head1 = number_node_e1
            # j=0
            while head1 != 0:
                node1 = tree.nodes[head1]
                # print(node)
                head1 = node1["head"]
                # print('head', head1)
                path_e1.append(head1)
                # j+=1
            # print('path e1', path_e1)

            path_e2 = [number_node_e2]
            head2 = number_node_e2
            # j=0
            while head2 != 0:
                node2 = tree.nodes[head2]
                # print(node)
                head2 = node2["head"]
                # print('head', head1)
                path_e2.append(head2)
                # j+=1
            # print('path e2', path_e2)


            # (5) return the relations between the e1/e2 and the path until the common element between them
            rel_e1 = [] #path with the relations
            for ind in range(len(path_e1)):
                if not indexin(path_e1[ind], path_e2):
                    actual_node = tree.nodes[path_e1[ind]]
                    rel_e1.append(actual_node["rel"])
                else:
                    break
            # print('rel e1', rel_e1)
            if len(rel_e1) > 0:
                sentence = 'rel_e1='+rel_e1[0]
                if len(rel_e1) > 1:
                    for i in range(1, len(rel_e1)):
                        sentence = sentence+'-'+rel_e1[i]
                # print('output', sentence)
                features.append(sentence)

            rel_e2 = [] #path with the relations
            for ind in range(len(path_e2)):
                if not indexin(path_e2[ind], path_e1):
                    actual_node = tree.nodes[path_e2[ind]]
                    rel_e2.append(actual_node["rel"])
                else:
                    break
            # print('rel e2', rel_e2)
            if len(rel_e2) > 0:
                sentence = 'rel_e2='+rel_e2[0]
                if len(rel_e2) > 1:
                    for i in range(1, len(rel_e2)):
                        sentence = sentence+'-'+rel_e2[i]
                # print('output', sentence)
                features.append(sentence)


            # (2) check who is under who (direct child case)
            # look if in the dependencies of one of the entities appears the other
            if node_e1["head"] == number_node_e2:
                features.append('1under2')

            elif node_e2["head"] == number_node_e1:
                features.append('2under1')

            # (3) check who is under who (same parent case)
            # look if in the dependencies of the actual element appear both entities as childs
            elif node_e1["head"] == node_e2["head"]:
                features.append('same_father')

            all_heads = []
            for i in range(1, len(tree.nodes)):
                node = tree.nodes[i]

                if node["rel"]!='punct': # if it's not a punctuation
                    all_heads.append(node["head"])
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
            # print(all_heads)
        else:
            features.append('multiple_length')

        return features
