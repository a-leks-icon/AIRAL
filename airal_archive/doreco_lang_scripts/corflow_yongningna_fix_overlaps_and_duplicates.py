#Created: 2024-02-17
#Latest Version: 2024-02-17
#Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
#Corflow module created by François Delafontaine

'''
Fixes times of overlapping segments and removes duplicated segments (as well as moves for one file one segment one tier down) for the following six files of the language yongningna:
crdo-NRU_F4_BURIEDALIVE3.eaf, crdo-NRU_F4_BURIEDALIVE2.eaf, crdo-NRU_F4_35_DOG_WITH_EGG.eaf, crdo-NRU_F4_36_TIGER_WITH_EGG.eaf, crdo-NRU_F4_HOUSEBUILDING.eaf, crdo-NRU_F4_10_AGRICULTURAL_ACTIVITIES.eaf
'''

from corflow import fromElan, toElan
import sys
sys.path.append("../")
from corflow_additional_functions import get_duplicated_segments, get_overlapping_segments
import glob

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

input_path = "../../input_files/"
output_path = "../../output_files/"
eaf_files = glob.glob(input_path+"/*.eaf")

for file in eaf_files:
    file_name = file.replace(input_path,"")
    print(f"FILE: {file_name}")
    trans = fromElan.fromElan(file,encoding="utf-8")

    #Fix overlapping segments. Adjusting the end time of the first segment to the start time of the second segment.
    for tier,overlaps_l in get_overlapping_segments(trans).items():
        if overlaps_l:
            for seg1,seg2 in overlaps_l:
                seg1.end = seg2.start
    
    #Fix duplicated segments.
    for tier,duplicates_l in get_duplicated_segments(trans).items():
        if duplicates_l[1:]:
            if tier.name == "W-fr":
                print(f"duplicates: {duplicates_l}")
                for seg1,seg2 in duplicates_l[1:]:
                    prev_seg1_parent = seg1.struct.elem[seg1.index()-1].parent()
                    for prev_seg1_childs in prev_seg1_parent.childDict().values():
                        if prev_seg1_childs[0].struct != seg1.struct:
                            new_seg1_sister = copy_seg(prev_seg1_childs[0],same_parent=False)
                            new_seg1_sister.start = seg1.start
                            new_seg1_sister.end = seg1.end
                            new_seg1_sister.content = seg2.content
                            seg2.struct.remove(seg2)
            else:
                for seg1,seg2 in duplicates_l[1:]:
                    seg2.struct.remove(seg1)

    #Save new eaf file.
    toElan.toElan(output_path+file_name,trans)

