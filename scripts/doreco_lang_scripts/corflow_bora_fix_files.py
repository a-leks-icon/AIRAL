# Created: 2023-06-08
# Latest Version: 2023-07-31
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

from corflow import fromElan, toElan
import glob
import sys
sys.path.append("../")
from corflow_additional_functions import define_content, fill_gaps_match

input_path = "../../input_files/"
output_path = "../../output_files/"

eaf_files = glob.glob(input_path+"/*.eaf")

for file in eaf_files:
    file_name = file.replace(input_path,"")
    trans = fromElan.fromElan(file,encoding="utf-8")

    #On the ps-, gl-, mb-, and mt-tier: Substitute '?' and/or '-?' for '****'.
    #define_content(trans,"ps@","****",cond=("ps@","?"))
    #define_content(trans,"ps@","****",cond=("ps@","-?"))
    #define_content(trans,"gl@","****",cond=("gl@","?"))
    #define_content(trans,"gl@","****",cond=("gl@","-?"))
    #define_content(trans,"mb@","****",cond=("mb@","?"))
    #define_content(trans,"mb@","****",cond=("mb@","-?"))
    #define_content(trans,"mt@","****",cond=("mt@","?"))
    #define_content(trans,"mt@","****",cond=("mt@","-?"))

    #On every tier: substitute '***' for '****'.
    for tier in trans:
        define_content(trans,(tier.name,"MATCH"),"****",cond=(tier.name,"MATCH","***"))
        define_content(trans,(tier.name,"MATCH"),"****",cond=(tier.name,"MATCH","-***"))
        define_content(trans,(tier.name,"MATCH"),"****",cond=(tier.name,"MATCH","endswith","N/A"))
        define_content(trans,(tier.name,"MATCH"),"****",cond=(tier.name,"MATCH","startswith","N/A"))
        define_content(trans,(tier.name,"MATCH"),"****",cond=(tier.name,"MATCH","?"))
        define_content(trans,(tier.name,"MATCH"),"****",cond=(tier.name,"MATCH","-?"))
        define_content(trans,(tier.name,"MATCH"),"****",cond=(tier.name,"MATCH","?-"))
        #define_content(trans,(tier.name,"MATCH"),"****",cond=(tier.name,"MATCH",""))

    #Fixing for every speaker and the respective gl-, mb-, and ps-tiers the clitic-sign, if the respective mt-tier was found having the content '-CLT'.
    other_tiers_to_manipulate = ["mb@","ps@","gl@"]
    print(file_name)
    for tier in trans:
        if tier.name.startswith("mt@"):
            for tier2 in trans:
                for tier_part_name in other_tiers_to_manipulate:
                    if tier2.name.startswith(tier_part_name):
                        if tier2.name.partition("@")[-1] == tier.name.partition("@")[-1]:
                            define_content(trans,(tier2.name,"MATCH"),("=","REPLACE_BY_INDEX",0),cond1=(tier.name,"MATCH","-CLT"),cond2=(tier2.name,"MATCH","startswith","-"))
                            define_content(trans,(tier2.name,"MATCH"),("=","ADD_TO_START"),cond1=(tier.name,"MATCH","-CLT"),cond2=(tier2.name,"MATCH","startswith","-",False),cond3=(tier2.name,"MATCH","startswith","=",False))
            define_content(trans,(tier.name,"MATCH"),"=CLT",cond=(tier.name,"MATCH","-CLT"))

    collected_tier_names = []
    for tier in trans:
        if tier.name.startswith("ntvr_"):
            collected_tier_names.append(tier.name)
            for tier2 in trans:
                if (tier2.name.startswith("mb@")) & (tier.name.partition("@")[-1] == tier2.name.partition("@")[-1]):
                    #collected_tier_names.append(tier2.name)
                    for tier3 in trans:
                        if (tier3.name.startswith("gl@")) & (tier2.name.partition("@")[-1] == tier3.name.partition("@")[-1]):
                            collected_tier_names.append(tier3.name)

                            define_content(trans,tier2.name,"ó",cond=(tier2.name,"o"))
                            define_content(trans,tier3.name,"1SG",cond1=(tier2.name,"ó"),cond2=(tier3.name,"how",False))
                            define_content(trans,tier2.name,("=","ADD_TO_END"),cond1=(tier2.name,"ó"),cond2=(tier.name,"startswith","BPN"))

                            define_content(trans,tier3.name,"2SG",cond=(tier3.name,"2.SG"))
                            define_content(trans,tier2.name,("=","ADD_TO_END"),cond1=(tier2.name,"u"),cond2=(tier3.name,"2SG"),cond3=(tier.name,"startswith","BPN"))

                            define_content(trans,tier2.name,"i=",cond1=(tier2.name,"i-"),cond2=(tier3.name,"3-"))

                            define_content(trans,tier2.name,"=va",cond1=(tier2.name,"-va"),cond2=(tier3.name,"-QUOT"))
                            define_content(trans,tier2.name,"=pe",cond1=(tier2.name,"-pe"),cond2=(tier3.name,"-REM"))
                            define_content(trans,tier2.name,"-úvu",cond1=(tier2.name,"=úvu"))

                            for tier4 in trans:
                                if (tier4.name.startswith("mt@")) & (tier4.name.partition("@")[-1] == tier3.name.partition("@")[-1]):
                                    collected_tier_names.append(tier4.name)
                                    for tier5 in trans:
                                        if (tier5.name.startswith("ps@")) & (tier5.name.partition("@")[-1] == tier2.name.partition("@")[-1]):
                                            define_content(trans,(tier2.name,"MATCH"),"=re",cond1=(tier2.name,"MATCH","-re"),cond2=(tier5.name,"MATCH","-cli"))
                                            collected_tier_names.append(tier5.name)

                                            #This operation searches for every instance of the gloss '=yet' and a previously occuring gloss 'finally' or 'wait'. It merges the contents of the time-aligned morphs and afterwards deletes the respective morph-gloss pair (the gloss "=yet" and ist manifestations e.g. '=iíkye'). Additionally, defining the content of the time-aligned segment on the t-tier being the same as the content of the time-aligned segment on the mb-tier.
                                            for gl_seg in tier3:
                                                if (gl_seg.content == "yet") | (gl_seg.content == "-yet") | (gl_seg.content == "=yet"):
                                                    if gl_seg.index() != 0:
                                                        if (tier3.elem[gl_seg.index()-1].content == "finally") | (tier3.elem[gl_seg.index()-1].content == "wait"):
                                                            if gl_seg.start == tier3.elem[gl_seg.index()-1].end:
                                                                for mb_seg in tier2:
                                                                    if (mb_seg.start == gl_seg.start) & (mb_seg.end == gl_seg.end):
                                                                        tier2.elem[mb_seg.index()-1].end = mb_seg.end
                                                                        tier2.elem[mb_seg.index()-1].content += mb_seg.content.replace("=","").replace("-","")
                                                                        tier3.elem[gl_seg.index()-1].end = gl_seg.end
                                                                        for tier_x in trans:
                                                                            for seg_x in tier_x:
                                                                                if seg_x.parent() == mb_seg:
                                                                                    tier_x.elem[seg_x.index()-1].end = seg_x.end
                                                                                    tier_x.pop(seg_x.index())
                                                                        tier2.elem[mb_seg.index()-1].parent().content = tier2.elem[mb_seg.index()-1].content
                                                                        tier2.pop(mb_seg.index())
                                                                            
                                            for tier_name in collected_tier_names:
                                                #For every child segment of every morph segment.

                                                #Substitute '-' for '=', if the mb seg has a '=':
                                                define_content(trans,(tier_name,"MATCH"),("=","REPLACE_BY_INDEX",0),cond1=(tier2.name,"startswith","="),cond2=(tier_name,"MATCH","startswith","-"))
                                                define_content(trans,(tier_name,"MATCH"),("=","REPLACE_BY_INDEX",-1),cond1=(tier2.name,"endswith","="),cond2=(tier_name,"MATCH","endswith","-"))

                                                #Substitute '=' for '-', if the mb seg has a '-':
                                                define_content(trans,(tier_name,"MATCH"),("-","REPLACE_BY_INDEX",0),cond1=(tier2.name,"startswith","-"),cond2=(tier_name,"MATCH","startswith","="))
                                                define_content(trans,(tier_name,"MATCH"),("-","REPLACE_BY_INDEX",-1),cond1=(tier2.name,"endswith","-"),cond2=(tier_name,"MATCH","endswith","="))

                                                #Add '-' to the segment, if the mb seg has a '-', but the former segment not.
                                                define_content(trans,(tier_name,"MATCH"),("-","ADD_TO_START"),cond1=(tier2.name,"startswith","-"),cond2=(tier_name,"MATCH","startswith","-",False),cond3=(tier_name,"MATCH","****",False))
                                                define_content(trans,(tier_name,"MATCH"),("-","ADD_TO_END"),cond1=(tier2.name,"endswith","-"),cond2=(tier_name,"endswith","-",False),cond3=(tier_name,"MATCH","****",False))

                                                #Add '=' to the segment, if the mb seg has a '=', but the former segment not.
                                                define_content(trans,(tier_name,"MATCH"),("=","ADD_TO_START"),cond1=(tier2.name,"startswith","="),cond2=(tier_name,"MATCH","startswith","=",False),cond3=(tier_name,"MATCH","****",False))
                                                define_content(trans,(tier_name,"MATCH"),("=","ADD_TO_END"),cond1=(tier2.name,"endswith","="),cond2=(tier_name,"MATCH","endswith","=",False),cond3=(tier_name,"MATCH","****",False))

                                                #For one found case
                                                define_content(trans,(tier_name,"MATCH"),("","REPLACE_BY_INDEX",0),cond=(tier_name,"MATCH","startswith","--"))

                                            #Fixing segments on the mt-, and ps-tier.
                                            define_content(trans,tier4.name,"CLT=",cond=(tier4.name,"ROOT="))

                                            define_content(trans,tier4.name,"-DRV",cond1=(tier4.name,"-CLT"),cond2=(tier2.name,"-úvu"))
                                            define_content(trans,(tier5.name,"MATCH"),"-nd",cond1=(tier5.name,"MATCH","-cli"),cond2=(tier2.name,"MATCH","-úvu"))

                                            #ps-tier clitics
                                            define_content(trans,(tier5.name,"MATCH"),"=cli",cond1=(tier2.name,"MATCH","startswith","="),cond2=(tier5.name,"MATCH","-cli"))
                                            define_content(trans,(tier5.name,"MATCH"),"cli=",cond=(tier2.name,"MATCH","endswith","="))
                                            define_content(trans,(tier5.name,"MATCH"),"=cli",cond=(tier2.name,"MATCH","startswith","="))

                                            #mt-tier clitics
                                            define_content(trans,(tier4.name,"MATCH"),"CLT=",cond=(tier2.name,"MATCH","endswith","="))
                                            define_content(trans,(tier4.name,"MATCH"),"=CLT",cond=(tier2.name,"MATCH","startswith","="))

                                            #Fixing cases, where certain morphs had time-aligned segments of '****', but which were clear to define as far as possible segment-combintions are concerned.
                                            #This was in the end not done, because Ludger said, that these are getting filled with content in the reinjection scripts anyway.
                                            #define_content(trans,(tier3.name,"MATCH"),"-FRUS",cond1=(tier2.name,"-ró"),cond2=(tier.name,"MATCH","endswith","=AFFIX"))
                                            #define_content(trans,(tier5.name,"MATCH"),"-vi",cond1=(tier2.name,"-ró"),cond2=(tier.name,"MATCH","endswith","=AFFIX"))
                                            #define_content(trans,(tier4.name,"MATCH"),"-INF",cond1=(tier2.name,"-ró"),cond2=(tier.name,"MATCH","endswith","=AFFIX"))

                                            #define_content(trans,(tier3.name,"MATCH"),"-CLF.place",cond1=(tier2.name,"MATCH","-tsi"),cond2=(tier4.name,"MATCH","-INF"),cond3=(tier.name,"MATCH","=AFFIX"))
                                            #define_content(trans,(tier5.name,"MATCH"),"-clf",cond1=(tier2.name,"MATCH","-tsi"),cond2=(tier4.name,"MATCH","-INF"),cond3=(tier.name,"MATCH","=AFFIX"))

                                            #define_content(trans,(tier3.name,"MATCH"),"-PRED",cond1=(tier2.name,"MATCH","-hí"),cond2=(tier.name,"MATCH","=AFFIX"))
                                            #define_content(trans,(tier5.name,"MATCH"),"-vi",cond1=(tier2.name,"MATCH","-hí"),cond2=(tier.name,"MATCH","=AFFIX"))
                                            #define_content(trans,(tier4.name,"MATCH"),"-INF",cond1=(tier2.name,"MATCH","-hí"),cond2=(tier.name,"MATCH","=AFFIX"))

                                            #define_content(trans,(tier3.name,"MATCH"),"-MULT.TR")



            #Fixing the ntvr-tier: No '=' are allowed.
            define_content(trans,(tier.name,"MATCH"),("-","REPLACE_BY_INDEX",0),cond=(tier.name,"MATCH","startswith","="))
            define_content(trans,(tier.name,"MATCH"),("-","REPLACE_BY_INDEX",-1),cond=(tier.name,"MATCH","endswith","="))
            define_content(trans,(tier.name,"MATCH"),"-AFFIX",cond=(tier.name,"MATCH","-AFFIXX"))
            define_content(trans,(tier.name,"MATCH"),"-AFFIX",cond=(tier.name,"MATCH","-0AFFIXX"))
            define_content(trans,(tier.name,"MATCH"),"OTHER",cond=(tier.name,"MATCH","OTHJER"))

    #Fore unknown reasons, one specific instance of '=AFFIX' in the file minga_2.eaf was not changed by the above function calls, therefore it had to be changed here. Maybe it had to do with some bad matching of tiers because of previous imprecision, but it stays here just in case.
    for tier in trans:
        if tier.name.startswith("ntvr_"):
            for seg in tier:
                if seg.content.startswith("="):
                    seg.content = seg.content.replace("=","-")

    #Lastly, filling gaps for certain morphs on the ps- and ntvr-tiers based on the content of the mb-tier.
    for mb_tier in trans:
        if mb_tier.name.startswith("mb@"):
            for mt_tier in trans:
                if mt_tier.name.startswith("mt@"):
                    if (mb_tier.name.partition("@")[-1]) == (mt_tier.name.partition("@")[-1]):
                        fill_gaps_match(trans,mb_tier.name,mt_tier.name,"=va","=CLT")
                        fill_gaps_match(trans,mb_tier.name,mt_tier.name,"=pe","=CLT")
                        fill_gaps_match(trans,mb_tier.name,mt_tier.name,"=re","=CLT")
                        fill_gaps_match(trans,mb_tier.name,mt_tier.name,"i=","CLT=")
                        fill_gaps_match(trans,mb_tier.name,mt_tier.name,"-híjcya","-INF")
                        fill_gaps_match(trans,mb_tier.name,mt_tier.name,"-háñe","-INF")
                        fill_gaps_match(trans,mb_tier.name,mt_tier.name,"-múpɨ","-INF")
                        fill_gaps_match(trans,mb_tier.name,mt_tier.name,"-ne","-INF")
                        fill_gaps_match(trans,mb_tier.name,mt_tier.name,"nahbe","ROOT")
                        #fill_gaps_match(trans,mb_tier.name,mt_tier.name,"ehdu","ROOT")
                        #nahbe
            for ntvr_tier in trans:
                if ntvr_tier.name.startswith("ntvr_"):
                    if (mb_tier.name.partition("@")[-1]) == (ntvr_tier.name.partition("@")[-1]):
                        fill_gaps_match(trans,mb_tier.name,ntvr_tier.name,"=va","-AFFIX")
                        fill_gaps_match(trans,mb_tier.name,ntvr_tier.name,"=pe","-AFFIX")
                        fill_gaps_match(trans,mb_tier.name,ntvr_tier.name,"=re","-AFFIX")
                        fill_gaps_match(trans,mb_tier.name,ntvr_tier.name,"i=","BPN-")
                        fill_gaps_match(trans,mb_tier.name,ntvr_tier.name,"-híjcya","-AFFIX")
                        fill_gaps_match(trans,mb_tier.name,ntvr_tier.name,"-háñe","-AFFIX")
                        fill_gaps_match(trans,mb_tier.name,ntvr_tier.name,"-múpɨ","-BPN")
                        fill_gaps_match(trans,mb_tier.name,ntvr_tier.name,"-ne","-AFFIX")
                        fill_gaps_match(trans,mb_tier.name,ntvr_tier.name,"nahbe","N")
                        #fill_gaps_match(trans,mb_tier.name,ntvr_tier.name,"ehdu","OTHER")


    toElan.toElan(output_path+file_name,trans)
