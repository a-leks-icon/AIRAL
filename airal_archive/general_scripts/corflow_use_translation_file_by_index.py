# Created: 2023-06-03
# Latest Version: 2023-06-03
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

'''
Script description:

The following script takes a txt-file with translation-values (encoded as a line starting with '\tre') and assigns those to the content of their respective segments on the translation-tier by index.
'''

from corflow import fromElan, toElan

#The path of the txt-file and eaf-file.
input_path = "../../input_files/"

#The path where the new eaf-file will be saved.
output_path = "../../output_files/"


#The respective file names:
txt_file = "JuanFlojo_tre_format_modified.txt"
eaf_file = "JuanFlojo.eaf"

#Loading the txt-file and saving the translation values in a list for those cases, where a segment on the translation tier exists (this is checked by searching for lines starting with a specific string; see below). The lenght of the list must match the length of the translation tier in the eaf-file, otherwise the actual operation won't work properly.
with open(input_path+txt_file,"r") as translation:
    translation_lines = []
    block_exists = False
    for line in translation.readlines():
        if line.startswith("\\rf Juan Flojo"):
            block_exists = True
        if line.startswith("\\tre") & block_exists:
            translation_lines.append(line[5:].replace("\n",""))
            block_exists = False


'''
#I used the following code block to repair the txt-file with the translations manually via regex patterns. It was "damaged" in the first place because of how newlines were formatted, which was not recognized by visual studio code. Therefore, I had to use Regex in order to create these linebreaks and apparently created some errors in the structure of the files content.

with open(main_path+txt_file,"r") as translation:
    translation_lines = []
    tre_line_number = 18
    for number,line in enumerate(translation.readlines()):
        if number == tre_line_number:
            tre_line_number += 8
            if not line.startswith("\\tre"):
                print(number)

'''

trans = fromElan.fromElan(input_path+eaf_file,encoding="utf-8")

for tier in trans:
    if "tre" in tier.name:
        for index,tre_seg in enumerate(tier):
            tre_seg.content = translation_lines[index]

toElan.toElan(output_path+eaf_file,trans)
