
def return_type(text, ind, tlist):
    type = "other"
    typeaux = 'other'

    if (
        "MHD" in text or
        "NaC" in text or
        "MC" in text or
        "gaine" in text or
        (len(text)>16 and ((text[0].isdigit() and text[1]=='-') or (text[0].isdigit() and text[1].isdigit() and text[2]=='-'))) or #1- or 16-
        (len(text)>10 and ((text[0].isdigit() and text[1]==',' and text[2].isdigit()))) or #1,3
        text.lower().startswith('bombe') or
        text.lower().startswith('contor') or
        text.lower().startswith('dmp') or
        text.lower().startswith('egf') or
        text.lower().startswith('ginse') or
        text.lower().startswith('hero') or
        text.lower().startswith('ibo') or
        text.lower().startswith('jac') or
        "PTX" in text or
        text.lower().startswith('phen') and text[4]!='o' and text[4]!='y' or
        'PCP' in text ):
            type = "drug_n"

    elif(
    text.lower().startswith('(') and tlist[ind+1][0]==('-' or '+') ):
            type = 4
            typeaux = 'drug_n'

    # if it has the prefix word, it returns a special case
    elif ( len(tlist)-ind >2 and (
        text.lower().startswith('central') and tlist[ind+1][0].lower().startswith('nervous') and tlist[ind+2][0].lower().startswith('system') )):
        # text.lower().startswith('beFsdgsgsg') )):
            type = 4
            typeaux = 'group'
    elif ( len(tlist)-ind >2 and (
        text.lower().startswith('beta-adre') or
        (text.lower().startswith('hmg') or text.lower().startswith('monoamine')) and tlist[ind+2][0].lower().startswith('inh') or
        text.lower().startswith('calcium') and tlist[ind+2][0].lower().startswith('blocke') or
        text.lower().startswith('cns') and tlist[ind+1][0].lower().startswith('blocke') and tlist[ind+1][0].lower().startswith('blocke') or
        text.lower().startswith('cns') and tlist[ind+2][0].lower().startswith('drugs') )):
        # text.lower().startswith('beFsdgsgsg') )):
            type = 3
            typeaux = 'group'
    elif ( len(tlist)-ind >1 and (
        text.lower().startswith('beta') and 'blocke' in tlist[ind+1][0].lower() or
        text.lower().startswith('psycho') or
        (text.lower().startswith('cepha') or text.lower().startswith('macro')) and 'antibiotics' in tlist[ind+1][0].lower() or
        (text.lower().startswith('prot') or text.lower().startswith('ace') or text.lower().startswith('mao')) and tlist[ind+1][0].lower().startswith('inh') or
        text.lower().startswith('cardiac') and tlist[ind+1][0].lower().startswith('glyco') or
        text.lower().startswith('cns') and tlist[ind+1][0].lower().startswith('depres') or
        text.lower().startswith('hormonal') and tlist[ind+1][0].lower().startswith('contrac') or
        text.lower().startswith('cou') and tlist[ind+1][0].lower().startswith('anti') or
        text.lower().startswith('digi') and (tlist[ind+1][0].lower().startswith('gly') or tlist[ind+1][0].lower().startswith('prep')) or
        (text.lower().startswith('pota') or text.lower().startswith('loop') or text.lower().startswith('thiazide')) and tlist[ind+1][0].lower().startswith('diu') )):
        # text.lower().startswith('fdgsdgsdg') )):
            type = 2
            typeaux = 'group'

    elif (
        text.endswith('zides') or
        text.startswith('sali') or
        "ids" in text or
        "urea" in text.lower() or
        text.lower().startswith('quino') and not tlist[ind+1][0].lower().startswith('anti') or
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
        text.lower().startswith('diu') ):
        # "fjksdgksd" in text.lower() ):
            type = "group"

    elif (
        text.isupper() or
        text.startswith("SPR") or
        text.startswith('Acc') or
        "aspirin" in text.lower() or
        "PEGA" in text or
        "XX" in text or
        "IVA" in text ):
            type = "brand"

    elif (
        text.endswith('azole') or
        text.endswith('ine') or
        text.endswith('amine') or
        text.endswith('mycin') or
        text.endswith('avir') or
        text.endswith('ide') or
        text.endswith('olam') or
        text.endswith('il') or
        text.lower().endswith('cin') or
        text.lower().endswith('tin') or
        text.startswith('z') or
        text.startswith('cef') or
        text.startswith("amph") or
        "hydr" in text or
        "cyclo" in text or
        "ole" in text or
        "ano" in text or
        "ium" in text or
        'phen' in text or
        'yl' in text or
        'hol' in text or
        'carb' in text.lower() or
        'chlor' in text.lower() or
        'ofen' in text.lower() ):
            type = "drug"

    # if len(text) <= 2:
    #         type = "other"
    return type, typeaux
