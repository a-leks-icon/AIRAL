# Created: 2023-05-26
# Latest Version: 2023-05-29
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

from corflow import fromElan,toElan
import glob

def merging_in_savosavo(transcription,morph_tier_condition:tuple,gloss_tier_condition:tuple,pos_tier_name:str|tuple,word_tier_name:str|tuple):

    word_tier_exists = False
    morph_tier_exists = False
    gloss_tier_exists = False
    pos_tier_exists = False

    for tier in transcription:

        if len(morph_tier_condition) == 2:
            if morph_tier_condition[0] in tier.name:
                morph_tier = transcription.getName(tier.name)
                morph_tier_exists = True
                morph_seg_content = morph_tier_condition[1]
        elif len(morph_tier_condition) == 3:
            if morph_tier_condition[1] == "MATCH":
                if morph_tier_condition[0] == tier.name:
                    morph_tier = transcription.getName(tier.name)
                    morph_tier_exists = True
                    morph_seg_content = morph_tier_condition[2]
            elif morph_tier_condition[1] == "IN":
                if morph_tier_condition[0] in tier.name:
                    morph_tier = transcription.getName(tier.name)
                    morph_tier_exists = True
                    morph_seg_content = morph_tier_condition[2]

        if len(gloss_tier_condition) == 2:
            if gloss_tier_condition[0] in tier.name:
                gloss_tier = transcription.getName(tier.name)
                gloss_tier_exists = True
                gloss_seg_content = gloss_tier_condition[1]
        elif len(gloss_tier_condition) == 3:
            if gloss_tier_condition[1] == "MATCH":
                if gloss_tier_condition[0] == tier.name:
                    gloss_tier = transcription.getName(tier.name)
                    gloss_tier_exists = True
                    gloss_seg_content = gloss_tier_condition[2]
            elif gloss_tier_condition[1] == "IN":
                if gloss_tier_condition[0] in tier.name:
                    gloss_tier = transcription.getName(tier.name)
                    gloss_tier_exists = True
                    gloss_seg_content = gloss_tier_condition[2]

        if isinstance(pos_tier_name,str):
            if pos_tier_name in tier.name:
                pos_tier = transcription.getName(tier.name)
                pos_tier_exists = True
        elif isinstance(pos_tier_name,tuple):
            if len(pos_tier_name) == 2:
                if pos_tier_name[1] == "MATCH":
                    if pos_tier_name[0] == tier.name:
                        pos_tier = transcription.getName(tier.name)
                        pos_tier_exists = True
                elif pos_tier_name[1] == "IN":
                    if pos_tier_name[0] in tier.name:
                        pos_tier = transcription.getName(tier.name)
                        pos_tier_exists = True

        if isinstance(word_tier_name,str):
            if word_tier_name in tier.name:
                word_tier = transcription.getName(tier.name)
                word_tier_exists = True
        elif isinstance(word_tier_name,tuple):
            if len(word_tier_name) == 2:
                if word_tier_name[1] == "MATCH":
                    if word_tier_name[0] == tier.name:
                        word_tier = transcription.getName(tier.name)
                        word_tier_exists = True
                elif word_tier_name[1] == "IN":
                    if word_tier_name[0] in tier.name:
                        word_tier = transcription.getName(tier.name)
                        word_tier_exists = True

        if morph_tier_exists & gloss_tier_exists & pos_tier_exists & word_tier_exists:
            word_tier_exists = False
            morph_tier_exists = False
            gloss_tier_exists = False
            pos_tier_exists = False

            print("Found tiers:")
            print(morph_tier.name)
            print(gloss_tier.name)
            print(pos_tier.name)
            print(word_tier.name)

            for morph_seg in morph_tier:
                if morph_seg.content == morph_seg_content:
                    for gloss_seg in gloss_tier:
                        if (gloss_seg.content == gloss_seg_content) & ((gloss_seg.start == morph_seg.start) & (gloss_seg.end == morph_seg.end)):
                            for word_seg in word_tier:
                                if (((word_seg.start == morph_seg.start) & (word_seg.end == morph_seg.end)) & ((word_seg.start == gloss_seg.start) & (word_seg.end == gloss_seg.end))) & (word_seg.content.startswith(morph_seg_content)):

                                    word_tier.elem[word_seg.index()-1].end = word_seg.end
                                    word_tier.elem[word_seg.index()-1].content += word_seg.content

                                    morph_seg.setParent(word_tier.elem[word_seg.index()-1])
                                    morph_seg.content = "=" + morph_seg.content
                                    gloss_seg.content = "=" + gloss_seg.content

                                    for pos_seg in pos_tier:
                                        if (pos_seg.start == word_seg.start) & (pos_seg.end == word_seg.end):
                                            pos_seg.content = "=" + pos_seg.content

                                    word_tier.pop(word_seg.index())

                                elif ((word_seg.start == morph_seg.start) & (word_seg.start == gloss_seg.start)) & (word_seg.content.startswith(morph_seg_content)):

                                    word_tier.elem[word_seg.index()-1].end = word_seg.end
                                    word_tier.elem[word_seg.index()-1].content += word_seg.content

                                    morph_seg.content = "=" + morph_seg.content
                                    gloss_seg.content = "=" + gloss_seg.content

                                    for pos_seg in pos_tier:
                                        if pos_seg.start == word_seg.start:
                                            pos_seg.content = "=" + pos_seg.content

                                    for m_seg in morph_tier:
                                        if (m_seg.start == word_seg.start) | ((m_seg.start > word_seg.start) & (m_seg.end < word_seg.end)) | (m_seg.end == word_seg.end):
                                            m_seg.setParent(word_tier.elem[word_seg.index()-1])

                                    word_tier.pop(word_seg.index())

    print("Done!")

