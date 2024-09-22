# Created: 2023-05-26
# Latest Version: 2023-06-08
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

from corflow import fromElan,toElan
import glob
import sys
sys.path.append("../")
from corflow_additional_functions import define_content

path="../../input_files/"
eaf_files = glob.glob(path+"/*.eaf")

#These custom created functions enabled to check for conditions more easily. But because the respective function calls were commented out, they became useless.
'''

def pos_check_1(pos_segment):
    pos_content_list = ["vai-", "vai.incorp-", "vai.rel-", "na-", "vta-", "vti-", "vii-", "vai.pass-", "prefix.vti-"]
    if pos_segment in pos_content_list:
        return True
    else:
        return False

def pos_check_2(pos_segment):
    pos_content_list = ["-vta", "-vai", "-vai.impers", "-na"]
    if pos_segment in pos_content_list:
        return True
    else:
        return False

'''

for file in eaf_files:
    file_name = file.replace(path,"")

    trans = fromElan.fromElan(file,encoding="utf-8")

    #Global replacements

    define_content(trans,"ps@","****",cond=("ps@",""))
    define_content(trans,"ps@","****",cond=("ps@","-"))
    define_content(trans,"ps@","****",cond=("ps@","???","IN"))
    define_content(trans,"ge@","****",cond=("ge@",""))
    define_content(trans,"ge@","****",cond=("ge@","-"))
    define_content(trans,"ge@","****",cond=("ge@","???","IN"))

    #define_content(trans,"ps@","-deriv",cond=("ps@","deriv"))
    #define_content(trans,"ge@",("-","ADD_TO_START"),cond1=("ps@","-deriv"),cond2=("ge@","startswith","-",False))
    #define_content(trans,"mb@",("-","ADD_TO_START"),cond1=("ps@","-deriv"),cond2=("mb@","startswith","-",False))

    #Special cases

    #define_content(trans,"ps@","part.adv",cond=("ps@",".adv"))
    #define_content(trans,"ps@","vai.recip",cond=("ps@","vai.reci["))
    #define_content(trans,"ps@","-infl",cond=("ps@","-in"))
    #define_content(trans,"ps@","-infl",cond=("ps@","- infl"))
    #define_content(trans,"ps@","****",cond=("ps@","3i'otox"))
    #define_content(trans,"ps@","****",cond=("ps@","3ou3oxuusuu"))
    #define_content(trans,"ge@","****",cond=("ge@","3i'otox"))
    #define_content(trans,"ge@","****",cond=("ge@","3ou3oxuusuu"))

    #define_content(trans,"pe@","prefix-",cond1=("pe@","****"),cond2=("mb@","co'-"),cond3=("ge@","again-"))

    #define_content(trans,"ge@",("","REPLACE_BY_INDEX",-1),cond1=("ge@","endswith","-"),cond2=("ps@",pos_check_1))
    #define_content(trans,"mb@",("","REPLACE_BY_INDEX",-1),cond1=("mb@","endswith","-"),cond2=("ps@",pos_check_1))
    #define_content(trans,"ps@",("","REPLACE_BY_INDEX",-1),cond=("ps@",pos_check_1))

    #define_content(trans,"ge@",("","REPLACE_BY_INDEX",0),cond1=("ge@","startswith","-"),cond2=("ps@",pos_check_2))
    #define_content(trans,"mb@",("","REPLACE_BY_INDEX",0),cond1=("mb@","startswith","-"),cond2=("ps@",pos_check_2))
    #define_content(trans,"ps@",("","REPLACE_BY_INDEX",0),cond=("ps@",pos_check_2))

    #define_content(trans,"ge@",("-","ADD_TO_END"),cond1=("ge@","endswith","-",False),cond2=("ps@","prefix.prefix"))
    #define_content(trans,"mb@",("-","ADD_TO_END"),cond1=("mb@","endswith","-",False),cond2=("ps@","prefix.prefix"))
    define_content(trans,"ps@","prefix.prefix-",cond=("ps@","prefix.prefix"))

    #define_content(trans,"ps@","vai",cond=("ge@","six-"))
    #define_content(trans,"mb@",("","REPLACE_BY_INDEX",-1),cond1=("mb@","endswith","-"),cond2=("ge@","six-"))
    #define_content(trans,"ge@","six",cond=("ge@","six-"))

    #define_content(trans,"ge@",("","REPLACE_BY_INDEX",0),cond=("ps@","startswith","-na"))
    #define_content(trans,"mb@",("","REPLACE_BY_INDEX",0),cond=("ps@","startswith","-na"))
    #define_content(trans,"ps@",("","REPLACE_BY_INDEX",0),cond=("ps@","startswith","-na"))

    #Changing 'proclitic-' to 'proclitic=' and also substituting the dashes by equal signs for all time-aligned segments on the moprh-, and gloss-tier.

    define_content(trans,"mb@",("=","REPLACE_BY_INDEX",-1),cond1=("ps@","proclitic-"),cond2=("mb@","endswith","-"))
    define_content(trans,"ge@",("=","REPLACE_BY_INDEX",-1),cond1=("ps@","proclitic-"),cond2=("ge@","endswith","-"))

    define_content(trans,"mb@",("=","ADD_TO_END"),cond1=("ps@","proclitic-"),cond2=("mb@","endswith","-",False),cond3=("mb@","endswith","=",False))
    define_content(trans,"geb@",("=","ADD_TO_END"),cond1=("ps@","proclitic-"),cond2=("ge@","endswith","-",False),cond3=("ge@","endswith","=",False))

    define_content(trans,"ps@","proclitic=",cond=("ps@","proclitic-"))

    define_content(trans,"ge@",("=","REPLACE_BY_INDEX",-1),cond1=("ps@","proclitic/part-"),cond2=("mb@","ci'-"),cond3=("ge@","endswith","-"))

    toElan.toElan("../../output_files/"+str(file_name),trans)