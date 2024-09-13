# Created: 2023-11-19
# Latest Version: 2023-12-09
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by François Delafontaine

from corflow import fromElan,toElan
import glob
import pandas as pd
import sys
sys.path.append("../")
from corflow_additional_functions import find_tiers

def move_segments(base_tier,move_tier,start_index,end_index,move_pattern:list):
    '''Moves every segment within a range of indices from *start_index* to *end_index* on a tier *move_tier*, whose time corresponds (is time-aligned) to a segment within the same range of indices on a tier *base_tier*. Every such segment on *move_tier* (and all of their children) are moved based on the indices given in *move_pattern*: The numbers values represent the indices of the segments within the given range from the *base_tier* ('0' represents the first segment, '1' the second, and so on). The numbers order represents the order of the segments within the range from the *move_tier* (the first number represents the first segment, the second number the second segment, and so on).'''

    def copy_structure(seg,dic):
        '''Returns the hierarchical structure (in form of the dictionary *dic*) of a segment *seg*, which is a key in the dictionary *dic* with a 3-tuple as its value: The first element is the segments structure (tier), the second is the segments content and the third is an empty list for possible child segments. For every child segment *seg* has, a new dictionary with the same structure is created and added to the empty list within the 3-tuple of the segment *seg*.  This is done recursivly for every child (and smaller) segment that exists within the hierarchical structure of *seg*.'''
        if seg.children():
            for tier,val in seg.childDict().items():
                for ch_seg in val:
                    ch_dict = {ch_seg:(ch_seg.struct,ch_seg.content,[])}
                    dic[seg][-1].append(ch_dict)
                    copy_structure(ch_seg,ch_dict)
        return dic

    def get_first_indices(all_segs,indices_dict):
        '''Returns the (initially empty) dictionary *indices_dict* with tier objects as keys and as their values the index of the first segment, which is potentially moved, within a list of segments to be moved *all_segs*. Every segment is within a dictionary the key with a 3-tuple as its value.'''

        for seg_dict in all_segs:
            seg = list(seg_dict.keys())[0]
            seg_val = list(seg_dict.values())[0]
            if not seg_val[0] in indices_dict.keys():
                indices_dict[seg_val[0]] = seg.index()
            if seg.struct.children():
                if seg.children():
                    get_first_indices(seg_val[2],indices_dict)

        return indices_dict

    def del_segs(seg):
        '''Removes a segment *seg* and all of its child segments from their tiers.'''
        if seg.children():
            for ch_seg in seg.children():
                del_segs(ch_seg)
        seg.struct.remove(seg)

    def get_par_tier(move_tier):
        '''Returns the parent tier, if the *move_tier* has one. Returns None otherwise.'''
        if move_tier.parent() == None:
            m_par_tier = None
        elif move_tier.parent() != None:
            m_par_tier = move_tier.parent()
        return m_par_tier

    def overwrite_structure(msegs,first_indices_dict,move_tier,par_tier,count_added,poss_par_seg):
        '''Adds for every mseg (moved segment) in a list with all msegs (having their hierarchical structure) *msegs* a new segment to their tier (*move_tier*) and defines a) their parent as the bseg (base segment) *poss_par_seg*, if the *move_tier* is a child tier of the base tier *par_tier*, b) their content based on the informations in *msegs* and c) their name in a unique way. This is done recursively for all possible child (and smaller) segments within the hierarchical structure of an mseg.'''
        new_msegs = []
        for seg_d in msegs:
            seg_val = list(seg_d.values())[0]
            seg_tier = seg_val[0]
            seg_index = first_indices_dict[seg_tier]
            if seg_index > 0:
                add_seg = seg_tier.elem[seg_index-1]
            else:
                add_seg = seg_tier.elem[seg_index]
            seg_tier.add(seg_index,add_seg)
            new_seg = seg_tier.elem[seg_index]
            new_seg.content = seg_val[1]
            new_seg.name += "_"+str(count_added)
            if par_tier == poss_par_seg.struct:
                new_seg.setParent(poss_par_seg)
            elif par_tier != None:
                new_seg.setParent(par_tier.getTime(poss_par_seg.start))
            else:
                new_seg.setParent(par_tier)
            if new_seg.struct == move_tier:
                new_msegs.append(new_seg)
            count_added += 1
            first_indices_dict[seg_tier] += 1
            if seg_val[-1]:
                overwrite_structure(seg_val[-1],first_indices_dict,move_tier,seg_tier,count_added,new_seg)
        return new_msegs

    def set_seg_times(new_msegs,dic):
        '''Sets the start and end time for every newly added mseg from *new_msegs* (and all of its possible child segments) based on the total number of msegs per bseg in base_tier_d *dic*.'''

        def set_child_seg_times(par_seg):
            if par_seg.children():
                total_time = par_seg.end - par_seg.start
                for child_segs in par_seg.childDict().values():
                    if child_segs:
                        time_frag = total_time/len(child_segs)
                        for i,ch_seg in enumerate(child_segs):
                            if i == 0:
                                ch_seg.start = par_seg.start
                                if (i+1) == len(child_segs):
                                    ch_seg.end = par_seg.end
                                else:
                                    ch_seg.end = ch_seg.start + time_frag
                                    start = ch_seg.end
                            elif (i+1) == len(child_segs):
                                ch_seg.start = start
                                ch_seg.end = par_seg.end
                            else:
                                ch_seg.start = start
                                ch_seg.end = start + time_frag
                                start = ch_seg.end
                            set_child_seg_times(ch_seg)

        msegs_distr_and_times = []
        count = 0
        for bseg_val in list(dic.values()):
            bseg = bseg_val[0]
            msegs = bseg_val[-1]
            msegs_per_bseg = []
            for mseg in msegs:
                msegs_per_bseg.append(count)
                count += 1
            bseg_times = (bseg.start,bseg.end)
            msegs_distr_and_times.append((bseg_times,msegs_per_bseg))
        for i,new_mseg in enumerate(new_msegs):
            for times_distr in msegs_distr_and_times:
                times = times_distr[0]
                distr = times_distr[-1]
                if distr:
                    total_time = times[1] - times[0]
                    time_frag = total_time/(len(distr))
                    if distr[0] == i:
                        new_mseg.start = times[0]
                        if distr[-1] == i:
                            new_mseg.end = times[1]
                        else:
                            new_mseg.end = times[0]+time_frag
                            start = new_mseg.end
                    elif distr[-1] == i:
                        new_mseg.start = start
                        new_mseg.end = times[1]
                    elif i in distr:
                        new_mseg.start = start
                        new_mseg.end = start + time_frag
                        start = new_mseg.end
            set_child_seg_times(new_mseg)



    base_tier_d = {}
    time_aligned_segs = []
    for i,index in enumerate(range(start_index,end_index+1)):
        base_seg = base_tier.elem[index]
        b_start = base_seg.start
        b_end = base_seg.end
        collected_segs = False
        move_tier_segs = [seg for seg in move_tier]
        num_collected = len(time_aligned_segs)
        while collected_segs == False:
            seg_index = int(len(move_tier_segs)/2)
            if len(move_tier_segs) == 0:
                break
            move_seg = move_tier_segs[seg_index]
            if (move_seg.start < b_start) & (move_seg.end < b_end):
                move_tier_segs = move_tier_segs[seg_index+1:]
            elif (move_seg.start > b_start) & (move_seg.end > b_end):
                move_tier_segs = move_tier_segs[:seg_index]
            elif move_seg.start == b_start:
                if move_seg.end == b_end:
                    time_aligned_segs.append(move_seg)
                    collected_segs = True
                else:
                    while move_seg.end <= b_end:
                        time_aligned_segs.append(move_seg)
                        seg_index += 1
                        if len(move_tier_segs) < seg_index+1:
                            break
                        move_seg = move_tier_segs[seg_index]
                    collected_segs = True
            elif (move_seg.end == b_end) | ((move_seg.start > b_start) & (move_seg.end < b_end)):
                while move_seg.start != b_start:
                    seg_index -= 1
                    move_seg = move_tier_segs[seg_index]
                while move_seg.end <= b_end:
                    time_aligned_segs.append(move_seg)
                    seg_index += 1
                    if len(move_tier_segs) < seg_index+1:
                        break
                    move_seg = move_tier_segs[seg_index]
                collected_segs = True

        b_length = len(time_aligned_segs)-num_collected
        base_tier_d[i] = (base_seg,b_length,[])

    for i,seg in enumerate(time_aligned_segs):
        seg_structure = {seg:(seg.struct,seg.content,[])}
        seg_final_structure = copy_structure(seg,seg_structure)
        time_aligned_segs[i] = seg_final_structure

    first_indices_dict = {}
    first_indices_dict = get_first_indices(time_aligned_segs,first_indices_dict)

    if ("l" in move_pattern) | ("r" in move_pattern):
        pass
    elif len(move_pattern) != len(time_aligned_segs):
        return print("The length of the *move_pattern* is not the same as the number of collected move segments.")
    else:
        pass
        for i,index in enumerate(move_pattern):
            base_tier_d[index][-1].append(time_aligned_segs[i])

    move_tier_par_tier = get_par_tier(move_tier)

    #Deleting all resplective move segments and their possible children.
    for mseg_d in time_aligned_segs:
        seg = list(mseg_d.keys())[0]
        del_segs(seg)

    new_msegs = []
    for bseg,blen,msegs in base_tier_d.values():
        new_msegs += overwrite_structure(msegs,first_indices_dict,move_tier,move_tier_par_tier,0,bseg)

    set_seg_times(new_msegs,base_tier_d)

    return print("Segments moved!")


