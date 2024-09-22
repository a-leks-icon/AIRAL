#Created: 2024-02-15
#Latest Version: 2024-02-16
#Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
#Corflow module created by François Delafontaine

'''
Prints all groups of segments appearing, where segments are either duplicates of one another or overlap with one another, for all files and tiers.
'''

from corflow import fromElan
import sys
sys.path.append("../")
from corflow_additional_functions import get_duplicated_segments,get_overlapping_segments
import glob

#File paths.
input_path = "../../input_files/"
output_path = "../../output_files/"
eaf_files = glob.glob(input_path+"/*.eaf")

for file in eaf_files:
    file_name = file.replace(input_path,"")
    trans = fromElan.fromElan(file,encoding="utf-8")
    print(f"FILE: {file_name}")
    #Creating for every file two dictionaries, which contain lists of tuples representing groups of a) overlapping and b) duplicated segments (the tiers are the dictionary keys).
    overlaps_dict = get_overlapping_segments(trans)
    duplicates_dict = get_duplicated_segments(trans)

    #Overlaps:
    print(f"Overlaps from file {file_name}:")
    for tier,overlaps_l in overlaps_dict.items():
        print(f"TIER: {tier.name}")
        print(f"OVERLAPPING SEGMENTS [content,start,end,internal_name]:\n#####\n")
        for overlaps in overlaps_l:
            print(f"{[(s.content,s.start,s.end,s.name) for s in overlaps]}")
        print(f"\n#####\n")

    #Duplicates:
    print(f"Duplicates from file {file_name}:")
    for tier,duplicates_l in duplicates_dict.items():
        print(f"TIER: {tier.name}")
        print(f"DUPLICATED SEGMENTS [content,start,end,internal_name]:\n#####\n")
        for duplicates in duplicates_l:
            print(f"{[(s.content,s.start,s.end,s.name) for s in duplicates]}")
        print(f"\n#####\n")