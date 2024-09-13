# Created: 2023-07-28
# Latest Version: 2023-07-28
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

from corflow import fromElan
import glob
from collections import Counter

'''
This file collects in every modified bora eaf-file for every morph occuring as either an affix or clitic its children (meaning the content of its gloss-, ps-, mt- and ntvr-tiers) and displays their frequency.
'''

output_path = "../../output_files/"

eaf_files = glob.glob(output_path+"/*.eaf")

children_of_affixes_and_clitics = {}
children_of_non_affixes_and_clitics = {}

complete_children_of_non_affixes_and_clitics_with_gaps = {}

for file in eaf_files:
    trans = fromElan.fromElan(file,encoding="utf-8")
    for mb_tier in trans:
        if mb_tier.name.startswith("mb@"):
            for mb_seg in mb_tier:
                if (mb_seg.content.startswith("-")) | (mb_seg.content.startswith("=")) | (mb_seg.content.endswith("-")) | (mb_seg.content.endswith("=")):
                    if not mb_seg.content in children_of_affixes_and_clitics:
                        children_of_affixes_and_clitics[mb_seg.content] = []
                    if not [child.content for child in mb_seg.children()] in children_of_affixes_and_clitics[mb_seg.content]:
                        children_of_affixes_and_clitics[mb_seg.content].append([child.content for child in mb_seg.children()])
                elif len(mb_seg.children()) < 4:
                    if not mb_seg.content in children_of_non_affixes_and_clitics:
                        children_of_non_affixes_and_clitics[mb_seg.content] = []
                    if not [child.content for child in mb_seg.children()] in children_of_non_affixes_and_clitics[mb_seg.content]:
                        children_of_non_affixes_and_clitics[mb_seg.content].append([child.content for child in mb_seg.children()])
            for mb_seg in mb_tier:
                if mb_seg.content in children_of_non_affixes_and_clitics.keys():
                    for key in children_of_non_affixes_and_clitics.keys():
                        if mb_seg.content == key:
                            if not key in complete_children_of_non_affixes_and_clitics_with_gaps:
                                complete_children_of_non_affixes_and_clitics_with_gaps[key] = []
                            if not [child.content for child in mb_seg.children()] in complete_children_of_non_affixes_and_clitics_with_gaps[key]:
                                complete_children_of_non_affixes_and_clitics_with_gaps[key].append([child.content for child in mb_seg.children()])


for key,val in children_of_affixes_and_clitics.items():
    print(key)
    print("~~~")
    print(val)
    print("#######################################################")

print("+++++++++++++++++++++++++++++++++++++++")
print("+++++++++++++++++++++++++++++++++++++++")
print("LISTS WITH MISSING SEGMENTS ON SOME TIERS")
print("+++++++++++++++++++++++++++++++++++++++")
for key,val in children_of_affixes_and_clitics.items():
    for list in val:
        if len(list) < 4:
            print(key)
            print("~~~")
            print(val)
            print("#######################################################")
print("+++++++++++++++++++++++++++++++++++++++")
print("+++++++++++++++++++++++++++++++++++++++")
print("LISTS WITH **** AS VALUE")
print("+++++++++++++++++++++++++++++++++++++++")
for key,val in children_of_affixes_and_clitics.items():
    for list in val:
        if "****" in list:
            print(key)
            print("~~~")
            print(val)
            print("#######################################################")

print("+++++++++++++++++++++++++++++++++++++++")
print("+++++++++++++++++++++++++++++++++++++++")
print("OTHER GAPS")
print("+++++++++++++++++++++++++++++++++++++++")
for key,val in children_of_non_affixes_and_clitics.items():
    print(key)
    print("~~~")
    print(val)
    print("#######################################################")

print("+++++++++++++++++++++++++++++++++++++++")
print("+++++++++++++++++++++++++++++++++++++++")
print("ACTUAL CHILDREN OF OTHER GAPS")
print("+++++++++++++++++++++++++++++++++++++++")
for key,val in complete_children_of_non_affixes_and_clitics_with_gaps.items():
    print(key)
    print("~~~")
    print(val)
    print("#######################################################")


