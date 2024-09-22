#Created: 2024-02-15
#Latest Version: 2024-02-16
#Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
#Corflow module created by François Delafontaine

'''
Fixes for the savosavo file 'pb_cs_batugha.eaf' two instances, where a) a merging process did not apply due to bad input and b) in one case, where segments were misaligned.
'''

from corflow import fromElan,toElan
import sys
sys.path.append("../")
from corflow_additional_functions import find_tiers, merge_segments

def copy_seg(seg,right=True,name_suffix="_0",same_parent=True):
    '''Creates a copy of an existing segment *seg* either right next to it, if *right* is True, or left to it, if *right* is False. Its name is defined as *seg*'s name + *name_suffix*. Its start and end time are the same as those of *seg*. If *same_parent* is True, its parent is the same as that of *seg*. Otherwise, it is either the right or left segment of *seg* depending on the value of *right*. Returns the newly added seg.'''
    tier = seg.struct
    if right:
        tier.add(seg.index()+1,seg)
        new_seg = tier.elem[seg.index()+1]
        if same_parent:
            new_seg.setParent(seg.parent())
        else:
            parent_tier = seg.parent().struct
            next_parent_seg = parent_tier.elem[seg.parent().index()+1]
            new_seg.setParent(next_parent_seg)
    else:
        tier.add(seg.index(),seg)
        new_seg = tier.elem[seg.index()-1]
        if same_parent:
            new_seg.setParent(seg.parent())
        else:
            parent_tier = seg.parent().struct
            previous_parent_seg = parent_tier.elem[seg.parent().index()-1]
            new_seg.setParent(previous_parent_seg)
    new_seg.name = seg.name + name_suffix
    return new_seg

def adjust_seg_times(seg):
    '''Adjusts the start and end time recursively and equally among all child segments of a segment *seg*. Returns nothing.'''
    if seg.children():
        total_time = seg.end-seg.start
        for seg_childs in seg.childDict().values():
            child_segs = sorted([(ch.index(),ch) for ch in seg_childs])
            child_segs = [ch for ind,ch in child_segs]
            time_portion = total_time/len(child_segs)
            for ind,ch_seg in enumerate(child_segs):
                if ind == 0:
                    if ind+1 == len(child_segs):
                        ch_seg.start = seg.start
                        ch_seg.end = seg.end
                    else:
                        ch_seg.start = seg.start
                        ch_seg.end = seg.start+time_portion
                        start = ch_seg.end
                elif ind+1 == len(child_segs):
                    ch_seg.start = start
                    ch_seg.end = seg.end
                else:
                    ch_seg.start = start
                    ch_seg.end = start+time_portion
                    start = ch_seg.end
                adjust_seg_times(ch_seg)



#File and transcription.
input_path = "../../input_files/"
output_path = "../../output_files/"
file = "pb_cs_batugha.eaf"
trans = fromElan.fromElan(input_path+file,encoding="utf-8")

#Operations.
for tier in find_tiers(trans,"^sa@PB$"):
    #help(tier)
    #break
    for seg in tier:
        if seg.start > 920:
            if seg.content == "soteghue":
                next_seg = seg.struct.elem[seg.index()+1]
                merged_seg = merge_segments(next_seg)
                merged_seg.content = merged_seg.content[:-2]
                for ch_seg in merged_seg.children():
                    if ch_seg.content == "la":
                        ch_seg.struct.allRemove(ch_seg)
                next_seg = merged_seg.struct.elem[merged_seg.index()+1]
                next_seg.content = "lona."
                for ch_seg in next_seg.children():
                    if ch_seg.content == "na":
                        ch_seg.content = "=" + ch_seg.content
                        for ch_ch_seg in ch_seg.children():
                            ch_ch_seg.content = "=" + ch_ch_seg.content
                adjust_seg_times(merged_seg)
        if seg.start > 1341:
            if seg.content == "lo":
                merged_seg = merge_segments(seg,1)
                for child in merged_seg.children():
                    if child.content == "na":
                        child.content = "=" + "na"
                        for ch_seg in child.children():
                            if ch_seg.struct.name.startswith("gl@"):
                                ch_seg.content = "=NOM"
                            else:
                                ch_seg.content = "=" + ch_seg.content
                break

#Save new eaf.
toElan.toElan(output_path+file,trans)


#This was the wrong merging.
'''
next_seg = seg.struct.elem[seg.index()+1]
merged_seg = merge_segments(next_seg)
print(f"merged seg: {(merged_seg.content,merged_seg.start,merged_seg.end)}")
mb_seg = merged_seg.children()[0]
print(f"its mb seg: {(mb_seg.content,mb_seg.start,mb_seg.end,mb_seg.index())}")
new_mb_seg = copy_seg(mb_seg)
new_mb_seg.content = "lo"
mb_seg.end = mb_seg.start + ((mb_seg.end-mb_seg.start)/2)
new_mb_seg.start = mb_seg.end
print(f"new mb seg: {(new_mb_seg.content,new_mb_seg.start,new_mb_seg.end,new_mb_seg.index())}")
for ch_seg in mb_seg.children():
    print(f"mb ch seg: {(ch_seg.content,ch_seg.start,ch_seg.end,ch_seg.index())}")
    new_ch_seg = copy_seg(ch_seg,same_parent=False)
    ch_seg.end = mb_seg.end
    new_ch_seg.start = new_mb_seg.start
    new_ch_seg.end = new_mb_seg.end
    if ch_seg.struct.name.startswith("gl"):
        new_ch_seg.content = "3SG.M"
    else:
        new_ch_seg.content = "pp"
    print(f"new ch seg: {(new_ch_seg.content,new_ch_seg.start,new_ch_seg.end,new_ch_seg.index())}")
next_seg = merged_seg.struct.elem[merged_seg.index()+1]
print(f"next seg: {(next_seg.content,next_seg.start,next_seg.end,next_seg.index())}")
next_seg_mb = next_seg.children()[0]
next_seg_mb.struct.allRemove(next_seg_mb)
next_seg_mb2 = next_seg.children()[0]
next_seg_mb2.start = next_seg.start
for ch_seg in next_seg_mb2.children():
    ch_seg.start = next_seg_mb2.start
for tier,children in merged_seg.childDict().items():
    if tier.name.startswith("mb@"):
        for ch_seg in children:
            if ch_seg.content == "la":
                ch_seg.struct.allRemove(ch_seg)
adjust_seg_times(merged_seg)
break
'''