############################################################

path = "../../input_files/"
eaf_files = glob.glob(path+"/*.eaf")

for file in eaf_files:
    file_name = file.replace(path,"")
    print(file_name)

    trans = fromElan.fromElan(file,encoding="utf-8")

    word_tier_exists = False
    morph_tier_exists = False
    gloss_tier_exists = False
    pos_tier_exists = False
    referenced_tier_exists = False

    for tier in trans:
        if "sa@" in tier.name:
            word_tier = trans.getName(tier.name)
            word_tier_exists = True
        elif "mb@" in tier.name:
            morph_tier = trans.getName(tier.name)
            morph_tier_exists = True
        elif "gl@" in tier.name:
            gloss_tier = trans.getName(tier.name)
            gloss_tier_exists = True
        elif "wc@" in tier.name:
            pos_tier = trans.getName(tier.name)
            pos_tier_exists = True
        elif ("ref@" in tier.name) & (tier.name != "ref@unknown" ):
            referenced_tier = trans.getName(tier.name)
            referenced_tier_exists = True

        if word_tier_exists & morph_tier_exists & gloss_tier_exists & pos_tier_exists & referenced_tier_exists:

            word_tier_exists = False
            morph_tier_exists = False
            gloss_tier_exists = False
            pos_tier_exists = False
            referenced_tier_exists = False

            for word_seg in word_tier:
                if word_seg.index()+1 < len(word_tier):
                    next_word_seg = word_tier.elem[word_seg.index()+1]
                    for ref_seg in referenced_tier:
                        if (word_seg.start == ref_seg.start) | (word_seg.end == ref_seg.end) | ((word_seg.start > ref_seg.start) & (word_seg.end < ref_seg.end)):
                            if (next_word_seg.start == ref_seg.start) | (next_word_seg.end == ref_seg.end) | ((next_word_seg.start > ref_seg.start) & (next_word_seg.end < ref_seg.end)):
                                word_seg.end = next_word_seg.start
                            elif (word_seg.end ==  ref_seg.end) | ((word_seg.start > ref_seg.start) & (word_seg.end < ref_seg.end)):
                                word_seg.end = ref_seg.end

            for morph_seg in morph_tier:
                if morph_seg.index()+1 < len(morph_tier):
                    next_morph_seg = morph_tier.elem[morph_seg.index()+1]
                    for ref_seg in referenced_tier:
                        if (morph_seg.start == ref_seg.start) | (morph_seg.end == ref_seg.end) | ((morph_seg.start > ref_seg.start) & (morph_seg.end < ref_seg.end)):
                            if (next_morph_seg.start == ref_seg.start) | (next_morph_seg.end == ref_seg.end) | ((next_morph_seg.start > ref_seg.start) & (next_morph_seg.end < ref_seg.end)):
                                morph_seg.end = next_morph_seg.start
                            elif (morph_seg.end ==  ref_seg.end) | ((morph_seg.start > ref_seg.start) & (morph_seg.end < ref_seg.end)):
                                morph_seg.end = ref_seg.end

            for gloss_seg in gloss_tier:
                if gloss_seg.index()+1 < len(gloss_tier):
                    next_gloss_seg = gloss_tier.elem[gloss_seg.index()+1]
                    for ref_seg in referenced_tier:
                        if (gloss_seg.start == ref_seg.start) | (gloss_seg.end == ref_seg.end) | ((gloss_seg.start > ref_seg.start) & (gloss_seg.end < ref_seg.end)):
                            if (next_gloss_seg.start == ref_seg.start) | (next_gloss_seg.end == ref_seg.end) | ((next_gloss_seg.start > ref_seg.start) & (next_gloss_seg.end < ref_seg.end)):
                                gloss_seg.end = next_gloss_seg.start
                            elif (gloss_seg.end ==  ref_seg.end) | ((gloss_seg.start > ref_seg.start) & (gloss_seg.end < ref_seg.end)):
                                gloss_seg.end = ref_seg.end

            for pos_seg in pos_tier:
                if pos_seg.index()+1 < len(pos_tier):
                    next_pos_seg = pos_tier.elem[pos_seg.index()+1]
                    for ref_seg in referenced_tier:
                        if (pos_seg.start == ref_seg.start) | (pos_seg.end == ref_seg.end) | ((pos_seg.start > ref_seg.start) & (pos_seg.end < ref_seg.end)):
                            if (next_pos_seg.start == ref_seg.start) | (next_pos_seg.end == ref_seg.end) | ((next_pos_seg.start > ref_seg.start) & (next_pos_seg.end < ref_seg.end)):
                                pos_seg.end = next_pos_seg.start
                            elif (pos_seg.end ==  ref_seg.end) | ((pos_seg.start > ref_seg.start) & (pos_seg.end < ref_seg.end)):
                                pos_seg.end = ref_seg.end


    merging_in_savosavo(trans,("mb@","na"),("gl@","NOM"),"wc@","sa@")
    merging_in_savosavo(trans,("mb@","kona"),("gl@","NOM.F"),"wc@","sa@")
    merging_in_savosavo(trans,("mb@","tona"),("gl@","NOM.DU"),"wc@","sa@")
    merging_in_savosavo(trans,("mb@","ka"),("gl@","LOC.F"),"wc@","sa@")
    merging_in_savosavo(trans,("mb@","la"),("gl@","LOC.M"),"wc@","sa@")


    toElan.toElan(f"../../output_files/{file_name}",trans)


