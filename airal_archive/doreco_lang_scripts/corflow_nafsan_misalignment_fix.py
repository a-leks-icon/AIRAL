# Created: 2023-08-25
# Latest Version: 2023-09-07
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

'''
This script uses a csv-file to fix all found cases of misaligments between words and their morphological structures across all eaf-files.
'''

#FUNCTIONS
def get_unique_values(df,label):
    '''Returns a list with all unique values of a column labeled *label* in a dataframe *df*.'''
    unique_values = []
    for value in df[label]:
        if not value in unique_values:
            unique_values.append(value)
    return unique_values

def get_unique_value_combinations(df,label:str,labels:str|list):
    '''Returns a dictionary with all unique values of a column *label* as keys and with all unique values in at least on column in *labels*'''
    unique_values = {}
    for value in df[label]:
        if not value in unique_values.keys():
            unique_values[value] = []
    if isinstance(labels,str):
        for row_num,value in enumerate(df[labels]):
            unique_val = unique_values[df[label].iloc[row_num]]
            if not value in unique_val:
                unique_val.append(value)
    elif isinstance(labels,list):
        return print("Not implemented yet.")
    return unique_values

def check_duplic_seg(tier):
    '''If a (phrase) segment shares the same content with another segment on the same tier (but itself), they are collected in a list, which gets returned at the end. If no case was found, False gets returned.'''
    duplic_segs = []
    for seg in tier:
        for seg2 in tier:
            if seg != seg2:
                if seg.content == seg2.content:
                    duplic_segs.append(seg.content)
    if duplic_segs:
        return duplic_segs
    else:
        return False

def check_seg_cont(seg,re_pattern):
    '''Returns True, if a segments content matches the regex pattern. If not, returns False.'''
    if re.search(re_pattern,seg):
        return True
    else:
        return False


#def get_child_tiers(parent_tier,amount:int):
#    '''Returns a list with tier objects of a *parent_tier* based on the *amount* of child tiers the *parent_tier* is supposed to have.'''
#    for seg in parent_tier:
#        if len(seg.childDict().keys()) == amount:
#            child_tiers = [x for x in seg.childDict().keys()]
#            break
#   return child_tiers


def get_child_segs_cont(parent_segments,child_tiers:list):
    '''Returns for all *parent_segments* a list which contains for every child tier in *child_tiers* a separate list with the content of every child segment.
    
    - parent_segments -- a list of segments, who must have child segments.

    - child_tiers -- a list of all those tier objects, which are child tiers of the *parent_segments* tier.
    '''
    child_tiers_cont_dict = {}
    for num in range(len(child_tiers)):
        child_tiers_cont_dict[num] = []
    for seg in parent_segments:
        for num,child_tier in enumerate(child_tiers):
            if child_tier in seg.childDict().keys():
                child_tiers_cont_dict[num] += [child_seg.content for child_seg in seg.childDict()[child_tier]]
            else:
                child_tiers_cont_dict[num].append("")
    final_child_cont_list = [val_list for val_list in child_tiers_cont_dict.values()]
    return final_child_cont_list

def remove_segments(segment):
    '''Removes the *segment* object and all of its direct child segment objects from their respective tiers.'''
    if segment.children():
        for seg_child in segment.children():
            seg_child.struct.remove(seg_child)
        segment.struct.remove(segment)

def add_multiple_segs(tier,index):
    '''Adds a new segment to *tier* at *index* based on (currently not active, therefore it does nothing.)'''


#IMPORTS
from corflow import fromElan,toElan
import pandas as pd
import glob
import re

#SCRIPT STARTS HERE
#Files (eaf-files and csv-file).
input_path = "../../input_files/"
output_path = "../../output_files/"
#eaf_files = glob.glob(input_path+"/*.eaf")
#csv_file = "nafsan_misaligned_values_260823.csv"
csv_file = "nafsan_misaligned_values_2023-09-07.csv"

#csv-file as a dataframe
df = pd.read_csv(input_path+csv_file,sep=";",header=0,on_bad_lines="skip")
unique_value_combs = get_unique_value_combinations(df,"File Name","Phrase")
print(unique_value_combs)

#Regex pattern used to exlude word segments from collecting.
re_pattern_neg_cont = "[0-9]|§|\$|^.$|^,$|\"|“|edited|\[|\]|pause|\?|\.\.|\(|\)|\/|corrected|^NT$|^KK$"

