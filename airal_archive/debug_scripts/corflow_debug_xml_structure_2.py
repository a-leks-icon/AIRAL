#Created: 2024-03-10
#Latest Version: 2024-03-10
#Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
#Corflow module created by François Delafontaine

import xml.etree.ElementTree as ET
import glob

input_path = "../../input_files/"
eaf_files = glob.glob(input_path+"/*.eaf")
for file in eaf_files:
    file_name = file.replace(input_path,"")
    print(f"File: {file_name}\n#####\n")
    xml_tree = ET.parse(file)
    root = xml_tree.getroot()
    for tier in root.iter("TIER"):
        tier_id = tier.attrib["TIER_ID"]
        print(f"tier: {tier_id}\n***")
        #print(tier.attrib)
        print("---\n")
        '''
        for ind,an in enumerate(tier.findall("ANNOTATION/ALIGNABLE_ANNOTATION")):
            print(an.attrib)
            break
        for an2 in tier.findall("ANNOTATION/REF_ANNOTATION"):
            print(an.attrib)
            break
        '''
        #print(f"tier {tier_id}: {tier.attrib}")
    print("###\n")