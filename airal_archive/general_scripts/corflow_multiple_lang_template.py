# Created: 2023-08-23
# Latest Version: 2023-08-30
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

'''
This script works as a template for changing the gloss and morph segments in multiple files of different languages (the template has to be adjusted for every language indivdually and is a script for that very language only).

Every time the comment '#TO-BE-EDITED' appears, something has or can be changed in order to cover language specific cases/operations.
'''

from corflow import fromElan,toElan
import glob
import pandas as pd
import re

#TO-BE-EDITED: Both the import and adjusting the path-attribute are optional. However, they are necessary, if the script 'corflow_additional_functions.py' is not in the same folder where this script is.
import sys
sys.path.append("../")

from corflow_additional_functions import define_content


# DEFINING FUNCTIONS
def check_exceptions(df,gl_cont:str,mb_cont:str,gl_lab="gl",mb_lab="mb",return_lab="status",split_by="§§§"):
    '''Checks whether a gloss and its respective morph appear in a given data frame and returns the respective value, if they do so; otherwise, returns False.

    - df -- the dataframe (loaded with pandas).

    - gl_cont -- the content of the respective gloss segment.

    - mb_cont -- the content of the respective morph segment.

    - gl_lab -- the header/label of the column containing gloss values.

    - mb_lab -- the header/label of the column containing the concatenated morph values.

    - return_lab -- the header/label of the column containing the status values, which get returned, if the *gl_cont* matches a value in *gl_lab*, and *mb_cont* in *mb_lab*.
    
    - split_by -- the string, which is used to separate the concatenated morph values.
    '''
    gl_exc_exists = False
    mb_exc_exists = False
    for index,gl_entry in enumerate(df[gl_lab]):
        if gl_cont == gl_entry:
            gl_exc_exists = True
            if df[mb_lab].iloc[index] == "":
                return df[return_lab].iloc[index]
            elif mb_cont in df[mb_lab].iloc[index].split(split_by):
                return df[return_lab].iloc[index]
            else:
                mb_exc_exists = False
    if (gl_exc_exists) & (mb_exc_exists == False):
        print(f"###\nThe gloss *{gl_cont}* was found as an exception, but not with the particular morph *{mb_cont}*!\n###")
    return False

def find_multiple_tiers(trans,tier_re:list,func=None):
    '''Searches for any number of tiers to be found based on any number of regex patterns in *tier_re*. If *func* is None, the found tiers get returned in a list. If *func* is True, the respective function with the list of found tiers as its input gets returned.

    - trans -- the transcription

    - tier_re -- a list with regex patterns (strings) to be used to find any number of tiers in *trans*.

    - func -- If None, a list with all found tiers gets returned. If callable, it gets returned with the list of found tiers as its input.
    '''
    found_tiers = []
    for tier_pattern in tier_re:
        for tier in trans:
            if re.search(tier_pattern,tier.name):
                found_tiers.append(tier)
    if callable(func):
        return func(found_tiers)
    else:
        return found_tiers

def find_tier_triples(trans,tier1_re,tier2_re,tier3_re,func=None):
    '''Searches for three tiers based on regex patterns and optionally additionally based on a function and adds them as a triple (3-tuple) to a list. Returns this list.

    - trans -- the transcription.

    - tier1_re -- regex pattern to identify the first tier.

    - tier2_re -- regex pattern to identify the second tier.

    - tier3_re -- regex pattern to identify the third tier.

    - func -- if not specified, it is None and will not be used. If specified, it has to be a callable function with the first three arguments being reserved for the three tiers. It has to return bool (True/False). If True, the three tiers will be added to the list as a triple, which will be returned at the end of this functions excecution.
    '''
    tier_triples = []
    for tier1 in trans:
        if re.search(tier1_re,tier1.name):
            for tier2 in trans:
                if re.search(tier2_re,tier2.name):
                    for tier3 in trans:
                        if re.search(tier3_re,tier3.name):
                            if func == None:
                                tier_triples.append((tier1,tier2,tier3))
                            elif callable(func):
                                if func(tier1,tier2,tier3):
                                    tier_triples.append((tier1,tier2,tier3))
    for triple in tier_triples:
        if len(triple) != 3:
            print(f"A supposed triple of tiers with more or less tiers was found. It has {len(triple)} tiers. These are {[tier.name for tier in triple]}.")
    return tier_triples

