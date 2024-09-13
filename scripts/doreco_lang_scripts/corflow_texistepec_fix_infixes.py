# Created: May 2023
# Latest Version: 2023-06-11
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

from corflow import fromElan, toElan
import glob

input_path = "../../input_files/"
output_path = "../../output_files/"
eaf_files = glob.glob(input_path+"/*.eaf")

for file in eaf_files:
    file_name = file.replace(input_path,"")
    print(file_name)
    trans = fromElan.fromElan(file,encoding="utf-8")

    word_tier_exists = False
    morph_tier_exists = False
    gloss_tier_exists = False
    pos_tier_exists = False
    morph_type_tier_exists = False

    for tier in trans:
        if "tx@" in tier.name:
            word_tier = trans.getName(tier.name)
            word_tier_exists = True
        elif "mr@" in tier.name:
            morph_tier = trans.getName(tier.name)
            morph_tier_exists = True
        elif "ge@" in tier.name:
            gloss_tier = trans.getName(tier.name)
            gloss_tier_exists = True
        elif "ps@" in tier.name:
            pos_tier = trans.getName(tier.name)
            pos_tier_exists = True
        elif "mt@" in tier.name:
            morph_type_tier = trans.getName(tier.name)
            morph_type_tier_exists = True

        if word_tier_exists & morph_tier_exists & gloss_tier_exists & pos_tier_exists & morph_type_tier_exists:

            word_tier_exists = False
            morph_tier_exists = False
            gloss_tier_exists = False
            pos_tier_exists = False
            morph_tier_exists = False

            digraphs = ["dy", "ch", "sh", "kk", "tz"]

            for morph_seg in morph_tier:
                if morph_seg.content == "y-":
                    morph_seg_condition_start = morph_seg.start
                    morph_seg_condition_end = morph_seg.end
                    for morph_type_seg in morph_type_tier:
                        if (morph_type_seg.content == "INF-") & ((morph_type_seg.start == morph_seg_condition_start) & (morph_type_seg.end == morph_seg_condition_end)):
                            morph_seg_old_start = morph_seg.start
                            morph_seg_old_end = morph_seg.end

                            #Count current morphs for time-aligned word
                            count_m_segs_per_word = 0
                            for word_seg in word_tier:
                                if morph_seg.parent() == word_seg:
                                    word_seg_duration = word_seg.end - word_seg.start
                                    word_seg_start = word_seg.start
                                    word_seg_end = word_seg.end
                                    for m_seg in morph_tier:
                                        if m_seg.parent() == word_seg:
                                            count_m_segs_per_word += 1

                            #Adding new morph_seg
                            morph_tier.add(morph_seg.index(),morph_seg)

                            #Add +1 because of newly added segment
                            count_m_segs_per_word += 1

                            #Changing content of a) new seg, b) copied seg and c) found seg
                            if morph_tier.elem[morph_seg.index()+1].content[0:2] in digraphs:

                                morph_tier.elem[morph_seg.index()-1].content = morph_tier.elem[morph_seg.index()+1].content[0:2]
                                morph_tier.elem[morph_seg.index()+1].content = morph_tier.elem[morph_seg.index()+1].content[2:]
                                morph_seg.content = "-" + morph_seg.content

                            else:
                                morph_tier.elem[morph_seg.index()-1].content = morph_tier.elem[morph_seg.index()+1].content[0]
                                morph_tier.elem[morph_seg.index()+1].content = morph_tier.elem[morph_seg.index()+1].content[1:]
                                morph_seg.content = "-" + morph_seg.content

                            #Parenting and name for new seg
                            morph_tier.elem[morph_seg.index()-1].setParent(morph_seg.parent())
                            morph_tier.elem[morph_seg.index()-1].name = str(morph_seg.name)+"_added_before"

                            #Setting times for the a) first, b) second, c) last and d) all other possible morph segs in between.
                            morph_tier.elem[morph_seg.index()-1].start = word_seg_start
                            morph_tier.elem[morph_seg.index()-1].end = word_seg_start + (word_seg_duration/count_m_segs_per_word)

                            morph_seg.start = morph_tier.elem[morph_seg.index()-1].end
                            morph_seg.end = morph_seg.start + (word_seg_duration/count_m_segs_per_word)

                            morph_tier.elem[morph_seg.index()-2+count_m_segs_per_word].end = word_seg_end

                            if count_m_segs_per_word == 3:
                                morph_tier.elem[morph_seg.index()-2+count_m_segs_per_word].start = morph_seg.end
                            elif count_m_segs_per_word > 3:
                                starting_reference_time = morph_seg.end
                                for m_seg_position in range(1,count_m_segs_per_word-1):
                                    morph_tier.elem[morph_seg.index()+m_seg_position].start = starting_reference_time
                                    morph_tier.elem[morph_seg.index()+m_seg_position].end = starting_reference_time + (word_seg_duration/count_m_segs_per_word)
                                    starting_reference_time = morph_tier.elem[morph_seg.index()+m_seg_position].end
                                morph_tier.elem[morph_seg.index()-2+count_m_segs_per_word].end = word_seg_end

                            #Adding copying (and therefore adding) the segments for the a) gloss, b) pos and c) morph-type tier, as well as changing their attributes (content, time, parent, name)
                            for gloss_seg in gloss_tier:
                                if (gloss_seg.start == morph_seg_old_start) & (gloss_seg.end == morph_seg_old_end):
                                    if not gloss_seg.content.startswith("-"):
                                        gloss_seg.content = "-" + gloss_seg.content
                                    gloss_tier.add(gloss_seg.index(),gloss_tier.elem[gloss_seg.index()+1])
                                    gloss_tier.elem[gloss_seg.index()-1].start = word_seg_start
                                    gloss_tier.elem[gloss_seg.index()-1].end = morph_tier.elem[morph_seg.index()-1].end
                                    gloss_tier.elem[gloss_seg.index()-1].setParent(morph_tier.elem[morph_seg.index()-1])
                                    gloss_tier.elem[gloss_seg.index()-1].name = str(gloss_seg.name)+"_added_before"

                                    for gl_seg_position in range(0,count_m_segs_per_word-1):
                                        gloss_tier.elem[gloss_seg.index()+gl_seg_position].start = morph_tier.elem[morph_seg.index()+gl_seg_position].start
                                        gloss_tier.elem[gloss_seg.index()+gl_seg_position].end = morph_tier.elem[morph_seg.index()+gl_seg_position].end

                            for pos_seg in pos_tier:
                                if (pos_seg.start == morph_seg_old_start) & (pos_seg.end == morph_seg_old_end):
                                    if not pos_seg.content.startswith("-"):
                                        pos_seg.content = "-" + pos_seg.content
                                    pos_tier.add(pos_seg.index(),pos_tier.elem[pos_seg.index()+1])
                                    pos_tier.elem[pos_seg.index()-1].start = word_seg_start
                                    pos_tier.elem[pos_seg.index()-1].end = morph_tier.elem[morph_seg.index()-1].end
                                    pos_tier.elem[pos_seg.index()-1].setParent(morph_tier.elem[morph_seg.index()-1])
                                    pos_tier.elem[pos_seg.index()-1].name = str(pos_seg.name)+"_added_before"

                                    for pos_seg_position in range(0,count_m_segs_per_word-1):
                                        pos_tier.elem[pos_seg.index()+pos_seg_position].start = morph_tier.elem[morph_seg.index()+pos_seg_position].start
                                        pos_tier.elem[pos_seg.index()+pos_seg_position].end = morph_tier.elem[morph_seg.index()+pos_seg_position].end

                            for mt_seg in morph_type_tier:
                                if (mt_seg.start == morph_seg_old_start) & (mt_seg.end == morph_seg_old_end):
                                    if not mt_seg.content.startswith("-"):
                                        mt_seg.content = "-" + mt_seg.content
                                    morph_type_tier.add(mt_seg.index(),morph_type_tier.elem[mt_seg.index()+1])
                                    morph_type_tier.elem[mt_seg.index()-1].start = word_seg_start
                                    morph_type_tier.elem[mt_seg.index()-1].end = morph_tier.elem[morph_seg.index()-1].end
                                    morph_type_tier.elem[mt_seg.index()-1].setParent(morph_tier.elem[morph_seg.index()-1])
                                    morph_type_tier.elem[mt_seg.index()-1].name = str(mt_seg.name)+"_added_before"

                                    for mt_seg_position in range(0,count_m_segs_per_word-1):
                                        morph_type_tier.elem[mt_seg.index()+mt_seg_position].start = morph_tier.elem[morph_seg.index()+mt_seg_position].start
                                        morph_type_tier.elem[mt_seg.index()+mt_seg_position].end = morph_tier.elem[morph_seg.index()+mt_seg_position].end


    toElan.toElan(output_path+file_name,trans)
