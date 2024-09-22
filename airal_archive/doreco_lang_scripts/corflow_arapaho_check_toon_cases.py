# Created: 2023-06-08
# Latest Version: 2023-06-08
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

from corflow import fromElan,toElan
import glob

input_path = "../../input_files/"
eaf_files = glob.glob(input_path+"/*.eaf")

count = 0

for file in eaf_files:
    file_name = file.replace(input_path,"")
    trans = fromElan.fromElan(file,encoding="utf-8")
    
    mb_tier_exists = False
    ps_tier_exists = False
    tx_tier_exists = False
    ge_tier_exists = False

    for tier in trans:
        if "tx@" in tier.name:
            tx_tier = trans.getName(tier.name)
            tx_tier_exists = True
        elif "mb@" in tier.name:
            mb_tier = trans.getName(tier.name)
            mb_tier_exists = True
        elif "ps@" in tier.name:
            ps_tier = trans.getName(tier.name)
            ps_tier_exists = True
        elif "ge@" in tier.name:
            ge_tier = trans.getName(tier.name)
            ge_tier_exists = True
        if ge_tier_exists & mb_tier_exists & ps_tier_exists:
            mb_tier_exists = False
            tx_tier_exists = False
            ps_tier_exists = False
            ge_tier_exists = False

            '''
            #Printing the content of every segment on the tx-tier, if it is time-aligned (in a broader sense) with an mb-segment, whose content equals 'toon-'.
            for mb_seg in mb_tier:
                if mb_seg.content == "toon-":
                    for tx_seg in tx_tier:
                        if (tx_seg.start == mb_seg.start) | (tx_seg.end == mb_seg.end) | ((tx_seg.start < mb_seg.start) & (tx_seg.end > mb_seg.end)):
                            print(tx_seg.content)
            '''

            #Printing every pair of ge-segment and ps-segment for every instance, which is time-algined with an mb-segment, whose content equals 'toon-'.
            for mb_seg in mb_tier:
                if mb_seg.content == "toon-":
                    for ge_seg in ge_tier:
                        if (ge_seg.start == mb_seg.start) & (ge_seg.end == mb_seg.end):
                            for ps_seg in ps_tier:
                                if (ps_seg.start == mb_seg.start) & (ps_seg.end == mb_seg.end):
                                    print(f"GE-SEG: {ge_seg.content} & PS-SEG: {ps_seg.content}")

