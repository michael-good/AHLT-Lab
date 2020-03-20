def return_type(text, index, token_list):
    type_ = 'other'
    type_aux = 'other'

    if (
            'MHD' in text or
            'NaC' in text or
            'MC' in text or
            'gaine' in text or
            (len(text) > 16 and ((text[0].isdigit() and text[1] == '-') or
                                 (text[0].isdigit() and text[1].isdigit() and text[2] == '-'))) or  # 1- or 16-
            (len(text) > 10 and (text[0].isdigit() and text[1] == ',' and text[2].isdigit())) or  # 1,3
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

    elif (
            text.lower().startswith('(') and token_list[index + 1][0] == ('-' or '+')):
        type_ = 4
        type_aux = 'drug_n'

    # if it has the prefix word, it returns a special case
    elif (len(token_list) - index > 2 and
          (text.lower().startswith('central') and
           token_list[index + 1][0].lower().startswith('nervous') and
           token_list[index + 2][0].lower().startswith('system'))):
        # text.lower().startswith('beFsdgsgsg') )):
        type_ = 4
        type_aux = 'group'
    elif (len(token_list) - index > 2 and
          (text.lower().startswith('beta-adre') or
           (text.lower().startswith('hmg') or text.lower().startswith('monoamine')) and token_list[index + 2][
               0].lower().startswith('inh') or
           text.lower().startswith('calcium') and token_list[index + 2][0].lower().startswith('blocke') or
           text.lower().startswith('cns') and token_list[index + 1][0].lower().startswith('blocke') and
           token_list[index + 1][
               0].lower().startswith('blocke') or
           text.lower().startswith('cns') and token_list[index + 2][0].lower().startswith('drugs'))):
        # text.lower().startswith('beFsdgsgsg') )):
        type_ = 3
        type_aux = 'group'
    elif (len(token_list) - index > 1 and (
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
        # text.lower().startswith('fdgsdgsdg') )):
        type_ = 2
        type_aux = 'group'

    elif (
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
        # "fjksdgksd" in text.lower() ):
        type_ = 'group'

    elif (
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

    # if len(text) <= 2:
    #         type = "other"
    return type_, type_aux
