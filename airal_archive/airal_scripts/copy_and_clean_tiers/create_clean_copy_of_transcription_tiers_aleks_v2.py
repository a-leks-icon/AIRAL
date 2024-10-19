from corflow import fromElan,toElan
import re

#Path to .eaf-file.
eaf = "RG_16_fixed.eaf"
# Pattern for detecting bracketed content
bracket_pattern = r"\(.*?\)|\[.*?\]|\{.*?\}"
# Pattern for detecting ampersand-comments
ampersand_pattern = r'&\S+(?=\s|$)'# r"\&.+[\s]"
# Common tags to be deleted
tags = ["&", "@s:eng", "@e", "@c", "@wp", "@l", '+"', "xxx", "<", ">"]
#Create a transcription object.
trans = fromElan.fromElan(eaf,encoding="utf-8")
#Iterate through every tier.
for ind in range(len(trans)):
    tier = trans.elem[ind]
    #Add a copy of the tier to the transcription as a
    #child tier of the original tier.
    new_tier = trans.add(len(trans),tier,tier)
    #Change the names of the old and new tier.
    new_tier.name += "_clean"
    tier.name += "_original"
    #Remove substrings in the content of the segments
    #of the new tier based on a regex pattern.
    for seg in new_tier:
        #seg.content = re.sub(pattern,"",seg.content)
        seg.content = re.sub(bracket_pattern, "", seg.content)
        seg.content = re.sub(ampersand_pattern, "", seg.content)
        for i in range(len(tags)):
            seg.content = seg.content.replace(tags[i], "").replace("_", " ")
#Consistently define names of segments after
#having added new segments and tiers.
incr = 0
for tier in trans:
    incr = tier.renameSegs("a",incr)
#Define the parents of the segments of the
#new child tiers to the time-aligned segments
#on the original tiers. Otherwise, those segments
#have no parent segments.
for tier in trans:
    if "clean" in tier.name:
        prefix = tier.name.partition("_")[0]
        parent_tier_name = prefix + "_original"
        for seg in tier:
            seg.setParent(trans.findName(parent_tier_name).getTime(seg.start))
#Save transcription to new .eaf-file.
name = eaf.partition(".eaf")
toElan.toElan(name[0]+"_cleaned_hierarchy"+name[1], trans)