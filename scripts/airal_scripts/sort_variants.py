#Created: 2024-06-16
#Latest Version: 2024-06-16
#Script written by Aleksandr Schamberger (GitHub: JLEKS) as part of the AIRAL project by Ludger Paschen at ZAS Berlin.

import copy

def clean(token:str):
    tok = copy.copy(token)
    if tok.startswith(("-","=")):
        tok = tok[1:]
    if tok.endswith(("=","-")):
        tok = tok[:-1]
    return tok

input_path = "../../input_files"

#variants = [('-1INCL', '1INCL'), ('-1SG', '1SG-'), ('1EXCL=', '1EXCL'), ('3PL', '-3PL'), ('ASP=', 'ASP'), ('3SG', '-3SG'), ('2SG-', '-2SG'), ('NEG', 'NEG='), ('courir', 'courir='), ('être=', 'être'), ('DEI.P', '=DEI.P'), ('-PA', 'PA'), ('-IRR', 'IRR'), ('NOM', '-NOM'), ('1SG', '1SG='), ('=DIR', 'DIR'), ('3SG=', '-3SG'), ('3PL.DU', '3PL.DU='), ('2SG', '-2SG'), ('1SG=', '1SG-'), ('1SG=', '-1SG'), ('-1INCL', '1INCL='), ('3SG.ASP.EC-', '3SG.ASP.EC='), ('3SG', '3SG-'), ('3PL.ASP.EC', '3PL.ASP.EC='), ('2SG=', '-2SG'), ('3SG.ASP.EC', '3SG.ASP.EC='), ('1INCL.DU', '-1INCL.DU'), ('regarder', 'regarder='), ('ART.C=', 'ART.C'), ('ASP.J=', 'ASP.J'), ('3SG-', '-3SG'), ('3SG', '3SG='), ('2SG.ASP.EC', '2SG.ASP.EC='), ('DIR', 'DIR='), ('3SG=', '3SG-'), ('oiseau', '-oiseau'), ('nager=', 'nager'), ('3PL=', '-3PL'), ('2SG-', '2SG='), ('-DEI.P', 'DEI.P'), ('3SG.ASP.EC-', '3SG.ASP.EC'), ('FUT=', 'FUT'), ('ART.P=', 'ART.P'), ('INDEF', '-INDEF'), ('2SG', '2SG-'), ('1INCL', '1INCL='), ('COO.VB=', 'COO.VB'), ('1SG', '1SG-'), ('=DIR', 'DIR='), ('3PL.DU=', '-3PL.DU'), ('ASP.C', 'ASP.C='), ('1SG', '-1SG'), ('-IRR', 'IRR='), ('OBJ', 'OBJ='), ('-DEI.P', '=DEI.P'), ('2SG', '2SG='), ('3PL.DU', '-3PL.DU'), ('2PL=', '2PL'), ('INT', '-INT'), ('IRR', 'IRR='), ('3PL', '3PL=')]

variants = [('=2SG', '-2SG'), ('IND-', '-IND'), ('-NEG', 'NEG'), ('DEM', '-DEM'), ('2SG', '-2SG'), ('-NEG', 'NEG-'), ('3SG', '=3SG'), ('3PL-', '-3PL'), ('=3SG', '-3SG'), ('3SG.OBL', '=3SG.OBL'), ('=COP.1SG', 'COP.1SG='), ('NEG', 'NEG-'), ('1PL', '-1PL'), ('-2PL', '2PL'), ('FUT=', '=FUT'), ('3PL-', '3PL'), ('1SG', '-1SG'), ('EZ-', '-EZ'), ('2SG', '=2SG')]

unique_tokens = set()
for x,y in variants:
    unique_tokens.add(x)
    unique_tokens.add(y)
unique_tokens = list(unique_tokens)

var_groups = [[]]
for tok1 in unique_tokens:
    group = set()
    for tok2 in unique_tokens:
        if tok1 == tok2:
            continue
        if clean(tok1) == clean(tok2):
            old_group = False
            for grp in var_groups:
                if (tok1 in grp) | (tok2 in grp):
                    grp.add(tok1)
                    grp.add(tok2)
                    old_group = True
                    break
            if old_group == False:
                group.add(tok1)
                group.add(tok2)
    if group:
        var_groups.append(group)

var_groups = var_groups[1:]
with open(input_path+"/pairs.csv", "w") as file:
    for group in var_groups:
        for tok in group:
            file.write(tok+",")
        file.write("\n")