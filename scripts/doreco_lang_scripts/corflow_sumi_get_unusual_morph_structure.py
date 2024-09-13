# Created: 2023-08-08
# Latest Version: 2023-09-19
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

from corflow import fromElan
import glob
import re
from collections import Counter

input_path = "../../input_files/"

eaf_files = glob.glob(input_path+"/*.eaf")
find_word_tier = "Words-txt-nsm"

#Creating a dictionary with keys to organize the soon to be found cases of unusual morphological structures of words.
unus_morph_struc = {}
unusual_morph_structure_entries = ["no_stem_clitics_ordered","no_stem_clitics_orderless","no_stem_affixes_ordered","no_stem_affixes_orderless","no_stem_mixed_ordered","no_stem_mixed_orderless","no_stem_other","two_stems",]
for key in unusual_morph_structure_entries:
    unus_morph_struc[key] = {}

#having a separate dict for collecting all morphs, which appear within an unusual morph scturcture and their gloss tokens. This way, it is possible a) to count the total amount of tokens of a morph appearing in an unusual structure (having a measure of importance) and b) to be sure that only certain morph-gloss-pairs appear in unusual structures, while others do not.
unus_struc_mbs_gls = {}

#Starting times of all word segs with unusual morph structure.
unus_word_segs_time = []

words_with_gaps = []
word_with_unus_struc = []

def find_tiers(transcription,string):
    '''Returns a list with all tiers in the transcription that match the given regex string pattern.'''
    found_tiers = []
    for tier in transcription:
        if re.search(string,tier.name):
            found_tiers.append(tier)
    return found_tiers

#Going through each file and...
for file in eaf_files:
    file_name = file.replace(input_path,"")
    print(f"File {file_name}")
    trans = fromElan.fromElan(file,encoding="utf-8")
    #...its respective word tiers.
    for word_tier in (find_tiers(trans,find_word_tier)):
        print(f"Found word tier {word_tier.name}")
        for word_seg in word_tier:
            add_mbs_gls = False
            word_seg_c = word_seg.content.replace(",","").replace(".","")
            #All morph segment contents of a word segment.
            mb_segs_cont = [child_seg.content for child_seg in word_seg.children() if child_seg.struct == word_tier.children()[1]]
            mb_segs = [child_seg for child_seg in word_seg.children() if child_seg.struct == word_tier.children()[1]]
            if len(mb_segs_cont) > 0:
                #Words with more than one stem.
                if (len(mb_segs_cont) > 1) & (all(not (mb_seg_c.startswith(("-","="))) and (not mb_seg_c.endswith(("-","="))) for mb_seg_c in mb_segs_cont)):
                    if not word_seg_c in unus_morph_struc["two_stems"].keys():
                        unus_morph_struc["two_stems"][word_seg_c] = []
                    if not mb_segs_cont in unus_morph_struc["two_stems"][word_seg_c]:
                        unus_morph_struc["two_stems"][word_seg_c].append(mb_segs_cont)
                    unus_word_segs_time.append((word_seg.start,word_seg.end))
                    add_mbs_gls = True

                #Words with only clitics, which are in order (either only proclitics or enclitics).
                elif all(re.search("^=",mb_seg_c) for mb_seg_c in mb_segs_cont) or all(re.search("=$",mb_seg_c) for mb_seg_c in mb_segs_cont):
                    if not word_seg_c in unus_morph_struc["no_stem_clitics_ordered"].keys():
                        unus_morph_struc["no_stem_clitics_ordered"][word_seg_c] = []
                    if not mb_segs_cont in unus_morph_struc["no_stem_clitics_ordered"][word_seg_c]:
                        unus_morph_struc["no_stem_clitics_ordered"][word_seg_c].append(mb_segs_cont)
                    unus_word_segs_time.append((word_seg.start,word_seg.end))
                    add_mbs_gls = True

                #Words with only clitics, which are not in order (proclitics and enclitics mixed).
                elif all(re.search("^=|=$",mb_seg_c) for mb_seg_c in mb_segs_cont):
                    if not word_seg_c in unus_morph_struc["no_stem_clitics_orderless"].keys():
                        unus_morph_struc["no_stem_clitics_orderless"][word_seg_c] = []
                    if not mb_segs_cont in unus_morph_struc["no_stem_clitics_orderless"][word_seg_c]:
                        unus_morph_struc["no_stem_clitics_orderless"][word_seg_c].append(mb_segs_cont)
                    unus_word_segs_time.append((word_seg.start,word_seg.end))
                    add_mbs_gls = True

                #Words with only affixes, which are in order (either only prefixes or suffixes).
                elif all(re.search("^-",mb_seg_c) for mb_seg_c in mb_segs_cont) or all(re.search("-$",mb_seg_c) for mb_seg_c in mb_segs_cont):
                    if not word_seg_c in unus_morph_struc["no_stem_affixes_ordered"].keys():
                        unus_morph_struc["no_stem_affixes_ordered"][word_seg_c] = []
                    if not mb_segs_cont in unus_morph_struc["no_stem_affixes_ordered"][word_seg_c]:
                        unus_morph_struc["no_stem_affixes_ordered"][word_seg_c].append(mb_segs_cont)
                    unus_word_segs_time.append((word_seg.start,word_seg.end))
                    add_mbs_gls = True

                #Words with only affixes, which are not in order (prefixes and suffixes mixed).
                elif all(re.search("^-|-$",mb_seg_c) for mb_seg_c in mb_segs_cont):
                    if not word_seg_c in unus_morph_struc["no_stem_affixes_orderless"].keys():
                        unus_morph_struc["no_stem_affixes_orderless"][word_seg_c] = []
                    if not mb_segs_cont in unus_morph_struc["no_stem_affixes_orderless"][word_seg_c]:
                        unus_morph_struc["no_stem_affixes_orderless"][word_seg_c].append(mb_segs_cont)
                    unus_word_segs_time.append((word_seg.start,word_seg.end))
                    add_mbs_gls = True

                #Words with only clitics and affixes, which are in order (either only prefixes and proclitics or suffixes and enclitics).
                elif all(re.search("^[=-]",mb_seg_c) for mb_seg_c in mb_segs_cont) or all(re.search("[=-]$",mb_seg_c) for mb_seg_c in mb_segs_cont):
                    if not word_seg_c in unus_morph_struc["no_stem_mixed_ordered"].keys():
                        unus_morph_struc["no_stem_mixed_ordered"][word_seg_c] = []
                    if not mb_segs_cont in unus_morph_struc["no_stem_mixed_ordered"][word_seg_c]:
                        unus_morph_struc["no_stem_mixed_ordered"][word_seg_c].append(mb_segs_cont)
                    unus_word_segs_time.append((word_seg.start,word_seg.end))
                    add_mbs_gls = True

                #Words with only clitics and affixes in any order and combination.
                elif all(re.search("^[=-]|[=-]$",mb_seg_c) for mb_seg_c in mb_segs_cont):
                    if not word_seg_c in unus_morph_struc["no_stem_mixed_orderless"].keys():
                        unus_morph_struc["no_stem_mixed_orderless"][word_seg_c] = []
                    if not mb_segs_cont in unus_morph_struc["no_stem_mixed_orderless"][word_seg_c]:
                        unus_morph_struc["no_stem_mixed_orderless"][word_seg_c].append(mb_segs_cont)
                    unus_word_segs_time.append((word_seg.start,word_seg.end))
                    add_mbs_gls = True

            elif len(mb_segs_cont) == 0:
                words_with_gaps.append(word_seg_c)
                #print(f"Gap for word {word_seg.content}")

            if add_mbs_gls:
                for index,mb_seg_c in enumerate(mb_segs_cont):
                    if not mb_seg_c in unus_struc_mbs_gls.keys():
                        unus_struc_mbs_gls[mb_seg_c] = []
                    if mb_segs[index].children():
                        gl_seg_c = mb_segs[index].children()[0].content
                    unus_struc_mbs_gls[mb_seg_c].append(gl_seg_c)
                word_with_unus_struc.append(word_seg_c)

