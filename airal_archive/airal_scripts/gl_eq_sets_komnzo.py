#Created: 2024-04-13
#Latest Version: 2024-04-19
#Script written by Aleksandr Schamberger (GitHub: JLEKS) as part of the AIRAL project by Ludger Paschen at ZAS Berlin.

import pandas as pd
import re

'''
The goal behind this script is to reduce the number of gloss-pairs belonging to the same morph in the csv file 'Gloss_equivalence_sets_komn1238.csv' as there are originally more than 47k of them (Ludgers script).


'''

#Directories and file paths.
input_path = "../../input_files/"
output_path = "../../output_files/"
csv_gl = "Gloss_equivalence_sets_komn1238.csv"
csv_ph = "doreco_komn1238_ph.csv"

#Read csv_ph file and create a data frame. Remove pure NaN-rows.
df_ph = pd.read_csv(input_path+csv_ph,header=0)
df_ph = df_ph.loc[:,["wd_ID","wd","mb_ID","mb","ps","gl"]]
df_ph.dropna(how="all",inplace=True)

#Iterate and remove rows with the same morph id.
drop_rows = []
for ind in range(len(df_ph)-1):
    cell1 = df_ph.at[ind,"mb_ID"]
    cell2 = df_ph.at[ind+1,"mb_ID"]
    if cell1 == cell2:
        drop_rows.append(ind+1)
df_ph.drop(drop_rows,inplace=True)

#Iterate and remove the stem information from a row (gloss) by matching a substring.
for label,row in df_ph.iterrows():
    gl: str = row["gl"]
    match_gl = re.search("/(.*)\[",gl)
    if match_gl:
        row["gl"] = gl.replace("/"+match_gl.group(1),"")

#Get the frequency of every (changed) gloss and sort them. 
gls = list(set(df_ph["gl"]))
gls_freq = []
for gl in gls:
    freq = len(df_ph[df_ph['gl'] == gl])
    gls_freq.append((freq,gl))
gls_freq = sorted(gls_freq)

#Remove glosses with frequency greater than 2. After that: Remove morph type information and dashes, and remove remaining duplicates.
gls_freq_lteq2 = [gl for i,gl in gls_freq if i <= 3]
gls_freq_lteq2 = [gl.partition("[")[0].removeprefix("-") for gl in gls_freq_lteq2]
#Membership conditions (x in s) are faster for sets.
gls_freq_lteq2 = set(gls_freq_lteq2)

#Read csv_gl file and create data frame. Remove pure NaN-rows.
df_gl = pd.read_csv(input_path+csv_gl,header=0)
df_gl.dropna(how="all",inplace=True)

print(df_gl)

#Remove all rows starting with glosses with freq <= 2.
#This takes a lot of time (its O(n²)) [45 minutes], but I did not know a better/more efficient way to do this. See below for the new, way better solution.
'''
for ind,gl in enumerate(gls_freq_lteq2):
    drop_rows = []
    print(f"{gl} | {ind+1} of {len(gls_freq_lteq2)}")
    for label,row in df_gl.iterrows():
        if row["gl"].startswith(gl):
            drop_rows.append(label)
    df_gl.drop(drop_rows,inplace=True)
'''

#Comment for me: While the above solution with O(n²) (looping over the glosses in a list, than iterating over all rows in the df for one gloss and checking for every row the condition) took 45 minutes; this new solution (iterating over rows in the df, changing the string and checking whether the string is in the set of glosses) took only 8 seconds with the same outcome!!!
drop_rows = []
for label,row in df_gl.iterrows():
    gl: str = row["gl"]
    gl_pre = gl.partition("/")[0].removeprefix("-")
    if gl_pre in gls_freq_lteq2:
        drop_rows.append(label)
df_gl.drop(drop_rows,inplace=True)

print(df_gl)

#Save new csv file with possible gloss equivalences.
df_gl.to_csv(output_path+csv_gl)
