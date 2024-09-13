# Created: 2023-07-03
# Latest Version: 2023-07-26
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

from corflow import fromElan,toElan
from collections import Counter
import sys
sys.path.append("../")
from corflow_additional_functions import define_content

input_path = "../../input_files/"
output_path = "../../output_files/"

old_eaf_files = ["meenujkatsi.wordtimes.eaf","piivyeebe_ajyu.wordtimes.eaf"]
new_eaf_files = ["mc_bora_meenujkatsi.eaf","mc_bora_ajyuwa.eaf"]

for file_index in range(len(old_eaf_files)):
    trans_old_file = fromElan.fromElan(input_path+old_eaf_files[file_index],encoding="UTF-8")
    trans_new_file = fromElan.fromElan(input_path+new_eaf_files[file_index],encoding="UTF-8")
    old_file_name = old_eaf_files[file_index]
    new_file_name = new_eaf_files[file_index]
    print(f"Old file name: {old_file_name}")
    print(f"New file name: {new_file_name}")
    print("*******************************")

    #Old file.
    mb_tier_exists = False
    mt_tier_exists = False

    #DICT: Collect every mb_seg type as a key, if it occurs as either an affix or a clitic. It gets an empty list as a value. Afterwards, every mt_seg instance gets appended to that list.
    mb_seg_type_affix_or_clitic = {}

    for tier in trans_old_file:
        if "mb@" in tier.name:
            mb_tier = trans_old_file.getName(tier.name)
            mb_tier_exists = True
        elif "mt@" in tier.name:
            mt_tier = trans_old_file.getName(tier.name)
            mt_tier_exists = True

        if mb_tier_exists & mt_tier_exists:
            mb_tier_exists = False
            mt_tier_exists = False
            print("mb and mt Tiers were found.")

            for mb_seg in mb_tier:
                if mb_seg.children()[2].content.startswith("-") or mb_seg.children()[2].content.endswith("-"):
                    if not mb_seg.content in mb_seg_type_affix_or_clitic.keys():
                        mb_seg_type_affix_or_clitic[mb_seg.content] = []
            for mb_seg_type in mb_seg_type_affix_or_clitic.keys():
                for mb_seg in mb_tier:
                    if mb_seg_type == mb_seg.content:
                        mb_seg_type_affix_or_clitic[mb_seg_type].append(mb_seg.children()[2].content)
    print("ALL AFFIXES/CLITICS:")
    print("####################")
    print([(key,Counter(value)) for (key,value) in mb_seg_type_affix_or_clitic.items()])
    print("####################")

    #3 DICTS: Sort every mb_seg type, occuring as an affix or clitic, into one of the three following dicts: a) mb_seg types only occuring as affixes; b) mb_seg types only occuring as clitics, c) mb_seg types having instances occuring as affixes and as clitics.
    mb_seg_type_only_clitic = {}
    mb_seg_type_only_affix = {}
    mb_seg_type_affix_clitic_mix = {}

    for mb_seg_type,mt_segs_list in mb_seg_type_affix_or_clitic.items():
        affix_clitic_mix_found = False
        if "-CLT" in mt_segs_list:
            for mt_seg in mt_segs_list:
                if mt_seg != "-CLT":
                    mb_seg_type_affix_clitic_mix[mb_seg_type] = mt_segs_list
                    affix_clitic_mix_found = True
                    break
            if affix_clitic_mix_found == False:
                mb_seg_type_only_clitic[mb_seg_type] = mt_segs_list
        else:
            mb_seg_type_only_affix[mb_seg_type] = mt_segs_list

    #Fixing the 3 DICTS: Certain morphs a) either had not their correct morph type assigned to them or b) are to complicated to be handeled. The a)-cases get removed and then added to their appropriate list. The b)-cases get extra treatment.

    #a)-cases: Removing from the wrong dict.
    #'-úvu' is a suffix only.
    if "-úvu" in mb_seg_type_only_clitic.keys():
        mb_seg_type_only_clitic.pop("-úvu")
    if "-úvu" in mb_seg_type_affix_clitic_mix.keys():
        mb_seg_type_affix_clitic_mix.pop("-úvu")
    #'-hja' is a clitic only.
    if "-hja" in mb_seg_type_affix_clitic_mix.keys():
        mb_seg_type_affix_clitic_mix.pop("-hja")
    if "-hja" in mb_seg_type_only_affix.keys():
        mb_seg_type_only_affix.pop("-hja")

    #a)-cases: Adding tho the right dict.
    if not "-úvu" in mb_seg_type_only_affix.keys():
        mb_seg_type_only_affix["-úvu"] = ["-INF"]
    if not "-hja" in mb_seg_type_only_clitic.keys():
        mb_seg_type_only_clitic["-hja"] = ["-CLT"]

    #b)-cases: 'juco' will be changed based on Franks annotations. Therefore, it gets removed here:
    if "-juco" in mb_seg_type_only_clitic.keys():
        mb_seg_type_only_clitic.pop("-juco")
    if "-jucoo" in mb_seg_type_only_clitic.keys():
        mb_seg_type_only_clitic.pop("-jucoo")
    if "-juco" in mb_seg_type_only_affix.keys():
        mb_seg_type_only_affix.pop("-juco")
    if "-jucoo" in mb_seg_type_only_affix.keys():
        mb_seg_type_only_affix.pop("-jucoo")
    if "-juco" in mb_seg_type_affix_clitic_mix.keys():
        mb_seg_type_affix_clitic_mix.pop("-juco")
    if "-jucoo" in mb_seg_type_affix_clitic_mix.keys():
        mb_seg_type_affix_clitic_mix.pop("-jucoo")

    print("ONLY CLITICS")
    for key,val in mb_seg_type_only_clitic.items():
        print(f"{key}: {Counter(val)}")
    print("############")
    print("ONLY AFFIXES")
    for key,val in mb_seg_type_only_affix.items():
        print(f"{key}: {Counter(val)}")
    print("############")
    print("MIXED")
    for key,val in mb_seg_type_affix_clitic_mix.items():
        print(f"{key}: {Counter(val)}")
    print("############")

    #3 DICTS: Creating dicts collecting every gl_seg type that gets assigned to the previously collected mb_seg types, which are affixes or clitics:
    gl_seg_type_only_clitic = {}
    for key in mb_seg_type_only_clitic.keys():
        gl_seg_type_only_clitic[key] = []
    gl_seg_type_only_affix = {}
    for key in mb_seg_type_only_affix.keys():
        gl_seg_type_only_affix[key] = []
    gl_seg_type_affix_clitic_mix = {}
    for key in mb_seg_type_affix_clitic_mix.keys():
        gl_seg_type_affix_clitic_mix[key] = []

    mb_tier_exists = False
    gl_tier_exists = False
    for tier in trans_old_file:
        if "mb@" in tier.name:
            mb_tier = trans_old_file.getName(tier.name)
            mb_tier_exists = True
        elif "gl@" in tier.name:
            gl_tier = trans_old_file.getName(tier.name)
            gl_tier_exists = True

        if mb_tier_exists & gl_tier_exists:
            mb_tier_exists = False
            gl_tier_exists = False

            for mb_seg_type,gl_seg_type_list in gl_seg_type_only_affix.items():
                for mb_seg in mb_tier:
                    if mb_seg.content == mb_seg_type:
                        if not mb_seg.children()[0].content in gl_seg_type_list:
                            gl_seg_type_list.append(mb_seg.children()[0].content)
            for mb_seg_type,gl_seg_type_list in gl_seg_type_only_clitic.items():
                for mb_seg in mb_tier:
                    if mb_seg.content == mb_seg_type:
                        if not mb_seg.children()[0].content in gl_seg_type_list:
                            gl_seg_type_list.append(mb_seg.children()[0].content)
            for mb_seg_type,gl_seg_type_list in gl_seg_type_affix_clitic_mix.items():
                for mb_seg in mb_tier:
                    if mb_seg.content == mb_seg_type:
                        if not mb_seg.children()[0].content in gl_seg_type_list:
                            gl_seg_type_list.append(mb_seg.children()[0].content)

    #The b)-cases again: Changing the new gl_seg type dicts:
    gl_seg_type_only_clitic["-va"] = ["-QUOT"]
    if "-va" in gl_seg_type_only_affix.keys():
        if "-QUOT" in gl_seg_type_only_affix["-va"]:
            gl_seg_type_only_affix["-va"].pop(gl_seg_type_only_affix["-va"].index("-QUOT"))
    if "-va" in gl_seg_type_affix_clitic_mix.keys():
        if "-QUOT" in gl_seg_type_affix_clitic_mix["-va"]:
            gl_seg_type_affix_clitic_mix["-va"].pop(gl_seg_type_affix_clitic_mix["-va"].index("-QUOT"))
    gl_seg_type_only_affix["-va"] = gl_seg_type_affix_clitic_mix["-va"]
    gl_seg_type_affix_clitic_mix.pop("-va")

    #Processing those mb_seg types again, which had instances of affixes and clitics.
    mb_tier_exists = False
    gl_tier_exists = False
    for tier in trans_old_file:
        if "mb@" in tier.name:
            mb_tier = trans_old_file.getName(tier.name)
            mb_tier_exists = True
        elif "gl@" in tier.name:
            gl_tier = trans_old_file.getName(tier.name)
            gl_tier_exists = True

        if mb_tier_exists & gl_tier_exists:
            mb_tier_exists = False
            gl_tier_exists = False

            for mb_type in gl_seg_type_affix_clitic_mix.keys():
                gl_segs_for_mb_type_as_clitic = []
                gl_segs_for_mb_type_as_affix = []
                for mb_seg in mb_tier:
                    if mb_type == mb_seg.content:
                        if mb_seg.children()[2].content == "-CLT":
                            if not mb_seg.children()[0].content in gl_segs_for_mb_type_as_clitic:
                                gl_segs_for_mb_type_as_clitic.append(mb_seg.children()[0].content)
                        elif (mb_seg.children()[2].content.startswith("-")) | (mb_seg.children()[2].content.endswith("-")):
                            if not mb_seg.children()[0].content in gl_segs_for_mb_type_as_affix:
                                gl_segs_for_mb_type_as_affix.append(mb_seg.children()[0].content)
                gl_seg_type_only_affix[mb_type] = gl_segs_for_mb_type_as_affix
                gl_seg_type_only_clitic[mb_type] = gl_segs_for_mb_type_as_clitic

    #Fixing one mixed b)-case where one gloss appeared as one for an affix and clitic, but has to be reserved for the affix case only.
    gl_seg_type_only_clitic["-ne"] = ["-REC"]

    print("GL SEG TYPES FOR: ONLY CLITICS")
    for key,val in gl_seg_type_only_clitic.items():
        print(f"{key}: {val}")
    print("############")
    print("GL SEG TYPES FOR: ONLY AFFIXES")
    for key,val in gl_seg_type_only_affix.items():
        print(f"{key}: {val}")
    print("############")
    print("GL SEG TYPES FOR: AFFIXES AND CLITICS MIXED")
    for key,val in gl_seg_type_affix_clitic_mix.items():
        print(f"{key}: {val}")
    print("############")

    #Before the actual manipulations happen: Check whether a gloss type of a morph type also occurs as a gloss for another morph type. This makes sure that a) affix and clitic instances of a morph type can be strictly distinguished by their gloss types and that b) morph types with the same sign except for the dash can also be strictly distinguished from another by their gloss types.
    print_similarities_between_morph_types = False
    if print_similarities_between_morph_types:
        for mb_type,gl_type_list in gl_seg_type_only_clitic.items():
            for gl_type in gl_type_list:
                for mb_type2,gl_type_list2 in gl_seg_type_only_clitic.items():
                    if mb_type != mb_type2:
                        if gl_type in gl_type_list2:
                            print(f"Found gl_type occurence for CLITIC /MORPH: {mb_type} with GLOSS: {gl_type}/ in CLITIC <MORPH2: {mb_type2} in {gl_type_list2}.")
                            print("-----------------------------------")
                for mb_type2,gl_type_list2 in gl_seg_type_only_affix.items():
                    if gl_type in gl_type_list2:
                        print(f"Found gl_type occurence for CLITIC /MORPH: {mb_type} with GLOSS: {gl_type}/ in AFFIX <MORPH2: {mb_type2} in {gl_type_list2}.")
                        print("-----------------------------------")
        for mb_type,gl_type_list in gl_seg_type_only_affix.items():
            for gl_type in gl_type_list:
                for mb_type2,gl_type_list2 in gl_seg_type_only_affix.items():
                    if mb_type != mb_type2:
                        if gl_type in gl_type_list2:
                            print(f"Found gl_type occurence for AFFIX /MORPH: {mb_type} with GLOSS: {gl_type}/ in AFFIX <MORPH2: {mb_type2} in {gl_type_list2}>.")
                            print("-----------------------------------")
                for mb_type2,gl_type_list2 in gl_seg_type_only_clitic.items():
                    if gl_type in gl_type_list2:
                        print(f"Found gl_type occurence for AFFIX /MORPH: {mb_type} with GLOSS: {gl_type}/ in CLITIC <MORPH2: {mb_type2} in {gl_type_list2}>.")
                        print("-----------------------------------")

    #New file.
    gram_ftok_tier_exists = False
    gram_mtok_tier_exists = False
    gloss_ftok_tier_exists = False
    gloss_mtok_tier_exists = False
    gram_tier_exists = False

    for tier in trans_new_file:
        if "grammatical_words_mtok" == tier.name:
            gram_mtok_tier = trans_new_file.getName(tier.name)
            gram_mtok_tier_exists = True
        elif "grammatical_words_ftok" == tier.name:
            gram_ftok_tier = trans_new_file.getName(tier.name)
            gram_ftok_tier_exists = True
        elif "gloss_mtok" == tier.name:
            gloss_mtok_tier = trans_new_file.getName(tier.name)
            gloss_mtok_tier_exists = True
        elif "gloss_ftok" == tier.name:
            gloss_ftok_tier = trans_new_file.getName(tier.name)
            gloss_ftok_tier_exists = True
        elif "grammatical_words" == tier.name:
            gram_tier = trans_new_file.getName(tier.name)
            gram_tier_exists = True

        if gram_mtok_tier_exists & gram_ftok_tier_exists & gloss_mtok_tier_exists & gloss_ftok_tier_exists & gram_tier_exists:
            gram_ftok_tier_exists = False
            gram_mtok_tier_exists = False
            gloss_ftok_tier_exists = False
            gloss_mtok_tier_exists = False
            gram_tier_exists = False
            print("!!!ALL NECESSARY TIERS TO MANIPULATE WERE FOUND!!!")

            #The actual manipulations for all cases of clear <morph type,gloss type>-pairs.
            for mb_type,gl_type_list in gl_seg_type_only_clitic.items():
                for gl_type in gl_type_list:
                    define_content(trans_new_file,gram_ftok_tier.name,mb_type.replace("-","="),cond1=(gram_ftok_tier.name,mb_type.replace("-","")),cond2=(gloss_ftok_tier.name,gl_type.replace("-","")))
            for mb_type,gl_type_list in gl_seg_type_only_affix.items():
                for gl_type in gl_type_list:
                    define_content(trans_new_file,gram_ftok_tier.name,mb_type,cond1=(gram_ftok_tier.name,mb_type.replace("-","")),cond2=(gloss_ftok_tier.name,gl_type.replace("-","")))

            #The following manipulations had to be done based on other informations than those collected from the old files:
            #There was only one strange instance, where 'ó' was glossed as 'how'.
            define_content(trans_new_file,gram_ftok_tier.name,"ó",cond1=(gram_ftok_tier.name,"o"),cond2=(gloss_ftok_tier.name,"1SG"))
            define_content(trans_new_file,gloss_ftok_tier.name,"1SG",cond1=(gram_ftok_tier.name,"ó"),cond2=(gloss_ftok_tier.name,"how",False))
            define_content(trans_new_file,gram_ftok_tier.name,"ó=",cond1=(gram_ftok_tier.name,"ó"),cond2=(gram_tier.name,"MATCH","ó="))

            define_content(trans_new_file,gloss_ftok_tier.name,"2SG",cond=(gloss_ftok_tier.name,"2.SG"))
            define_content(trans_new_file,gram_ftok_tier.name,("=","ADD_TO_END"),cond1=(gram_ftok_tier.name,"u"),cond2=(gloss_ftok_tier.name,"2SG"),cond3=(gram_tier.name,"MATCH","u="))

            define_content(trans_new_file,gram_ftok_tier.name,"i=",cond1=(gram_ftok_tier.name,"i-"),cond2=(gloss_ftok_tier.name,"3"))

            #'juco' and 'jucoo': gram_mtok_tier as condition.
            define_content(trans_new_file,gram_ftok_tier.name,"=juco",cond1=(gram_ftok_tier.name,"juco"),cond2=(gram_mtok_tier.name,"juco="))
            define_content(trans_new_file,gram_ftok_tier.name,"=jucoo",cond1=(gram_ftok_tier.name,"jucoo"),cond2=(gram_mtok_tier.name,"jucoo="))
            define_content(trans_new_file,gram_ftok_tier.name,"-juco",cond1=(gram_ftok_tier.name,"juco"),cond2=(gram_mtok_tier.name,"juco-"))
            define_content(trans_new_file,gram_ftok_tier.name,"-jucoo",cond1=(gram_ftok_tier.name,"jucoo"),cond2=(gram_mtok_tier.name,"jucoo-"))

            #'juco' and 'jucoo': gram_ftok_tier as condition.
            define_content(trans_new_file,gram_ftok_tier.name,"=juco",cond=(gram_ftok_tier.name,"juco="))
            define_content(trans_new_file,gram_ftok_tier.name,"=jucoo",cond=(gram_ftok_tier.name,"jucoo="))
            define_content(trans_new_file,gram_ftok_tier.name,"-juco",cond=(gram_ftok_tier.name,"juco-"))
            define_content(trans_new_file,gram_ftok_tier.name,"-jucoo",cond=(gram_ftok_tier.name,"jucoo-"))

            define_content(trans_new_file,gram_ftok_tier.name,"****",cond=(gram_ftok_tier.name,"?"))
            define_content(trans_new_file,gram_ftok_tier.name,"****",cond=(gram_ftok_tier.name,"-?"))
            define_content(trans_new_file,gloss_ftok_tier.name,"****",cond=(gloss_ftok_tier.name,"?"))
            define_content(trans_new_file,gloss_ftok_tier.name,"****",cond=(gloss_ftok_tier.name,"-?"))

            #Changing all gl_segs as affixes or clitics accordingly to their morph type parent and its status.
            define_content(trans_new_file,gloss_ftok_tier.name,("=","ADD_TO_START"),cond=(gram_ftok_tier.name,"startswith","="))
            define_content(trans_new_file,gloss_ftok_tier.name,("=","ADD_TO_END"),cond=(gram_ftok_tier.name,"endswith","="))
            define_content(trans_new_file,gloss_ftok_tier.name,("-","ADD_TO_START"),cond=(gram_ftok_tier.name,"startswith","-"))
            define_content(trans_new_file,gloss_ftok_tier.name,("-","ADD_TO_END"),cond=(gram_ftok_tier.name,"endswith","-"))

            define_content(trans_new_file,gram_ftok_tier.name,"=i",cond1=(gram_ftok_tier.name,"i"),cond2=(gloss_ftok_tier.name,"yet"))
            define_content(trans_new_file,gloss_ftok_tier.name,"=yet",cond1=(gram_ftok_tier.name,"=i"),cond2=(gloss_ftok_tier.name,"yet"))

            #One specific instance of '-ne' glossed as 'INAN' changed to be glossed as 'say' was done manually in the second mc-file.

            #This operation searches for every instance of the gloss '=yet' and a previously occuring gloss 'finally' or 'wait'. It merges the contents of the time-aligned morphs and afterwards deletes the respective morph-gloss pair (the gloss "=yet" and ist manifestations e.g. '=iíkye').
            for gl_seg in gloss_ftok_tier:
                if (gl_seg.content == "yet") | (gl_seg.content == "-yet") | (gl_seg.content == "=yet"):
                    if gl_seg.index() != 0:
                        if (gloss_ftok_tier.elem[gl_seg.index()-1].content == "finally") | (gloss_ftok_tier.elem[gl_seg.index()-1].content == "wait"):
                            if gl_seg.start == gloss_ftok_tier.elem[gl_seg.index()-1].end:
                                for mb_seg in gram_ftok_tier:
                                    if (mb_seg.start == gl_seg.start) & (mb_seg.end == gl_seg.end):
                                        gram_ftok_tier.elem[mb_seg.index()-1].end = mb_seg.end
                                        gloss_ftok_tier.elem[gl_seg.index()-1].end = gl_seg.end
                                        gram_ftok_tier.elem[mb_seg.index()-1].content += mb_seg.content.replace("=","").replace("-","")
                                        gram_ftok_tier.pop(mb_seg.index())
                                        gloss_ftok_tier.pop(gl_seg.index())
            
            define_content(trans_new_file,gram_ftok_tier.name,["ó","=iíkye"],cond=(gram_ftok_tier.name,["ó=","=iíkye"]))
            define_content(trans_new_file,gloss_ftok_tier.name,["1SG","=yet"],cond=(gloss_ftok_tier.name,["1SG=","=yet"]))



    toElan.toElan(output_path+new_file_name,trans_new_file)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("END OF PROCESSING A FILE PAIR")
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
