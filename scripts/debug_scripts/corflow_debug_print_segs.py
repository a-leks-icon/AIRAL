#Created: 2024-02-24
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
    for tier in trans:
        print(f"tier: {tier.name}\n")
        if len(tier) >= 50:
            for n in range(50):
                seg = tier.elem[n]
                print((seg.content,seg.start,seg.end))
        else:
            for seg in tier:
                print((seg.content,seg.start,seg.end))
        print("###########")