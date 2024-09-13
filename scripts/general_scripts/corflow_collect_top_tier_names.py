#Created: 2024-02-18
#Latest Version: 2024-02-18
#Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
#Corflow module created by François Delafontaine

from corflow import fromElan
import os

input_path = "../../input_files/"
output_path = "../../output_files/"
print_infos = []

ignore_tiers = ["tx@", "ph@", "ft@", "wd@", "mb@", "gl@", "ps@", "ref@", "doreco-mb-algn@", "refind@", "isnref@", "mc-zero"]

for root,dirs,files in os.walk(input_path):
    if not files:
        continue
    top_tiers = set()
    eaf_files = [file for file in files if file.endswith(".eaf")]
    print(f"\n|{root.rpartition('/')[-1]}|\n")
    for file in eaf_files:
        print(f"File: {file}")
        trans = fromElan.fromElan(root+"/"+file,encoding="utf-8")
        for tier in trans.getTop():
            if tier.children():
                continue
            top_tiers.add(tier.name)
    print_infos.append(f"All top tiers across all eaf files of lang |{root.rpartition('/')[-1]}|")
    print_infos.append(str(top_tiers))
    print_infos.append("\n#####\n\n")

with open(output_path+"all_top_tiers.txt","w") as file:
    for line in print_infos:
        file.write(line)