# Created: March 2023
# Latest Version: 2023-03-26
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

'''
This script produces a txt-file with the following informations for all eaf-files in the relative path "../input_files/" to this script:

i) All morph instances, which do not have a corresponding, time-aligned gloss assigned to them.
ii) The type-frequency of those morphs with no assigned gloss (morphs with a gap).
iii) All glosses which were at least once assigned to any instance of a morph with a gap and their frequency.
iv) A list of all morph instances with no corresponding, time-aligned gloss, with their respective index in the file and their length (starting and end time).
'''

from corflow import fromElan,toElan
import glob
from collections import Counter

path="../../input_files/"
list_of_files = glob.glob(path+"/*.eaf")

printing_report = []
count_cases = 0
count_observed_files = 0
count_observed_speakers = 0
misalignment_instances = []
misalignment_instances_typed = []
glosses_of_a_gap = {}

for file in list_of_files:
    transcription = fromElan.fromElan(file,encoding="utf-8")
    mb_tier_exists = False
    gl_tier_exists = False
    new_file = True
    for tier in transcription:
        if "morph-txt" in tier.name:
            mb_tier = transcription.getName(tier.name)
            mb_tier_exists = True
        elif "morph-gls-en" in tier.name:
            gl_tier = transcription.getName(tier.name)
            gl_tier_exists = True
        if mb_tier_exists & gl_tier_exists:
            if new_file == True:
                count_observed_files += 1
                new_file = False
            count_observed_speakers += 1
            mb_tier_exists = False
            gl_tier_exists = False
            gl_tier_segtime_list = []
            for gl_seg in gl_tier:
                gl_tier_segtime_list.append(gl_seg.start)
            printing_report.append("\n**********\n"+str(file)+"\n**********\n")
            for mb_seg in mb_tier:
                if not mb_seg.start in gl_tier_segtime_list:
                    printing_report.append(str(mb_seg.content)+" Index: "+str(mb_seg.index())+" Time: "+str(mb_seg.start)+"-"+str(mb_seg.end)+".\n")
                    count_cases += 1
                    if not mb_seg.content in glosses_of_a_gap:
                        glosses_of_a_gap[mb_seg.content] = []
                    misalignment_instances.append(mb_seg.content)

for gap in misalignment_instances:
    if not gap in misalignment_instances_typed:
        misalignment_instances_typed.append(gap)

for file in list_of_files:
    transcription = fromElan.fromElan(file,encoding="utf-8")
    mb_tier_exists = False
    gl_tier_exists = False
    for tier in transcription:
        if "morph-txt" in tier.name:
            mb_tier = transcription.getName(tier.name)
            mb_tier_exists = True
        elif "morph-gls-en" in tier.name:
            gl_tier = transcription.getName(tier.name)
            gl_tier_exists = True
        if mb_tier_exists & gl_tier_exists:
            mb_tier_exists = False
            gl_tier_exists = False
            for gap_type in misalignment_instances_typed:
                gloss_instances = []
                for mb_seg in mb_tier:
                    if gap_type == mb_seg.content:
                        for gl_seg in gl_tier:
                            if (mb_seg.start == gl_seg.start) & (mb_seg.end == gl_seg.end):
                                gloss_instances.append(gl_seg.content)
                if gap_type in glosses_of_a_gap:
                    glosses_of_a_gap[gap_type] = glosses_of_a_gap[gap_type] + gloss_instances

sort_misalignment_instances_gt1 = [(x,value) for x,value in Counter(misalignment_instances).most_common() if value > 1]
sort_misalignment_instances_eq_or_lt1 = [(x,value) for x,value in Counter(misalignment_instances).most_common() if value == 1]

with open("./report_corflow_detect_and_describe_gaps.txt","w") as report:
    report.write("#############\n#GAPS REPORT#\n#############\n\nThere were "+str(count_cases)+" gaps found in "+str(count_observed_files)+" from "+str(len(list_of_files))+" observed files for "+str(count_observed_speakers)+" speakers.\nA gap is defined as a morph-token without a corresponding, time-aligned gloss-token.\n\n")
    report.write("##########\nHow often does the same type of a gap occur?\n##########\n\n")
    report.write("---\n---\nThe morph-type has more than one gap:\n---\n---\n\n")
    for entry in sort_misalignment_instances_gt1:
        report.write(str(entry)+"\n")
    report.write("\n---\n---\nThe morph-type has exactly one gap:\n---\n---\n\n")
    for entry in sort_misalignment_instances_eq_or_lt1:
        report.write(str(entry)+"\n")
    report.write("\n##########\nTaking a look at the morph-types, which have at least one occuring gap across all files: i) Which and how many different glosses get assigned to the tokens of the morph-type and ii) how often do the different gloss-types get assigned:\n##########\n\n")
    report.write("---\n---\nExactly one gloss-type is assigned to a morph-type with at least one gap:\n---\n---\n\n")
    report.write("+++\n+++\nThe gloss-type is more than once assigned to the respective morph-type with a gap:\n+++\n+++\n\n")
    for morph in glosses_of_a_gap:
        if len(Counter(glosses_of_a_gap[morph])) == 1:
            if len(glosses_of_a_gap[morph]) > 1:
                report.write("Morph: "+str(morph)+": Gloss: "+str(Counter(glosses_of_a_gap[morph]).most_common())+"\n\n")
    report.write("+++\n+++\nThe gloss-type is only once assigned to the respective morph-type with a gap:\n+++\n+++\n\n")
    for morph in glosses_of_a_gap:
        if len(Counter(glosses_of_a_gap[morph])) == 1:
            if len(glosses_of_a_gap[morph]) == 1:
                report.write("Morph: "+str(morph)+": Gloss: "+str(Counter(glosses_of_a_gap[morph]).most_common())+"\n\n")
    report.write("---\n---\nMore than one different gloss-type gets assigned to a morph-type with a gap:\n---\n---\n\n")
    for morph in glosses_of_a_gap:
        if len(Counter(glosses_of_a_gap[morph])) > 1:
            report.write("Morph: "+str(morph)+": Glosses: "+str(Counter(glosses_of_a_gap[morph]).most_common())+"\n\n")
    report.write("---\n---\nNo glosses at all get assigned to a morph-type with a gap:\n---\n---\n\n")
    for morph in glosses_of_a_gap:
        if len(Counter(glosses_of_a_gap[morph])) < 1:
            report.write("Morph: "+str(morph)+": Glosses: "+str(Counter(glosses_of_a_gap[morph]).most_common())+"\n\n")