# Created: 2023-09-20
# Latest Version: 2024-01-11
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by François Delafontaine

from corflow import fromElan,toElan
import glob
import re
import unicodedata as uc
import sys
sys.path.append("../")
from corflow_additional_functions import find_tiers,merge_segments
from collections import Counter



def copy_tier(transcription,tier,new_tier_name,parent_tier,char_num=1):
    '''Copies an existing *tier* and adds it to a *transcription* with its *new_tier_name* and newly assigned *parent_tier*. All segments of the newly added tier get renamed based on their first characters letter and the number *char_num* given. By default, this number euqals 1 meaning that if e.g. the first character in a segments name is 'a', it gets substituted by 'b'. If char_num equals 2 and the first character is again 'a', it gets substituted by the character 'c', and so on. Returns the newly added tier.'''
    transcription.add(-1,tier)
    new_tier = transcription.elem[-1]
    new_tier.name = new_tier_name
    for seg in new_tier:
        seg.name = chr(ord(seg.name[0])+char_num) + seg.name[1:]
    new_tier.setParent(parent_tier)
    for seg in new_tier:
        seg.setParent(parent_tier.getTime(seg.start))
    return new_tier

def get_unus_morph_struc(wd_seg,mb_tier_index,regex_pattern):
    '''Returns True, if the word_segment *wd_seg* has an unusual morphological structure on the morph tier. Returns False otherwise. The morph tier gets referenced as the child tier of the word segment with the index *mb_tier_index*. The unusual morphological structure is identified based on the *regex_pattern*, which all morph segments have to fulfill.'''
    mb_segs = [mb_seg for mb_seg in wd_seg.children() if mb_seg.struct == wd_seg.struct.children()[mb_tier_index]]
    if (len(mb_segs) > 0) & (all(re.search(regex_pattern,mb_seg.content) for mb_seg in mb_segs)):
        return True
    else:
        return False

def fix_affixes_clitics(ref_tier,man_tier,time=True,ignore_cont=False):
    '''Fix every segment on the *man_tier* regarding its encoding as an affix or clitic based on the encoding of the segments on the *ref_tier*. If *time* is True, segments on the *ref_tier* and *man_tier* have to be time-aligned or fall in between their times. If *time* is false, segments on the *ref_tier* have to be the parents of the segments on the *man_tier*. If a segments content on *man_tier* matches the regex pattern *ignore_cont*, its skipped. By default, *ignore_cont* is False (not a string type) and therefore no regex pattern for ignoring segments is applied.'''

    for ref_seg in ref_tier:

        if time:
            man_seg = man_tier.getTime(ref_seg.start)
        else:
            if ref_seg.children():
                for child_seg in ref_seg.children():
                    if child_seg.struct == man_tier:
                        man_seg = child_seg
                        break
            else:
                continue

        if isinstance(ignore_cont,str):
            if re.search(ignore_cont,man_seg.content):
                continue

        if (ref_seg.content.startswith("-")) & (ref_seg.content.endswith("-")):
            if not man_seg.content.startswith("-"):
                if man_seg.content.startswith("="):
                    man_seg.content[0] = "-"
                else:
                    man_seg.content = "-" + man_seg.content
            if not man_seg.content.endswith("-"):
                if man_seg.content.endswith("="):
                    man_seg.content[-1] = "-"
                else:
                    man_seg.content = man_seg.content + "-"
        elif ref_seg.content.startswith("-"):
            if not man_seg.content.startswith("-"):
                if man_seg.content.startswith("="):
                    man_seg.content[0] = "-"
                else:
                    man_seg.content = "-" + man_seg.content
        elif ref_seg.content.endswith("-"):
            if not man_seg.content.endswith("-"):
                if man_seg.content.endswith("="):
                    man_seg.content[-1] = "-"
                else:
                    man_seg.content = man_seg.content + "-"
        elif ref_seg.content.startswith("="):
            if not man_seg.content.startswith("="):
                if man_seg.content.startswith("-"):
                    man_seg.content[0] = "="
                else:
                    man_seg.content = "=" + man_seg.content
        elif ref_seg.content.endswith("="):
            if not man_seg.content.endswith("="):
                if man_seg.content.endswith("-"):
                    man_seg.content[-1] = "="
                else:
                    man_seg.content = man_seg.content + "="

