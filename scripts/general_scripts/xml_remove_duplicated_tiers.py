#Created: 2024-03-12
#Latest Version: 2024-03-12
#Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
#Corflow module created by François Delafontaine


import xml.etree.ElementTree as ET
import glob

def remove_duplicated_tier_xml(eaf_file,ipath,opath):
    '''Removes from the xml strucutre of an *eaf_file* those xml elements representing tiers, but which are empty (do not contain any elements inside them). Overwrites those *eaf_file*s.'''
    tree = ET.parse(ipath+eaf_file)
    root = tree.getroot()
    for tier in root.iter("TIER"):
        el_len = len([el for el in tier])
        if el_len <= 0:
            root.remove(tier)
    tree.write(opath+eaf_file,encoding="utf-8",xml_declaration=True)


input_path = "../../input_files/"
output_path = "../../output_files/"
eaf_files = glob.glob(input_path+"/*.eaf")

for file in eaf_files:
    file_name = file.replace(input_path,"")
    print(f"File: {file_name}")
    remove_duplicated_tier_xml(file_name,input_path,output_path)