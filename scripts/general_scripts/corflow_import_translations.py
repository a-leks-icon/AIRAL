#Created: 2024-04-16
#Latest Version: 2024-05-03
#Script written by Aleksandr Schamberger (GitHub: JLEKS) as part of the AIRAL project by Ludger Paschen at ZAS Berlin.
#Corflow module created by François Delafontaine.

'''
Importing translations from a file (tbt or txt) for a tier in a corresponding ELAN (eaf) file and adding those translations to either an existing or newly created tier in that ELAN file.
'''

from corflow import fromElan, toElan
#import datetime as dt
import os
import re

def copy_tier(tier,new_tier_name,parent_tier,char_num=1):
    '''Copies an existing *tier* to its transcription named as *new_tier_name* and its parent tier being *parent_tier*. All segments of the newly added tier get renamed based on their first characters letter and the number *char_num* given. By default, this number equals 1 meaning that if e.g. the first character in a segments name is 'a', it gets substituted by 'b'. If char_num equals 2 and the first character is again 'a', it gets substituted by the character 'c', and so on. Returns the newly added tier.'''
    trans = tier.struct
    trans.add(-1,tier)
    new_tier = trans.elem[-1]
    new_tier.name = new_tier_name
    for seg in new_tier:
        seg.name = chr(ord(seg.name[0])+char_num) + seg.name[1:]
    new_tier.setParent(parent_tier)
    for seg in new_tier:
        seg.setParent(parent_tier.getTime(seg.start))
    return new_tier

#Input path of the eaf and translation (tbt or txt) files.
input_path = "../../input_files/"
eaf_path = "evenki_eaf_files/"
tr_path = "doreco_evenki_translations_tbt/"
eaf_files = os.listdir(input_path+eaf_path)
eaf_files = [file for file in eaf_files if file.endswith(".eaf")]
tr_files = os.listdir(input_path+tr_path)

#Output path, where the new eaf file will be saved.
output_path = "../../output_files/"

#Regex used to idenfity the name of the lines in the translation file, which contain the actual translations.
tr_line_name = r"^\\ft1?"

#Regex used to identify the name of the translation tier in the ELAN (eaf) file. If no tier with this name already exists, a new tier with that name will be created (currently, it is expected, that no such tier already exists. The script may not work properly, if such a tier already exist in the eaf file).
tr_tier_name = r"eng1?"

#Regex used to idenfity the name of the sister tier of the translation tier. Its segment's start and end times have to be time-aligned with those on the translation tier.
sister_tier_name = r"rus1?"

#Name of the lines in the translation file containing the start and end times.
start_line = "\\ELANBegin"
end_line = "\\ELANEnd"



#---ACTUAL OPERATIONS---#

#Loading the translation files, and saving the start and end times and the translation values in seperate lists.
eaf_match = 0
tr_files_copy = tr_files.copy()
for tr_file in tr_files:
    print(f"Translation file: {tr_file}")
    with open(input_path+tr_path+tr_file,"r") as tr:
        times = []
        translations = []
        for line in tr.readlines():
            line_regex_obj = re.search(tr_line_name,line)
            if line.startswith(start_line):
                time = line.removeprefix(start_line+" ").removesuffix("\n")
                #start = dt.timedelta(seconds=int(time[:-4]),milliseconds=int(time[-3:])).total_seconds()
                start = float(time)
            elif line.startswith(end_line):
                time = line.removeprefix(end_line+" ").removesuffix("\n")
                #end = dt.timedelta(seconds=int(time[:-4]),milliseconds=int(time[-3:])).total_seconds()
                end = float(time)
                times.append((start,end))
            #elif line.startswith(tr_line_name):
            elif line_regex_obj:
                translation = line.removeprefix(line_regex_obj.group(0)+" ").removesuffix("\n")
                translations.append(translation)

    #Raise an exception, if the number of times and translation values is different.
    if len(times) != len(translations):
        raise Exception(f"Different number of found translations ({len(translations)}) and of segment times ({len(times)}). Stopping script.")

    #Finding and loading the corresponding eaf file.
    match = False
    end_ind = -4
    while match == False:
        for eaf_file in eaf_files:
            if not eaf_file.endswith(".eaf"):
                continue
            if eaf_file.startswith(tr_file[:end_ind]):
                match = True
                trans = fromElan.fromElan(input_path+eaf_path+eaf_file,encoding="utf-8")
                eaf_match += 1
                eaf_files.remove(eaf_file)
                print(f"eaf file: {eaf_file}")
                break
        end_ind -= 1

    #Getting the translation tier and its sister tier.
    #tr_tier = trans.getName(tr_tier_name)
    tr_tier = trans.findName(tr_tier_name)
    #sister_tier = trans.getName(sister_tier_name)
    sister_tier = trans.findName(sister_tier_name)

    #Raising an exception, if the sister tier does not exist in the eaf file.
    if sister_tier == None:
        raise Exception(f"The respective sister tier '{sister_tier_name}' was not found in the eaf file. Stopping script.")
    #Creating a new translation tier if it does not exist yet.
    if tr_tier == None:
        print(f"Creating a new translation tier in the eaf file.")
        #If a new translation tier gets created, it will be named as follows:
        tr_tier_actual_name = str(tr_tier_name)[:len(sister_tier.name)]
        tr_tier = copy_tier(sister_tier,tr_tier_actual_name,sister_tier.parent())
    print(f"translation tier: {tr_tier.name}")
    print(f"its sister tier: {sister_tier.name}")

    #The actual operation: Adding the translation values of the translation file based on the start and end times of the respective segments.
    for ind,seg in enumerate(tr_tier):
        if (seg.start == times[ind][0]) & (seg.end == times[ind][-1]):
            seg.content = translations[ind]

    #Saving new eaf file.
    toElan.toElan(output_path+eaf_file,trans)
    print(f"Done.")

    tr_files_copy.remove(tr_file)
    print("-----\n")

print(f"##########\n")
if eaf_files:
    print(f"Remaining eaf files ({len(eaf_files)}) without a corresponding translation file: {eaf_files}\n")
else:
    print(f"No remaining eaf files without a corresponding translation file.\n")

if tr_files_copy:
    print(f"Remaining translation files ({len(tr_files_copy)}) without a corresponding eaf file: {eaf_files}")
else:
    print(f"No remaining translation files without a corresponding eaf file.")