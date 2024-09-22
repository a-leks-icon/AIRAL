# Created: 2023-06-10
# Latest Version: 2023-06-15
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

from corflow import fromElan,toElan
import glob
import sys
sys.path.append("../")
from corflow_additional_functions import define_content

input_path = "../../input_files/"
output_path = "../../output_files/"

eaf_files = glob.glob(input_path+"/*.eaf")

print("First operation: fixing segment strcuture")
print("###############")
for file in eaf_files:
    file_name = file.replace(input_path,"")
    print(file_name)

    trans = fromElan.fromElan(file,encoding="UTF-8")

    morph_tier_exists = False
    gloss_tier_exists = False
    word_tier_exists = False
    pos_tier_exists = False

    for tier in trans:
        if "mb@" in tier.name:
            morph_tier = trans.getName(tier.name)
            morph_tier_exists = True
        elif "gl@" in tier.name:
            gloss_tier = trans.getName(tier.name)
            gloss_tier_exists = True
        elif "wd@" in tier.name:
            word_tier = trans.getName(tier.name)
            word_tier_exists = True
        elif "pos@" in tier.name:
            pos_tier = trans.getName(tier.name)
            pos_tier_exists = True

        if morph_tier_exists & gloss_tier_exists & word_tier_exists & pos_tier_exists:

            morph_tier_exists = False
            gloss_tier_exists = False
            word_tier_exists = False
            pos_tier_exists = False

            for morph_seg in morph_tier:

                #Fix cases of solo stems.
                if (morph_seg.content.startswith("\\")) & (morph_seg.content.endswith("/")):
                    morph_seg.content = morph_seg.content[1:-1]

                    for gloss_seg in gloss_tier:
                        if (gloss_seg.start == morph_seg.start) & (gloss_seg.end == morph_seg.end):
                            gloss_seg.content = gloss_seg.content + "[stem]"

                #Fix cases of prefix+stem.
                #I checked beforehand, that every instance a) consists of exactly 2 morphs (prefix+stem), b) and has both signs ('\' and '/'). I also checked and could confirm, that NOT every instance is perfectly time-aligned with the respective word-segment, meaning that there are instances, were the e.g. the start time, but not the end time is the same.
                elif (morph_seg.content.endswith("/")) & ("\\" in morph_seg.content):
                    morph_seg_content_split = morph_seg.content.replace("/","").split("\\")

                    #This variable checks (and other similar variables as well), whether a segment was added. The newly added segment influences the current for-loop: A new segment to the left increases the index of the current segment, so that the same segment will therefore be the next segment to loop over. This must not happen. A new segment to the right loops over this segment, which must not happen as well, otherwise a  
                    gloss_seg_added = False

                    for gloss_seg in gloss_tier:
                        if (gloss_seg.parent() == morph_seg) & (gloss_seg_added == False):
                            gloss_seg_content = gloss_seg.content

                            pos_seg_added = False

                            for pos_seg in pos_tier:
                                if (pos_seg.parent() == morph_seg) & (pos_seg_added == False):

                                    #Add new (morph/gloss/pos) segment to the left of the current (morph/gloss/pos) segment.
                                    morph_tier.add(morph_seg.index(),morph_seg)
                                    gloss_tier.add(gloss_seg.index(),gloss_seg)
                                    pos_tier.add(pos_seg.index(),pos_seg)

                                    #Define the name of the new (morph/gloss/pos) segment.
                                    morph_tier.elem[morph_seg.index()-1].name = morph_seg.name + "_added_before"
                                    gloss_tier.elem[gloss_seg.index()-1].name = gloss_seg.name + "_added_before"
                                    pos_tier.elem[pos_seg.index()-1].name = pos_seg.name + "_added_before"

                                    #Set the parent of the new (morph/gloss/pos) segment.
                                    morph_tier.elem[morph_seg.index()-1].setParent(morph_seg.parent())
                                    gloss_tier.elem[gloss_seg.index()-1].setParent(morph_tier.elem[morph_seg.index()-1])
                                    pos_tier.elem[pos_seg.index()-1].setParent(morph_tier.elem[morph_seg.index()-1])

                                    #Define the content of the current morph segment as the second (last) string of the splitting-list.
                                    morph_seg.content = morph_seg_content_split[-1]

                                    #Define the content of the newly added morph segment as the first string of the splitting-list.
                                    morph_tier.elem[morph_seg.index()-1].content = morph_seg_content_split[0]

                                    #Define the content of the current and new gloss segment accordingly.
                                    gloss_seg.content = gloss_seg_content + "[stem]"
                                    gloss_tier.elem[gloss_seg.index()-1].content = gloss_seg_content + "[affix]"

                                    #Define the content of the newly added pos segment.
                                    pos_tier.elem[pos_seg.index()-1].content = "prefix"

                                    gloss_seg_added = True
                                    pos_seg_added = True

                                elif pos_seg_added:
                                    pos_seg_added = False
                                    continue

                        elif gloss_seg_added:
                            gloss_seg_added = False
                            continue

                #Fix cases of stem+suffix.
                elif (morph_seg.content.startswith("\\")) & ("/" in morph_seg.content):
                    morph_seg_content_split = morph_seg.content.replace("\\","").split("/")

                    gloss_seg_added = False

                    for gloss_seg in gloss_tier:
                        if (gloss_seg.parent() == morph_seg) & (gloss_seg_added == False):
                            gloss_seg_content = gloss_seg.content

                            pos_seg_added = False

                            for pos_seg in pos_tier:
                                if (pos_seg.parent() == morph_seg) & (pos_seg_added == False):

                                    #Add new (morph/gloss/pos) segment to the right of the current (morph/gloss/pos) segment.
                                    morph_tier.add(morph_seg.index()+1,morph_seg)
                                    gloss_tier.add(gloss_seg.index()+1,gloss_seg)
                                    pos_tier.add(pos_seg.index()+1,pos_seg)

                                    #Define the name of the new (morph/gloss/pos) segment.
                                    morph_tier.elem[morph_seg.index()+1].name = morph_seg.name + "_added_after"
                                    gloss_tier.elem[gloss_seg.index()+1].name = gloss_seg.name + "_added_after"
                                    pos_tier.elem[pos_seg.index()+1].name = pos_seg.name + "_added_after"

                                    #Set the parent of the new (morph/gloss/pos) segment.
                                    morph_tier.elem[morph_seg.index()+1].setParent(morph_seg.parent())
                                    gloss_tier.elem[gloss_seg.index()+1].setParent(morph_tier.elem[morph_seg.index()+1])
                                    pos_tier.elem[pos_seg.index()+1].setParent(morph_tier.elem[morph_seg.index()+1])

                                    #Define the content of the current morph segment as the first string of the splitting-list.
                                    morph_seg.content = morph_seg_content_split[0]

                                    #Define the content of the newly added morph segment as the second (last) string of the splitting-list.
                                    morph_tier.elem[morph_seg.index()+1].content = morph_seg_content_split[-1]

                                    #Define the content of the current and new gloss segment accordingly.
                                    gloss_seg.content = gloss_seg_content + "[stem]"
                                    gloss_tier.elem[gloss_seg.index()+1].content = gloss_seg_content + "[affix]"

                                    #Define the content of the newly added pos segment.
                                    pos_tier.elem[pos_seg.index()+1].content = "suffix"

                                    gloss_seg_added = True
                                    pos_seg_added = True

                                elif pos_seg_added:
                                    pos_seg_added = False
                                    continue

                        elif gloss_seg_added:
                            gloss_seg_added = False
                            continue

                #Fix cases of circumfix_left-stem-circumfix:right.
                elif ("\\" in morph_seg.content) & ("/" in morph_seg.content):
                    morph_seg_content_split = morph_seg.content.replace("\\","/").split("/")

                    multiple_gloss_segs_added = 0

                    for gloss_seg in gloss_tier:
                        if (gloss_seg.parent() == morph_seg) & (multiple_gloss_segs_added == 0):
                            gloss_seg_content = gloss_seg.content

                            multiple_pos_segs_added = 0

                            for pos_seg in pos_tier:
                                if (pos_seg.parent() == morph_seg) & (multiple_pos_segs_added == 0):

                                    #Add new (morph/gloss/pos) segments to the left and right of the current (morph/gloss/pos) segment.

                                    #Left.
                                    morph_tier.add(morph_seg.index(),morph_seg)
                                    gloss_tier.add(gloss_seg.index(),gloss_seg)
                                    pos_tier.add(pos_seg.index(),pos_seg)

                                    #Right.
                                    morph_tier.add(morph_seg.index()+1,morph_seg)
                                    gloss_tier.add(gloss_seg.index()+1,gloss_seg)
                                    pos_tier.add(pos_seg.index()+1,pos_seg)

                                    #Define the name of the new (morph/gloss/pos) segments.

                                    #Left.
                                    morph_tier.elem[morph_seg.index()-1].name = morph_seg.name + "_added_before"
                                    gloss_tier.elem[gloss_seg.index()-1].name = gloss_seg.name + "_added_before"
                                    pos_tier.elem[pos_seg.index()-1].name = pos_seg.name + "_added_before"

                                    #Right.
                                    morph_tier.elem[morph_seg.index()+1].name = morph_seg.name + "_added_after"
                                    gloss_tier.elem[gloss_seg.index()+1].name = gloss_seg.name + "_added_after"
                                    pos_tier.elem[pos_seg.index()+1].name = pos_seg.name + "_added_after"

                                    #Set the parent of the new (morph/gloss/pos) segments.

                                    #Left.
                                    morph_tier.elem[morph_seg.index()-1].setParent(morph_seg.parent())
                                    gloss_tier.elem[gloss_seg.index()-1].setParent(morph_tier.elem[morph_seg.index()-1])
                                    pos_tier.elem[pos_seg.index()-1].setParent(morph_tier.elem[morph_seg.index()-1])

                                    #Right.
                                    morph_tier.elem[morph_seg.index()+1].setParent(morph_seg.parent())
                                    gloss_tier.elem[gloss_seg.index()+1].setParent(morph_tier.elem[morph_seg.index()+1])
                                    pos_tier.elem[pos_seg.index()+1].setParent(morph_tier.elem[morph_seg.index()+1])

                                    #Define the content of the current morph segment as the second string of the splitting-list.
                                    morph_seg.content = morph_seg_content_split[1]

                                    #Define the content of the newly added morph segments as the a) first and b) third (last) string of the splitting-list.
                                    morph_tier.elem[morph_seg.index()-1].content = morph_seg_content_split[0] #Left
                                    morph_tier.elem[morph_seg.index()+1].content = morph_seg_content_split[-1] #Right.

                                    #Define the content of the current and new gloss segments accordingly.
                                    gloss_seg.content = gloss_seg_content + "[stem]"
                                    gloss_tier.elem[gloss_seg.index()-1].content = gloss_seg_content + "[affix]" #Left.
                                    gloss_tier.elem[gloss_seg.index()+1].content = gloss_seg_content + "[affix]" #Right.

                                    #Define the content of the newly added pos segments.
                                    pos_tier.elem[pos_seg.index()-1].content = "circumfix-"
                                    pos_tier.elem[pos_seg.index()+1].content = "-circumfix"

                                    multiple_gloss_segs_added = 2
                                    multiple_pos_segs_added = 2

                                elif multiple_pos_segs_added > 0:
                                    multiple_pos_segs_added -= 1
                                    continue

                        elif multiple_gloss_segs_added > 0:
                            multiple_gloss_segs_added -= 1
                            continue

            #Fixing the start and end time for those morph-, gloss-, and pos segments, which were newly added, as well as for those, that belong together with the newly added segments to the same word segment.
            for word_seg in word_tier:

                morph_seg_children = []

                for morph_seg in morph_tier:
                    if morph_seg.parent() == word_seg:
                        morph_seg_children.append((morph_seg.index(),morph_seg.name))

                if any((morph_seg_name.endswith("_added_before")) | (morph_seg_name.endswith("_added_after")) for morph_seg_index,morph_seg_name in morph_seg_children):

                    word_seg_time_add = (word_seg.end - word_seg.start)/len(morph_seg_children)
                    word_seg_start_ref = word_seg.start
                    m_seg_name_and_start_and_end_time = []

                    for m_seg_index,m_seg_name in morph_seg_children:

                        morph_tier.elem[m_seg_index].start = word_seg_start_ref
                        morph_tier.elem[m_seg_index].end = word_seg_start_ref + word_seg_time_add
                        word_seg_start_ref = morph_tier.elem[m_seg_index].end
                        m_seg_name_and_start_and_end_time.append((m_seg_name,morph_tier.elem[m_seg_index].start,morph_tier.elem[m_seg_index].end))

                    for gl_seg in gloss_tier:
                        for m_seg_name,m_seg_start,m_seg_end in m_seg_name_and_start_and_end_time:
                            if gl_seg.parent().name == m_seg_name:
                                gl_seg.start = m_seg_start
                                gl_seg.end = m_seg_end
                    
                    for ps_seg in pos_tier:
                        for m_seg_name,m_seg_start,m_seg_end in m_seg_name_and_start_and_end_time:
                            if ps_seg.parent().name == m_seg_name:
                                ps_seg.start = m_seg_start
                                ps_seg.end = m_seg_end

    toElan.toElan(output_path+file_name,trans)


