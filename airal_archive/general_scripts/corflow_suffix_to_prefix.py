#Created: 2024-03-10
#Latest Version: 2024-03-10
#Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
#Corflow module created by François Delafontaine

from corflow import fromElan, toElan
import glob
import sys
sys.path.append("../")
from corflow_additional_functions import find_tiers
import re

input_path = "../../input_files/"
output_path = "../../output_files/"
eaf_files = glob.glob(input_path+"/*.eaf")
for file in eaf_files:
    trans = fromElan.fromElan(file,encoding="utf-8")
    gl_tier = trans.findName("gloss_mtok")
    print(f"gloss mtok tier: {gl_tier.name}")
    gram_tier = trans.findName("grammatical_words_mtok")
    print(f"gram mtok tier: {gram_tier.name}")
    for seg in gl_tier:
        if re.search("0.+",seg.content):
            for seg2 in [s for s in gl_tier if s.index() > seg.index()]:
                if not seg2.content.startswith("-"):
                    break
                seg2.content = seg2.content[1:] + "-"
                gram_seg = gram_tier.getTime(seg2.start)
                gram_seg.content = gram_seg.content[1:] + "-"
    toElan.toElan(output_path+trans.name+".eaf",trans)