#Created: 2024-03-22
#Latest Version: 2024-03-22
#Script written by Aleksandr Schamberger (GitHub: JLEKS) as part of the AIRAL project by Ludger Paschen at ZAS Berlin.

import pandas as pd

input_path = "../../input_files/"
file = input_path + "doreco_dolg1241_ph.csv"

df = pd.read_csv(file)
unique_gls = sorted(set(df["gl"]))
gl_dict = {}
for gl in unique_gls:
    gl_tok_freq = len(df[df["gl"] == gl])
    mb_dict = {}
    unique_mbs = list(set(df[df["gl"] == gl]["mb"]))
    for mb in unique_mbs:
        mb_tok_freq = len(df[(df["gl"] == gl) & (df["mb"] == mb)])
        ps_dict = {}
        unique_ps = sorted(set(df[(df["gl"] == gl) & (df["mb"] == mb)]["ps"]))
        for ps in unique_ps:
            ps_tok_freq = len(df[(df["gl"] == gl) & (df["mb"] == mb) & (df["ps"] == ps)])
            wd_dict = {}
            unique_wds = sorted(set(df[(df["gl"] == gl) & (df["mb"] == mb) & (df["ps"] == ps)]["wd"]))
            for wd in unique_wds:
                wd_tok_freq = len(df[(df["gl"] == gl) & (df["mb"] == mb) & (df["ps"] == ps) & (df["wd"] == wd)])
                wd_dict[wd] = [wd_tok_freq]
            ps_dict[ps] = [ps_tok_freq,wd_dict]
        mb_dict[mb] = [mb_tok_freq,ps_dict]
    gl_dict[gl] = [gl_tok_freq,mb_dict]


for gl,gl_val in gl_dict.items():
    print(f"gl: {gl} | freq: {gl_val[0]}")

print("\n\n")

for gl,gl_val in gl_dict.items():
    print(f"gl: {gl} | freq: {gl_val[0]}")
    mbs: dict = gl_val[1]
    for mb,mb_val in mbs.items():
        print(f"\tmb: {mb} | freq: {mb_val[0]}")
        pss: dict = mb_val[1]
        for ps,ps_val in pss.items():
            print(f"\t\tps: {ps} | freq: {ps_val[0]}")
            wds: dict = ps_val[1]
            for wd,wd_val in wds.items():
                print(f"\t\t\twd: {wd} | freq: {wd_val[0]}")