#TO-BE-EDITED: The following function is a subfunction used in the function 'find_tier_tuples'. It ensures, that all found tiers belong to the same speaker. For this to work for other languages, it may be necessary to adjust the function or to write another custom function.
def tier_name_condition_dolgan(tier1,tier2,tier3):
    '''Returns True, if *tier1*, *tier2* and *tier3* belong to the same speaker, which is checked by certain conditions their names have to fulfill. Returns False otherwise.
    '''
    if tier1.name.replace("ge","") == tier2.name.replace("mb",""):
        if (tier3.name == "tx (tx)") | (tier1.name.replace("ge","").replace("_mtok","") in tier3.name):
            return True
        else:
            return False
    else:
        return False

def get_tier_names(eaf_files):
    '''Returns a list with the name of every unique tier name, that occurs in a given transcription for all *eaf_files*.'''
    tier_names = []
    for file in eaf_files:
        trans = fromElan.fromElan(file,encoding="utf-8")
        for tier in trans:
            if not tier.name in tier_names:
                tier_names.append(tier.name)
    return tier_names

def get_tier_names_per_file(eaf_files):
    '''Prints a list with all tier names for a given transcription for a file of all *eaf_files*.'''
    for file in eaf_files:
        tier_names_per_file = []
        trans = fromElan.fromElan(file,encoding="utf-8")
        for tier in trans:
            tier_names_per_file.append(tier.name)
        print(f"\nThe file {file} has the following tiers:\n{tier_names_per_file}")



# THE ACTUAL OPERATIONS BEGIN HERE
#File paths (eaf-files and csv-file).

#TO-BE-EDITED: Path, were currently the eaf-files are.
input_path = "../../input_files/"
#TO-BE-EDITED: Path, were the new eaf-files will get saved.
output_path = "../../output_files/"

eaf_files = glob.glob(input_path+"/*.eaf")

#TO_BE_EDITED: Change the string after the plus-symbol to the name of the relevant csv-file.
exception_file = input_path+"dolg1241_exceptions.csv"

#Loading the csv file with the exceptions as a dataframe.
df = pd.read_csv(exception_file,header=0)
#Turning Null values (NA/NaN) into empty strings.
df = df.fillna("")
#print(df)


#TO-BE-EDITED: regular expressions to identify the tiers. These variables will get used below in the function 'find_tier_triples'.
gl_tier_re_pattern = "ge.*mtok" #regular expression to identify the gloss tier(s)
mb_tier_re_pattern = "mb.*mtok" #regular expression to identify the morph tier(s)
tx_tier_re_pattern = "^tx" #regular expression to identify the word tier(s)
sort_func = tier_name_condition_dolgan # Either 'None', if no additional sorting function is used, or the name of the custom function, which is used to sort the tiers.

#Printing all unique tier names across all eaf files:
print(f"#####\nAll unique tier names across all eaf files:\n#####\n{get_tier_names(eaf_files)}")

#Printing all tier names per file:
get_tier_names_per_file(eaf_files)


