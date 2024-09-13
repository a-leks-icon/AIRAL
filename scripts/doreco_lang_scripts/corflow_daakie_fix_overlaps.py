# Created: 2023-10-28
# Latest Version: 2024-01-29
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

'''In a first step, this script searches for overlapping segments (segments with the same start and/or end time on the same tier), concatenates the content of all those overlapping segments, defines the first segments content as such and deletes the rest of the segments entirely from the file. Also; it fixes parenting and time issues during the process.

In a second step, this script '''

from corflow import fromElan,toElan
import glob
import sys
sys.path.append("../")
from corflow_additional_functions import find_tiers
from collections import Counter

def get_overlapping_segments(transcription):
    '''Returns for a given *transcription* a dictionary with tiers as keys and lists as values. Those lists contain tuples of segments of the same tier, which share their start and/or end time.'''
    overlapping_segments = {}
    for tier in transcription:
        overlapping_segments[tier] = []
        overlapping_segments[tier].append(set())
        for seg1 in tier:
            seg_set = set()
            for seg2 in tier:
                if (seg1.start == seg2.start) | (seg1.end == seg2.end) | ((seg1.start > seg2.start) & (seg1.end < seg2.end)):
                    if seg1 != seg2:
                        seg_set.add(seg1)
                        seg_set.add(seg2)
            if not seg_set in overlapping_segments[tier]:
                overlapping_segments[tier].append(seg_set)
                #This more strict condition is for cases, where one segment overlaps with at least two other segments, which themselves do not overlap with each other.
                for ind,added_seg_set in enumerate(overlapping_segments[tier][:-1]):
                    if any(seg in added_seg_set for seg in seg_set):
                        if len(seg_set) > len(added_seg_set):
                            overlapping_segments[tier].pop(ind)
                        else:
                            overlapping_segments[tier].pop(-1)
                        break
        for index,segs in enumerate(overlapping_segments[tier]):
            indexed_segs = [(seg.index(),seg) for seg in segs]
            ordered_segs = sorted(indexed_segs)
            segs_l = [seg for index,seg in ordered_segs]
            overlapping_segments[tier][index] = tuple(segs_l)
    return overlapping_segments


def remove_all_segments(tier):
    '''Removes all segments from a given *tier*.'''
    segs = [seg for seg in tier]
    for seg in segs:
        tier.remove(seg)
    print(f"Removed all segments from the tier {tier.name}.")


#ACTUAL OPERATIONS BEGIN HERE#
#STEP 1: Getting the overlapping segments, saving their contents, deleting the rest and fixing parent-child relations, and some start and end times of some segments.
input_path = "../../input_files/"
output_path = "../../output_files/"
eaf_files = glob.glob(input_path+"/*.eaf")

print("\n######\nSTEP 1:\n######\n")
for file in eaf_files:
    file_name = file.replace(input_path,"")
    print(f"\n/////////\nfile name: {file_name}\n//////////\n")
    trans = fromElan.fromElan(file,encoding="utf-8")
    #Iterating over every tier and its list of tuples containig overlapping segments.
    for tier,overlap_l in get_overlapping_segments(trans).items():
        print(f"\n##########\ntier: {tier.name}\n##########\n")
        if overlap_l:
            for seg_tuple in overlap_l:
                if seg_tuple:
                    #Getting the concatenated content from all overlapping segments.
                    seg_set = set()
                    seg_content = ""
                    for seg in seg_tuple:
                        seg_set.add(seg.content)
                        #This line is for debugging purposes only.
                        #seg_content += (seg.content + "[" + str(seg.index()) + "]")
                        seg_content += seg.content + "//"
                    #If overlapping segments have a different content, then the concatenated content gets used for the first segments content.
                    if len(seg_set) > 1:
                        seg_content = seg_content.removesuffix("//")
                        seg_tuple[0].content = seg_content
                    #Removing all overlapping segments except for the first.
                    for seg in seg_tuple[1:]:
                        tier.remove(seg)

        #Setting for every segment, which has no parent, even though it is supposed to have one, its parent segment based on its start and end time.
        for tier in trans:
            if tier.parent() != None:
                for seg in tier:
                    if seg.parent() == None:
                        for seg2 in tier.parent():
                            if (seg.start == seg2.start) | (seg.end == seg2.end) | ((seg.start > seg2.start) & (seg.end < seg2.end)):
                                seg.setParent(seg2)
                                break
                    #Aligning the start and end time of the gloss and pos segments with their parent segments (morph segments).
                    if ("ge@unknown" in tier.name) | ("ps@unknown" in tier.name):
                        seg.start = seg.parent().start
                        seg.end = seg.parent().end

    #Saving the new eaf file.
    toElan.toElan(output_path+file_name,trans)

