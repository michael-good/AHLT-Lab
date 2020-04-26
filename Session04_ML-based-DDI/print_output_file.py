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
            if check and number_node_e1 == None:
                print('e1: ', start_e1, end_e1)
                # print('e1 '+str(i)+': ', node["start"], node["start"] >= start_e1, node["end"], node["end"] <= end_e1)
                # print('e1 '+str(i)+': ', node["start"], node["start"] <= start_e1, node["end"], node["end"] >= end_e1)
                print('e1 ' + str(i) + ': ', node["start"], node["start"] >= start_e1, node["start"] <= end_e1)
                print('e1 ' + str(i) + ': ', node["end"], node["end"] <= start_e1, node["end"] >= end_e1)
            if check and number_node_e2 == None:
                print('e2: ', start_e2, end_e2)
                # print('e2 '+str(i)+': ', node["start"], node["start"] >= start_e2, node["end"], node["end"] <= end_e2)
                # print('e2 '+str(i)+': ', node["start"], node["start"] >= start_e2, node["end"], node["end"] >= end_e2)
                print('e2 ' + str(i) + ': ', node["start"], node["start"] >= start_e2, node["start"] <= end_e2)
                print('e2 ' + str(i) + ': ', node["end"], node["end"] >= start_e2, node["end"] >= end_e2)
            # if ((start_e1 >= node["start"] and node["end"] <= end_e1 and number_node_e1 is None) or
            #     (node["start"] <= start_e1 and node["end"] >= end_e1 and number_node_e1 is None) ):
            if ((start_e1 >= node["start"] and start_e1 <= node["end"] and number_node_e1 is None) or
                    (end_e1 >= node["start"] and end_e1 <= node["end"] and number_node_e1 is None)):
                if check:
                    print('found e1')
                number_node_e1 = i
            # elif ((node["start"] >= start_e2 and node["end"] <= end_e2 and number_node_e2 is None) or
            #     (node["start"] <= start_e2 and node["end"] >= end_e2 and number_node_e2 is None) ):
            if ((start_e2 >= node["start"] and start_e2 <= node["end"] and number_node_e2 is None) or
                    (end_e2 >= node["start"] and end_e2 <= node["end"] and number_node_e2 is None)):
                if check:
                    print('found e2')
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


def print_output(sentence, ground, outf, type):
    if ground == type:
        outf.write(sentence+'\n')
