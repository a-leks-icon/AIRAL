# Created: May 2023
# Latest Version: 2023-05-17
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

'''
This script uses the define_content-function to fix some issues in the urum files: It changes the content of certain segments (annotations) based on a variety of conditions of the contn of time-aligned segments of other tiers.
'''

from corflow import fromElan,toElan
import glob
import sys
sys.path.append("../")
from corflow_additional_functions import define_content, fix_affixes

path = "../../input_files/"

eaf_files = glob.glob(path+"/*.eaf")

for file in eaf_files:
    file_name = file.replace(path,"")
    #print(file_name)
    trans = fromElan.fromElan(file,encoding="utf-8")

    #Simple replacements

    define_content(trans,("ge@unknown","MATCH"),("","REPLACE_BY_SIGN","-THM"),cond=("ge@unknown","MATCH","-THM","IN"))
    define_content(trans,("ge@unknown","MATCH"),"coming",cond=("ge@unknown","MATCH","comming"))
    define_content(trans,("ge@unknown","MATCH"),"-until",cond=("ge@unknown","MATCH","-untill"))
    define_content(trans,("ge@unknown","MATCH"),"come",cond=("ge@unknown","MATCH","-come"))
    define_content(trans,("ge@unknown","MATCH"),"go",cond=("ge@unknown","MATCH","-go"))
    define_content(trans,("ge@unknown","MATCH"),"live",cond=("ge@unknown","MATCH","-live"))
    define_content(trans,("ge@unknown","MATCH"),"do",cond=("ge@unknown","MATCH","-do"))
    define_content(trans,("mb@unknown","MATCH"),"yaša",cond=("mb@unknown","MATCH","yaš-a"))
    define_content(trans,("mb@unknown","MATCH"),"ed",cond=("mb@unknown","MATCH","-ed"))

    #More complex replacements

    define_content(trans,("ge@unknown","MATCH"),"what",cond=("mb@unknown","MATCH","nä"))
    define_content(trans,("ps@unknown","MATCH"),"PN",cond=("mb@unknown","MATCH","nä"))

    define_content(trans,("mb@unknown","MATCH"),"näbl",cond=("mb@unknown","MATCH","nä-bl"))
    define_content(trans,("ps@unknown","MATCH"),"V",cond=("mb@unknown","MATCH","nä-bl"))
    define_content(trans,("ge@unknown","MATCH"),"not_know",cond=("mb@unknown","MATCH","nä-bl"))

    define_content(trans,("ge@unknown","MATCH"),("-","ADD_TO_START"),cond1=("ps@unknown","MATCH","-prs"),cond2=("ge@unknown","MATCH","startswith","-",False))

    define_content(trans,("ge@unknown","MATCH"),"NEG.EXIST",cond=("mb@unknown","MATCH","yoh"))

    define_content(trans,("ge@unknown","MATCH"),"-ACC",cond=("ge@unknown","MATCH","ACC")) # Maybe we just use the fix_affixes function instead.

    define_content(trans,("ge@unknown","MATCH"),"-PST",cond=("ge@unknown","MATCH","PST")) # Maybe we just use the fix_affixes function instead.

    define_content(trans,("ge@unknown","MATCH"),("","REPLACE_BY_INDEX",0),cond1=("ps@unknown","MATCH","PN"),cond2=("ge@unknown","MATCH","startswith","-"))

    define_content(trans,("ge@unknown","MATCH"),("","REPLACE_BY_INDEX",0),cond1=("ps@unknown","MATCH","-N"),cond2=("ge@unknown","MATCH","-Tsalka"))
    define_content(trans,("ps@unknown","MATCH"),("","REPLACE_BY_INDEX",0),cond1=("ps@unknown","MATCH","-N"),cond2=("ge@unknown","MATCH","Tsalka"))

    define_content(trans,("ge@unknown","MATCH"),"be",cond1=("mb@unknown","MATCH","var"),cond2=("ps@unknown","MATCH","V"))

    define_content(trans,("mb@unknown","MATCH"),("=","REPLACE_BY_INDEX",0),cond1=("ps@unknown","MATCH","-C"),cond2=("mb@unknown","MATCH","startswith","-"))
    define_content(trans,("ge@unknown","MATCH"),("=","REPLACE_BY_INDEX",0),cond1=("ps@unknown","MATCH","-C"),cond2=("ge@unknown","MATCH","startswith","-"))
    define_content(trans,("ps@unknown","MATCH"),"=C",cond=("ps@unknown","MATCH","-C"))

    define_content(trans,("ge@unknown","MATCH"),"****",cond=("ge@unknown","MATCH","xxx"))
    define_content(trans,("ps@unknown","MATCH"),"****",cond=("ps@unknown","MATCH","xxx"))
    define_content(trans,("ge-a@unknown","MATCH"),("****","REPLACE_BY_SIGN","xxx"),cond=("ge-a@unknown","MATCH","xxx","IN"))
    define_content(trans,("ft@unknown","MATCH"),("****","REPLACE_BY_SIGN","xxx"),cond=("ft@unknown","MATCH","xxx","IN"))

    fix_affixes(trans,"ge@unknown","mb@unknown")
    fix_affixes(trans,"mb@unknown","ge@unknown")

    toElan.toElan("../../output_files/"+str(file_name),trans)