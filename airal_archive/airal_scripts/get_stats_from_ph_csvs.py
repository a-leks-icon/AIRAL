#Created: 2024-04-04
#Latest Version: 2024-04-05
#Script written by Aleksandr Schamberger (GitHub: JLEKS) as part of the AIRAL project by Ludger Paschen at ZAS Berlin.

'''This script iterates over every ph.csv file in the input folder and creates a new txt file in the output folder, which contains useful, statistical data about each ph-csv file's data. Those data contain a) the token frequency of all glosses, morphs, pos tags and words, as well as b) an ordered list of every morph, pos and word type a gloss type occures as.'''

import pandas as pd
import numpy as np
import os

#Paths and file directory.
input_path = "../../input_files/"
output_path = "../../output_files/"

for file in os.listdir(input_path):
    print(f"\nRead file: {file}")
    file_out = file.removesuffix(".csv")
    txt_file_name = file_out+"_output.txt"
    if txt_file_name in os.listdir(output_path):
        print(f"txt file already generated. Skip file.")
        continue

    #Read ph.csv file and create a data frame with only the desired columns.
    df = pd.read_csv(input_path+file,header=0)
    print(f"df1: {df}")
    df = df.loc[:,["wd","mb_ID","mb","ps","gl"]]
    print(f"df2: {df}")


    #Remove columns with NaN values.
    #df.dropna(axis=1,inplace=True,how="all")

    if all(df["gl"].isna()):
        print(f"csv file has no gloss data. Skip file.")
        continue

    #Iterate and remove rows with the same morph id.
    drop_rows = []
    for ind in range(len(df)-1):
        cell1 = df.at[ind,"mb_ID"]
        cell2 = df.at[ind+1,"mb_ID"]
        if cell1 == cell2:
            drop_rows.append(ind+1)
    df.drop(drop_rows,inplace=True)

    #Replace NaN values (here: empty cells) with None.
    df = df.replace(np.nan,"NONE")

    print(f"Get statistics.")
    #Iterate over every gl type and its mb, ps and wd types it corresponds with.
    gl_types = list(set(df["gl"]))
    gl_dict = {}
    for gl in gl_types:
        gl_tok_freq = len(df[df["gl"] == gl])
        mb_dict = {}
        mb_types = list(set(df[df["gl"] == gl]["mb"]))
        for mb in mb_types:
            mb_tok_freq = len(df[(df["gl"] == gl) & (df["mb"] == mb)])
            ps_dict = {}
            ps_types = list(set(df[(df["gl"] == gl) & (df["mb"] == mb)]["ps"]))
            for ps in ps_types:
                ps_tok_freq = len(df[(df["gl"] == gl) & (df["mb"] == mb) & (df["ps"] == ps)])
                #Comment out lines 63 to 67, if statistics only up to pos-tags should be collected and displayed.
                wd_dict = {}
                wd_types = list(set(df[(df["gl"] == gl) & (df["mb"] == mb) & (df["ps"] == ps)]["wd"]))
                for wd in wd_types:
                    wd_tok_freq = len(df[(df["gl"] == gl) & (df["mb"] == mb) & (df["ps"] == ps) & (df["wd"] == wd)])
                    wd_dict[wd] = [wd_tok_freq]
                ps_dict[ps] = [ps_tok_freq,wd_dict]
            mb_dict[mb] = [mb_tok_freq,ps_dict]
        gl_dict[gl] = [gl_tok_freq,mb_dict]

    #Print the statistics.
    gls_sorted = sorted([(freq[0],gl) for gl,freq in gl_dict.items()],reverse=True)

    txt_content = []
    for freq_gl,gl in gls_sorted:
        txt_content.append(f"gl: {gl} | freq: {freq_gl}\n")
    txt_content.append("\n\n\n")

    for freq_gl,gl in gls_sorted:
        txt_content.append(f"gl: {gl} | freq: {freq_gl}\n")
        mb_dict = gl_dict[gl][1]
        mbs_sorted = sorted([(freq[0],mb) for mb,freq in mb_dict.items()],reverse=True)
        for freq_mb,mb in mbs_sorted:
            txt_content.append(f"\tmb: {mb} | freq: {freq_mb}\n")
            ps_dict = mb_dict[mb][1]
            pss_sorted = sorted([(freq[0],ps) for ps,freq in ps_dict.items()],reverse=True)
            for freq_ps,ps in pss_sorted:
                txt_content.append(f"\t\tps: {ps} | freq: {freq_ps}\n")
                #Comment out lines 91 to 94, if statistics only up to pos-tags should be collected and displayed.
                wd_dict = ps_dict[ps][1]
                wds_sorted = sorted([(freq[0],wd) for wd,freq in wd_dict.items()],reverse=True)
                for freq_wd,wd in wds_sorted:
                    txt_content.append(f"\t\t\twd: {wd} | freq: {freq_wd}\n")
        #txt_content.append("\n")

    print(f"Save txt file.\n###")
    #Save statistics in a txt file.
    with open(output_path+txt_file_name,"w") as file:
        for line in txt_content:
            file.write(line)