# Created: 2023-06-03
# Latest Version: 2023-06-08
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

'''
Script description:

The following script takes a txt-file with translation-values (encoded as a line starting with '\tre') and assigns those to the content of their respective segments on the translation tier by start and end times, which are also encoded as values in the txt-file ('\ELANBegin' and '\ELANEnd').
'''

from corflow import fromElan, toElan
import datetime

#The path of the txt-file and eaf-file.
input_path = "../../input_files/"

#The path where the new eaf-file will be saved.
output_path = "../../output_files/"

#The respective file names:
txt_file = "JuanFlojo_tre_format_modified.txt"
eaf_file = "JuanFlojo.eaf"

#The name of the translation tier in ELAN. The name is used to a) identify the respective line in the txt-file as well as b) to find the respective tier in the eaf-file.
translation_tier_name = "tre"

#Part of the name of the tier in ELAN, which has the time informations. The start and end times of its segments have to be time-aligned with those on the translation tier.
reference_tier_name = "rf"

#Loading the txt-file and saving the start times, end times and the translation values in seperate lists. Every list has to have the same length, otherwise changing the content of the translation segments later won't work properly.
with open(input_path+txt_file,"r") as translation:
    translation_lines = []
    seg_start_times = []
    seg_end_times = []
    for line in translation.readlines():
        if line.startswith("\\ELANBegin"):
            seg_start_times.append(datetime.timedelta(hours=int(line[-13:-11]),minutes=int(line[-10:-8]),seconds=int(line[-7:-5]),milliseconds=int(line[-4:-1])).total_seconds())
        if line.startswith("\\ELANEnd"):
            seg_end_times.append(datetime.timedelta(hours=int(line[-13:-11]),minutes=int(line[-10:-8]),seconds=int(line[-7:-5]),milliseconds=int(line[-4:-1])).total_seconds())
        if line.startswith(f"\\{translation_tier_name}"):
            translation_lines.append(line[5:].replace("\n",""))

#Loading the eaf-file and searching/finding the relevant tiers. Because the start and end times in the txt-file belong to the parent tier (the reference tier), it has to be found besides the translation tier.
trans = fromElan.fromElan(input_path+eaf_file,encoding="utf-8")

translation_tier_exists = False
reference_tier_exists = False
for tier in trans:
    if translation_tier_name in tier.name:
        translation_tier = trans.getName(tier.name)
        translation_tier_exists = True
    elif reference_tier_name in tier.name:
        reference_tier = trans.getName(tier.name)
        reference_tier_exists = True

    if translation_tier_exists & reference_tier_exists:
        translation_tier_exists = False
        reference_tier_exists = False

        #After the two tiers are found, the actual operation begins: If a segment on the translation tier has the same start and end time as collected before (which is basically the start and end time of a segment on the reference tier), its content gets changed to the respective translation.
        for index in range(0,len(seg_start_times)):
            for translation_seg in translation_tier:
                if (translation_seg.start == seg_start_times[index]) & (translation_seg.end == seg_end_times[index]):
                    translation_seg.content = translation_lines[index]

toElan.toElan(output_path+eaf_file,trans)

