#Created: 2024-04-14
#Latest Version: 2024-04-14
#Script written by Aleksandr Schamberger (GitHub: JLEKS) as part of the AIRAL project by Ludger Paschen at ZAS Berlin.

'''
The goal behind this script is to reduce the number of gloss-pairs belonging to the same morph in the csv file 'Gloss_equivalence_sets_komn1238.csv' as there are originally more than 47k of them (Ludgers script).

This script reads the phone-based data from Komnzo and creates two new csv files: The first is a smaller version of the csv file containing only the relevant data for the task, e.g. the gloss and morph columns. The second csv file lists for every unique gloss (removing the stem and morph status information) the specific morph and pos-tag it occurs as. Finally, those last information are used to count and list all unique combinations of corcumfixes + stem and/or prefix + stem those glosses occur as.
'''

import pandas as pd

#Directory and file paths.
input_path = "../../input_files/"
output_path = "../../output_files/"
csv_ph = "doreco_komn1238_ph.csv"

#Read csv file and create data frame. Remove pure NaN-rows.
df = pd.read_csv(input_path+csv_ph,header=0)
df = df.loc[:,["wd_ID","wd","mb_ID","mb","ps","gl"]]
df.dropna(how="all",inplace=True)

#Iterate and remove rows with the same morph id.
drop_rows = []
for ind in range(len(df)-1):
    cell1 = df.at[ind,"mb_ID"]
    cell2 = df.at[ind+1,"mb_ID"]
    if cell1 == cell2:
        drop_rows.append(ind+1)
df.drop(drop_rows,inplace=True)

print(f"Created df from csv file: {csv_ph}\nwith length: {len(df)}.")
#Save data frame as new csv file.
df.to_csv(output_path+"komnzo_relevant_data.csv")
print(f"Saved new df as csv file with length: {len(df)}")

drop_rows = []
ps_tags = ["prefix-","-suffix","circumfix-","-circumfix","verb"]
for label,row in df.iterrows():
    #Exactly one noun occurs, which is actually a verb.
    #if not row["ps"] in ps_tags:
        #drop_rows.append(label)
    if ("[affix]" in row["gl"]) | ("[stem]" in row["gl"]):
        gl: str = row["gl"]
        gl_pre = gl.partition("/")[0]
        #gl_suf = "[" + gl.partition("[")[-1]
        #gl_new = gl_pre + gl_suf
        #row["gl"] = gl_new.replace("-","")
        row["gl"] = gl_pre.replace("-","")
        continue
    drop_rows.append(label)
df.drop(drop_rows,inplace=True)

#Save data frame as new csv file.
df.to_csv(output_path+"komnzo_affixes.csv")
print(f"Saved new df as csv file with length: {len(df)}")

gls_types = list(set(df["gl"]))
print(f"gls: {len(gls_types)}")
gls_dict = {gl: [] for gl in gls_types}

mb_col_ind = df.columns.get_loc("mb")
for gl in gls_dict:
    df_sub = df[df["gl"] == gl]
    #print(df_sub)
    for ind,(label,row) in enumerate(df_sub.iterrows()):
        ps: str = row["ps"]
        if ps == "prefix-":
            if ind+1 < len(df_sub):
                gls_dict[gl].append((row["mb"],df_sub.iat[ind+1,mb_col_ind]))
        elif ps == "circumfix-":
            if ind+2 < len(df_sub):
                gls_dict[gl].append((row["mb"],df_sub.iat[ind+1,mb_col_ind],df_sub.iat[ind+2,mb_col_ind]))
        elif ps == "-suffix":
            gls_dict[gl].append((df_sub.iat[ind-1,mb_col_ind],row["mb"]))

for key,val in gls_dict.items():
    print(f"{key} || total length: {len(val)} || unique length: {len(set(val))}\n{val}\n")