#Created: 2024-03-10
#Latest Version: 2024-03-10
#Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
#Corflow module created by François Delafontaine

from corflow import fromElan, toElan
import glob

def fill_times(tier):
    '''Sets the start and end time for every segment either starting or ending with -1 of every child tier of the parent *tier* recursively. Returns nothing.'''

    def set_times_of_segs(segs:list,parent_seg):
        if len(segs) == 1:
            segs[0].start = parent_seg.start
            segs[0].end = parent_seg.end
        elif len(segs) > 1:
            total_time = parent_seg.end-parent_seg.start
            part_time = total_time/len(segs)
            start = parent_seg.start
            for seg in segs[:-1]:
                seg.start = start
                seg.end = start + part_time
                start = seg.end
            segs[-1].start = start
            segs[-1].end = parent_seg.end

    if tier.children():
        for seg in tier:
            if seg.children():
                for ch_tier,ch_segs in seg.childDict().items():
                    if ch_segs:
                        if any((ch_seg.start == -1) | (ch_seg.end == -1) for ch_seg in ch_segs):
                            set_times_of_segs(ch_segs,seg)
        for ch_tier in tier.children():
            fill_times(ch_tier)

input_path = "../../input_files/"
output_path = "../../output_files/"
eaf_files = glob.glob(input_path+"/*.eaf")
for file in eaf_files:
    file_name = file.replace(input_path,"")
    print(f"File: {file_name}")
    trans = fromElan.fromElan(file,encoding="utf-8")
    for top_tier in trans.getTop():
        print(f"top tier: {top_tier.name}")
        fill_times(top_tier)
    toElan.toElan(output_path+file_name,trans)