eaf_files2 = glob.glob(output_path+"/*.eaf")

print("Second operation: define_content")
print("###############")
for file2 in eaf_files2:
    file_name2 = file2.replace(output_path,"")
    print(file_name2)

    trans = fromElan.fromElan(file2,encoding="UTF-8")

    #Fix affixes (prefixes and suffixes).
    define_content(trans,"mb@",("-","ADD_TO_END"),cond1=("mb@","endswith","-",False),cond2=("pos@","prefix"))
    define_content(trans,"gl@",("-","ADD_TO_END"),cond1=("gl@","endswith","-",False),cond2=("pos@","prefix"))
    define_content(trans,"pos@","prefix-",cond=("pos@","prefix"))
    define_content(trans,"mb@",("-","ADD_TO_START"),cond1=("mb@","startswith","-",False),cond2=("pos@","suffix"))
    define_content(trans,"gl@",("-","ADD_TO_START"),cond1=("gl@","startswith","-",False),cond2=("pos@","suffix"))
    define_content(trans,"pos@","-suffix",cond=("pos@","suffix"))
    
    #Fix circumfixes (left and right part).
    define_content(trans,"mb@",("-","ADD_TO_END"),cond1=("mb@","endswith","-",False),cond2=("pos@","circumfix-"))
    define_content(trans,"gl@",("-","ADD_TO_END"),cond1=("gl@","endswith","-",False),cond2=("pos@","circumfix-"))

    define_content(trans,"mb@",("-","ADD_TO_START"),cond1=("mb@","startswith","-",False),cond2=("pos@","-circumfix"))
    define_content(trans,"gl@",("-","ADD_TO_START"),cond1=("gl@","startswith","-",False),cond2=("pos@","-circumfix"))

    #Fix clitics (pro- and enclitics): I assume that the longest words containing clitics have a complexity of six morphs. I checked beforehand that the longest chain of adjacent clitics is three across all files (eight cases in total). Therefore, I start with matching cases of three adjacent (pro/en-)clitics and end with one.

    #Three proclitics.
    define_content(trans,"pos@",["proclitic","proclitic","proclitic",">.<",">.<",">.<"],cond1=("wd@",">.<"),cond2=("pos@",["clitic","clitic","clitic",">.<",">.<",">.<"]))
    define_content(trans,"pos@",["proclitic","proclitic","proclitic",">.<",">.<"],cond1=("wd@",">.<"),cond2=("pos@",["clitic","clitic","clitic",">.<",">.<"]))
    define_content(trans,"pos@",["proclitic","proclitic","proclitic",">.<"],cond1=("wd@",">.<"),cond2=("pos@",["clitic","clitic","clitic",">.<"]))

    #Two proclitics.
    define_content(trans,"pos@",["proclitic","proclitic",">.<",">.<",">.<",">.<"],cond1=("wd@",">.<"),cond2=("pos@",["clitic","clitic",">.<",">.<",">.<",">.<"]))
    define_content(trans,"pos@",["proclitic","proclitic",">.<",">.<",">.<"],cond1=("wd@",">.<"),cond2=("pos@",["clitic","clitic",">.<",">.<",">.<"]))
    define_content(trans,"pos@",["proclitic","proclitic",">.<",">.<"],cond1=("wd@",">.<"),cond2=("pos@",["clitic","clitic",">.<",">.<"]))
    define_content(trans,"pos@",["proclitic","proclitic",">.<"],cond1=("wd@",">.<"),cond2=("pos@",["clitic","clitic",">.<"]))

    #One proclitic.
    define_content(trans,"pos@",["proclitic",">.<",">.<",">.<",">.<",">.<"],cond1=("wd@",">.<"),cond2=("pos@",["clitic",">.<",">.<",">.<",">.<",">.<"]))
    define_content(trans,"pos@",["proclitic",">.<",">.<",">.<",">.<"],cond1=("wd@",">.<"),cond2=("pos@",["clitic",">.<",">.<",">.<",">.<"]))
    define_content(trans,"pos@",["proclitic",">.<",">.<",">.<"],cond1=("wd@",">.<"),cond2=("pos@",["clitic",">.<",">.<",">.<"]))
    define_content(trans,"pos@",["proclitic",">.<",">.<"],cond1=("wd@",">.<"),cond2=("pos@",["clitic",">.<",">.<"]))
    define_content(trans,"pos@",["proclitic",">.<"],cond1=("wd@",">.<"),cond2=("pos@",["clitic",">.<"]))

    #Three enclitics.
    define_content(trans,"pos@",[">.<",">.<",">.<","enclitic","enclitic","enclitic"],cond1=("wd@",">.<"),cond2=("pos@",[">.<",">.<",">.<","clitic","clitic","clitic"]))
    define_content(trans,"pos@",[">.<",">.<","enclitic","enclitic","enclitic"],cond1=("wd@",">.<"),cond2=("pos@",[">.<",">.<","clitic","clitic","clitic"]))
    define_content(trans,"pos@",[">.<","enclitic","enclitic","enclitic"],cond1=("wd@",">.<"),cond2=("pos@",[">.<","clitic","clitic","clitic"]))

    #Two enclitics.
    define_content(trans,"pos@",[">.<",">.<",">.<",">.<","enclitic","enclitic"],cond1=("wd@",">.<"),cond2=("pos@",[">.<",">.<",">.<",">.<","clitic","clitic"]))
    define_content(trans,"pos@",[">.<",">.<",">.<","enclitic","enclitic"],cond1=("wd@",">.<"),cond2=("pos@",[">.<",">.<",">.<","clitic","clitic"]))
    define_content(trans,"pos@",[">.<",">.<","enclitic","enclitic"],cond1=("wd@",">.<"),cond2=("pos@",[">.<",">.<","clitic","clitic"]))
    define_content(trans,"pos@",[">.<","enclitic","enclitic"],cond1=("wd@",">.<"),cond2=("pos@",[">.<","clitic","clitic"]))

    #One enclitic.
    define_content(trans,"pos@",[">.<",">.<",">.<",">.<",">.<","enclitic"],cond1=("wd@",">.<"),cond2=("pos@",[">.<",">.<",">.<",">.<",">.<","clitic"]))
    define_content(trans,"pos@",[">.<",">.<",">.<",">.<","enclitic"],cond1=("wd@",">.<"),cond2=("pos@",[">.<",">.<",">.<",">.<","clitic"]))
    define_content(trans,"pos@",[">.<",">.<",">.<","enclitic"],cond1=("wd@",">.<"),cond2=("pos@",[">.<",">.<",">.<","clitic"]))
    define_content(trans,"pos@",[">.<",">.<","enclitic"],cond1=("wd@",">.<"),cond2=("pos@",[">.<",">.<","clitic"]))
    define_content(trans,"pos@",[">.<","enclitic"],cond1=("wd@",">.<"),cond2=("pos@",[">.<","clitic"]))

    #Adding the equal sign to all (pro/-en)clitics and to the respective, time-aligned segments on the morph-, and gloss-tier:
    define_content(trans,"mb@",("=","ADD_TO_END"),cond1=("pos@","proclitic"),cond2=("mb@","endswith","=",False))
    define_content(trans,"gl@",("=","ADD_TO_END"),cond1=("pos@","proclitic"),cond2=("gl@","endswith","=",False))
    define_content(trans,"pos@","proclitic=",cond1=("pos@","proclitic"))

    define_content(trans,"mb@",("=","ADD_TO_START"),cond1=("pos@","enclitic"),cond2=("mb@","startswith","=",False))
    define_content(trans,"gl@",("=","ADD_TO_START"),cond1=("pos@","enclitic"),cond2=("gl@","startswith","=",False))
    define_content(trans,"pos@","=enclitic",cond1=("pos@","enclitic"))

    #Lastly: Fixing some cases of clitics, that are not clitics.
    define_content(trans,"pos@","particle",cond1=("wd@","zə"),cond2=("pos@","clitic"))
    define_content(trans,"pos@","=enclitic",cond1=("mb@","me"),cond2=("pos@","clitic"))
    define_content(trans,"pos@","particle",cond1=("mb@","n"),cond2=("pos@","clitic"))
    define_content(trans,"pos@","particle",cond1=("mb@","m"),cond2=("pos@","clitic"))
    define_content(trans,"pos@","particle",cond1=("mb@","fä"),cond2=("pos@","clitic"))
    define_content(trans,"pos@","demonstrative",cond1=("mb@","ane"),cond2=("pos@","clitic"))
    define_content(trans,"pos@","demonstrative",cond1=("mb@","boba"),cond2=("pos@","clitic"))

    toElan.toElan(output_path+file_name2,trans)