def split_segments_sumi(seg,time,end=True):
    '''Splits a segment *seg* into two seperate segments at *time* in seconds. If *end* is True (the default), the new segment is to the left of *seg*. If *end* is False, the new segment is to the right of *seg*. All child segments of *seg* get the splitted segment as their new parent, if their times fall within the new segments times. Returns a tuple with its first element being the new segment and its second element being a list with all child segments, which had to be added due to the splitting.'''
    seg_times = (seg.start,seg.end)
    if end:
        seg.struct.add(seg.index(),seg)
        new_seg = seg.struct.elem[seg.index()-1]
        new_seg.start = seg.start
        new_seg.end = time
        seg.start = time
    else:
        seg.struct.add(seg.index()+1,seg)
        new_seg = seg.struct.elem[seg.index()+1]
        new_seg.start = time
        new_seg.end = seg.end
        seg.end = time
    new_seg.name = seg.name + "_0"
    if seg.parent() != None:
        new_seg.setParent(seg.parent().struct.getTime(new_seg.start))
    else:
        new_seg.setParent(None)
    if seg.children():
        new_ch_segs = []
        #The special condition, that one child tier is excluded is special to sumi and the operations we wanna do here.
        relevant_child_segs = [ch for ch in seg.children() if not "legacy" in ch.struct.name]
        for ch_seg in relevant_child_segs:
            if (ch_seg.start == seg_times[0]) & (ch_seg.end == seg_times[-1]):
                if end:
                    ch_seg.struct.add(ch_seg.index(),ch_seg)
                    new_ch_seg = ch_seg.struct.elem[ch_seg.index()-1]
                else:
                    ch_seg.struct.add(ch_seg.index()+1,ch_seg)
                    new_ch_seg = ch_seg.struct.elem[ch_seg.index()+1]
                new_ch_seg.start = new_seg.start
                new_ch_seg.end = new_seg.end
                new_ch_seg.name = ch_seg.name + "_0"
                new_ch_seg.setParent(new_seg)
                new_ch_segs.append(new_ch_seg)
                ch_seg.start = seg.start
                ch_seg.end = seg.end
            elif (ch_seg.start == new_seg.start) | (ch_seg.end == new_seg.end) | ((ch_seg.start > new_seg.start) & (ch_seg.end < new_seg.end)):
                ch_seg.setParent(new_seg)
    return (new_seg,new_ch_segs)

def def_all_segs(seg,content,ignore_tiers):
    '''Defines the content of a segment *seg* as *content*, and recursively for all of its children as well, as long as they do not belong to a tier in *ignore_tiers*.'''
    if seg.children():
        for ch in seg.children():
            def_all_segs(ch,content,ignore_tiers)
    if not seg.struct in ignore_tiers:
        seg.content = content

#ACTUAL OPERATIONS BEGIN HERE#
input_path = "../../input_files/"
output_path = "../../output_files/"
eaf_files = glob.glob(input_path+"/*.eaf")

