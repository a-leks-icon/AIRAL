#Created: 2024-02-24
#Latest Version: 2024-02-24
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
        if tier.parent() == None:
            continue
        print(f"tier: {tier.name}\n")
        for seg in tier:
            if seg.parent() == None:
                print(f"seg: {(seg.content,seg.start,seg.end)}")
                for ind,par_seg in enumerate(tier.parent()):
                    print(f"mb seg: {(par_seg.content,par_seg.start,par_seg.end)}")
                    print(f"wd seg: {(par_seg.parent().content,par_seg.parent().start,par_seg.parent().end)}")
                    if ind > 100:
                        break
                    if (seg.start == par_seg.start) | (seg.end == par_seg.end) | ((seg.start > par_seg.start) & (seg.end < par_seg.end)):
                        print(f"supposed par seg: {(par_seg.content,par_seg.start,par_seg.end)}")
                        seg.setParent(par_seg)
                        break
                break
                
    #toElan.toElan(output_path+file_name,trans)
    #break