#Structure of the dicitonary: {<category>: {<word segment content>: [morph segment content, morph segment content, ...]}}
for key,val_dict in unus_morph_struc.items():
    print("\n#######################\n",key,"\n#######################\n",sep="")
    for key2,val2 in val_dict.items():
        print(f"{key2}: {val2}")

#New dictionary to a) get the frequency of the most occuring types of morph segments in unsual morph structures and b) sort them.
unus_morph_struc_freq = {}

print("\n\n\n--------------------------------")
for key_cat in unus_morph_struc.keys():
    unus_morph_struc_freq[key_cat] = []
    for key_word,val_list_list in unus_morph_struc[key_cat].items():
        for val_list in val_list_list:
            for val in val_list:
                unus_morph_struc_freq[key_cat].append(val)

#New dicts for collecting every gloss of every morph in an unusual morph structure.
unus_morph_struc_gl = {}

print("\n\nNext\n\n")
sort_mb_seg_and_freq = []
for key,val in unus_morph_struc_freq.items():
    for key_count,val_count in Counter(val).items():
        sort_mb_seg_and_freq.append((val_count,key_count))

sort_mb_seg_and_freq.sort(reverse=True)
for mb_freq,mb_seg in sort_mb_seg_and_freq:
    unus_morph_struc_gl[f"{mb_seg}_{mb_freq}"] = []

for file in eaf_files:
    trans = fromElan.fromElan(file,encoding="utf-8")
    for morph_tier in find_tiers(trans,"morph-txt-nsm-cp"):
        for mb_seg in morph_tier:
            for key_mb in unus_morph_struc_gl.keys():
                if key_mb.partition("_")[0] == mb_seg.content:
                    if mb_seg.children():
                        unus_morph_struc_gl[key_mb].append(mb_seg.children()[0].content)

print("\n\nType Frequency: Glosses of morph segments in unusual morph structures:\n\n")
for key,val in unus_morph_struc_gl.items():
    print(f"{key}: {Counter(val)}")

print(f"\n\nWords with gaps:\n\n")
print(Counter(words_with_gaps))

print(f"\n\nToken Frequency: Morphs, which appeared in an unusual structure, and their specific glosses, with which they appeared.\n\n")

sort_mb_seg_gl_token_freq = []
for mb_seg,gl_segs_list in unus_struc_mbs_gls.items():
    count_gl_segs = 0
    for gl_seg in gl_segs_list:
        count_gl_segs += 1
    sort_mb_seg_gl_token_freq.append((count_gl_segs,mb_seg))
sort_mb_seg_gl_token_freq.sort(reverse=True)

unus_struc_mbs_gls_sorted = {}
for count,mb_seg in sort_mb_seg_gl_token_freq:
    unus_struc_mbs_gls_sorted[f"{mb_seg}_{count}"] = unus_struc_mbs_gls[mb_seg]

for mb_seg,gl_segs in unus_struc_mbs_gls_sorted.items():
    print(f"{mb_seg}: {Counter(gl_segs)}")

print(f"\n\nFrequency of word seg tokens appearing within unusual structures:\n\n")
print(Counter(word_with_unus_struc))