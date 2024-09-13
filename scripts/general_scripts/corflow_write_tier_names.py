#Created: 2024-02-19
#Latest Version: 2024-02-19
#Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
#Corflow module created by François Delafontaine

from corflow import fromElan
import pandas as pd
import os

'''
This script iterates over every language folder and its eaf-files, collects for every file its tier names and creates a csv file with these informations.
'''

input_path = "../../input_files/"
output_path = "../../output_files/"
lang_file_tier_l = []

for root,dirs,files in os.walk(input_path):
    if not files:
        continue
    eaf_files = [file for file in files if file.endswith(".eaf")]
    language = root.rpartition('/')[-1]
    print(f"\nLanguage: |{language}|\n")
    for file in eaf_files:
        print(f"File: {file}")
        trans = fromElan.fromElan(root+"/"+file,encoding="utf-8")
        for tier in trans:
            lang_file_tier_l.append({"language": language, "file": trans.name, "tier": tier.name})

df = pd.DataFrame(lang_file_tier_l)
df.to_csv(output_path+"tiers_per_lang_and_file.csv",sep=",")