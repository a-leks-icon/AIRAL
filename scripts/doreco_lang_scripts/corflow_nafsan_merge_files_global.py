# Created: 2023-07-30
# Latest Version: 2023-08-11
# Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
# Corflow module created by Francois Delafontaine

'''
The following script takes pairs (or triples) of eaf-files, where each file contains one speaker with his/her tiers (previously, both speakers shared the same tiers in an original file, before they got their own tiers in their separate files). All tiers of speakers 02 and 03 get copied and inserted to those of speaker 01, thereby merging the tiers of all speakers. Each transcription gets saved in a new eaf-file.
'''

#Loading the corflow-module.
from corflow import fromElan,toElan
import glob

#The general paths.
input_path = "../../input_files/"
output_path = "../../output_files/"

#All eaf files.
eaf_files = glob.glob(input_path+"/*.eaf")

end_names_tiers_to_copy = [(0,"_paragraph"), (1,"_phrase"), (2,"_phrase-gls-en"), (3,"_phrase-note-bi"), (4,"_phrase-note-en"), (5,"_word-txt-erk"), (6,"_morph-txt-erk"), (7,"_morph-gls"), (8,"_morph-gls-en"), (9,"_morph-msa-en"), (10,"_morph-type")]

#Iterating over every eaf-file with speaker 01.
for spk1_file in [speaker1 for speaker1 in eaf_files if speaker1.endswith("_speaker_01.eaf")]:
    speaker_03_exists = False
    trans_spk1 = fromElan.fromElan(spk1_file,encoding="utf-8")
    print(f"speaker 01 file name {spk1_file}")
    for tier in trans_spk1:
        print(tier.name)
    #Iterating over every eaf-file with the matching speaker 02.
    for spk2_file in [speaker2 for speaker2 in eaf_files if (speaker2.endswith("_speaker_02.eaf") & (speaker2.replace(input_path,"").partition("_")[0] == spk1_file.replace(input_path,"").partition("_")[0]))]:
        trans_spk2 = fromElan.fromElan(spk2_file,encoding="utf-8")
        print(f"speaker 02 file name {spk2_file}")
        #Because the order of the tiers in the transcription does not reflect their hierarchy, the have to be sorted that way. Otherwise, the actual copying of the tiers does not work. 
        spk2_tiers_sorted = []
        for tier in trans_spk2:
            for number,tier_end_name in end_names_tiers_to_copy:
                if tier.name.endswith(tier_end_name):
                    spk2_tiers_sorted.append((number,tier))
        spk2_tiers_sorted.sort()
        for index,(number,entry) in enumerate(spk2_tiers_sorted):
            spk2_tiers_sorted[index] = entry
        print("spk 2 tiers sorted:")
        for sorted_tier in spk2_tiers_sorted:
            print(sorted_tier.name)
        #Iterating over every eaf-file with the matching speaker 03.
        for spk3_file in [speaker3 for speaker3 in eaf_files if (speaker3.endswith("_speaker_03.eaf") & (speaker3.replace(input_path,"").partition("_")[0] == spk1_file.replace(input_path,"").partition("_")[0]))]:
            trans_spk3 = fromElan.fromElan(spk3_file,encoding="utf-8")
            #Noting, that the file has a third speaker (which is not always the case).
            speaker_03_exists = True
            print(spk3_file)
            #Because the order of the tiers in the transcription does not reflect their hierarchy, the have to be sorted that way. Otherwise, the actual copying of the tiers does not work. 
            spk3_tiers_sorted = []
            for tier in trans_spk3:
                for number,tier_end_name in end_names_tiers_to_copy:
                    if tier.name.endswith(tier_end_name):
                        spk3_tiers_sorted.append((number,tier))
            spk3_tiers_sorted.sort()
            for index,(number,entry) in enumerate(spk3_tiers_sorted):
                spk3_tiers_sorted[index] = entry
            for sorted_tier in spk3_tiers_sorted:
                print(sorted_tier)
            for tier in trans_spk3:
                print(tier.name)


    print("////////////////\nTIERS PROCESSING\n////////////////")
    #Iterating over every tier for speaker 02, which is going to be copied.
    for spk2_tier in spk2_tiers_sorted:
        print(f"spk2 tier name (sorted): {spk2_tier.name}")
        if (spk2_tier.name.startswith("NT_")) | (spk2_tier.name.startswith("N_")):
            #Adding the tier to the first speakers transcription as the last tier.
            trans_spk1.add(-1,spk2_tier)
            #Defining its name as it was before.
            trans_spk1.elem[-1].name = spk2_tier.name
            #If the tier has segments, every segment has to be renamed. Otherwise, there would be possibly (and very likely) different segments with the same name in the transcription, thereby corrupting the transcription and eaf-file.
            #Segments on the phrase tier startet with '-'; on other tiers with 'a'.
            print(f"name of newly added tier: {trans_spk1.elem[-1].name}")
            if len(spk2_tier) > 0:
                print("Renaming segments")
                for new_seg in trans_spk1.elem[-1]:
                    new_seg.name = new_seg.name.replace("a","b").replace("-","p")
            #Depending on whether the tier has a parent or not, it is the first tier or not. These have to be treated differently.
            if spk2_tier.parent() != None:
                #If the previously added tier was the parent in the second speakers transcription, it will remain so also in the first speakers transcription.
                trans_spk1.elem[-1].setParent(trans_spk1.elem[new_parent_index])
                #The segments in the newly added tier get their parent segments assigned, which are those segments in the previous step newly added tier, that correspond to those segments in the old tier (from speaker 02).
                print(f"name of newly added tier with a parent: {trans_spk1.elem[-1].name}")
                print(f"name of its parent (previously added): {trans_spk1.elem[new_parent_index].name} bzw. {trans_spk1.elem[-1].parent().name}")
                old_segs_parent_names = [old_seg.parent().name for old_seg in spk2_tier]
                for index,new_seg in enumerate(trans_spk1.elem[-1]):
                    for new_seg_parent in trans_spk1.elem[new_parent_index]:
                        if new_seg_parent.name.replace("b","a").replace("p","-") == old_segs_parent_names[index]:
                            new_seg.setParent(new_seg_parent)
                #Creating a dummy segment in case a phrase tier has only one segment. In this case, strangely the segment loses its time slots (start and end time in the eaf-file itself) and shares its parents time, which is not desirable here. Creating a dummy segment prevents this from happening. I then delete the dummy segment in ELAN manually.
                #This was removed as François fixed this issue in corflow directly. It had to do with the ELAN types, which could have been forced to be something different than 'assoc' with the setMeta method.
                #if (len(spk2_tier) == 1) & ((spk2_tier.name == "NT_phrase") | (spk2_tier.name == "N_phrase")):
                    #trans_spk1.elem[-1].add(1,spk2_tier.elem[0])
                    #trans_spk1.elem[-1].elem[-1].name = "dummy"
                    #trans_spk1.elem[-1].elem[-1].content = "dummy"
                    #trans_spk1.elem[-1].elem[-1].setParent(trans_spk1.elem[-2].elem[0])
                    #trans_spk1.elem[-1].elem[-1].start = trans_spk1.elem[-1].elem[0].end
                    #trans_spk1.elem[-1].elem[-1].end = trans_spk1.elem[-1].elem[-1].start + 1
                if spk2_tier.children():
                    print(f"the tier has children and is the new parent!")
                    print(f"its children are {[child.name for child in spk2_tier.children()]}")
                    new_parent_index = trans_spk1.elem[-1].index()
            else:
                print(f"tier has no parent!")
                #Setting its parent to None (therefore, it is not dependend on any other tier).
                trans_spk1.elem[-1].setParent(None)
                #Defining a tuple with a) the tier from speakers 02 transcription and b) the index of its respective counterpart in spekaers 01 transcription (this will be important to define paranting in the new file for the newly added tiers).
                new_parent_index = trans_spk1.elem[-1].index()
        print(f"!!!\nNEXT TIER\n!!!")

    if speaker_03_exists:
        speaker_03_exists = False

        #The same operation as for the tiers from speaker 02, but for the tiers of speaker 03.
        for spk3_tier in spk3_tiers_sorted:
            if spk3_tier.name.startswith("Abet"):
                trans_spk1.add(-1,spk3_tier)
                trans_spk1.elem[-1].name = spk3_tier.name
                if len(spk3_tier) > 0:
                    #Segments in newly added tiers of speaker 03 get different names assigned than those of speaker 01 and 02.
                    for new_seg in trans_spk1.elem[-1]:
                        new_seg.name = new_seg.name.replace("a","c").replace("-","q")
                if spk3_tier.parent() != None:
                    trans_spk1.elem[-1].setParent(trans_spk1.elem[new_parent_index])
                    old_segs_parent_names = [old_seg.parent().name for old_seg in spk3_tier]
                    for index,new_seg in enumerate(trans_spk1.elem[-1]):
                        for new_seg_parent in trans_spk1.elem[new_parent_index]:
                            if new_seg_parent.name.replace("c","a").replace("q","-") == old_segs_parent_names[index]:
                                new_seg.setParent(new_seg_parent)
                    if spk3_tier.children():
                        new_parent_index = trans_spk1.elem[-1].index()
                else:
                    trans_spk1.elem[-1].setParent(None)
                    new_parent_index = trans_spk1.elem[-1].index()

    toElan.toElan(output_path+spk1_file.replace(input_path,"").replace("_speaker_01",""),trans_spk1)
    print("!!!FILE SAVED!!!")