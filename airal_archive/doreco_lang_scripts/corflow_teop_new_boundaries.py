# Created: May 2023
# Latest Version: 2023-06-07
# Script written by Michelle Elizabeth Throssell Balagué and Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

from corflow import fromElan,toElan
import glob

path="../../input_files/"
eaf_files = glob.glob(path+"/*.eaf")

for file in eaf_files:
    file_name = file.replace(path,"")
    trans = fromElan.fromElan(file,encoding="utf-8")
    gram_tier_exists = False
    mtok_tier_exists = False
    for tier in trans:
        if "grammatical_words" == tier.name:
            gram_tier = trans.getName(tier.name)
            gram_tier_exists = True
        elif "grammatical_words_mtok" == tier.name:
            mtok_tier = trans.getName(tier.name)
            mtok_tier_exists = True
    if gram_tier_exists & mtok_tier_exists:
        mtok_seg_times = []
        mtok_seg_contents = []
        for mtok_seg in mtok_tier:
            if mtok_seg.content == "":
                mtok_seg_times.append(mtok_seg.end)
                mtok_seg_contents.append(mtok_tier.elem[mtok_seg.index()+1].content)
        for number,end_time in enumerate(mtok_seg_times):
            gram_segs_before = []
            for gram_seg in gram_tier:
                if (gram_seg.start < end_time):
                    gram_segs_before.append(gram_seg.index())
            for mtok_seg in mtok_tier:
                if mtok_seg.end == end_time:
                    gram_tier.add(gram_segs_before[len(gram_segs_before)-1]+1,mtok_seg)

                    gram_tier.elem[gram_segs_before[len(gram_segs_before)-1]+1].setParent(gram_tier.elem[gram_segs_before[len(gram_segs_before)-1]+2].parent())

                    gram_tier.elem[gram_segs_before[len(gram_segs_before)-1]+1].end = gram_tier.elem[gram_segs_before[len(gram_segs_before)-1]+2].start

                    gram_tier.elem[gram_segs_before[len(gram_segs_before)-1]+1].start = end_time

                    gram_tier.elem[gram_segs_before[len(gram_segs_before)-1]].end = gram_tier.elem[gram_segs_before[len(gram_segs_before)-1]+1].start

                    gram_tier.elem[gram_segs_before[len(gram_segs_before)-1]+1].content = mtok_seg_contents[number]
    toElan.toElan("../../output_files/"+str(file_name),trans)



path2="../../output_files/"
eaf_files2 = glob.glob(path2+"/*.eaf")

for file in eaf_files2:
    file_name2 = file.replace(path2,"")
    trans = fromElan.fromElan(file,encoding="utf-8")
    gloss_tier_exists = False
    gl_mtok_tier_exists = False
    gram_tier_exists = False
    for tier in trans:
        if "gloss" == tier.name:
            gloss_tier = trans.getName(tier.name)
            gloss_tier_exists = True
        elif "gloss_mtok" == tier.name:
            gl_mtok_tier = trans.getName(tier.name)
            gl_mtok_tier_exists = True
        elif "grammatical_words" == tier.name or "grammatical words" == tier.name:
            gram_tier = trans.getName(tier.name)
            gram_tier_exists = True
    if gloss_tier_exists & gl_mtok_tier_exists & gram_tier_exists:
        gl_mtok_seg_times = []
        gl_mtok_seg_contents = []
        for gl_mtok_seg in gl_mtok_tier:
            if gl_mtok_seg.content == "":
                gl_mtok_seg_times.append(gl_mtok_seg.end)
                gl_mtok_seg_contents.append(gl_mtok_tier.elem[gl_mtok_seg.index()+1].content)
        
        gram_segs_time_and_index = []
        for gram_seg in gram_tier:
            gram_segs_time_and_index.append((gram_seg.end,gram_seg.index()))
        for number,end_time in enumerate(gl_mtok_seg_times):
            gloss_segs_before = []
            for gloss_seg in gloss_tier:
                if (gloss_seg.start < end_time):
                    gloss_segs_before.append(gloss_seg.index())
            for gl_mtok_seg in gl_mtok_tier:
                if gl_mtok_seg.end == end_time:
                    for (gram_seg_end,gram_seg_index) in gram_segs_time_and_index:
                        if gram_seg_end == gl_mtok_seg.end:
                            corresponding_gram_seg_index = gram_seg_index

                    gloss_tier.add(gloss_segs_before[len(gloss_segs_before)-1]+1,gl_mtok_seg)

                    gloss_tier.elem[gloss_segs_before[len(gloss_segs_before)-1]+1].setParent(gram_tier.elem[corresponding_gram_seg_index])

                    gloss_tier.elem[gloss_segs_before[len(gloss_segs_before)-1]+1].end = gloss_tier.elem[gloss_segs_before[len(gloss_segs_before)-1]+2].start

                    gloss_tier.elem[gloss_segs_before[len(gloss_segs_before)-1]+1].start = end_time

                    gloss_tier.elem[gloss_segs_before[len(gloss_segs_before)-1]].end = gloss_tier.elem[gloss_segs_before[len(gloss_segs_before)-1]+1].start

                    gloss_tier.elem[gloss_segs_before[len(gloss_segs_before)-1]+1].content = gl_mtok_seg_contents[number]
    toElan.toElan("../../output_files/"+str(file_name),trans)

