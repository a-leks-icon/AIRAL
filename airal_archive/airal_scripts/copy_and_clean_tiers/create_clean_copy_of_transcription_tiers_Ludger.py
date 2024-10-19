from corflow import fromElan,toElan
from general_functions import get_segs
import re

def copy_tier(transcription,tier,new_tier_name,parent_tier,char_num=1):
    '''Copies an existing *tier* and adds it to a *transcription* with its *new_tier_name* and newly assigned *parent_tier*. All segments of the newly added tier get renamed based on their first characters letter and the number *char_num* given. By default, this number euqals 1 meaning that if e.g. the first character in a segments name is 'a', it gets substituted by 'b'. If char_num equals 2 and the first character is again 'a', it gets substituted by the character 'c', and so on. Returns the newly added tier.'''
    transcription.add(-1,tier)
    new_tier = transcription.elem[-1]
    new_tier.name = new_tier_name
    for seg in new_tier:
        seg.name = chr(ord(seg.name[0])+char_num) + seg.name[1:]
    new_tier.setParent(parent_tier)
    if parent_tier != None:
        for seg in new_tier:
            seg.setParent(parent_tier.getTime(seg.start))
    return new_tier

#Path to .eaf-file.
eaf = "RG_16.eaf"
# Pattern for detecting bracketed content
bracket_pattern = r"\(.*?\)|\[.*?\]|\{.*?\}"
# Pattern for detecting ampersand-comments
ampersand_pattern = r'&\S+(?=\s|$)'# r"\&.+[\s]"
# Common tags to be deleted
tags = ["&", "@s:eng", "@e", "@c", "@wp", "@l", '+"', "xxx", "<", ">"]
#Create a transcription object.
trans = fromElan.fromElan(eaf,encoding="utf-8")
#Get segments based on a specific regex pattern.
tier_segs = get_segs(trans, ".*", [".*", ampersand_pattern],[".*",bracket_pattern], mode="or",log=True) # log=True is optional, use for logging
#Iterate through every tier and collected segments.
for tier,segs in tier_segs.items():
    #Copy the original tier and save it.
    copy_tier(trans,tier,tier.name+"_original",None)
    #Change the original tier's name.
    tier.name += "_clean"
    #Replace substrings
    for seg in segs:
        seg.content = re.sub(bracket_pattern, "", seg.content)
        seg.content = re.sub(ampersand_pattern, "", seg.content)
        for i in range(len(tags)):
            seg.content = seg.content.replace(tags[i], "").replace("_", " ")
#Save transcription to new .eaf-file.
toElan.toElan("test_lp.eaf", trans)
