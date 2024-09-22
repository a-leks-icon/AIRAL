# Created: 2023-07-30
# Latest Version: 2023-08-03
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

from corflow import fromElan,toElan
import sys
sys.path.append("../")
from corflow_additional_functions import define_content,fill_gaps_match,remove_segments

input_path = "../../input_files/"
output_path = "../../output_files/"

file1 = "071_cut_changes_01.eaf"
file2 = "086_cut_changes_01.eaf"

trans1 = fromElan.fromElan(input_path+file1,encoding="utf-8")
trans2 = fromElan.fromElan(input_path+file2,encoding="utf-8")

#Fixing the word-tier and its child-tiers (morph-, gloss-, morph-msa- and morph type-tiers) for those segments, which are children of certain segments on the phrase-tier for certain files: For file1: '1.19' on the phrase-tier; for file2: '1.20' on the phrase tier. The current content and/or structure of thoese segments is wrong, because of a previous issue in ELAN.

#Collecting information about the content and structure of those word segments, which have to be fixed, in a dictionary (per file).

#File 1.
glosses_of_misaligned_word_segs_f1 = {}
f1_word_tier_exists = False
for tier in trans1:
    if "A_word-txt-erk" == tier.name:
        word_tier_f1 = trans1.getName(tier.name)
        f1_word_tier_exists = True

    if f1_word_tier_exists:
        f1_word_tier_exists = False

        for word_seg in word_tier_f1:
            if word_seg.parent().content == "1.19":
                if not word_seg.content in glosses_of_misaligned_word_segs_f1.keys():
                    glosses_of_misaligned_word_segs_f1[word_seg.content] = []
        for word_seg in word_tier_f1:
            if word_seg.parent().content != "1.19":
                if word_seg.content in glosses_of_misaligned_word_segs_f1.keys():
                    for mb_seg in word_seg.children():
                        glosses_of_misaligned_word_segs_f1[word_seg.content].append([mb_seg.content]+[child_seg.content for child_seg in mb_seg.children()])

#File 2.
glosses_of_misaligned_word_segs_f2 = {}
f2_word_tier_exists = False
for tier in trans2:
    if "A_word-txt-erk" == tier.name:
        word_tier_f2 = trans2.getName(tier.name)
        f2_word_tier_exists = True

    if f2_word_tier_exists:
        f2_word_tier_exists = False

        for word_seg in word_tier_f2:
            if word_seg.parent().content == "1.20":
                if not word_seg.content in glosses_of_misaligned_word_segs_f2.keys():
                    glosses_of_misaligned_word_segs_f2[word_seg.content] = []
        for word_seg in word_tier_f2:
            if word_seg.parent().content != "1.20":
                if word_seg.content in glosses_of_misaligned_word_segs_f2.keys():
                    for mb_seg in word_seg.children():
                        glosses_of_misaligned_word_segs_f2[word_seg.content].append([mb_seg.content]+[child.content for child in mb_seg.children()])

        print(f"########################\nFILE {file1}\n########################")
        for key,val in glosses_of_misaligned_word_segs_f1.items():
            print(f"{key}: {val}")

        print(f"########################\nFILE {file2}\n########################")
        for key,val in glosses_of_misaligned_word_segs_f2.items():
            print(f"{key}: {val}")

#Certain changes could be done manually in ELAN itself (defining known content and deleting misplaced and adding missing segments). Adding missing segments on the child tiers of the morph tier have to be done via script in corflow, because there was no manual possibility to do it in ELAN.

#File 1.
seg_content_not_adding_childs = [".",",","§","071-019",",\"",".\""]
words_with_no_morph_seg = ["mai","nagis","ga","kaaru","tap̃o"]
for word_tier in trans1:
    if "A_word-txt-erk" == word_tier.name:
        morph_tier = word_tier.children()[0]
        print(morph_tier.name)
        for word_seg in word_tier:
            if word_seg.parent().content == "1.19":
                if not word_seg.content in seg_content_not_adding_childs:
                    if len(word_seg.children()) == 0:
                        print(word_seg.content)
                        for miss_morph in words_with_no_morph_seg:
                            #Adding missing morph segments for every above word segment.
                            fill_gaps_match(trans1,word_tier.name,morph_tier.name,miss_morph,"")
        for mb_seg in morph_tier:
            if len(mb_seg.children()) == 0:
                for morph_child_tier in morph_tier.children():
                    #Adding missing segments on those tiers, which are children of the morph tier, for those segments on the morph tier, that miss their children segments.
                    fill_gaps_match(trans1,morph_tier.name,morph_child_tier.name,"","")

#toElan.toElan(output_path+file1.replace("_changes_01","_changes_02"))

#File 2.
#True, if the operation has to take place and be exported to the new eaf-file. False, if not (if these changes were already made and the next step below has to be done).
apply_changes_02 = False

if apply_changes_02:
    for word_tier in trans2:
        if "A_word-txt-erk" == word_tier.name:
            #Finding the word tier.
            parent_child_cond = "‎‎There's a good side and a bad side. That's about all there is."
            #Iterating over all word segs on the 1.20 phrase seg with a specific translation seg.
            for word_seg_filtered in [word_seg for word_seg in word_tier if ((word_seg.parent().content == "1.20") & (parent_child_cond in [parent_child.content for parent_child in word_seg.parent().children()]))]:
                if word_seg_filtered.children():
                    fill_gaps_match(trans2,word_tier.name,word_tier.children()[0].name,"","")

if apply_changes_02:
    toElan.toElan(output_path+file2.replace("_changes_01","_changes_02"),trans2)

#False, if the above step was completed and the next manipulation has to take place. True, if not.
if apply_changes_02 == False:
    trans2_2 = fromElan.fromElan(output_path+file2.replace("_changes_01","_changes_03"),encoding="utf-8")

    for morph_tier in trans2_2:
        if "A_morph-txt-erk" == morph_tier.name:
            for child_tier in morph_tier.children():
                if child_tier.name != "A_morph-gls":
                    fill_gaps_match(trans2_2,morph_tier.name,child_tier.name,"","")

    toElan.toElan(output_path+file2.replace("_changes_01","_changes_04"),trans2_2)

