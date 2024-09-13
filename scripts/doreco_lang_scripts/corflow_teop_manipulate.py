# Created: May 2023
# Latest Version: 2023-06-07
# Script written by Michelle Elizabeth Throssell Balagué and Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

import os
from corflow import fromElan, toElan
import glob
import re
import sys
sys.path.append("../")
from corflow_additional_functions import define_content_old_version_tier_match

path = "../../input_files"
eaf_files = glob.glob(path + "/*.eaf")
#print(eaf_files)

for file in eaf_files:
    file_name = file.replace(path, "")
    print("##########################")
    print(file_name)
    print("############################")
    trans = fromElan.fromElan(file, encoding="utf-8")

    gl_tier_fix_exists = False
    gram_tier_fix_exists = False
    for tier in trans:
        if tier.name == "gloss":
            gl_tier_fix = trans.getName(tier.name)
            gl_tier_fix_exists = True
        elif tier.name == "grammatical_words":
            gram_tier_fix = trans.getName(tier.name)
            gram_tier_fix_exists = True
        if gl_tier_fix_exists & gram_tier_fix_exists:
            for gl_seg_fix in gl_tier_fix:
                if gl_seg_fix.parent() == None:
                    print("Content: "+str(gl_seg_fix.content))
                    print((gl_seg_fix.start,gl_seg_fix.end))
                    print("Now Parent: "+str(gl_seg_fix.parent()))
                    print("*******************")
                    for gram_seg_fix in gram_tier_fix:
                        if (gram_seg_fix.start == gl_seg_fix.start) & (gram_seg_fix.end == gl_seg_fix.end):
                            gl_seg_fix.setParent(gram_seg_fix)
                            print("New parent: "+str(gl_seg_fix.parent().content))
                            print("------------------------")
                        elif (gram_seg_fix.start < gl_seg_fix.start) & (gram_seg_fix.end == gl_seg_fix.end):
                            gl_seg_fix.setParent(gram_seg_fix)
                            print("New parent: "+str(gl_seg_fix.parent().content))
                            print("------------------------")
                        elif (gram_seg_fix.start == gl_seg_fix.start) & (gram_seg_fix.end > gl_seg_fix.end):
                            gl_seg_fix.setParent(gram_seg_fix)
                            print("New parent: "+str(gl_seg_fix.parent().content))
                            print("------------------------")
                        elif (gram_seg_fix.start < gl_seg_fix.start) & (gram_seg_fix.end > gl_seg_fix.end):
                            gl_seg_fix.setParent(gram_seg_fix)
                            print("New parent: "+str(gl_seg_fix.parent().content))
                            print("------------------------")

    # bea
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","be=a",["be=","a"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","be=a",["if|when=","ART2.SG"])
    # bean
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","be=an",["be=","an"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","be=an",["if|when=","2SG.PRON"])
    # beori
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","be=ori",["be=","ori"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","be=ori",["if|when=","3PL.PRON"])
    # benaa
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","be=naa",["be=","naa"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","be=naa",["if|when=","1SG.PRON"])

    # teo
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","te=o",["te=","o"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","te=o",["PREP=","ART3.SG"])
    # teori
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","te=ori",["te=","ori"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","te=ori",["PREP=","3PL.PRON"])
    # tea
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","te=a",["te=","a"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","te=a",["PREP=","ART2.SG"])
    # tenaa
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","te=naa",["te=","naa"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","te=naa",["PREP=","1SG.PRON"])
    # tean
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","te=an",["te=","an"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","te=an",["PREP=","2SG.PRON"])
    # tenam
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","te=nam",["te=","nam"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","te=nam",["PREP=","1PL.EX.PRON"])
    # tee
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","te=e",["te=","e"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","te=e",["PREP=","ART1.SG"])
    # teve
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","te=eve",["te=","eve"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","te=eve",["PREP=","3SG.PRON"])

    # meo
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","me=o",["me=","o"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","me=o",["and4=","ART3.SG"])
    # meori
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","me=ori",["me=","ori"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","me=ori",["PREP=","3PL.PRON"])
    # mee
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","me=e",["me=","e"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","me=e",["and4=","ART1.SG"])
    # mea
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","me=a",["me=","a"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","me=a",["and4=","ART2.SG"])
    # mean
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","me=an",["me=","an"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","me=an",["and4=","2SG.PRON"])
    # menaa
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","me=naa",["me=","naa"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","me=naa",["and4=","1SG.PRON"])
    # menam
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","me=nam",["me=","nam"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","me=nam",["and4=","1PL.EX.PRON"])
    # merau
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","me=rau",["me=","rau"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","me=rau",["and4=","DEM5"])
    # merau
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","me=erau",["me=","erau"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","me=erau",["and4=","so"])

    # mai
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","ma=i",["ma=","i"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","ma=i",["hither=","3SG.PRON"])
    # mae
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","ma=e",["ma=","e"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","ma=i",["hither=","ART1.SG"])
    # mau
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","ma=u",["ma=","=u"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","ma=u",["hither=","=IMM"])

    # voen
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","vo=en",["vo=","en"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","vo=en",["like=","DEM3"])
    # vone
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","vo=n=e",["vo=","n=","e"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","vo=n=e",["like=","3IPFV=","ART1.SG"])
    # voa
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","vo=a",["vo=","a"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","vo=a",["like=","ART2.SG"])
    # vomaen
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","vo=ma=en",["vo=","ma=","en"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","vo=nom=en",["like=","hither=","DEM3"])

    # voan
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","vo=an",["vo=","an"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","vo=an",["GOAL=","2SG.PRON"])
    # vori
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","vo=ori",["vo=","ori"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","vo=ori",["GOAL=","3PL.PRON"])
    #check all vori's
    # vonomen
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","vo=nom=en",["vo=","nom=","en"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","vo=nom=en",["GOAL=","IPFV=","DEM3"])
    # venei
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","v=enei",["v=","enei"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","v=enei",["GOAL=","this.way"])
    
    # mepaa
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","me=paa",["me=","paa"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","me=paa",["and4=","TAM3"])
    # repaa
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","re=paa",["re=","paa"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","re=paa",["CONSEC=","TAM3"])

    # riori
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","ri=ori",["ri=","ori"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","ri=ori",["3PL.IPFV=","3PL.PRON"])

    # kie
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","ki=e",["ki=","e"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","ki=e",["DAT=","3SG.PRON"])
    # kiri
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","ki=ri",["ki=","ri"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","ki=ri",["DAT=","3PL.OBJM"])
    # kirie
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","ki=ri=e",["ki=","ri=","e"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","ki=ri=e",["DAT=","3PL.IPFV=","3SG.PRON"])

    # nie
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","ni=e",["ni","=e"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","ni=e",["APPL","=3SG.PRON"])
    # nia
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","ni=a",["ni","=a"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","ni=a",["APPL","=ART2.SG"])

    # ore
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","o=re",["o=","re"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","o=re",["3PRON=","CONSEC"])
    # are
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","a=re",["a=","re"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","a=re",["1PL.IN=","CONSEC"])

    # vua
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","vu=a",["vu=","a"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","vu=a",["IMM=","ART2.SG"])
    # vuan
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","vu=an",["vu=","an"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","vu=an",["2SG.OBJM=","2SG.PRON"])

    # vonaen
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","vo=na=en",["vo=","na=","en"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","vo=na=en",["IMM=","3SG.IPFV=","DEM3"])
    # vonaenei
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","vo=na=enei",["vo=","na=","enei"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","vo=na=enei",["IMM=","3SG.IPFV=","this.way"])

    # maana
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","maa=na",["maa","=na"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","maa=na",["hither","=3SG.IPFV"])
    # maaen
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","maa=en",["maa","=en"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","maa=en",["hither","=DEM3"])
    # maari
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","maa=ri",["maa","=ri"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","maa=ri",["hither","=3PL.IPFV"])

    # amaa
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","a=maa",["a","=maa"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","a=maa",["ART2.SG","=PLM"])
    # anaa
