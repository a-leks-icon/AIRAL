# Created: March 2023
# Latest Version: 2023-05-16
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

'''
This script i) applies the 'fill_gaps'-function (and the 'define_content'-function and similar ones) a number of times to all eaf-files (for the 'Gubeeher' language) in the relative path "../../input_files/" to this script and saves them in the relative path "../../output_files/", and ii) applies the 'fix_affixes'-function to all eaf-files in the relative path "../output_files/" to this script (as well as the functions 'remove_segment') and saves the result again in the relative path "../../output_files/" to this script.

As an example for the fill_gaps-function, the first called function does the following: It adds a time-aligned segment with the content "return" on the tier whose name contains the string "morph-gls-en" for every segment with the content "ŋey" (which has no corresponding, time-aligned segment on the tier whose name contains the string "morph-gls-en") on the tier whose name contains the string "morph-txt".

The manipulated file is saved to the relative path "../../output_file/" to this script.
'''

from corflow import fromElan,toElan
import glob
import sys
sys.path.append("../")
from corflow_additional_functions import fill_gaps, fix_affixes, remove_segments, define_content_old_version, define_content

path="../../input_files/"
list_of_files = glob.glob(path+"/*.eaf")

for d in list_of_files:
    file_name = d.replace(path,"")
    print(file_name)
    trans = fromElan.fromElan(d,encoding="utf-8")

    #Exactly one gloss-type is assigned to a morph-type with at least one gap: The gloss-type is more than once assigned to the respective morph-type with a gap:

    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","n-","Pl")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","saat","pass")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","jir","run")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","nëër","give")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","këëb","chew")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","mundum","hyena")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","ra","do")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","ye","do")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","-ne","Sub")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","tuma","story")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","-hënito","1Pl.incl.Poss")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","e-","Cl.e")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","m-","Pl")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","jop","take")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","góóm","central branch of ronier")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","yax","hit")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","tëëd","cook")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","yah","hit")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","naak","two")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","doxo","work")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","-ox","Hab")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","gini","Rel")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","d-","Neg:Fut")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","ŋei","return")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","mër","Pron")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","naaf","cultivate")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","bo","AUX")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","ta-","Agr.ta")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","lal","three")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","yen","say")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","-oonuŋ","2Pl.Obj")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","lah","take, grasp")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","lamba","boy")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","-ya","Refl")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","lika","stand")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","-eenen","3Pl.Obj")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","sin-","Cl.sin")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","dél","reach")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","ba","almost do sth.")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","-kum","1SgPoss")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","dén","put")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","honj","thing")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","-hén","2SgPoss")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","-ni","Sub")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","hun","pound")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","-gëni","Rel")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","ceek","side")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","lall","three")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","ya","hit")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","yit","know")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","naaŋ","there")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","laat","-ever")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","ceŋg","get up")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","-uh","Pass.Hab")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","miñ","last")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","tooxul","cut")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","gëni","Rel")

    #Exactly one gloss-type is assigned to a morph-type with at least one gap: The gloss-type is only once assigned to the respective morph-type with a gap:

    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","ŋaari","shut up")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","tuc","throw")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","duf","draw water")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","miix","ask")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","tobor","Tobor")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","-x","Hab")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","maregen","truth")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","bëër","butter")

    #More than one different gloss-type gets assigned to a morph-type with a gap

    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","ŋey","return")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","lax","take, grasp")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","-em","3Sg.Obj")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","gu","be")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","ni","Rel")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","-ëx","Hab")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","ë","Prep")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","xëëb","chew")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","-ëŋ","2Pl")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","de","Emph")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","a","Prep")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","diigén","man")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","tib","look for")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","lób","speak")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","liix","first")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","-ux","Pass.Hab")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","kë-","Agr.kan")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","-eŋ","Pl")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","noox","sit")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","-i","Perf")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","ruk","some")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","im-","Foc.Subj")

    #No glosses at all get assigned to a morph-type with a gap

    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","ummu","Agr.u:Dem.Prox")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","iŋko","Agr.ko:Loc")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","kën-","Loc-")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","rendek","four")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","Manga","PN")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","haam","new")
    fill_gaps(trans,"morph-txt-qaa","morph-gls-en","poom","basket")

    #Unify glosses:

    define_content_old_version(trans,"morph-txt-qaa","morph-gls-en","kë-","Agr.kan","Agr. kan")
    define_content_old_version(trans,"morph-txt-qaa","morph-gls-en","ruk","some","one")
    define_content_old_version(trans,"morph-txt-qaa","morph-gls-en","im-","Foc.Subj","Foc.Sbj")

    #Fix bad morphological structures: structures without a stem

    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","gun",["gu-","n"],["gu-","-n"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","bun",["bu-","n"],["bu-","-n"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","jën",["jë-","n"],["jë-","-n"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","bën",["bë-","n"],["bë-","-n"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","bin",["bi-","n"],["bi-","-n"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","ën",["ë-","n"],["ë-","-n"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","un",["u-","n"],["u-","-n"])

    define_content_old_version(trans,"word-txt-qaa","morph-type","gun",["prefix","stem"],["prefix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","bun",["prefix","stem"],["prefix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","jën",["prefix","stem"],["prefix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","bën",["prefix","stem"],["prefix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","bin",["prefix","stem"],["prefix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","ën",["prefix","stem"],["prefix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","un",["prefix","stem"],["prefix","suffix"])

    #Fix bad morphological structures: structures with a prefix after a stem

    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","gafuttox",["g-", "a-", "fu", "-tt", "-ox"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","guloboh",["g-", "u-", "lob", "-oh"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","gëtéba",["g-", "ë-", "téb", "-a"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","gaanohuma",["ga-", "a-", "noh", "-um", "-a"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","galohonoŋ",["g-", "a-", "loh", "-onoŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","gayiti",["g-", "a-", "yit", "-i"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","gataakah",["g-", "a-", "taak", "-ah"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","gataakane",["g-", "a-", "taak", "-a", "-ne"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","gamukuna",["g-", "a-", "mukuna"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","gëfutohne",["g-", "ë-", "fu", "-t", "-oh", "-ne"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","giyégeh",["g-", "i-", "yég", "-eh"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","gibifex",["g-", "i-", "bif", "-ex"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","gahay",["g-", "a-", "hay"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","galax",["g-", "a-", "lax"])

    define_content_old_version(trans,"word-txt-qaa","morph-type","gafuttox",["prefix", "prefix", "stem", "suffix", "suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","guloboh",["prefix", "prefix", "stem", "suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","gëtéba",["prefix", "prefix", "stem", "suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","gaanohuma",["prefix", "prefix", "stem", "suffix", "suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","galohonoŋ",["prefix", "prefix", "stem", "suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","gayiti",["prefix", "prefix", "stem", "suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","gataakah",["prefix", "prefix", "stem", "suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","gataakane",["prefix", "prefix", "stem", "suffix", "suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","gamukuna",["prefix", "prefix", "stem"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","gëfutohne",["prefix", "prefix", "stem", "suffix", "suffix", "suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","giyégeh",["prefix", "prefix", "stem", "suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","gibifex",["prefix", "prefix", "stem", "suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","gahay",["prefix", "prefix", "stem"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","galax",["prefix", "prefix", "stem"])


    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","imbuŋ",["im","-bu","-ŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","innuŋ",["inn","-u","-ŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","imbaŋ",["im","-ba","-ŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","iññoŋ",["iñ","-ño","-ŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","innoŋ",["inn","-o","-ŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","iŋgoŋ",["iŋ","-go","-ŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","inoŋ",["in","-o","-ŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","imboŋ",["im","-bo","-ŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","iŋkoŋ",["iŋ","-ko","-ŋ"])

    define_content_old_version(trans,"word-txt-qaa","morph-type","imbuŋ",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","innuŋ",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","imbaŋ",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","iññoŋ",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","innoŋ",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","iŋgoŋ",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","inoŋ",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","imboŋ",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","iŋkoŋ",["stem","suffix","suffix"])


    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","imbooŋ",["im" ,"-boo" ,"-ŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","iŋgooŋ",["iŋ" ,"-goo" ,"-ŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","innooŋ",["inn" ,"-oo" ,"-ŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","iŋkoona",["iŋ" ,"-koo" ,"-na"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","imbam",["im" ,"-ba" ,"-m"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","imbum",["im" ,"-bu" ,"-m"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","imbana",["im" ,"-ba" ,"-na"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","imboom",["im" ,"-boo" ,"-m"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","immoona",["im" ,"-moo" ,"-na"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","iŋkoona",["iŋ" ,"-koo" ,"-na"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","inseeŋ",["in" ,"-see" ,"-ŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","iŋkoŋ",["iŋ" ,"-ko" ,"-ŋ"])

    define_content_old_version(trans,"word-txt-qaa","morph-type","imbooŋ",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","iŋgooŋ",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","innooŋ",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","iŋkoona",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","imbam",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","imbum",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","imbana",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","imboom",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","immoona",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","iŋkoona",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","inseeŋ",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","iŋkoŋ",["stem","suffix","suffix"])


    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","minu",["m-", "in", "-u"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","miinu",["m-", "iin", "-u"])

    define_content_old_version(trans,"word-txt-qaa","morph-type","minu",["prefix","stem","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","miinu",["prefix","stem","suffix"])
    

    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","minnoŋ",["m-", "inn", "-o", "-ŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","minoŋ",["m-", "in", "-o", "-ŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","miinoŋ",["m-", "iin", "-o", "-ŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","minooŋ",["m-", "in", "-oo", "-ŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","miŋguna",["m-", "iŋ", "-gu", "-na"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","mineemin",["m-", "in", "-ee", "-min"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","miéni",["m-", "i", "-én", "-i"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","miyéni",["m-", "i", "-yén", "-i"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","minuŋoon",["m-", "in", "-u", "-ŋ", "-oon"])


    define_content_old_version(trans,"word-txt-qaa","morph-type","minnoŋ",["prefix","stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","minoŋ",["prefix","stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","miinoŋ",["prefix","stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","minooŋ",["prefix","stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","miŋguna",["prefix","stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","mineemin",["prefix","stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","miéni",["prefix","stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","miyéni",["prefix","stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","minuŋoon",["prefix", "stem", "suffix", "suffix", "suffix"])


    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","inno",["inn", "-o"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","innu",["inn", "-u"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","imba",["im", "-ba"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","imbu",["im", "-bu"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","ummu",["umm", "-u"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","inja",["in", "-ja"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","iŋgu",["iŋ", "-gu"])

    define_content_old_version(trans,"word-txt-qaa","morph-type","inno",["stem","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","innu",["stem","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","imba",["stem","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","imbu",["stem","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","ummu",["stem","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","inja",["stem","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","iŋgu",["stem","suffix"])


    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","innoŋoŋ",["in", "-no", "-ŋ", "-oŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","iniŋeen",["in", "-i", "-ŋ", "-een"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","inoombim",["in", "-oo", "-m", "-bim"])

    define_content_old_version(trans,"word-txt-qaa","morph-type","innoŋoŋ",["stem","suffix","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","iniŋeen",["stem","suffix","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","inoombim",["stem","suffix","suffix","suffix"])


    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","ihobim",["i", "-ho", "-bim"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","iŋkot",["iŋ", "-ko", "-t"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","iññoño",["iñ", "-ño", "-ño"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","innom",["inn", "-o", "-m"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","inoona",["in", "-oo", "-na"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","inona",["in", "-o", "-na"])

    define_content_old_version(trans,"word-txt-qaa","morph-type","ihobim",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","iŋkot",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","iññoño",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","innom",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","inoona",["stem","suffix","suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","inona",["stem","suffix","suffix"])


    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","finooŋ",["f-", "in", "-oo", "-ŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","umayenem",["u-", "m-", "a-", "yen", "-em"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","jinjeeŋ",["ji-", "n", "-j", "-eeŋ"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","iŋkokona",["iŋ", "-ko", "-ko", "-na"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","iŋko koni",["iŋ", "-ko", "-ko", "-ni"])



    define_content_old_version(trans,"word-txt-qaa","morph-type","finooŋ",["prefix", "stem", "suffix", "suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","umayenem",["prefix", "prefix", "prefix", "stem", "suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","jinjeeŋ",["prefix", "stem", "suffix", "suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","iŋkokona",["stem", "suffix", "suffix", "suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","iŋkokoni",["stem", "suffix", "suffix", "suffix"])


    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","n'ëguni",["n'-", "ë-", "gu", "-ni"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","n'ayene",["n'-", "a-", "ye", "-ne"])
    define_content_old_version(trans,"word-txt-qaa","morph-txt-qaa","n'ubirenne",["n'-", "u-", "bir", "-en", "-en"])

    define_content_old_version(trans,"word-txt-qaa","morph-type","n'ëguni",["prefix", "prefix", "stem", "suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","n'ayene",["prefix", "prefix", "stem", "suffix"])
    define_content_old_version(trans,"word-txt-qaa","morph-type","n'ubirenne",["prefix", "prefix", "stem", "suffix", "suffix"])

    #Using the new define_content-function to fix more complex (and/or just different) cases.

    #Fix 'Conn | stem' to '-Conn | suffix':



    define_content(trans,"morph-type",("xyzConn","REPLACE_BY_INDEX",-1),cond1=("morph-type",["stem","stem"]),cond2=("morph-gls-en",[">.<","Conn"]),cond3=("word-txt-qaa",">.<"))

    define_content(trans,"morph-type",("xyzConn","REPLACE_BY_INDEX",-1),cond1=("morph-type",["prefix","stem","stem"]),cond2=("morph-gls-en",[">.<",">.<","Conn"]),cond3=("word-txt-qaa",">.<"))

    define_content(trans,"morph-type",("xyzConn","REPLACE_BY_INDEX",2),cond1=("morph-type",[">.<",">.<","stem",">.<"]),cond2=("morph-gls-en",[">.<",">.<","Conn",">.<"]),cond3=("word-txt-qaa",">.<"))

    define_content(trans,"morph-gls-en","-Conn",cond1=("morph-type","xyzConn"),cond2=("morph-gls-en","Conn"))

    define_content(trans,"morph-type","suffix",cond1=("morph-type","xyzConn"))

    #Fix '3SgPoss | stem' to '-3SgPoss | suffix':

    define_content(trans,"morph-type",("xyz3SgPoss","REPLACE_BY_INDEX",-1),cond1=("morph-type",["stem","stem"]),cond2=("morph-gls-en",[">.<","3SgPoss"]),cond3=("word-txt-qaa",">.<"))

    define_content(trans,"morph-type",("xyz3SgPoss","REPLACE_BY_INDEX",-1),cond1=("morph-type",[">.<","stem","stem"]),cond2=("morph-gls-en",[">.<",">.<","3SgPoss"]),cond3=("word-txt-qaa",">.<"))

    define_content(trans,"morph-gls-en","-3SgPoss",cond1=("morph-type","xyz3SgPoss"),cond2=("morph-gls-en","3SgPoss"))

    define_content(trans,"morph-type","suffix",cond1=("morph-type","xyz3SgPoss"))



    #Fix 'Emph | stem' to '-Emph | suffix':

    define_content(trans,"morph-type",("xyzEmph","REPLACE_BY_INDEX",-1),cond1=("morph-type",["stem","stem"]),cond2=("morph-gls-en",[">.<","Emph"]),cond3=("word-txt-qaa",">.<"))

    define_content(trans,"morph-type",("xyzEmph","REPLACE_BY_INDEX",-1),cond1=("morph-type",[">.<","stem","stem"]),cond2=("morph-gls-en",[">.<",">.<","Emph"]),cond3=("word-txt-qaa",">.<"))

    define_content(trans,"morph-type",("xyzEmph","REPLACE_BY_INDEX",-1),cond1=("morph-type",[">.<",">.<","suffix","stem"]),cond2=("morph-gls-en",[">.<",">.<",">.<","Emph"]),cond3=("word-txt-qaa",">.<"))

    define_content(trans,"morph-type",("xyzEmph","REPLACE_BY_INDEX",-1),cond1=("morph-type",[">.<",">.<",">.<","suffix","stem"]),cond2=("morph-gls-en",[">.<",">.<",">.<",">.<","Emph"]),cond3=("word-txt-qaa",">.<"))

    define_content(trans,"morph-gls-en","-Emph",cond1=("morph-type","xyzEmph"),cond2=("morph-gls-en","Emph"))

    define_content(trans,"morph-type","suffix",cond1=("morph-type","xyzEmph"))



    #Fix '1Pl.incl | stem' to '-1Pl.incl | suffix':

    define_content(trans,"morph-type",("xyz1Pl.incl","REPLACE_BY_INDEX",-1),cond1=("morph-type",[">.<",">.<",">.<",">.<"]),cond2=("morph-gls-en",[">.<",">.<",">.<","1Pl.incl"]),cond3=("word-txt-qaa",">.<"))

    define_content(trans,"morph-gls-en","-1Pl.incl",cond1=("morph-type","xyz1Pl.incl"),cond2=("morph-gls-en","1Pl.incl"))

    define_content(trans,"morph-type","suffix",cond1=("morph-type","xyz1Pl.incl"))

    #Fix 'there | stem' to '-there | suffix':

    define_content(trans,"morph-type",("xyzthere","REPLACE_BY_INDEX",-1),cond1=("morph-type",[">.<",">.<","suffix","stem"]),cond2=("morph-gls-en",[">.<",">.<",">.<","there"]),cond3=("word-txt-qaa",">.<"))

    define_content(trans,"morph-type",("xyzthere","REPLACE_BY_INDEX",-1),cond1=("morph-type",[">.<","stem","stem"]),cond2=("morph-gls-en",[">.<",">.<","there"]),cond3=("word-txt-qaa",">.<"))

    define_content(trans,"morph-gls-en","-there",cond1=("morph-type","xyzthere"),cond2=("morph-gls-en","there"))

    define_content(trans,"morph-type","suffix",cond1=("morph-type","xyzthere"))

    #Fix 'Loc | stem' to 'Loc- | prefix':

    define_content(trans,"morph-type",("xyzLoc","REPLACE_BY_INDEX",0),cond1=("morph-type",["stem","stem",">.<"]),cond2=("morph-gls-en",["Loc",">.<",">.<"]),cond3=("word-txt-qaa",">.<"))

    define_content(trans,"morph-type",("xyzLoc","REPLACE_BY_INDEX",0),cond1=("morph-type",["stem","prefix",">.<"]),cond2=("morph-gls-en",["Loc",">.<",">.<"]),cond3=("word-txt-qaa",">.<"))

    define_content(trans,"morph-gls-en","Loc-",cond1=("morph-type","xyzLoc"),cond2=("morph-gls-en","Loc"))

    define_content(trans,"morph-type","prefix",cond1=("morph-type","xyzLoc"))

    #Change exact matches of '?' or '-' to '****' on the gloss-tier:

    define_content(trans,"morph-gls-en","****",cond=("morph-gls-en","?"))
    define_content(trans,"morph-gls-en","****",cond=("morph-gls-en","-"))



    toElan.toElan("../../output_files/"+str(file_name),trans)



path_second="../../output_files/"

for eaf_file in glob.glob(path_second+"*.eaf"):
    file_name = eaf_file.replace(path_second,"")
    trans = fromElan.fromElan(eaf_file,encoding="utf-8")
    #Remove for every word-tier those segments, whose content matches either the comma or the single quote sign or the dot
    remove_segments(trans,",","word-txt-qaa")
    remove_segments(trans,"’","word-txt-qaa")
    remove_segments(trans,".","word-txt-qaa")
    #Fix affixes for those files where the gaps where filled already
    fix_affixes(trans,"morph-txt","morph-gls-en")
    fix_affixes(trans,"morph-gls-en","morph-txt")
    toElan.toElan("../../output_files/"+str(file_name),trans)