for file,phrase_val_list in unique_value_combs.items():
    print(f"!!!\nFILE: {file}\n!!!")
    trans = fromElan.fromElan(input_path+file,encoding="utf-8")
    #I checked manually beforehand, that only the 'A-phrase' tier and not the tier of a second or thirds peaker is problematic, something I could and should have done automatically in the first place with the check-script.
    phrase_tier = trans.findName("^A_phrase$")
    print(f"Phrase tier name: {phrase_tier.name}")
    #This ensured, that none of those phrase segments, which shared their content with another segment on the same tier (those exist in every phrase tier), were part of the problematic cases. They were not.
    #bad_cases = check_duplic_seg(phrase_tier)
    #for bad_case in bad_cases:
        #print(f"Bad case: *{bad_case}*.")
        #if bad_case in phrase_val_list:
            #print(f"ALARM FOR *{bad_case}*!")
    #print("###########################")

    #The dict used to store the content of all morph segments and their child segments, whose parent is the problematic phrase segment.
    morph_tier_prob_cases = {}

    #Used to count the newly added segments per file.
    new_add_count = 0

    morph_tier = phrase_tier.children()[-1].children()[-1]
    #print(f"morph tier name: {morph_tier.name}")
    morph_child_tiers = [mb_child_tier for mb_child_tier in morph_tier.children()]

    for phrase_seg in phrase_tier:
        for val in phrase_val_list:
            #The second condition  '(phrase_tier.elem[-1] != phrase_seg)' can be set to not change those phrase segments, that have the same content but are actually intact, which I think are most of the time the last phrase segments, but I have not verified that.
            if (phrase_seg.content == str(val)):
                #Iterating over every word segment, which has at least one child (morph) segment.
                word_segs_with_child = [seg for seg in list(phrase_seg.childDict().values())[-1] if seg.children()]
                #1. Step: For every word segment with at least one child (morph) segment, a) the content of the morph segments get concatenated, which is used as the dict_key and b) a list with four (up to six in some cases) lists each containing the content of all child tiers segments (morph, gloss, msa- and morph type tiers) gets collected and used as the value for the dict_key.

                for word_seg in word_segs_with_child:
                    morph_concat = ""
                    #print(f"word segment: {word_seg.content}")
                    
                    for morph_seg in word_seg.children():
                        morph_concat += morph_seg.content.replace("=","").replace("-","")
                    #print(f"morph segments: {[x.content for x in word_seg.children()]}")
                    #print(f"morph child tiers: {[x.name for x in morph_child_tiers]}")
                    #print("#######")
                    #print(get_child_segs_cont(word_seg.children(),morph_child_tiers))
                    #print("#######")
                    morph_tier_prob_cases[morph_concat] = [
                        [mb_seg.content for mb_seg in word_seg.children()]
                        ] + get_child_segs_cont(word_seg.children(),morph_child_tiers)
                print(f"DICT: {morph_tier_prob_cases}")
                    #print(f"first morph concat entry: {morph_tier_prob_cases}")
                #2. Step: For every word segment with at least one child (morph) segment, every morph segment and its children get deleted.
                #for morph_seg in morph_tier:
                    #if (morph_seg.start == phrase_seg.start) | (morph_seg.end == phrase_seg.end) | ((morph_seg.start > phrase_seg.start) & (morph_seg.end < phrase_seg.end)):
                            #remove_segments(morph_seg)
                for word_seg in word_segs_with_child:
                    for morph_seg in word_seg.children():
                        remove_segments(morph_seg)

                #3. Step: For every word segment with a meaningful content, create the appropriate number of segments on the morph, gloss, msa- and morph type tiers (and possible also on up to two other tiers). Define their content based on the concatenated morph segments content by the previously in step 1 collected contents.

                word_segs_good_cont = [seg for seg in list(phrase_seg.childDict().values())[-1] if not re.search(re_pattern_neg_cont,seg.content)]
                for word_seg in word_segs_good_cont:
                    print(f"word seg: {word_seg.content}")
                    found_key = False
                    for key,val_list_list in morph_tier_prob_cases.items():
                        if (word_seg.content == key) | (word_seg.content.lower() == key) | (word_seg.content.lower() == key.lower()):
                            found_key = True
                            print(f"good word seg: {word_seg.content}\n###########")
                            for count,val_list in enumerate(val_list_list):
                                new_seg_start = word_seg.start
                                if count == 0:
                                    print(f"morph segs: {val_list}")
                                    if len(morph_tier) < 1:
                                        add_index = 0
                                        ref_index = 0
                                    elif morph_tier.elem[-1].start < word_seg.start:
                                        #BEWARE: Because new segments ged added BEFORE a given index, insofar as new segments have to be added to the right of the last segment, the referenced index has to be increased by 1.
                                        add_index = morph_tier.elem[-1].index()+1
                                        ref_index = morph_tier.elem[-1].index()
                                    else:
                                        for mb_seg in morph_tier:
                                            if mb_seg.start > word_seg.start:
                                                add_index = mb_seg.index()
                                                ref_index = mb_seg.index()
                                                break
                                    print(f"mb tier add index: {add_index} ref index: {ref_index} with content "+str(morph_tier.elem[ref_index].content))
                                    
                                    new_added_mb_segs = []
                                    for val in val_list:
                                        #print(f"morph seg to add: {val} at index {ref_index}")
                                        morph_tier.add(add_index,morph_tier.elem[ref_index])
                                        new_seg = morph_tier.elem[add_index]
                                        new_seg.setParent(word_seg)
                                        new_seg.start = new_seg_start
                                        new_seg.end = (new_seg.start+((word_seg.end-word_seg.start)/len(val_list)))
                                        new_seg.name = "b"+str(new_add_count)
                                        new_add_count += 1
                                        new_seg_start = new_seg.end
                                        new_seg.content = val
                                        new_added_mb_segs.append(new_seg)
                                        add_index += 1
                                        ref_index += 1
                                        print(f"new mb seg index {new_seg.index()} and content {new_seg.content}")

                                else:
                                    print(f"other tier segs: {val_list}")
                                    morph_child_tier = morph_child_tiers[count-1]
                                    print(f"morph child tier: {morph_child_tier.name}")
                                    if len(morph_child_tier) < 1:
                                        add_index = 0
                                        ref_index = 0
                                    elif morph_child_tier.elem[-1].start < word_seg.start:
                                        #BEWARE: Because new segments ged added BEFORE a given index, insofar as new segments have to be added to the right of the last segment, the referenced index has to be increased by 1.
                                        add_index = morph_child_tier.elem[-1].index()+1
                                        ref_index = morph_child_tier.elem[-1].index()
                                    else:
                                        for seg in morph_child_tier:
                                            if seg.start > word_seg.start:
                                                add_index = seg.index()
                                                ref_index = seg.index()
                                                break
                                    print(f"mb child tier add index: {add_index} ref index: {ref_index} with content "+str(morph_child_tier.elem[ref_index].content))
                                    for count2,val in enumerate(val_list):
                                        #print(f"mb child seg to add: {val}")
                                        morph_child_tier.add(add_index,morph_child_tier.elem[ref_index])
                                        new_seg = morph_child_tier.elem[add_index]
                                        new_seg.setParent(new_added_mb_segs[count2])
                                        new_seg.start = new_seg_start
                                        new_seg.end = (new_seg.start+((word_seg.end-word_seg.start)/len(val_list)))
                                        #new_seg.setParent(morph_tier.getTime(new_seg.start))
                                        #Using different names, because one file previously went through the merging-script and got its segments renamed with the prefix 'b'. Using'b' again caused the file to be corrupt (because there were different segments with identical names/reference).
                                        new_seg.name = "bx"+str(new_add_count)
                                        new_add_count += 1
                                        new_seg_start = new_seg.end
                                        new_seg.content = val
                                        add_index += 1
                                        ref_index += 1
                                        print(f"new mb child seg index {new_seg.index()} and content {new_seg.content}")
                    #If finding the appropriate key (concatenation of previously collected morph segment contents) failed for a word segment, it gets on the morph and on every of its child tiers exactly one segment with empty content.
                    if found_key == False:
                        print(f"Word seg without the appropriate key!")
                '''
                        if len(morph_tier) < 1:
                            add_index = 0
                        else:
                            for mb_seg in morph_tier:
                                if mb_seg.start > word_seg.start:
                                    add_index = mb_seg.index()
                                    #print(f"mb tier add index: {add_index}")
                                    break
                                elif morph_tier.elem[-1].start < word_seg.start:
                                    add_index = morph_tier.elem[-1].index()
                                    #print(f"mb tier add index: {add_index}")
                                    break
                        new_added_mb_segs = []
                        #print(f"empty morph seg to add at index {add_index}")
                        morph_tier.add(add_index,morph_tier.elem[add_index])
                        new_seg = morph_tier.elem[add_index]
                        new_seg.setParent(word_seg)
                        new_seg.start = word_seg.start
                        new_seg.end = word_seg.end
                        new_seg.name = "b"+str(new_add_count)
                        new_add_count += 1
                        new_seg.content = ""
                        new_added_mb_seg = new_seg

                        for morph_child_tier in morph_child_tiers:
                            if len(morph_child_tier) < 1:
                                add_index = 0
                            else:
                                for seg in morph_child_tier:
                                    if seg.start > word_seg.start:
                                        add_index = seg.index()
                                        #print(f"other tier add index: {add_index}")
                                        break
                                    elif morph_child_tier.elem[-1].start < word_seg.start:
                                        add_index = morph_child_tier.elem[-1].index()
                                        #print(f"other tier add index: {add_index}")
                                        break
                            #print(f"empty mb child seg to add at index {add_index}")
                            morph_child_tier.add(add_index,morph_child_tier.elem[add_index])
                            new_seg = morph_child_tier.elem[add_index]
                            new_seg.setParent(new_added_mb_seg)
                            new_seg.start = word_seg.start
                            new_seg.end = word_seg.end
                            #new_seg.setParent(morph_tier.getTime(new_seg.start))
                            new_seg.name = "b"+str(new_add_count)
                            new_add_count += 1
                            new_seg.content = ""
                        '''

    toElan.toElan(output_path+file,trans)
    print("\n!!!\nNEXT FILE\n!!!\n")
