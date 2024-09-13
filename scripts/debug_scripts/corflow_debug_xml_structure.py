#Created: 2024-02-24
#Latest Version: 2024-02-25
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
    negative_time_slots = []
    for time in root.findall("./TIME_ORDER/TIME_SLOT/[@TIME_VALUE='-1000']"):
        negative_time_slots.append(time.attrib["TIME_SLOT_ID"])
    if negative_time_slots:
        tiers = {}
        print(f"Found negative time slot(s): {negative_time_slots}\n\n")
        for tier in root.iter("TIER"):
            tier_id = tier.attrib["TIER_ID"]
            while tier_id in tiers.keys():
                tier_id += "_0"
            tiers[tier_id] = []
            for an in tier.findall("ANNOTATION/ALIGNABLE_ANNOTATION"):
                if (an.attrib["TIME_SLOT_REF1"] in negative_time_slots) | (an.attrib["TIME_SLOT_REF2"] in negative_time_slots):
                    name = an.attrib["ANNOTATION_ID"]
                    value = an[0].text
                    tiers[tier_id].append((name,value))
        for tier,ts in tiers.items():
            pass
            print(f"tier: {tier}")
            print(ts)
            print("-----")
    else:
        print("No negative time slots were found!")