#Created: 2024-02-29
#Latest Version: 2024-02-29
#Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
#Corflow module created by François Delafontaine

from corflow import fromElan, toElan
import glob

input_path = "../../input_files/"
output_path = "../../output_files/"
eaf_files = glob.glob(input_path+"/*.eaf")
for file in eaf_files:
    file_name = file.replace(input_path,"")
    print(file_name+"\n#####")
    trans = fromElan.fromElan(file,encoding="utf-8")
    bad_times = False
    for tier in trans:
        print(f"Tier: {tier.name}\n#####\n")
        for seg in tier:
            if (seg.start == -1) | (seg.end == -1) | ((seg.start == 0) & (seg.end == 0)):
                #print(f"content: {seg.content} | index: {seg.index()} | times: {seg.start,seg.end}")
                print(f"tier {tier.name} has -1-1 segments: content: {seg.content} | index: {seg.index()} | times: {seg.start,seg.end}")
                break
                bad_times = True
    #if bad_times:
        #toElan.toElan(output_path+file_name,trans)