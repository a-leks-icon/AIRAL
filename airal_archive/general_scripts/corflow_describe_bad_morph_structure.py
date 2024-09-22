# Created: April 2023
# Latest Version: 2023-05-01
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

'''
This script produces a txt-file with the following informations for all eaf-files in the relative path "../input_files/" to this script:

i) All instances of all word segments which are time-aligned to a bad morph structure.
ii) The frequency of those instances described in i).
iii) The actual morphological structure of those instances described in i).
iv) A list of all those instances described in i) per file with their respective starting and end time.
'''

from corflow import fromElan
import glob
from collections import Counter
import datetime

path = "../../input_files/"
eaf_files = glob.glob(path+"/*.eaf")



words_with_bad_morph_struc = {}

words_with_bad_morph_struc["one prefix"] = []
words_with_bad_morph_struc["one suffix"] = []
words_with_bad_morph_struc["else (single one)"] = []

words_with_bad_morph_struc["multiple suffixes"] = []
words_with_bad_morph_struc["multiple prefixes"] = []
words_with_bad_morph_struc["multiple prefixes and suffixes"] = []
words_with_bad_morph_struc["else (multiple ones)"] = []

words_with_bad_morph_struc["prefix after stem"] = []
words_with_bad_morph_struc["suffix before stem"] = []
words_with_bad_morph_struc["stem after stem"] = []
words_with_bad_morph_struc["suffix-prefix"] = []
words_with_bad_morph_struc["prefix-suffix_before_stem"] = []



bad_morph_struc = {}

bad_morph_struc["one prefix"] = []
bad_morph_struc["one suffix"] = []
bad_morph_struc["else (single one)"] = []

bad_morph_struc["multiple suffixes"] = []
bad_morph_struc["multiple prefixes"] = []
bad_morph_struc["multiple prefixes and suffixes"] = []
bad_morph_struc["else (multiple ones)"] = []

bad_morph_struc["prefix after stem"] = []
bad_morph_struc["suffix before stem"] = []
bad_morph_struc["stem after stem"] = []
bad_morph_struc["suffix-prefix"] = []
bad_morph_struc["prefix-suffix_before_stem"] = []



count_observed_files = 0
count_total_files = 0
count_observed_speakers = 0

printing_instances_per_file = []

