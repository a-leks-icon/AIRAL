#Created: 2024-02-06
#Latest Version: 2024-02-06
#Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
#Corflow module created by François Delafontaine

from corflow import fromElan,toElan
import glob

def fix_parent_child_relation(tier,overwrite=False):
    '''If *overwrite* is False, set for every segment of a *tier* with an existing parent tier its parent segment based on its times, if the segment lacks a parent segment. If *overwrite* is True, it does this operation for every segment, even if it already has a parent segment assigned to it. Returns nothing.'''
    if tier.parent() != None:
        if overwrite:
            for seg in tier:
                par_seg = tier.parent().getTime(seg.start)
                seg.setParent(par_seg)
        else:
            for seg in tier:
                if seg.parent() == None:
                    par_seg = tier.parent().getTime(seg.start)
                    seg.setParent(par_seg)


#ACTUAL OPERATIONS BEGIN HERE#
input_path = "../../input_files/"
output_path = "../../output_files/"
eaf_files = glob.glob(input_path+"/*.eaf")


#eaf files.
for file in eaf_files:
    file_name = file.replace(input_path,"")
    print(f"file: {file_name}")
    trans = fromElan.fromElan(file,encoding="utf-8")
    #Set for every segment of a tier based on its start time its parent, if it lacks such.
    for tier in trans:
        fix_parent_child_relation(tier,True)
    toElan.toElan(output_path+file_name,trans)