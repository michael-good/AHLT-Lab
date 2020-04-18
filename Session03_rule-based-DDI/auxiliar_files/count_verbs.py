# file to obtain the number of times a verb appears on a file
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def main():
    feat_file_effects=open('verbs_effect.txt', 'r')
    line = feat_file_effects.readline()
    dict = {}
    #elements in general
    for line in feat_file_effects:
        if not is_number(line):
            verb = line.split()[0]
            if verb in dict:
                dict[verb]+=1
            else:
                dict[verb]=1
    feat_file_effects.close()
    results_effect=open('verbs_effect_count.txt', 'w')
    for key, value in sorted(dict.items(), key=lambda item: item[1]):
        results_effect.write("%s: %s \n" % (key, value))
    results_effect.close()

    feat_file_effects=open('verbs_mechanism.txt', 'r')
    line = feat_file_effects.readline()
    dict = {}
    #elements in general
    for line in feat_file_effects:
        if not is_number(line):
            verb = line.split()[0]
            if verb in dict:
                dict[verb]+=1
            else:
                dict[verb]=1
    feat_file_effects.close()
    results_effect=open('verbs_mechanism_count.txt', 'w')
    for key, value in sorted(dict.items(), key=lambda item: item[1]):
        results_effect.write("%s: %s \n" % (key, value))
    results_effect.close()

    feat_file_effects=open('verbs_advise.txt', 'r')
    line = feat_file_effects.readline()
    dict = {}
    #elements in general
    for line in feat_file_effects:
        if not is_number(line):
            verb = line.split()[0]
            if verb in dict:
                dict[verb]+=1
            else:
                dict[verb]=1
    feat_file_effects.close()
    results_effect=open('verbs_advise_count.txt', 'w')
    for key, value in sorted(dict.items(), key=lambda item: item[1]):
        results_effect.write("%s: %s \n" % (key, value))
    results_effect.close()

    feat_file_effects=open('verbs_int.txt', 'r')
    line = feat_file_effects.readline()
    dict = {}
    #elements in general
    for line in feat_file_effects:
        if not is_number(line):
            verb = line.split()[0]
            if verb in dict:
                dict[verb]+=1
            else:
                dict[verb]=1
    feat_file_effects.close()
    results_effect=open('verbs_int_count.txt', 'w')
    for key, value in sorted(dict.items(), key=lambda item: item[1]):
        results_effect.write("%s: %s \n" % (key, value))
    results_effect.close()

    feat_file_effects=open('verbs_null.txt', 'r')
    line = feat_file_effects.readline()
    dict = {}
    #elements in general
    for line in feat_file_effects:
        if not is_number(line):
            verb = line.split()[0]
            if verb in dict:
                dict[verb]+=1
            else:
                dict[verb]=1
    feat_file_effects.close()
    results_effect=open('verbs_null_count.txt', 'w')
    for key, value in sorted(dict.items(), key=lambda item: item[1]):
        results_effect.write("%s: %s \n" % (key, value))
    results_effect.close()

if __name__ == '__main__':
    main()
