
def return_type(text, index, token_list, hsdb_list=None, drug_bank=None):
    """
    Parses given XML file and retrieves the elements with tag 'sentence'

    Parameters:
        text: token word
        index: position of the token in token list created out of the text sentence
        token_list: list of words of the sentence
        hsdb_list: list of drugs. Only available when external resources activated
        drug_bank: list of possible sentences and their corresponding label
                   Only available when external resources activated
    Returns:
        type_: classification type of the token (text) analyzed
        type_aux:
    """
    type_ = 'other'
    type_aux = 'other'

    # Next if block only executes if external resources are enabled i.e. they have been loaded into memory.
    # If that is the case, the system will first try to classify the token using them. If classification is not
    # possible, it will then move on to perform a standard rule-based classification
    if not (hsdb_list is None and drug_bank is None):
        # Checks if the token exists in HSDB durg list. If that is the case, it is directly classified as drug
        if text.lower() in hsdb_list:
            return 'drug', 'drug'
        # For each line in DrugBank.txt, if its sentence matches the token return the type indicated by the document
        for key, value in drug_bank.items():
            if text.lower() == key.lower():
                return value, value

    # Set of rules not based on external resources used to perform drug classification
    if (
        # Set of rules to classify as drug_n class
            'MHD' in text or
            'NaC' in text or
            'MC' in text or
            'gaine' in text or
            (len(text) > 16 and ((text[0].isdigit() and text[1] == '-') or
                                 (text[0].isdigit() and text[1].isdigit() and text[2] == '-'))) or
            (len(text) > 10 and (text[0].isdigit() and text[1] == ',' and text[2].isdigit())) or
            text.lower().startswith('bombe') or
            text.lower().startswith('contor') or
            text.lower().startswith('dmp') or
            text.lower().startswith('egf') or
            text.lower().startswith('ginse') or
            text.lower().startswith('hero') or
            text.lower().startswith('ibo') or
            text.lower().startswith('jac') or
            'PTX' in text or
            text.lower().startswith('phen') and text[4] != 'o' and text[4] != 'y' or
            'PCP' in text):
        type_ = 'drug_n'

    elif text.lower().startswith('(') and token_list[index + 1][0] == ('-' or '+'):
        # If above condition is fulfilled it is an indicator that the current token is of type drug_n
        # and that it is the union of 4 tokens
        type_ = 4
        type_aux = 'drug_n'

    # if it has the prefix word, it returns a special case
    elif (
            # Set of rules to classify as group class. type_ is set to 4, which means that this token
            # possibly belongs to a group of 4 tokens that represent the same group
            len(token_list) - index > 2 and
          (text.lower().startswith('central') and
           token_list[index + 1][0].lower().startswith('nervous') and
           token_list[index + 2][0].lower().startswith('system'))):
        type_ = 4
        type_aux = 'group'
    elif (
            # Set of rules to classify as group class. This token is the third of a group of related tokens
            len(token_list) - index > 2 and
          (text.lower().startswith('beta-adre') or
           (text.lower().startswith('hmg') or text.lower().startswith('monoamine')) and token_list[index + 2][
               0].lower().startswith('inh') or
           text.lower().startswith('calcium') and token_list[index + 2][0].lower().startswith('blocke') or
           text.lower().startswith('cns') and token_list[index + 1][0].lower().startswith('blocke') and
           token_list[index + 1][
               0].lower().startswith('blocke') or
           text.lower().startswith('cns') and token_list[index + 2][0].lower().startswith('drugs'))):
        type_ = 3
        type_aux = 'group'
    elif (
            # Set of rules to classify as brand class. This token is the second of a group of related tokens
            len(token_list) - index > 1 and (
            text.lower().startswith('beta') and 'blocke' in token_list[index + 1][0].lower() or
            text.lower().startswith('psycho') or
            (text.lower().startswith('cepha') or text.lower().startswith('macro')) and 'antibiotics' in
            token_list[index + 1][
                0].lower() or
            (text.lower().startswith('prot') or text.lower().startswith('ace') or text.lower().startswith('mao')) and
            token_list[index + 1][0].lower().startswith('inh') or
            text.lower().startswith('cardiac') and token_list[index + 1][0].lower().startswith('glyco') or
            text.lower().startswith('cns') and token_list[index + 1][0].lower().startswith('depres') or
            text.lower().startswith('hormonal') and token_list[index + 1][0].lower().startswith('contrac') or
            text.lower().startswith('cou') and token_list[index + 1][0].lower().startswith('anti') or
            text.lower().startswith('digi') and (
                    token_list[index + 1][0].lower().startswith('gly') or token_list[index + 1][0].lower().startswith(
                'prep')) or
            (text.lower().startswith('pota') or text.lower().startswith('loop') or text.lower().startswith(
                'thiazide')) and token_list[index + 1][0].lower().startswith('diu'))):
        type_ = 2
        type_aux = 'group'

    elif (
            # Set of rules to classify as group class
            text.endswith('zides') or
            text.startswith('sali') or
            'ids' in text or
            'urea' in text.lower() or
            text.lower().startswith('quino') and not token_list[index + 1][0].lower().startswith('anti') or
            text.lower().startswith('sali') or
            text.lower().startswith('ssri') or
            text.lower().startswith('cepha') or
            text.lower().startswith('sulfo') or
            text.startswith('TCA') or
            text.lower().startswith('thiaz') or
            text.lower().startswith('benzo') or
            text.lower().startswith('barb') or
            text.lower().startswith('contracept') or
            text.lower().startswith('cortico') or
            text.lower().startswith('digitalis') or
            text.lower().startswith('diu')):
        type_ = 'group'

    elif (
            # Set of rules to classify as brand class
            text.isupper() or
            text.startswith('SPR') or
            text.startswith('Acc') or
            text.lower().startswith('equ') or
            'aspirin' in text.lower() or
            'PEGA' in text or
            'XX' in text or
            'IVA' in text):
        type_ = 'brand'

    elif (
            # Set of rules to classify as drug class
            text.endswith('azole') or
            text.endswith('ine') or
            text.endswith('amine') or
            text.endswith('mycin') or
            text.endswith('avir') or
            text.endswith('ide') or
            text.endswith('olam') or
            text.endswith('il') or
            text.endswith('pril') or
            text.lower().endswith('cin') or
            text.lower().endswith('tin') or
            text.startswith('z') or
            text.startswith('cef') or
            text.startswith('amph') or
            text.lower().startswith('epin') or
            text.lower().startswith('eryth') or
            text.lower().startswith('theo') or
            'hydr' in text or
            'cyclo' in text or
            'ole' in text or
            'ano' in text or
            'ium' in text or
            'phen' in text or
            'yl' in text or
            'hol' in text or
            'carb' in text.lower() or
            'chlor' in text.lower() or
            'ofen' in text.lower() or
            'efav' in text.lower() or
            'theophy' in text.lower()):
        type_ = 'drug'

    return type_, type_aux