#yyyy = []
#Iterating over every sümi eaf-file.
for file in eaf_files:
    file_name = file.replace(input_path,"")
    print(f"\n**********\nFile: {file_name}\n**********\n")
    trans = fromElan.fromElan(file,encoding="utf-8")

    #1. Operations changing morph and/or gloss segments independently of the badness of the morphological structure they are part of.
    for morph_tier in find_tiers(trans,"morph-txt-nsm-cp"):
        for morph_seg in morph_tier:
            #Removing inappropriate signs (here '*') and using the doreco string '****' for inappropriate segments (here '?').
            morph_seg.content = morph_seg.content.replace("*","").replace("?","****")
            if morph_seg.children():
                #Substitute 'NA* by '****', etc.
                gloss_seg = morph_seg.children()[0]
                gloss_seg.content = gloss_seg.content.replace("*","")
                if re.search("^(=?\?)$",gloss_seg.content):
                    gloss_seg.content = "****"
                #morph segments with those contents get NA ('****') as their gloss.
                let_na = ['mudram', 'gari', 'tukri', 'buji', 'boini', 'chuti', 'din', 'teli', 'tukra', 'sapa', 'acha', 'aram', 'dukan', 'kamsa', 'mari', 'khamsa', 'thanda', 'andaz', 'malik']
                if gloss_seg.content == "NA":
                    if gloss_seg.parent().content in let_na:
                        gloss_seg.content = "****"
                    elif gloss_seg.parent().content == "bhai":
                        gloss_seg.content = "brother"
                    elif gloss_seg.parent().content == "naspati":
                        gloss_seg.content = "pear"
                    else:
                        gloss_seg.content = gloss_seg.parent().content
                if (morph_seg.content == "-mu") & (gloss_seg.content == "NEG"):
                    gloss_seg.content = "even.though"
                    if (morph_seg.content == "-mu") & (gloss_seg.content == "even.though"):
                        morph_seg.content = "=mu"
                elif (morph_seg.content == "=ti") & (gloss_seg.content == "=MED"):
                    morph_seg.content = "ti"
                    gloss_seg.content = "MED"

    #2. Processes based on the badness of the morphological stuctures of words. Most importantly, word segments get merged, if they have no stem/root.
    for word_tier in find_tiers(trans,"Words-txt-nsm"):
        print(f"#####\nword tier: {word_tier.name}")
        new_name = word_tier.name + "_legacy"
        #Copying the current/old word tier and saving it as a separate, legacy tier.
        copy_tier(trans,word_tier,new_name,word_tier)
        wd_segs = [wd_seg for wd_seg in word_tier]
        #I am not relying on the order of the child tiers. i) because it is less safe; ii) because the legacy tier got add as a child tier.
        for tier in word_tier.children():
            if "morph-txt-nsm-cp" in tier.name:
                m_tier = tier
            elif "word-pos-en-cp" in tier.name:
                pos_tier = tier
        if m_tier == None:
            continue
        print(f"morph tier: {m_tier.name}")
        print(f"pos tier: {pos_tier.name}\n#####")
        #2.1. Iterating over every word segment in a separate list and splitting those word segments with either a) enclitics as their starting morph segment or b) with affixes in between stems. I checked with the/a script and can confirm, that there are no cases of word segments having a stem and ending on a prefix/proclitic.
        for wd_seg in wd_segs:
            #Skip, if the word segment has either no morph segment or no pos segment (so at least one gap).
            if (not m_tier in wd_seg.childDict().keys()) | (not pos_tier in wd_seg.childDict().keys()):
                continue
            #Removing "," and "." and "-" from word segments content.
            wd_seg.content = wd_seg.content.replace(",","").replace(".","").replace("-","")
            msegs = wd_seg.childDict()[m_tier]
            if msegs:
                pos_segs = wd_seg.childDict()[pos_tier]
                if (len(msegs) > 1) & ((msegs[0].content.startswith("=")) | (msegs[0].content.startswith("-"))):
                    time = msegs[0].end
                    if any(re.search(r"^[^=-].*[^=-]$",mseg.content) for mseg in msegs[1:]):
                        ind_segs = split_segments_sumi(wd_seg,time)
                        new_wdseg = ind_segs[0]
                        new_wdseg.content = msegs[0].content.replace("=","").replace("-","")
                        wd_seg.content = uc.normalize("NFD",wd_seg.content).removeprefix(uc.normalize("NFD",new_wdseg.content))
                        if pos_segs:
                            #Those pos contents will be fixed later in the script.
                            pos_segs[0].content = "XXXX"
                        for ch_seg in ind_segs[-1]:
                            if ch_seg.struct == pos_tier:
                                ch_seg.content = "post"
                elif len(msegs) > 2:
                    #I only found word segs with having exactly 3 morph segments, if there was an affix/clitic in between two stems. They get split as well depending on the position of the affix.
                    #I also found one case of an infix ('-ku-'), which is wrong. Based on the grammar, its the word 'ku- sho'.
                    if all(not re.search("(^[-=])|([-=]$)",mseg.content) for mseg in msegs):
                        continue
                    #One file had an issue and was broken afterwards, because the morph segment had no gloss segment and this was an issue for the split_segments_sumi function.
                    elif any(not m.children() for m in msegs):
                        continue
                    elif (not re.search("(^[-=])|([-=]$)",msegs[0].content)) & ((not re.search("(^[-=])|([-=]$)",msegs[-1].content))):
                        #Because there are no structures, where more than one affix/alitic is encapsulated by stems, it is safe to split at the first (and only) affix/clitic.
                        if (msegs[1].content.endswith("-")) | (msegs[1].content.endswith("=")):
                            ind_segs = split_segments_sumi(wd_seg,msegs[1].start,False)
                            new_wdseg = ind_segs[0]
                            new_wdseg.content = uc.normalize("NFD",new_wdseg.content).removeprefix(uc.normalize("NFD",msegs[0].content))
                            wd_seg.content = uc.normalize("NFD",wd_seg.content).removesuffix(uc.normalize("NFD",new_wdseg.content))
                            #These lines of code are really just for the two instances of a falsely encoded infix.
                            if msegs[1].content.startswith("-"):
                                msegs[1].content = msegs[1].content.removeprefix("-")
                                msegs[1].children()[0].content = msegs[1].children()[0].content.removeprefix("-")
                            #if pos_segs:
                            #Those pos contents have to be fixed manually outside the script.
                                #pos_segs[0].content += "YYYY"
        
                        elif (msegs[1].content.startswith("-")) | (msegs[1].content.startswith("=")):
                            ind_segs = split_segments_sumi(wd_seg,msegs[1].end,True)
                            new_wdseg = ind_segs[0]
                            new_wdseg.content = uc.normalize("NFD",new_wdseg.content).removesuffix(uc.normalize("NFD",msegs[-1].content))
                            wd_seg.content = uc.normalize("NFD",wd_seg.content).removeprefix(uc.normalize("NFD",new_wdseg.content))
                            #if pos_segs:
                            #Those pos contents have to be fixed manually outside the script.
                                #pos_segs[-1].content += "YYYY"
                    elif len(msegs) >= 4:
                        found = []
                        #The following words get also split. They have one of the two substructures: AFFIX/CLITIC-STEM-AFFIX/CLITIC-STEM or STEM-AFFIX/CLITIC-STEM-AFFIX/CLITIC.
                        for ind,mseg in enumerate(msegs):
                            if (ind+4) <= len(msegs):
                                if re.search("(^[-=])|([-=]$)",msegs[ind].content):
                                    if not re.search("(^[-=])|([-=]$)",msegs[ind+1].content):
                                        if re.search("(^[-=])|([-=]$)",msegs[ind+2].content):
                                            if not re.search("(^[-=])|([-=]$)",msegs[ind+3].content):
                                                if not wd_seg in found:
                                                    found.append(wd_seg)
                                                    if (msegs[ind+2].content.startswith("-")) | (msegs[ind+2].content.startswith("=")):
                                                        split_index = ind+2
                                                    else:
                                                        split_index = ind+1
                                                    ind_segs = split_segments_sumi(wd_seg,msegs[split_index].end,True)
                                                    new_wdseg = ind_segs[0]
                                                    concat_content = ""
                                                    for m in msegs[:split_index+1]:
                                                        add_content = m.content.replace("-","").replace("=","")
                                                        concat_content += add_content
                                                    new_wdseg.content = uc.normalize("NFD",concat_content)
                                                    wd_seg.content = uc.normalize("NFD",wd_seg.content).removeprefix(uc.normalize("NFD",new_wdseg.content))
                                                    #if pos_segs:
                                                    #Those pos contents have to be fixed manually outside the script.
                                                        #pos_segs[-1].content += "YYYY"
                                elif re.search("(^[-=])|([-=]$)",msegs[ind+1].content):
                                    if not re.search("(^[-=])|([-=]$)$",msegs[ind+2].content):
                                        if re.search("(^[-=])|([-=]$)",msegs[ind+3].content):
                                            if not wd_seg in found:
                                                found.append(wd_seg)
                                                if (msegs[ind+1].content.startswith("-")) | (msegs[ind+1].content.startswith("=")):
                                                    split_index = ind+1
                                                else:
                                                    split_index = ind
                                                ind_segs = split_segments_sumi(wd_seg,msegs[split_index].end,True)
                                                new_wdseg = ind_segs[0]
                                                concat_content = ""
                                                for m in msegs[:split_index+1]:
                                                    add_content = m.content.replace("-","").replace("=","")
                                                    concat_content += add_content
                                                new_wdseg.content = uc.normalize("NFD",concat_content)
                                                wd_seg.content = uc.normalize("NFD",wd_seg.content).removeprefix(uc.normalize("NFD",new_wdseg.content))
                                                #if pos_segs:
                                                #Those pos contents have to be fixed manually outside the script.
                                                    #pos_segs[-1].content += "YYYY"
                        #The following words have to be split as well: They have more than one stem where in between the two stems are more than one affix/clitic, at the same time, those stems do not encapsulate the affixes/clitics.
                        #In the end, there were only two instances in total across all files. Those two instances were in the same file. 
                        first_stem = False
                        for ind,mseg in enumerate(msegs):
                            if not re.search("(^[-=])|([-=]$)",mseg.content):
                                if first_stem == False:
                                    first_stem = True
                                    first_stem_ind = ind
                                    continue
                                elif first_stem:
                                    if (ind-first_stem_ind) >= 2:
                                        if not wd_seg in found:
                                            found.append(wd_seg)
                                            ind_segs = split_segments_sumi(wd_seg,mseg.start,True)
                                            new_wdseg = ind_segs[0]
                                            concat_content = ""
                                            for m in msegs[:ind]:
                                                add_content = m.content.replace("-","").replace("=","")
                                                concat_content += add_content
                                            new_wdseg.content = uc.normalize("NFD",concat_content)
                                            wd_seg.content = uc.normalize("NFD",wd_seg.content).removeprefix(uc.normalize("NFD",new_wdseg.content))
                                            #if pos_segs:
                                            #Those pos contents have to be fixed manually outside the script.
                                                #pos_segs[-1].content += "YYYY"
                                        break
                                    else:
                                        first_stem_ind += 1

        #2.2. Iterating over every word segment in a separate list and doing different operations based on the details of the unusual structures.
        wd_segs = [wd_seg for wd_seg in word_tier]
        for wd_seg in wd_segs:
            #Skip, if the word segment has either no morph segment or no pos segment (so at least one gap).
            if (not m_tier in wd_seg.childDict().keys()) | (not pos_tier in wd_seg.childDict().keys()):
                continue
            mb_segs = [mb_seg for mb_seg in wd_seg.children() if mb_seg.struct == m_tier]
            #If all morphs are either enclitics and/or suffixes, the word segment they belong to gets merged with the previous segment.
            if (len(mb_segs) > 0) & (all(re.search("^(=|-)",mb_seg.content) for mb_seg in mb_segs)):
                if wd_seg.struct.elem[wd_seg.index()-1].childDict()[pos_tier]:
                    prev_wd_seg_pos_cont = wd_seg.struct.elem[wd_seg.index()-1].childDict()[pos_tier][0].content
                else:
                    #In case the previous word segment has no pos segment, which means, it has gaps. In these cases no merging operation should occur.
                    break
                #word_seg = word_tier.getTime(wd_seg.start)
                #Merging the respective word and also pos segments. The try-except-block is necessary for otherwise in case a segment is not merged, the merge_segments function does not return a segment, therefore causing an error if using segment attributes/methods as I do.
                try:
                    for tier,seg_l in merge_segments(wd_seg).childDict().items():
                        if "word-pos" in tier.name:
                            merge_segments(seg_l[0]).content = prev_wd_seg_pos_cont
                except:
                    pass
            #If all morphs are either proclitics and/or prefixes, the word segment they belong to gets merged with the next segment.
            elif (len(mb_segs) > 0) & (all(re.search("(=|-)$",mb_seg.content) for mb_seg in mb_segs)) & ((wd_seg.index()+1) < len(wd_segs)):
                if wd_seg.struct.elem[wd_seg.index()+1].childDict()[pos_tier]:
                    next_wd_seg_pos_cont = wd_seg.struct.elem[wd_seg.index()+1].childDict()[pos_tier][0].content
                else:
                    #In case the next word segment has no pos segment, which means, it has gaps. In these cases, no merging operation shoud occur. 
                    break
                try:
                    for tier,seg_l in merge_segments(wd_seg,1).childDict().items():
                        if "word-pos" in tier.name:
                            merge_segments(seg_l[0],1).content = next_wd_seg_pos_cont
                except:
                    pass
            #If the morphs 'i=' or 'o=' occur together with enclitics only, they together with their glosses loose their equal sign.
            elif (len(mb_segs) > 0) & (all(re.search("^=|=$",mb_seg.content) for mb_seg in mb_segs)):
                if ("i=" == mb_segs[0].content) | ("o=" == mb_segs[0].content):
                    mb_segs[0].content = mb_segs[0].content.replace("=","")
                    mb_segs[0].children()[0].content = mb_segs[0].children()[0].content.replace("=","")

    #3. Fixing morphs, which are encoded as affixes even though they appear before proclitics as prefixes or after enclitics as suffixes.
    for word_tier in find_tiers(trans,"Words-txt-nsm"):
        #Because of adding the new tier with an identical part in its name, it gets found by the function. It has to be sorted out here.
        if not "legacy" in word_tier.name:
            #I am not relying on the order of the child tiers. i) because it is less safe; ii) because the legacy tier got add as a child tier.
            m_tier = None
            pos_tier = None
            for tier in word_tier.children():
                if "morph-txt-nsm-cp" in tier.name:
                    m_tier = tier
                elif "word-pos-en-cp" in tier.name:
                    pos_tier = tier
            if m_tier == None:
                continue
            for word_seg in word_tier:
                #Skip, if the word segment has either no morph segment or no pos segment (so at least one gap).
                if (not m_tier in word_seg.childDict().keys()) | (not pos_tier in word_seg.childDict().keys()):
                    continue
                mb_index_seg = [(mb_seg.index(),mb_seg) for mb_seg in word_seg.children() if mb_seg.struct == m_tier]
                mb_index_seg = sorted(mb_index_seg)
                debug = [(mb_seg.index(),mb_seg.content) for mb_seg in word_seg.children() if mb_seg.struct == m_tier]
                for index,(mb_ind,mb_seg) in enumerate(mb_index_seg):
                    if (mb_seg.content.startswith("-")) & (index > 0):
                        if mb_index_seg[index-1][1].content.startswith("="):
                            mb_seg.content = mb_seg.content.replace("-","=")
                            mb_seg.children()[0].content = mb_seg.children()[0].content.replace("-","=")
                    elif (mb_seg.content.endswith("-")) & (index+1 < len(mb_index_seg)):
                        if mb_index_seg[index+1][1].content.endswith("="):
                            mb_seg.content = mb_seg.content.replace("-","=")
                            mb_seg.children()[0].content = mb_seg.children()[0].content.replace("-","=")

    #4. Fixing for glosses of affixes and clitics their respective sign (missing or wrongly fully assigned dashes and/or equal signs).
    for morph_tier in find_tiers(trans,"morph-txt-nsm-cp"):
        gloss_tier = morph_tier.children()[0]
        fix_affixes_clitics(morph_tier,gloss_tier,False,"\*{4}")

    #5. Defining the content of those pos segments, whose word segments had to be split.
    pos_v = ["pi","va","toi","shia","pipuno","vake","uva","khupu"]
    for pos_tier in find_tiers(trans,"word-pos-en-cp"):
        for pseg in pos_tier:
            if pseg.content == "XXXX":
                w_cont = pseg.parent().content
                if w_cont in pos_v:
                    pseg.content = "v"
                elif w_cont == "kemtsa":
                    pseg.content = "adv"
                elif (w_cont == "vi") | (w_cont == "pani"):
                    pseg.content = "v.aux"
                elif w_cont == "ti":
                    pseg.content = "dem"
                elif (w_cont == "thiuno") | (w_cont == "ghi") | (w_cont == "thiu"):
                    pseg.content = "post"
                elif (w_cont == "lai") | (w_cont == "na"):
                    pseg.content = "prt"
                elif w_cont == "tsa":
                    pseg.content = "n"
            '''
            elif "YYYY" in pseg.content:
                wseg = pseg.parent()
                wseg_chs = []
                for ch in wseg.children():
                    if (ch.struct != pos_tier) & ("legacy" not in ch.struct.name):
                        if ch.children():
                            wseg_chs.append((ch.content,ch.children()[0].content))
                        else:
                            wseg_chs.append((ch.content,"NO_GLOSS"))
                yyyy.append((wseg.content,pseg.content,[wseg_chs]))
            '''

    #6. Using the doreco string '****' for inappropriate (word) segments and all of their child segments.
    for wd_tier in find_tiers(trans,"Words-txt-nsm"):
        for wd_seg in wd_tier:
            if re.search("\(?unclear\)?",wd_seg.content):
                def_all_segs(wd_seg,"****",find_tiers(trans,"legacy"))
        #Using the split_segments_sumi-function made the transcribe tiers segments not clickable in the final ELAN files. The function turned the word tiers into the ELAN type 'time'. Turning it into the type 'subd' for subdivision (child segments having their independent times; here the word tiers are the child tiers and the transcribe tiers the parent tiers) made the problem vanish.
        wd_tier.setMeta("type","subd","tech")

    toElan.toElan(output_path+file_name,trans)
#print(yyyy)