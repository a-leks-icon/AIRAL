#Created: 2024-02-16
#Latest Version: 2024-02-16
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
    eaf_files = [file for file in files if file.endswith(".eaf")]
    print(f"\n|{root.rpartition('/')[-1]}|\n")
    unique_tiers_per_file_dict = {}
    for file in eaf_files:
        print(f"File: {file}")
        trans = fromElan.fromElan(root+"/"+file,encoding="utf-8")
        for tier in trans:
            #print(f"{tier.name} index: {tier.index()} and {len(tier.struct)}")#debug
            if any(tier.name.startswith(label) for label in ignore_tiers):
                continue
            if not tier.name in unique_tiers_per_file_dict:
                unique_tiers_per_file_dict[tier.name] = set()
                unique_tiers_per_file_dict[tier.name].add(len(tier.struct)-tier.index())
            else:
                #print(f"tier dict: {unique_tiers_per_file_dict}")
                unique_tiers_per_file_dict[tier.name].add(len(tier.struct)-tier.index())
    print_infos.append(f"All different and possible legacy tiers across all eaf files of lang |{root.rpartition('/')[-1]}| with their position(s):\n\n")
    print_infos.append(str(unique_tiers_per_file_dict))
    print_infos.append("\n#####\n\n")

with open(output_path+"all_possible_legacy_tiers.txt","w") as file:
    for line in print_infos:
        file.write(line)