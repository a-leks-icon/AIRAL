#Created: 2024-02-24
#Latest Version: 2024-02-24
#Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
#Corflow module created by François Delafontaine

from corflow import fromElan, toElan
import glob

input_path = "../../input_files/"
output_path = "../../output_files/"
eaf_files = glob.glob(input_path+"/*.eaf")
for file in eaf_files:
    file_name = file.replace(input_path,"")
    print(f"File: {file_name}")

    try:
        trans = fromElan.fromElan(file,encoding="utf-8")
        print("Import Works!")
    except:
        print("XML ERROR!")
    try:
        toElan.toElan(output_path+file_name,trans)
        print("Import and Export work!")
    except:
        print("corflow ERROR")
