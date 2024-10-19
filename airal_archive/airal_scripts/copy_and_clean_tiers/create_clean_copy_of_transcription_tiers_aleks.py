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
    #Get tier.
    tier = trans.elem[ind]
    #Add a copy of the tier to the transcription.
    new_tier = trans.add(len(trans),tier)
    #Change the names of the old and new tier.
    new_tier.name += "_clean"
    tier.name += "_original"
    #Remove substrings in the content of the segments
    #of the new tier based on regex patterns.
    for seg in new_tier:
        seg.content = re.sub(bracket_pattern, "", seg.content)
        seg.content = re.sub(ampersand_pattern, "", seg.content)
        for i in range(len(tags)):
            seg.content = seg.content.replace(tags[i], "").replace("_", " ")
#Consistently define names of segments after
#having added new segments and tiers.
incr = 0
for tier in trans:
    incr = tier.renameSegs("a",incr)
#Since the new tiers are root tiers without parents,
#there is no need to define parent-child relations
#for their segments.
#Save transcription to new .eaf-file.
name = eaf.partition(".eaf")
toElan.toElan(name[0]+"_cleaned"+name[1], trans)