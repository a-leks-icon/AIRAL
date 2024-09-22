#Created: 2024-01-28
#Latest Version: 2024-01-28
#Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
#Corflow module created by Francois Delafontaine

from corflow import fromElan,toElan
import glob
import sys
sys.path.append("../")
from corflow_additional_functions import find_tiers,fix_affixes_clitics
from collections import Counter

#ACTUAL OPERATIONS BEGIN HERE#
input_path = "../../input_files/"
output_path = "../../output_files/"
eaf_files = glob.glob(input_path+"/*.eaf")



'''
for file in eaf_files:
    file_name = file.replace(input_path,"")
    print(f"\n/////////\nfile name: {file_name}\n//////////\n")
    trans = fromElan.fromElan(file,encoding="utf-8")
    for tier in find_tiers(trans,"((tx)|(ref)|(mb)|(ge)|(ps))@unknown"):
        print(f"tier to be processed: {tier.name}")
        if "mb@unknown" == tier.name:
            for ch_tier in tier.children():
                fix_affixes_clitics(tier,ch_tier,False,"\*{3,}")
        for seg in tier:
            seg.content = seg.content.strip()
            if seg.content == "***":
                seg.content = "****"
            elif seg.content.startswith("*"):
                seg.content = seg.content.removeprefix("*")
    toElan.toElan(output_path+file_name,trans)
'''

#eaf_files = glob.glob(output_path+"/*.eaf")

daakie_data = {}
for file in eaf_files:
    #file_name = file.replace(output_path,"")
    file_name = file.replace(input_path,"")
    print(f"\n/////////\nfile name: {file_name}\n//////////\n")
    ctrans = fromElan.fromElan(file,encoding="utf-8")
    for mtier in ctrans:
        if "mb@unknown" == mtier.name:
            gltier = None
            postier = False
            for ch_tier in mtier.children():
                if "ge@unknown" == ch_tier.name:
                    gltier = ch_tier
                elif "ps@unknown" == ch_tier.name:
                    postier = ch_tier
            for mseg in mtier:
                if not mseg.content in daakie_data:
                    daakie_data[mseg.content] = ([],[])
                if mseg.children():
                    for ch_seg in mseg.children():
                        if ch_seg.struct == gltier:
                            daakie_data[mseg.content][0].append(ch_seg.content)
                        elif ch_seg.struct == postier:
                            daakie_data[mseg.content][-1].append(ch_seg.content)

for key,val in daakie_data.items():
    daakie_data[key] = (Counter(val[0]),Counter(val[1]))

#Getting an idea of the data. Creating a txt file.
with open(output_path+"daakie_grammar.txt", "w") as txtfile:
    for key,val in daakie_data.items():
        txtfile.write(key+":\n")
        txtfile.write("Gloss segs: "+str(Counter(val[0]))+"\n")
        txtfile.write("POS segs: "+str(Counter(val[1]))+"\n")
        txtfile.write("####################\n")
    txtfile.write("\n------------------------------\nAll Morphs:\n"+str(daakie_data.keys()))