#'''
#STEP 2: Fix a couple of issues.
new_input_path = output_path
clean_files_dir = "clean_daakie_files"
clean_eaf_files = glob.glob(input_path+clean_files_dir+"/*.eaf")
eaf_files = glob.glob(new_input_path+"/*.eaf")

daakie_data = {}
#STEP 2.1: Creating a dictionary with informations from all clean files about i) which morph segment contents occur across all files and ii) which gloss and pos segment contents those morphs get assigned. Finally, those gloss and pos content assigments are counted and used in a later step for fixing the gloss and pos contents containing "//". The clean files are in a separate subfolder inside the input folder, where the broken daakie (bong.eaf) file is.
#The format of the dictionary: {morph_segment_content: ( [{gloss_segment_content: count}, ...],[{pos_segment_content: count}, ...] ) }
print("\n######\nSTEP 2.1:\n######\n")
for cfile in clean_eaf_files:
    cfile_name = cfile.replace(input_path+clean_files_dir,"")
    print(f"\n/////////\nfile name: {cfile_name}\n//////////\n")
    ctrans = fromElan.fromElan(cfile,encoding="utf-8")
    for mtier in ctrans:
        if "mb@unknown" == mtier.name:
            gltier = None
            postier = False
            for ch_tier in mtier.children():
                if "ge@unknown" == ch_tier.name:
                    gltier = ch_tier
                elif "ps@unknown" == ch_tier.name:
                    postier = ch_tier
            for mseg in mtier:
                if not mseg.content in daakie_data:
                    daakie_data[mseg.content] = ([],[])
                if mseg.children():
                    for ch_seg in mseg.children():
                        if ch_seg.struct == gltier:
                            daakie_data[mseg.content][0].append(ch_seg.content)
                        elif ch_seg.struct == postier:
                            daakie_data[mseg.content][-1].append(ch_seg.content)

for key,val in daakie_data.items():
    daakie_data[key] = (Counter(val[0]),Counter(val[1]))

#Getting an idea of the data. Creating a txt file.
with open(output_path+"daakie_grammar.txt", "w") as txtfile:
    for key,val in daakie_data.items():
        txtfile.write(key+":\n")
        txtfile.write("Gloss segs: "+str(Counter(val[0]))+"\n")
        txtfile.write("POS segs: "+str(Counter(val[1]))+"\n")
        txtfile.write("####################\n")
    txtfile.write("\n------------------------------\nAll Morphs:\n"+str(daakie_data.keys()))