for file in eaf_files:
    print(file)
    count_total_files += 1
    file_name = file.replace(path,"")
    trans = fromElan.fromElan(file,encoding="utf-8")
    word_tier_exists = False
    morph_type_tier_exists = False
    morph_tier_exists = False
    new_file = True
    for tier in trans:
        if "word-txt-qaa" in tier.name:
            word_tier = trans.getName(tier.name)
            word_tier_exists = True
            word_tier_prefix = word_tier.name.partition("_")[0]
        elif "morph-type" in tier.name:
            morph_type_tier = trans.getName(tier.name)
            morph_type_tier_exists = True
        elif "morph-gls-en" in tier.name:
            morph_tier = trans.getName(tier.name)
            morph_tier_exists = True
        if word_tier_exists & morph_type_tier_exists & morph_tier_exists:
            if (morph_tier.name.partition("_")[0] == word_tier_prefix) & (morph_type_tier.name.partition("_")[0] == word_tier_prefix):
                print(word_tier.name)
                print(morph_tier.name)
                print(morph_type_tier.name)
                print("---------------------------------")
                printing_instances_per_file.append("\n**********\n"+str(file_name)+"\n**********\n")
                morph_type_order_all = []
                morph_type_order_times_all = []
                if new_file:
                    new_file = False
                    count_observed_files += 1
                count_observed_speakers += 1
                word_tier_exists = False
                morph_type_tier_exists = False
                morph_tier_exists = False
                for word_seg in word_tier:
                    morph_type_order = []
                    morph_type_order_times = []
                    for mt_seg in morph_type_tier:
                        if ((mt_seg.start == word_seg.start) | ((mt_seg.start > word_seg.start) & (mt_seg.end < word_seg.end))) | (mt_seg.end == word_seg.end):
                            morph_type_order.append(mt_seg.content)
                            morph_type_order_times.append((mt_seg.start,mt_seg.end))
                    morph_type_order_all.append(morph_type_order)
                    morph_type_order_times_all.append(morph_type_order_times)
                for c,mt_order in enumerate(morph_type_order_all):
                    if not "stem" in mt_order:
                        if len(mt_order) == 1:
                            for mt in mt_order:
                                if mt == "prefix":
                                    words_with_bad_morph_struc["one prefix"].append(word_tier.elem[c].content)

                                    printing_instances_per_file.append("'"+str(word_tier.elem[c].content)+"' with time: "+str(datetime.timedelta(seconds=word_tier.elem[c].start))+" - "+str(datetime.timedelta(seconds=word_tier.elem[c].end))+"\n")

                                    m_segs_no_stem_prefix = []
                                    for m_seg in morph_tier:
                                        if (m_seg.start,m_seg.end) in morph_type_order_times_all[c]:
                                            m_segs_no_stem_prefix.append(m_seg.content)
                                    if not m_segs_no_stem_prefix in bad_morph_struc["one prefix"]:
                                        bad_morph_struc["one prefix"].append(m_segs_no_stem_prefix)
                                elif mt == "suffix":
                                    words_with_bad_morph_struc["one suffix"].append(word_tier.elem[c].content)

                                    printing_instances_per_file.append("'"+str(word_tier.elem[c].content)+"' with time: "+str(datetime.timedelta(seconds=word_tier.elem[c].start))+" - "+str(datetime.timedelta(seconds=word_tier.elem[c].end))+"\n")

                                    m_segs_no_stem_suffix = []
                                    for m_seg in morph_tier:
                                        if (m_seg.start,m_seg.end) in morph_type_order_times_all[c]:
                                            m_segs_no_stem_suffix.append(m_seg.content)
                                    if not m_segs_no_stem_suffix in bad_morph_struc["one suffix"]:
                                        bad_morph_struc["one suffix"].append(m_segs_no_stem_suffix)
                                else:
                                    words_with_bad_morph_struc["else (single one)"].append(word_tier.elem[c].content)

                                    printing_instances_per_file.append("'"+str(word_tier.elem[c].content)+"' with time: "+str(datetime.timedelta(seconds=word_tier.elem[c].start))+" - "+str(datetime.timedelta(seconds=word_tier.elem[c].end))+"\n")

                                    m_segs_no_stem_else_single_one = []
                                    for m_seg in morph_tier:
                                        if (m_seg.start,m_seg.end) in morph_type_order_times_all[c]:
                                            m_segs_no_stem_else_single_one.append(m_seg.content)
                                    if not m_segs_no_stem_else_single_one in bad_morph_struc["else (single one)"]:
                                        bad_morph_struc["else (single one)"].append(m_segs_no_stem_else_single_one)
                        elif len(mt_order) > 1:
                            if all(mt == "prefix" for mt in mt_order):
                                words_with_bad_morph_struc["multiple prefixes"].append(word_tier.elem[c].content)

                                printing_instances_per_file.append("'"+str(word_tier.elem[c].content)+"' with time: "+str(datetime.timedelta(seconds=word_tier.elem[c].start))+" - "+str(datetime.timedelta(seconds=word_tier.elem[c].end))+"\n")

                                m_segs_no_stem_multiple_prefixes = []
                                for m_seg in morph_tier:
                                    if (m_seg.start,m_seg.end) in morph_type_order_times_all[c]:
                                        m_segs_no_stem_multiple_prefixes.append(m_seg.content)
                                    if not m_segs_no_stem_multiple_prefixes in bad_morph_struc["multiple prefixes"]:
                                        bad_morph_struc["multiple prefixes"].append(m_segs_no_stem_multiple_prefixes)
                            elif all(mt == "suffix" for mt in mt_order):
                                words_with_bad_morph_struc["multiple suffixes"].append(word_tier.elem[c].content)

                                printing_instances_per_file.append("'"+str(word_tier.elem[c].content)+"' with time: "+str(datetime.timedelta(seconds=word_tier.elem[c].start))+" - "+str(datetime.timedelta(seconds=word_tier.elem[c].end))+"\n")

                                m_segs_no_stem_multiple_suffixes = []
                                for m_seg in morph_tier:
                                    if (m_seg.start,m_seg.end) in morph_type_order_times_all[c]:
                                        m_segs_no_stem_multiple_suffixes.append(m_seg.content)
                                    if not m_segs_no_stem_multiple_suffixes in bad_morph_struc["multiple suffixes"]:
                                        bad_morph_struc["multiple suffixes"].append(m_segs_no_stem_multiple_suffixes)
                            elif all(((mt == "prefix") | (mt == "suffix")) for mt in mt_order):
                                words_with_bad_morph_struc["multiple prefixes and suffixes"].append(word_tier.elem[c].content)

                                printing_instances_per_file.append("'"+str(word_tier.elem[c].content)+"' with time: "+str(datetime.timedelta(seconds=word_tier.elem[c].start))+" - "+str(datetime.timedelta(seconds=word_tier.elem[c].end))+"\n")

                                m_segs_no_stem_multiple_pref_and_suf = []
                                for m_seg in morph_tier:
                                    if (m_seg.start,m_seg.end) in morph_type_order_times_all[c]:
                                        m_segs_no_stem_multiple_pref_and_suf.append(m_seg.content)
                                if not m_segs_no_stem_multiple_pref_and_suf in bad_morph_struc["multiple prefixes and suffixes"]:
                                    bad_morph_struc["multiple prefixes and suffixes"].append(m_segs_no_stem_multiple_pref_and_suf)
                            else:
                                words_with_bad_morph_struc["else (multiple ones)"].append(word_tier.elem[c].content)

                                printing_instances_per_file.append("'"+str(word_tier.elem[c].content)+"' with time: "+str(datetime.timedelta(seconds=word_tier.elem[c].start))+" - "+str(datetime.timedelta(seconds=word_tier.elem[c].end))+"\n")

                                m_segs_no_stem_multiple_else = []
                                for m_seg in morph_tier:
                                    if (m_seg.start,m_seg.end) in morph_type_order_times_all[c]:
                                        m_segs_no_stem_multiple_else.append(m_seg.content)
                                if not m_segs_no_stem_multiple_else in bad_morph_struc["else (multiple ones)"]:
                                    bad_morph_struc["else (multiple ones)"].append(m_segs_no_stem_multiple_else)
                    elif ("stem" in mt_order) & (len(mt_order) >= 2):
                        for c2,mt in enumerate(mt_order):
                            if (mt == "stem") & (c2+1 < len(mt_order)):
                                if mt_order[c2+1] == "prefix":
                                    words_with_bad_morph_struc["prefix after stem"].append(word_tier.elem[c].content)

                                    printing_instances_per_file.append("'"+str(word_tier.elem[c].content)+"' with time: "+str(datetime.timedelta(seconds=word_tier.elem[c].start))+" - "+str(datetime.timedelta(seconds=word_tier.elem[c].end))+"\n")
                                    
                                    m_segs_prefix_after_stem = []
                                    for m_seg in morph_tier:
                                        if (m_seg.start,m_seg.end) in morph_type_order_times_all[c]:
                                            m_segs_prefix_after_stem.append(m_seg.content)
                                    if not m_segs_prefix_after_stem in bad_morph_struc["prefix after stem"]:
                                        bad_morph_struc["prefix after stem"].append(m_segs_prefix_after_stem)
                                elif mt_order[c2+1] == "stem":
                                    words_with_bad_morph_struc["stem after stem"].append(word_tier.elem[c].content)

                                    printing_instances_per_file.append("'"+str(word_tier.elem[c].content)+"' with time: "+str(datetime.timedelta(seconds=word_tier.elem[c].start))+" - "+str(datetime.timedelta(seconds=word_tier.elem[c].end))+"\n")
                                    
                                    m_segs_stem_after_stem = []
                                    for m_seg in morph_tier:
                                        if (m_seg.start,m_seg.end) in morph_type_order_times_all[c]:
                                            m_segs_stem_after_stem.append(m_seg.content)
                                    if not m_segs_stem_after_stem in bad_morph_struc["stem after stem"]:
                                        bad_morph_struc["stem after stem"].append(m_segs_stem_after_stem)
                            elif (mt == "suffix") & (c2+1 < len(mt_order)):
                                if mt_order[c2+1] == "stem":
                                    words_with_bad_morph_struc["suffix before stem"].append(word_tier.elem[c].content)

                                    printing_instances_per_file.append("'"+str(word_tier.elem[c].content)+"' with time: "+str(datetime.timedelta(seconds=word_tier.elem[c].start))+" - "+str(datetime.timedelta(seconds=word_tier.elem[c].end))+"\n")
                                    
                                    m_segs_suffix_before_stem = []
                                    for m_seg in morph_tier:
                                        if (m_seg.start,m_seg.end) in morph_type_order_times_all[c]:
                                            m_segs_suffix_before_stem.append(m_seg.content)
                                    if not m_segs_suffix_before_stem in bad_morph_struc["suffix before stem"]:
                                        bad_morph_struc["suffix before stem"].append(m_segs_suffix_before_stem)
                                elif mt_order[c2+1] == "prefix":
                                    words_with_bad_morph_struc["suffix-prefix"].append(word_tier.elem[c].content)

                                    printing_instances_per_file.append("'"+str(word_tier.elem[c].content)+"' with time: "+str(datetime.timedelta(seconds=word_tier.elem[c].start))+" - "+str(datetime.timedelta(seconds=word_tier.elem[c].end))+"\n")
                                    
                                    m_segs_suffix_prefix = []
                                    for m_seg in morph_tier:
                                        if (m_seg.start,m_seg.end) in morph_type_order_times_all[c]:
                                            m_segs_suffix_prefix.append(m_seg.content)
                                    if not m_segs_suffix_prefix in bad_morph_struc["suffix-prefix"]:
                                        bad_morph_struc["suffix-prefix"].append(m_segs_suffix_prefix)
                            elif (mt == "prefix") & (c2+2 < len(mt_order)):
                                if mt_order[c2+1] == "suffix":
                                    if any((mt2 == "stem") & (mt_order.index(mt2) > c2+1) for mt2 in mt_order):
                                        words_with_bad_morph_struc["prefix-suffix_before_stem"].append(word_tier.elem[c].content)

                                    printing_instances_per_file.append("'"+str(word_tier.elem[c].content)+"' with time: "+str(datetime.timedelta(seconds=word_tier.elem[c].start))+" - "+str(datetime.timedelta(seconds=word_tier.elem[c].end))+"\n")
                                    
                                    m_segs_prefix_suffix_before_stem = []
                                    for m_seg in morph_tier:
                                        if (m_seg.start,m_seg.end) in morph_type_order_times_all[c]:
                                            m_segs_prefix_suffix_before_stem.append(m_seg.content)
                                    if not m_segs_prefix_suffix_before_stem in bad_morph_struc["prefix-suffix_before_stem"]:
                                        bad_morph_struc["prefix-suffix_before_stem"].append(m_segs_prefix_suffix_before_stem)