#    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","a=naa",["a=","naa"])
#    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","a=naa",["OBJM=","1SG.PRON"])

    # ka
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","k=a",["k=","a"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","k=a",["DAT=","OBJM"])
    # kanaa
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","k=a=naa",["k=","a=","naa"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","k=a=naa",["DAT=","OBJM=","1SG.PRON"])
    # karara
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","k=ara=ara",["k=","ara=","ara"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","k=ara=ara",["DAT=","1PL.IN.OBJM=","1PL.IN.PRON"])
    # kanom
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","ka=nom",["ka=","nom"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","ka=nom",["DAT=","IPFV"])

    # batana
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","bata=na",["bata=","na"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","bata=na",["CONT=","3SG.IPFV"])
    # batari
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","bata=ri",["bata=","ri"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","bata=ri",["CONT=","3PL.IPFV"])
    # batara
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","bata=ra",["bata=","ra"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","bata=ra",["CONT=","1PL.IN.IPFV"])

    # haana
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","haa=na",["haa=","na"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","haa=na",["NEG=","3SG.IPFV"])
    # haari
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","haa=ri",["haa=","ri"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","haa=ri",["NEG=","3PL.IPFV"])
    # haara
    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","haa=ra",["haa=","ra"])
    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","haa=ra",["NEG=","1PL.IN.IPFV"])

   # evehe
#    define_content_old_version_tier_match(trans,"grammatical_words","grammatical_words_mtok","evehe",["evehe"])
#    define_content_old_version_tier_match(trans,"grammatical_words","gloss_mtok","evehe",["but"])

    toElan.toElan("../../output_files"+str(file_name),trans)