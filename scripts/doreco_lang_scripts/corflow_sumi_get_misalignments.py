# Created: 2023-11-15
# Latest Version: 2023-11-19
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by François Delafontaine

from corflow import fromElan,toElan
import glob
import sys
sys.path.append("../")
from corflow_additional_functions import find_tiers
import unicodedata as uc
import pandas as pd

def word_morph_mismatches(tier,child_tier,seg_filter=[],child_seg_filter=["=","-"]):
    '''Checks for a given *tier*, if its segments content (without any symbols in *seg_filter*) matches the concatenated content (not containing any symbols in *child_seg_symbols*) of the (child) segments from the *child_tier*. If a segments content does not match, a new dictionary is created containing the following keys and values:

    * 1. The file name (without the file extension) of the *tier*.
    * 2. The internal ELAN name of the segment from *tier*.
    * 3. The segments content.
    * 4. The content of all respective (child) segments from *child_tier*.

    Ultimately, a list with all dictionaries is returned.''' 

    def check_mismatches(segment,child_tier,segment_filter,morph_type_symbols):
        '''Returns True, if the content of a *segment* does not match the concatenated content of its child segments (concatenation without any *morph_type_symbols*) for a given *child_tier*. Returns False otherwise. Returns None, if the *segment* has no child segments.'''
        try:
            child_segs = segment.childDict()[child_tier]
            segment_content = segment.content
            if segment_filter:
                for symbol in segment_filter:
                    segment_content = segment_content.replace(symbol,"")
            concat_child_content = ""
            if child_segs:
                for child_seg in child_segs:
                    child_content = child_seg.content
                    for symbol in morph_type_symbols:
                        child_content = child_content.replace(symbol,"")
                    concat_child_content += child_content
                if uc.normalize("NFD",segment_content) == uc.normalize("NFD",concat_child_content):
                    return False
                elif uc.normalize("NFD",segment_content.lower()) == uc.normalize("NFD",concat_child_content.lower()):
                    return False
                else:
                    return True
            else:
                return
        except:
            pass

    if child_tier in tier.children():
        mismatches_l = []
        for seg in tier:
            if check_mismatches(seg,child_tier,seg_filter,child_seg_filter):
                child_segs_content = [child.content for child in seg.childDict()[child_tier]]
                mismatches_d = {'File Name':tier.struct.name,
                                'Segment Name':seg.name,
                                'Segment Content':seg.content,
                                'Child Segments Content':child_segs_content
                                }
                mismatches_l.append(mismatches_d)
            else:
                continue
        return mismatches_l
    else:
        return

def export_dicts_to_csv(dicts,output_path):
    '''Creates a data frame in pandas from a list of dictionaries *dicts*, where every dictionary has the same number of keys and values, and represents one data point. Exports the data frame as a csv file in the given *output_path*.'''
    df = pd.DataFrame(dicts)
    df.to_csv(output_path)


input_path = "../../input_files/"
output_path ="../../output_files/"
eaf_files = glob.glob(input_path+"/*.eaf")

db_l = []
for file in eaf_files:
    trans = fromElan.fromElan(file,encoding="utf-8")
    print(f"file: {trans.name}")
    for word_tier in find_tiers(trans,"Words-txt-nsm"):
        print(f"word tier: {word_tier.name}")
        for morph_tier in word_tier.children():
            if "morph-txt-nsm-cp" in morph_tier.name:
                print(f"morph tier: {morph_tier.name}")
                db_l += word_morph_mismatches(word_tier,morph_tier,[",",".","-","(",")"],["-","="])
export_dicts_to_csv(db_l,output_path+"sumi_mismatches.csv")