#Iterating over every file in the input path and loading it as a transcription object in order to be edited.
for file in eaf_files:
    file_name = file.replace(input_path,"")
    print(f"FILE: {file_name}\n")
    trans = fromElan.fromElan(file,encoding="utf-8")

    #Finding the gloss and its respective morph tier.
    for gl_tier,mb_tier,tx_tier in find_tier_triples(trans,gl_tier_re_pattern,mb_tier_re_pattern,tx_tier_re_pattern,sort_func):
        print(f"gloss tier: {gl_tier.name}")
        print(f"morph tier: {mb_tier.name}")
        print(f"txt tier: {tx_tier.name}")
        print(f"END OF TIER TRIPLE")

        #This will be important later.
        root_encounter = False
        #Iterating over every gloss segment in the previously found gloss tier.
        for gl_seg in gl_tier:
            #The special rule for gloss segments in the Autography eaf file.
            if gl_seg.content.endswith(" "):
                gl_seg.content = gl_seg.content.replace(" ","")

            extra_signs = ["-","=","~","#"]
            sign_found = False
            for sign in extra_signs:
                if (gl_seg.content.startswith(sign)) | (gl_seg.content.endswith(sign)):
                    sign_found = True
            if sign_found:
                continue
            mb_seg = mb_tier.getTime(gl_seg.start)
            tx_seg = tx_tier.getTime(gl_seg.start)
            #If a gloss or morph segment does not exist, the loop gets continued.
            if (gl_seg == None) | (mb_seg == None):
                continue
            #Picking out the time-aligned morph and tx segments of the gloss segment.
            #Check, whether the contents of the gloss and morph segments are in the exception list. If False, the status of the gloss gets determined later. If True, its status is set to the returned value from the df (exceptions list).
            if check_exceptions(df,gl_seg.content,mb_seg.content) == False:
                status = None
            else:
                status = check_exceptions(df,gl_seg.content,mb_seg.content)
            #If the gloss was not in the exceptions list, its status gets determined here:
            ######TO-BE-EDITED: ADDING THE INDIVIDUAL CONDITIONS: BEGIN #####
            if status == None:
                if gl_seg.content.isupper():
                    status = "affix"
                else:
                    status = "root"

            #Going through the gloss segments and adjusting their content based on their status and position.
            if status == "root":
                root_encounter = True
            elif status == "affix":
                if root_encounter == True:
                    gl_seg.content = "-" + gl_seg.content
                else:
                    gl_seg.content = gl_seg.content + "-"
            elif status == "clitic":
                if root_encounter == True:
                    gl_seg.content = "=" + gl_seg.content
                else:
                    gl_seg.content = gl_seg.content + "="
            ######TO-BE-EDITED: ADDING THE INDIVIDUAL CONDITIONS: END #####

            #In case, if the corresponding tx segment was not found (for some unknown reason, but which occured in my case), it gets reset to the previous one. This is important to ensure whether a root occurred in the current word already or if a new word started.
            if tx_seg == None:
                if (gl_seg.index() - 1) >= 0:
                    prev_gl_seg = gl_tier.elem[gl_seg.index()-1]
                    if prev_gl_seg.end == gl_seg.start:
                        tx_seg = tx_tier.getTime(prev_gl_seg.start)
                        if tx_seg == None:
                            continue
                        elif tx_seg.end == gl_seg.end:
                            root_encounter = False
            elif gl_seg.end == tx_seg.end:
                root_encounter = False

        ##TO-BE-EDITED: Lastly, copying the respective morph status signs from the gloss segments to the morph segments.
        define_content(trans,(mb_tier.name,"MATCH"),("-","ADD_TO_START"),cond1=(mb_tier.name,"MATCH","startswith","-",False),cond2=(gl_tier.name,"MATCH","startswith","-"))
        define_content(trans,(mb_tier.name,"MATCH"),("-","ADD_TO_END"),cond1=(mb_tier.name,"MATCH","endswith","-",False),cond2=(gl_tier.name,"MATCH","endswith","-"))
        define_content(trans,(mb_tier.name,"MATCH"),("=","ADD_TO_START"),cond1=(mb_tier.name,"MATCH","startswith","=",False),cond2=(gl_tier.name,"MATCH","startswith","="))
        define_content(trans,(mb_tier.name,"MATCH"),("=","ADD_TO_END"),cond1=(mb_tier.name,"MATCH","endswith","=",False),cond2=(gl_tier.name,"MATCH","endswith","="))

    toElan.toElan(output_path+file_name,trans)

    print("\n!!! NEXT FILE !!!\n")