##############################
#ACTUAL OPERATIONS BEGIN HERE!
##############################
input_path = "../../input_files/"
output_path = "../../output_files/"
csv_file = "sumi_mismatches.csv"

mismatches_df = pd.read_csv(input_path+csv_file,sep=";",header=0)
eaf_files = glob.glob(input_path+"/*.eaf")
for file in eaf_files:
    print(f"File: {file.replace(input_path,'')}")
    trans = fromElan.fromElan(file,encoding="utf-8")
    names = []
    start = False
    for i,row in mismatches_df.iterrows():
        if (row["File Name"] == trans.name) & (row["Mismatch Group"] == "start"):
            start = True
            names.append(row["Segment Name"])
            morph_pattern = []
            num_str = ""
            for sign in str(row["Morph Move Pattern"])+",":
                if sign != ",":
                    num_str += sign
                elif sign == ",":
                    morph_pattern.append(int(num_str))
                    num_str = ""
            #morph_pattern = [int(num) for num in str(row["Morph Move Pattern"]) if num != ","]
            if str(row["POS Move Pattern"]) != "no":
                pos_pattern = []
                num_str = ""
                for sign in str(row["POS Move Pattern"])+",":
                    if sign != ",":
                        num_str += sign
                    elif sign == ",":
                        pos_pattern.append(int(num_str))
                        num_str = ""
                #pos_pattern = [int(num) for num in str(row["POS Move Pattern"]) if num != ","]
            else:
                pos_pattern = None
            print(f"Morph_pattern: {morph_pattern}")
            print(f"pos pattern: {pos_pattern}")
        elif (row["File Name"] == trans.name) & (row["Mismatch Group"] == "x") & (start):
            names.append(row["Segment Name"])
        elif (row["File Name"] == trans.name) & (row["Mismatch Group"] == "end") & (start):
            names.append(row["Segment Name"])
            start = False

            for w_tier in find_tiers(trans,"Words-txt-nsm"):
                print(f"Word tier: {w_tier.name}")
                m_tier = w_tier.children()[1]
                pos_tier = w_tier.children()[0]
                start_ind = None
                end_ind = None
                for w_seg in w_tier:
                    if w_seg.name == names[0]:
                        start_ind = w_seg.index()
                    elif w_seg.name == names[-1]:
                        end_ind = w_seg.index()
                        break
                if (start_ind != None) & (end_ind != None):
                    move_segments(w_tier,m_tier,start_ind,end_ind,morph_pattern)
                    if pos_pattern != None:
                        move_segments(w_tier,pos_tier,start_ind,end_ind,pos_pattern)

            names = []

    toElan.toElan(output_path+file.replace(input_path,""),trans)