with open("report_bad_morph_structure.txt", "w") as report:
    report.write("######################################\n#BAD MORPHOLOGICAL STRUCTURE REPORT#\n######################################\n\n")
    report.write(str(count_observed_speakers)+" speakers in "+str(count_observed_files)+" from "+str(count_total_files)+" files were observed.\n"+str(len(words_with_bad_morph_struc["one prefix"])+len(words_with_bad_morph_struc["one suffix"])+len(words_with_bad_morph_struc["multiple suffixes"])+len(words_with_bad_morph_struc["multiple prefixes"])+len(words_with_bad_morph_struc["multiple prefixes and suffixes"])+len(words_with_bad_morph_struc["prefix after stem"])+len(words_with_bad_morph_struc["suffix before stem"])+len(words_with_bad_morph_struc["stem after stem"])+len(words_with_bad_morph_struc["suffix-prefix"])+len(words_with_bad_morph_struc["prefix-suffix_before_stem"])+len(words_with_bad_morph_struc["else (single one)"])+len(words_with_bad_morph_struc["else (multiple ones)"]))+" cases with bad morphological structure were found.\n\n")
    report.write("##########\nHow often do words with a bad morphological structure occur?\n##########\n\n")
    report.write("---\nFrequency across all files:\n---\n\n")
    for entry in words_with_bad_morph_struc:
        report.write(str(entry)+": ")
        report.write(str(Counter(words_with_bad_morph_struc[entry])))
        report.write("\n\n")
    report.write("---\nHow does the actual bad morphological structure of a word look like?\n---\n\n")
    for entry in bad_morph_struc:
        report.write(str(entry)+":\n")
        for c3, subentry in enumerate(bad_morph_struc[entry]):
            report.write(str(bad_morph_struc[entry][c3]))
            report.write("\n")
        report.write("\n")
    report.write("---\nCases per file:\n---\n\n")
    for entry in printing_instances_per_file:
        report.write(entry)

