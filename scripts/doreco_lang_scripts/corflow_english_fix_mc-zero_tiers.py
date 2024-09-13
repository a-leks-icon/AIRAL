#Created: 2024-03-01
#Latest Version: 2024-03-01
#Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
#Corflow module created by François Delafontaine

from corflow import fromElan,toElan
import os
import xml.etree.ElementTree as ET
import sys
sys.path.append("../")
from corflow_additional_functions import find_tiers


def check_for_negative_time(eaf_file):
    '''chech whether an *eaf_file* (path to an eaf file) contains a negative time slots, which gets accessed by at least one segment (annotation). If so, returns a list with all respective tier names (ids). Returns False otherwise.'''
    tree = ET.parse(eaf_file)
    root = tree.getroot()
    negative_time_slots = []
    for time in root.findall("./TIME_ORDER/TIME_SLOT/[@TIME_VALUE='-1000']"):
        negative_time_slots.append(time.attrib["TIME_SLOT_ID"])
    if not negative_time_slots:
        return False
    tier_names = []
    for tier in root.iter("TIER"):
        tier_id = tier.attrib["TIER_ID"]
        for seg in tier.findall("ANNOTATION/ALIGNABLE_ANNOTATION"):
            if (seg.attrib["TIME_SLOT_REF1"] in negative_time_slots) | (seg.attrib["TIME_SLOT_REF2"] in negative_time_slots):
                tier_names.append(tier_id)
                break
    return tier_names

def copy_tier(transcription,tier,new_tier_name,parent_tier,char_num=1):
    '''Copies an existing *tier* and adds it to a *transcription* with its *new_tier_name* and newly assigned *parent_tier*. All segments of the newly added tier get renamed based on their first characters letter and the number *char_num* given. By default, this number euqals 1 meaning that if e.g. the first character in a segments name is 'a', it gets substituted by 'b'. If char_num equals 2 and the first character is again 'a', it gets substituted by the character 'c', and so on. Returns the newly added tier.'''
    transcription.add(-1,tier)
    new_tier = transcription.elem[-1]
    new_tier.name = new_tier_name
    for seg in new_tier:
        seg.name = chr(ord(seg.name[0])+char_num) + seg.name[1:]
    new_tier.setParent(parent_tier)
    if parent_tier == None:
        for seg in new_tier:
            seg.setParent(None)
    else:
        for seg in new_tier:
            seg.setParent(parent_tier.getTime(seg.start))
    return new_tier

def remove_duplicated_tier_xml(eaf_file):
    '''Removes from the xml strucutre of an *eaf_file* those xml elements representing tiers, but which are empty (do not contain any elements inside them). Overwrites those *eaf_file*s.'''
    tree = ET.parse(eaf_file)
    root = tree.getroot()
    for tier in root.iter("TIER"):
        el_len = len([el for el in tier])
        if el_len <= 0:
            root.remove(tier)
    tree.write(eaf_file,encoding="utf-8",xml_declaration=True)


input_path = "../../input_files/"
output_path = "../../output_files/"

clean_files_dir = input_path+"B_modified_eafs_before_sign_script"
now_files_dir = input_path+"English"

for root,dirs,files in os.walk(input_path):
    if root == now_files_dir:
        now_eafs = [file for file in files if file.endswith(".eaf")]
    elif root == clean_files_dir:
        clean_eafs = [file for file in files if file.endswith(".eaf")]
fix_eafs = []
for now_eaf in now_eafs:
    tier_names = check_for_negative_time(now_files_dir+"/"+now_eaf)
    if tier_names:
        fix_eafs.append((now_eaf,tier_names))

for eaf in clean_eafs:
    eaf_path = clean_files_dir+"/"+eaf
    remove_duplicated_tier_xml(eaf_path)

for new_eaf in fix_eafs:
    print(f"File pair: {new_eaf[0]}")
    trans_new = fromElan.fromElan(now_files_dir+"/"+new_eaf[0],encoding="utf-8")
    trans_old = fromElan.fromElan(clean_files_dir+"/"+new_eaf[0],encoding="utf-8")
    for tier_name in new_eaf[1]:
        for new_tier in find_tiers(trans_new,tier_name):
            print(f"remove tier from new eaf: {new_tier.name}")
            trans_new.remove(new_tier)
        tier_lens = []
        for old_tier in find_tiers(trans_old,tier_name):
            tier_lens.append((len(old_tier),old_tier))
        tier_lens = sorted(tier_lens,reverse=True)
        add_tier = tier_lens[0][-1]
        copy_tier(trans_new,add_tier,add_tier.name,None)
    toElan.toElan(output_path+new_eaf[0],trans_new)