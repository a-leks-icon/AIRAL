#Created: 2024-02-16
#Latest Version: 2024-02-21
#Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
#Corflow module created by François Delafontaine

''''
This script currently workes flawlessly with corflow version 3.2.6, but not with 3.2.12 or 3.2.14. This is not an issue with the script, but with the corflow version (not for every file though).
'''

import pandas as pd
from corflow import fromElan,toElan
import os

def save_child_tiers(tier,data):
    ''''''

    def check_child_tiers(tier,par_tier,trans,saved:list,data):
        if not tier.children:
            return saved
        for ch_tier in tier.children():
            if not ch_tier.name in data:
                trans.add(-1,ch_tier,struct=trans)
                new_tier = trans.elem[-1]
                new_tier.setParent(par_tier)
                for saved_tier in saved:
                    if saved_tier.name == ch_tier.parent().name:
                        new_tier.setParent(saved_tier)
                        break
                if new_tier.parent() != None:
                    for seg in new_tier:
                        seg.setParent(new_tier.parent().getTime(seg.start))
                else:
                    for seg in new_tier:
                        seg.setParent(None)
                saved.append(new_tier)
            check_child_tiers(ch_tier,par_tier,trans,saved,data)
        return saved

    saved_tiers = []
    parent_tier = tier.parent()
    transcription = tier.struct
    saved_tiers = check_child_tiers(tier,parent_tier,transcription,saved_tiers,data)
    return saved_tiers



input_path = "../../input_files/"
output_path = "../../output_files/"
csv_file = "legacy_tiers_prefinal.csv"

#Read tsv file containing to be removed tiers and create a df.
df = pd.read_csv(input_path+csv_file,sep=",",header=0)
df = df.dropna()

#A list collecting the information about removed tiers, which gets saved in a txt file at the end of the process.
log_infos = ["Removed tiers per language and file.\n##########\n\n"]

#Iterating over every subdirectory representing a language and containing all (eaf) files.
for root,dirs,files in os.walk(input_path,topdown=False):
    language = root.rpartition("/")[-1]
    eaf_files = [file for file in files if file.endswith(".eaf")]
    print(f"\nProcessing language |{language}|")

    #df1 only containing language specific eaf files.
    df_lang = df[df["language"] == language]
    if df_lang.empty:
        print(f"No entries were found!")
        continue
    print(f"Found entries!")

    log_infos.append(f"|{language}|\n")

    #Iterate over every eaf file, create a custom df for that file, and if not empty, iterate over every tier to find the tier to remove (and all of its potential children).
    for file in eaf_files:

        file_n = file.removesuffix(".eaf")
        #df_lang_file = df_remove_lang[df_remove_lang["file"] == file_n]

        log_infos.append(f"File: '{file}': ")
        print(f"File: {file}")

        removed_tiers = []
        copied_tiers = []
        trans = fromElan.fromElan(root+"/"+file,encoding="utf-8")
        tiers = [tier for tier in trans].copy()
        for tier in tiers:
            if tier.name in df_lang["name"].values:
                remove_tier = tier
                for copy_t in copied_tiers:
                    if tier.name == copy_t.name:
                        remove_tier = copy_t
                        break
                copied_tiers += save_child_tiers(remove_tier,df_lang["name"].values)
                removed_tiers.append(remove_tier.name)
                trans.allRemove(remove_tier)

        if copied_tiers:
            log_infos.append(f"{str(removed_tiers)} -- Saved tiers: {str([tier.name for tier in copied_tiers])}\n")
        else:
            log_infos.append(str(removed_tiers)+"\n")

        #Create new language subdirectory in the output directory if necessary.
        output_lang_dir = output_path+language
        os.makedirs(output_lang_dir,exist_ok=True)
        #Save new eaf file.
        toElan.toElan(output_lang_dir+"/"+file,trans)

    log_infos.append("#####\n")
    #break

with open(output_path+"log_remove_tiers.txt","w") as log_file:
    for line in log_infos:
        log_file.write(line)

'''old (worse) solution
for row_label,row in df.iterrows():
    file = row.loc["lang"] + "/" + row.loc["file"] + ".eaf"
    trans = fromElan.fromElan(input_path+file,encoding="utf-8")
    for tier in trans:
        if tier.name == row.loc["tier"]:
            trans.allRemove(tier)
            break
    toElan.toElan(output_path+file,trans)
'''