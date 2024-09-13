# Created: May 2023
# Latest Version: 2023-06-07
# Script written by Michelle Elizabeth Throssell Balagué as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

import os
import re
from corflow import fromElan, toElan

folder_path = "../../input_files/"
output_folder_path = "../../output_files/"

# Loop over all files in the input folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".eaf"):
        input_file_path = os.path.join(folder_path, file_name)
        output_file_path = os.path.join(output_folder_path, file_name)
        
        # Load the transcription from the input file
        trans = fromElan.fromElan(input_file_path, encoding="utf-8")

        # Get the grammatical_words_mtok and gloss_mtok tiers
        mb_tier = trans.getName("grammatical_words_mtok")
        gl_tier = trans.getName("gloss_mtok")

        if mb_tier is None:
            print(f"Error: grammatical_words_mtok tier not found in {file_name}")
            continue
        
        # Add ~ to the corresponding morph of RED~ glosses
        for i in gl_tier:
            if re.search(".+~", i.content):
                for n in mb_tier:
                    if (i.start == n.start) & (i.end == n.end):
                        if not n.content.endswith("~"):
                            n.content += "~"

        # Save the modified transcription to the output file
        toElan.toElan(output_file_path, trans)

