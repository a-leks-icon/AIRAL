#Created: 2024-01-04
#Latest Version: 2024-01-05
#Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
#Corflow module created by François Delafontaine

from corflow import fromElan,toElan
import glob
import re
import sys
sys.path.append("../")
from corflow_additional_functions import find_tiers
import unicodedata as uc

'''Notes for me after applying certain search patterns:

* Two stem words are common as well as two stem words with one or even more than one suffixes/enclitics. I assume therefore, that similar structures but with prefixes/proclitics instead are well-formed as well.

* Three stem words are sommon too.

All the other ones have to be checked. This script gives them as output.

'''

#ACTUAL OPERATIONS BEGIN HERE#
input_path = "../../input_files/"
output_path = "../../output_files/"
eaf_files = glob.glob(input_path+"/*.eaf")

all_cases = []
for file in eaf_files:
    file_name = file.replace(input_path,"")
    print(f"\n**********\nFile: {file_name}\n**********\n")
    trans = fromElan.fromElan(file,encoding="utf-8")

    for wd_tier in find_tiers(trans,"Words-txt-nsm"):
        if not "legacy" in wd_tier.name:
            print(f"#####\nword tier: {wd_tier.name}")
            for tier in wd_tier.children():
                if "morph-txt-nsm-cp" in tier.name:
                    m_tier = tier
                elif "word-pos-en-cp" in tier.name:
                    pos_tier = tier
            if m_tier == None:
                continue
            print(f"morph tier: {m_tier.name}")
            print(f"pos tier: {pos_tier.name}\n#####")
            for wd_seg in wd_tier:
                if not m_tier in wd_seg.childDict().keys():
                    continue
                msegs = wd_seg.childDict()[m_tier]
                if msegs:
                    glsegs = []
                    for mseg in msegs:
                        if mseg.children():
                            glsegs.append(mseg.children()[0].content)
                        else:
                            glsegs.append("NONE")
                    if len(msegs) > 2:
                        #For some unknown reason, I had to negate the regex '(^[-=])|([-=]$)' instead of using the regex '^[^-=].*[^-=]$' when trying to search for stems (it worked for most cases, but some cases were excluded).
                        if all(not re.search("(^[-=])|([-=]$)",mseg.content) for mseg in msegs):
                            continue
                        elif (not re.search("(^[-=])|([-=]$)",msegs[0].content)) & ((not re.search("(^[-=])|([-=]$)",msegs[-1].content))):
                            print(f"2 stems -- at least one affix/enlcitic in the middle: {[m.content for m in msegs]} at time: {wd_seg.start}\n{glsegs}")
                            all_cases.append(([m.content for m in msegs],glsegs,wd_seg.start,file_name,wd_tier.name))
                    if len(msegs) >= 4:
                        if re.search("(^[-=])|([-=]$)",msegs[0].content):
                            if re.search("(^[-=])|([-=]$)",msegs[-1].content):
                                if all(not re.search("(^[-=])|([-=]$)",mseg.content) for mseg in msegs[1:-1]):
                                    print(f"2 stems -- left/right affix/enclitic: {[m.content for m in msegs]}\n{glsegs}")
                                    all_cases.append(([m.content for m in msegs],glsegs,wd_seg.start,file_name,wd_tier.name))
                        mixed = []
                        mixed_gl = []
                        added = []
                        for ind,mseg in enumerate(msegs):
                            if (ind+4) <= len(msegs):
                                if re.search("(^[-=])|([-=]$)",msegs[ind].content):
                                    if not re.search("(^[-=])|([-=]$)",msegs[ind+1].content):
                                        if re.search("(^[-=])|([-=]$)",msegs[ind+2].content):
                                            if not re.search("(^[-=])|([-=]$)",msegs[ind+3].content):
                                                if not wd_seg in added:
                                                    mixed.append([m.content for m in msegs])
                                                    mixed_gl.append(glsegs)
                                                    all_cases.append(([m.content for m in msegs],glsegs,wd_seg.start,file_name,wd_tier.name))
                                                    added.append(wd_seg)
                                elif re.search("(^[-=])|([-=]$)",msegs[ind+1].content):
                                    if not re.search("(^[-=])|([-=]$)$",msegs[ind+2].content):
                                        if re.search("(^[-=])|([-=]$)",msegs[ind+3].content):
                                            if not wd_seg in added:
                                                mixed.append([m.content for m in msegs])
                                                mixed_gl.append(glsegs)
                                                all_cases.append(([m.content for m in msegs],glsegs,wd_seg.start,file_name,wd_tier.name))
                                                added.append(wd_seg)
                        if mixed:
                            print(f"Mixed structure: {mixed} at time: {wd_seg.start}")
                            print(f"Their glosses: {mixed_gl}")
print("\n\n\n")

for m,gl,time,file,tier in all_cases:
    print(m)
    print(gl)
    print(time,file,tier)
    print("\n")