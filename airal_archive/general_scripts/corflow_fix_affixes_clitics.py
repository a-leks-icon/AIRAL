#Created: 2024-02-06
#Latest Version: 2024-02-06
#Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
#Corflow module created by François Delafontaine

from corflow import fromElan,toElan
#Uncomment, if the file 'corflow_additional_functions.py' is not in the same folder as this script but e.g. one folder above.
#import sys
#sys.path.append("../")
from corflow_additional_functions import find_tiers,fix_affixes_clitics
import glob

#Change paths accordingly to your directories.
input_path = "../../input_files/"
output_path = "../../output_files/"

eaf_files = glob.glob(input_path+"/*.eaf")
for file in eaf_files:
    file_name = file.replace(input_path,"")
    print(f"File: {file_name}")
    trans = fromElan.fromElan(file,encoding="utf-8")

    #Specify the name (regex) of the base tier or tiers you want to iterate over.
    mb_tier_name = ""

    for mb_tier in find_tiers(trans,mb_tier_name):

        #If you want to use the mb tier as a base and change e.g. all segments contents on one of its child tiers, specify the name (or a part of it) of the relevant child tier.
        gl_tier_name = ""

        for gl_tier in mb_tier.children():
            if gl_tier_name == gl_tier.name:
                fix_affixes_clitics(mb_tier,gl_tier,time=False) #Set time to False, if the gl_tier is the mb tiers child tier. If it is not, set time to True and the condition will be of time-alignment.

        #Else; just iterate once more to find the relevant tier. If the file has potentially multiple mb and gl tiers with an identical part in their names used to find them, this method here is not recommended.
            #for gl_tier in find_tiers(trans,gl_tier_name)

    #Saves the new eaf file.
    toElan.toElan(output_path+file_name,trans)
