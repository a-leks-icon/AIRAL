# Created: 2023-08-17
# Latest Version: 2023-08-17
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by François Delafontaine

'''
This script produces a csv-file, which lists all cases of problematic word-morph structure pairs across all eaf-files. This is used to identify primarily cases of misalignments but also other problematic cases.
'''

from corflow import fromElan
import glob
import re
import pandas as pd

#Custom functions
def find_tiers(transcription,string):
    '''Returns a list with all tiers in the transcription that match the given regex string pattern.'''
    found_tiers = []
    for tier in transcription:
        if re.search(string,tier.name):
            found_tiers.append(tier)
    return found_tiers

def check_child_content(segment,re_pattern):
    '''Returns True, if the concatenated, adjusted content of child segments do not equal the adjusted content of the (parent) segment, and None otherwise. Returns None, if the (parent) segments content is not appropriate to begin with.'''
    morph_type_symbols = ["=","-"]
    if re.search(re_pattern,segment.content):
        return
    elif segment.children():
        concat_child_cont = ""
        for child_seg in segment.children():
            child_cont = child_seg.content
            for symbol in morph_type_symbols:
                child_cont = child_cont.replace(symbol,"")
            concat_child_cont += child_cont
        if segment.content.lower() == concat_child_cont:
            return False
        elif segment.content == concat_child_cont:
            return False
        else:
            return True

def check_seg_cont_and_struc(segment,re_pattern):
    '''Returns True, if the segments content is meaningful, but the segment still lacks child segments (has a gap).'''
    if not re.search(re_pattern,segment.content):
        if not segment.children():
            return True
        else:
            return False

#Folder and file paths.
input_path = "../../input_files/"
output_path = "../../output_files/"
eaf_files = glob.glob(input_path+"/*.eaf")

#Regular expression used to exclude cases.
re_pattern_bad_cont = "[0-9]|§|\$|^.$|^,$|\"|“|edited|\[|\]|pause|\?|\.\.|\(|\)|\/|corrected|^NT$|^KK$"

l_unusual_structure = []
for file in eaf_files:
    file_name = file.replace(input_path,"")
    trans = fromElan.fromElan(file,encoding="utf-8")
    #Iterating through every word tier in a file:
    for word_tier in find_tiers(trans,"_word-txt-erk"):
        for word_seg in word_tier:
            #Checking, whether word segs do not have the right morph children or no morph children at all, despite carrying meaningful content:
            if (check_child_content(word_seg,re_pattern_bad_cont)) or (check_seg_cont_and_struc(word_seg,re_pattern_bad_cont)):
                if word_seg.children():
                    word_child_content = [word_child.content for word_child in word_seg.children()]
                else:
                    word_child_content = ""
                #Creating a dict, which will later be one row in a df.
                d_unusual_structure = {'File Name': file_name,
                                       'Phrase': word_seg.parent().content,
                                       'Word': word_seg.content,
                                       'Morph(s)': word_child_content}
                l_unusual_structure.append(d_unusual_structure)
                #print(file.replace(input_path,""))
                #print(word_seg.parent().content)
                #print(word_seg.content)
                #print("###########################")

#Creating the df.
df_unusual_structure = pd.DataFrame(l_unusual_structure)
#Exporting the df as a csv-file.
df_unusual_structure.to_csv(output_path+"nafsan_unusual_structure.csv")