#STEP 2.2: Fix all remaining issues.
print("\n######\nSTEP 2.2:\n######\n")
for file in eaf_files:
    file_name = file.replace(new_input_path,"")
    print(f"\n/////////\nfile name: {file_name}\n//////////\n")
    trans = fromElan.fromElan(file,encoding="utf-8")

    #Fix times of morph segments with overlapping times (meaning that the end time of one morph segments is greater than the start time of the next morph segment). Found some morph segments to be this way.
    for tier in find_tiers(trans,"ref@unknown"):
        for ch_tier in tier.children():
            if "mb@unknown" in ch_tier.name:
                mtier = ch_tier
                break
        for refseg in tier:
            if not mtier in refseg.childDict():
                continue
            msegs = sorted([(m.index(),m) for m in refseg.childDict()[mtier]])
            msegs = [m for ind,m in msegs]
            for ind1,mseg1 in enumerate(msegs[:-1]):
                if mseg1.end > msegs[ind1+1].start:
                    num_msegs = len(msegs)
                    start = refseg.start
                    total_time = refseg.end-refseg.start
                    for mseg2 in msegs[:-1]:
                        mseg2.start = start
                        mseg2.end = start+(total_time/num_msegs)
                        if mseg2.children():
                            for ch_seg in mseg2.children():
                                ch_seg.start = mseg2.start
                                ch_seg.end = mseg2.end
                        start = mseg2.end
                    msegs[-1].start = start
                    msegs[-1].end = refseg.end
                    if msegs[-1].children():
                        for ch_seg in msegs[-1].children():
                            ch_seg.start = msegs[-1].start
                            ch_seg.end = msegs[-1].end
                    break

    #Fixing those morph segments (actually just one group) with "//" in their content. This much code is needed because of adding multiple (3) segments on (3) different tiers.
    for mtier in trans:
        if "mb@unknown" == mtier.name:
            for mseg in mtier:
                if "//" in mseg.content:
                    if mseg.end == mseg.parent().end:
                        mtier.add(mseg.index()+1,mseg)
                        partition_content = mseg.content.partition("//")
                        mseg.content = partition_content[0]
                        new_mseg = mtier.elem[mseg.index()+1]
                        new_mseg.content = partition_content[-1]
                        new_mseg.setParent(mseg.parent())
                        new_mseg.name = mseg.name+"_2"
                        for ch_tier in mtier.children():
                            prev_ch_seg = ch_tier.getTime(mseg.start)
                            ch_tier.add(prev_ch_seg.index()+1,prev_ch_seg)
                            new_ch_seg = ch_tier.elem[prev_ch_seg.index()+1]
                            partition_ch_content = prev_ch_seg.content.partition("//")
                            prev_ch_seg.content = partition_ch_content[0]
                            new_ch_seg.content = partition_ch_content[-1]
                            new_ch_seg.setParent(new_mseg)
                            new_ch_seg.name = prev_ch_seg.name+"_2"
                        current_msegs = mseg.parent().childDict()[mtier]
                        start = mseg.parent().start
                        total_time = mseg.parent().end - mseg.parent().start
                        num_current_msegs = len(current_msegs)
                        for seg in current_msegs[:-1]:
                            seg.start = start
                            seg.end = start+(total_time/num_current_msegs)
                            if seg.children():
                                for ch_seg in seg.children():
                                    ch_seg.start = seg.start
                                    ch_seg.end = seg.end
                            start = seg.end
                        current_msegs[-1].start = start
                        current_msegs[-1].end = mseg.parent().end
                        if current_msegs[-1].children():
                            for ch_seg in current_msegs[-1].children():
                                ch_seg.start = current_msegs[-1].start
                                ch_seg.end = current_msegs[-1].end
                    else:
                        mseg.content = mseg.content.partition("//")[0]

    #Defining every gloss and pos segments content based on their current possible contents and (given the morph segment content) which content occurs at all and the most in the daakie_data dict.
    for tier in trans:
        if ("ge@unknown" == tier.name) | ("ps@unknown" == tier.name):
            if "ge@unknown" == tier.name:
                index = 0
            elif "ps@unknown" == tier.name:
                index = -1
            for seg in tier:
                if "//" in seg.content:
                    mseg = seg.parent()
                    splitted_content = seg.content.split("//")
                    if mseg.content in daakie_data:
                        fav = "XXXXX"
                        for cont in splitted_content:
                            if cont in daakie_data[mseg.content][index]:
                                if fav == "XXXXX":
                                    fav = cont
                                elif daakie_data[mseg.content][index][fav] < daakie_data[mseg.content][index][cont]:
                                    fav = cont
                                #These concern gloss segments having two possible contents being identical.
                                #elif daakie_data[mseg.content][index][fav] == daakie_data[mseg.content][index][cont]:
                        if fav != "XXXXX":
                            seg.content = fav
                        else:
                            for cont in splitted_content:
                                if cont != seg.struct.elem[seg.index()+1].content:
                                    seg.content = cont#+"!!!"#for debugging purpose.
                                    #I manually added 'water' as a gloss and 'n' as a pos tag wo the morph 'we' (it always occured after the morph 'lake') after applying script.

                    else:
                        part_cont = seg.content.partition("//")
                        seg.content = part_cont[0]
                        if part_cont[0] == "":
                            seg.content = part_cont[-1]

    #Removing morph segments only consisting of dashes (as well as the time-aligned gloss and pos segments) and readjusting the times of the remaining morph segments.
    for mtier in trans:
        if "mb@unknown" == mtier.name:
            for mseg in mtier:
                #Removing the morph segment containing only a dash, and removing its children (gloss and pos segment).
                if mseg.content == "-":
                    if mseg.children():
                        for ch_seg in mseg.children():
                            ch_seg.struct.remove(ch_seg)
                    par_seg = mseg.parent()
                    mtier.remove(mseg)
                    #Adjusting the times of the remaining morph segments and their child segments.
                    if mtier in par_seg.childDict():
                        msegs = par_seg.childDict()[mtier]
                        start = par_seg.start
                        total_time = par_seg.end - par_seg.start
                        for seg in msegs[:-1]:
                            seg.start = start
                            seg.end = start+(total_time/len(msegs))
                            if seg.children():
                                for ch_seg in seg.children():
                                    ch_seg.start = seg.start
                                    ch_seg.end = seg.end
                            start = seg.end
                        msegs[-1].start = start
                        msegs[-1].end = par_seg.end
                        if msegs[-1].children():
                            for ch_seg in msegs[-1].children():
                                ch_seg.start = msegs[-1].start
                                ch_seg.end = msegs[-1].end

    #Saving the new (finally fixed) eaf file.
    toElan.toElan(output_path+file_name,trans)