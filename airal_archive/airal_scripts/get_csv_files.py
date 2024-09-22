#Created: 2024-04-04
#Latest Version: 2024-04-04
#Script written by Aleksandr Schamberger (GitHub: JLEKS) as part of the AIRAL project by Ludger Paschen at ZAS Berlin.

'''This script goes through every subfolder in the '70_Results' folder (except for 'Old_DoReCo1dot2', which has to be removed manually before excecuting the script) and copies all ph.csv files into the output folder.'''

import os

input_path = "../../input_files/"
output_path = "../../output_files/"

for root,dirs,files in os.walk(input_path):
    for file in files:
        if file.endswith("ph.csv"):
            os.popen(f"cp {root+'/'+file} {output_path+file}")
            print(f"copied file: {file}")