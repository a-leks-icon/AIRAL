#Created: 2024-05-10
#Latest Version: 2024-05-24
#Script written by Aleksandr Schamberger (GitHub: JLEKS) as part of the AIRAL project by Ludger Paschen at ZAS Berlin.
#Corflow module created by François Delafontaine

from corflow import fromElan,toElan
import glob
import re

def split_segments(seg,time,end=True):
    '''Splits a segment *seg* into two seperate segments at *time* in seconds. If *end* is True (the default), the new segment is to the left of *seg*. If *end* is False, the new segment is to the right of *seg*. All child segments of *seg* get the splitted segment as their new parent, if their times fall within the new segments times. Returns a tuple with its first element being the new segment and its second element being a list with all child segments, which had to be added due to the splitting.'''
    seg_times = (seg.start,seg.end)
    if end:
        seg.struct.add(seg.index(),seg)
        new_seg = seg.struct.elem[seg.index()-1]
        new_seg.start = seg.start
        new_seg.end = time
        seg.start = time
    else:
        seg.struct.add(seg.index()+1,seg)
        new_seg = seg.struct.elem[seg.index()+1]
        new_seg.start = time
        new_seg.end = seg.end
        seg.end = time
    new_seg.name = seg.name + "_0"
    if seg.parent() != None:
        new_seg.setParent(seg.parent().struct.getTime(new_seg.start))
    else:
        new_seg.setParent(None)
    new_ch_segs = []
    if seg.children():
        for ch_seg in seg.children():
            if (ch_seg.start == seg_times[0]) & (ch_seg.end == seg_times[-1]):
                if end:
                    ch_seg.struct.add(ch_seg.index(),ch_seg)
                    new_ch_seg = ch_seg.struct.elem[ch_seg.index()-1]
                else:
                    ch_seg.struct.add(ch_seg.index()+1,ch_seg)
                    new_ch_seg = ch_seg.struct.elem[ch_seg.index()+1]
                new_ch_seg.start = new_seg.start
                new_ch_seg.end = new_seg.end
                new_ch_seg.name = ch_seg.name + "_0"
                new_ch_seg.setParent(new_seg)
                new_ch_segs.append(new_ch_seg)
                ch_seg.start = seg.start
                ch_seg.end = seg.end
            elif (ch_seg.start == new_seg.start) | (ch_seg.end == new_seg.end) | ((ch_seg.start > new_seg.start) & (ch_seg.end < new_seg.end)):
                ch_seg.setParent(new_seg)
    return (new_seg,new_ch_segs)

def fix_affixes_clitics(ref_tier,man_tier,time=True,ignore_cont=False):
    '''Fix every segment on the *man_tier* regarding its encoding as an affix or clitic based on the encoding of the segments on the *ref_tier*. If *time* is True, segments on the *ref_tier* and *man_tier* have to be time-aligned or fall in between their times. If *time* is false, segments on the *ref_tier* have to be the parents of the segments on the *man_tier*. If a segments content on *man_tier* matches the regex pattern *ignore_cont*, its skipped. By default, *ignore_cont* is False (not a string type) and therefore no regex pattern for ignoring segments is applied. Returns a list with all changed segment objects on the *man_tier*.'''

    changed_segs = []

    for ref_seg in ref_tier:

        if time:
            man_seg = man_tier.getTime(ref_seg.start)
        else:
            if ref_seg.children():
                for child_seg in ref_seg.children():
                    if child_seg.struct == man_tier:
                        man_seg = child_seg
                        break
            else:
                continue

        if isinstance(ignore_cont,str):
            if re.search(ignore_cont,man_seg.content):
                continue

        if (ref_seg.content.startswith("-")) & (ref_seg.content.endswith("-")):
            if not man_seg.content.startswith("-"):
                if man_seg.content.startswith("="):
                    man_seg.content = "-" + man_seg.content[1:]
                else:
                    man_seg.content = "-" + man_seg.content
                changed_segs.append(man_seg)
            if not man_seg.content.endswith("-"):
                if man_seg.content.endswith("="):
                    man_seg.content = man_seg.content[:-1] + "-"
                else:
                    man_seg.content = man_seg.content + "-"
                changed_segs.append(man_seg)
        elif ref_seg.content.startswith("-"):
            if not man_seg.content.startswith("-"):
                if man_seg.content.startswith("="):
                    man_seg.content = "-" + man_seg.content[1:]
                else:
                    man_seg.content = "-" + man_seg.content
                changed_segs.append(man_seg)
        elif ref_seg.content.endswith("-"):
            if not man_seg.content.endswith("-"):
                if man_seg.content.endswith("="):
                    man_seg.content = man_seg.content[:-1] + "-"
                else:
                    man_seg.content = man_seg.content + "-"
                changed_segs.append(man_seg)
        elif ref_seg.content.startswith("="):
            if not man_seg.content.startswith("="):
                if man_seg.content.startswith("-"):
                    man_seg.content = "=" + man_seg.content[1:]
                else:
                    man_seg.content = "=" + man_seg.content
                changed_segs.append(man_seg)
        elif ref_seg.content.endswith("="):
            if not man_seg.content.endswith("="):
                if man_seg.content.endswith("-"):
                    man_seg.content = man_seg.content[:-1] + "="
                else:
                    man_seg.content = man_seg.content + "="
                changed_segs.append(man_seg)

    return changed_segs

def merge_segments(segment,n:int=-1):
    '''Merges a *segment*s content and structure (e.g. times) with a number of *n* segments on the same tier. If *n* is negative, the merged segments are to the left. If *n* is positive, the merged segments are to the right. All segments to be merged must share their start and/or end times with the other segments to be merged. Returns the changed segment object after the merging process.'''
    if segment.index()+n < 0:
        return print(f"Segment index {segment.index()+n} is too low (non existent)")
    elif segment.index()+n > segment.struct.elem[-1].index():
        return print(f"Segment index {segment.index()+n} is too high (non existent)")
    if n < 0:
        seg_range = range(-1,n-1,-1)
        for num in seg_range:
            current_seg = segment.struct.elem[segment.index()+num+1]
            next_seg = segment.struct.elem[segment.index()+num]
            if current_seg.start == next_seg.end:
                segment.content = next_seg.content + segment.content
            else:
                return print(f"The segment '{current_seg.content}' with index {current_seg.index()} and times {current_seg.start} - {current_seg.end} is not right adjacent to the segment '{next_seg.content}' with index {next_seg.index()} and times {next_seg.start} - {next_seg.end}.")
            if next_seg.children():
                for child_seg in next_seg.children():
                    child_seg.setParent(segment)
        segment.start = segment.struct.elem[segment.index()+n].start
        for num in seg_range:
            next_seg = segment.struct.elem[segment.index()-1]
            segment.struct.remove(next_seg)

    elif n > 0:
        seg_range = range(1,n+1)
        for num in seg_range:
            current_seg = segment.struct.elem[segment.index()+num-1]
            next_seg = segment.struct.elem[segment.index()+num]
            if current_seg.end == next_seg.start:
                segment.content += next_seg.content
            else:
                return print(f"The segment '{current_seg.content}' with index {current_seg.index()} and times {current_seg.start} - {current_seg.end} is not left adjacent to the segment '{next_seg.content}' with index {next_seg.index()} and times {next_seg.start} - {next_seg.end}.")
            if next_seg.children():
                for child_seg in next_seg.children():
                    child_seg.setParent(segment)
        segment.end = segment.struct.elem[segment.index()+n].end
        for num in seg_range:
            next_seg = segment.struct.elem[segment.index()+1]
            segment.struct.remove(next_seg)

    return segment


input_path = "../../input_files/"
output_path = "../../output_files/"
eaf_files = glob.glob(input_path+"*.eaf")

split_glosses = ["PREP=1SG.PRON", "PREP=2PL.PRON", "if|when=2SG", "body-3SG.POSS=", "tail-3SG.POSS=", "OBJM=1SG.PRON", "2SG.OBJM=2SG.PRON", "2SG.OBJM=2SG.PRON", "PREP=3SG.PRON", "CAUS-woman", "PREP=3SG"]

print(f"ROUND#1\n\n")
for file in eaf_files:
    file_name = file.replace(input_path,"")
    print(f"Processing file: {file_name}")
    trans = fromElan.fromElan(file,encoding="utf-8")
    gram_tier = trans.getName("grammatical_words_mtok")
    gl_tier = trans.getName("gloss_mtok")
    old_gram_tier = trans.getName("grammatical_words")
    for seg in gl_tier:
        #Removing dots.
        if seg.content.endswith((".","--","==")):
            print(f"REMOVE DOT/DASH/EQUAL SIGN:\n---")
            print(f"file: {file_name} | tier: {gl_tier.name} | seg: {seg.content}: {seg.start}-{seg.end}")
            seg.content = seg.content[:-1]

        #Splitting the gloss segments and respective morph segments.
        if seg.content in split_glosses:
            #if seg.content == "PREP=3SG":
            if seg.content in ["PREP=3SG.PRON","PREP=3SG"]:
                #Do not split 'teve', therefore change it to 'PREP.3SG.PRON' instead of 'PREP=3SG.PRON'.
                seg.content = "PREP.3SG.PRON"
                continue
            elif seg.content == "when.3SG.PRON":
                seg.content = "when=3SG.PRON"
            print("SPLIT\n---")
            print(f"file: {file_name} | tier: {gl_tier.name} | seg: {seg.content}: {seg.start}-{seg.end}")
            time = ((seg.end-seg.start)/2)+seg.start
            gram_seg = gram_tier.getTime(seg.start)
            print(f"file: {file_name} | tier: {gram_tier.name} | seg: {gram_seg.content}: {gram_seg.start}-{gram_seg.end}")
            new_gl_seg = split_segments(seg,time)[0]
            if "=" in seg.content[1:-1]:
                seg_part = seg.content.partition("=")
            elif "-" in seg.content[1:-1]:
                seg_part = seg.content.partition("-")
            new_gl_seg.content = seg_part[0] + seg_part[1]
            seg.content = seg_part[-1]

            print(f"gl split ->: {new_gl_seg.content} {new_gl_seg.start}-{new_gl_seg.end} |AND| {seg.content} {seg.start}-{seg.end}")

            #Split time-aligned morph segment.
            new_gram_seg = split_segments(gram_seg,time)[0]
            if ("-" in gram_seg.content[1:-1]):
                gram_seg_part = gram_seg.content.partition("-")
            elif ("=" in gram_seg.content[1:-1]):
                gram_seg_part = gram_seg.content.partition("=")
            elif gram_seg.content.startswith("be"):#startswith(("te","be"))
                gram_seg_part = [gram_seg.content[:2], "=", gram_seg.content[2:]]
            new_gram_seg.content = gram_seg_part[0] + gram_seg_part[1]
            gram_seg.content = gram_seg_part[-1]

            print(f"gram split ->: {new_gram_seg.content} {new_gram_seg.start}-{new_gram_seg.end} |AND| {gram_seg.content} {gram_seg.start}-{gram_seg.end}")
            print("---\n")

    toElan.toElan(output_path+file_name,trans)

#Fixing cases of words made up of a stem with a following proclitic and enclitic.
eaf_files = glob.glob(output_path+"*.eaf")
print(f"\n\nROUND#2\n\n")
for file in eaf_files:
    file_name = file.replace(output_path,"")
    print(f"Processing file: {file_name}")
    trans = fromElan.fromElan(file,encoding="utf-8")
    gram_tier = trans.getName("grammatical_words_mtok")
    gl_tier = trans.getName("gloss_mtok")
    old_gram_tier = trans.getName("grammatical_words")

    for ind in range(len(gl_tier)-2):
        s1 = gl_tier.elem[ind]
        s2 = gl_tier.elem[ind+1]
        s3 = gl_tier.elem[ind+2]
        g1 = gram_tier.getTime(s1.start)
        g2 = gram_tier.getTime(s2.start)
        g3 = gram_tier.getTime(s3.start)
        o1 = old_gram_tier.getTime(s1.start)
        o2 = old_gram_tier.getTime(s2.start)
        o3 = old_gram_tier.getTime(s3.start)
        osegs = [o1,o2,o3]
        if (not s1.content.startswith(("=","-"))) & (not s1.content.endswith(("=","-"))) & (s2.content.endswith(("=","-"))) & (s3.content.startswith(("=","-"))):
            if s1.content == "":
                continue
            same = True
            for seg in osegs:
                for seg2 in osegs:
                    if seg != seg2:
                        same = False
                        break
            if same:
                print(f"MORPH STATUS:\n---")
                print(f"file: {file_name} | tier: {gl_tier.name} | seg: {s1.content}: {s1.start}-{s1.end}")
                print(f"OLD structure:")
                print(f"morphs: {g1.content} {g2.content} {g3.content}")
                print(f"glosses: {s1.content} {s2.content} {s3.content}")

                s1.content = s1.content + "-"
                #s2.content = s2.content[:-1] + "-"
                s3.content = s3.content[1:]

                g1.content = g1.content + "-"
                #g2.content = g2.content[:-1] + "-"
                g3.content = g3.content[1:]

                print(f"NEW structure:")
                print(f"morphs: {g1.content} {g2.content} {g3.content}")
                print(f"glosses: {s1.content} {s2.content} {s3.content}")
                print(f"---\n")

    toElan.toElan(output_path+file_name,trans)

print(f"\n\nROUND#3\n\n")
print(f"MERGE, AND KINSHIP STEMS TO PREFIXES")
for file in eaf_files:
    file_name = file.replace(output_path,"")
    print(f"Processing file: {file_name}")
    trans = fromElan.fromElan(file,encoding="utf-8")
    gram_tier = trans.getName("grammatical_words_mtok")
    gl_tier = trans.getName("gloss_mtok")
    kinship = ["mother","father"]
    out_of_place_morphs = {"overe": "coconut", "nomaa": "come", "toraaraa": "axe"}
    for ind in range(len(gl_tier)-1):
        gl_seg1 = gl_tier.elem[ind]
        gl_seg2 = gl_tier.elem[ind+1]
        if (gl_seg1.content in kinship) & (gl_seg2.content == "DEREL"):
            print(f"KINSHIP\n---")
            print(f"gl segs found: {gl_seg1.content} {gl_seg1.start}-{gl_seg1.end} AND {gl_seg2.content} {gl_seg2.start}-{gl_seg2.end}")
            gl_seg1.content += "-"
            gram_seg1 = gram_tier.getTime(gl_seg1.start)
            gram_seg2 = gram_tier.getTime(gl_seg2.start)
            print(f"gram segs found: {gram_seg1.content} {gram_seg1.start}-{gram_seg1.end} AND {gram_seg2.content} {gram_seg2.start}-{gram_seg2.end}")
            gram_seg1.content += "-"
            print(f"-> new gl seg: {gl_seg1.content} {gl_seg1.start}-{gl_seg1.end}")
            print(f"-> new gram seg: {gram_seg1.content} {gram_seg1.start}-{gram_seg1.end}\n---")
        elif gl_seg1.content in out_of_place_morphs.keys():
            print(f"OUT OF PLACE MORPH\n---")
            gram_seg1 = gram_tier.getTime(gl_seg1.start)
            print(f"gl seg: {gl_seg1.content} {gl_seg1.start}-{gl_seg1.end}")
            print(f"gram seg: {gram_seg1.content} {gram_seg1.start}-{gram_seg1.end}")
            gl_seg1.content = out_of_place_morphs[gl_seg1.content]
            print(f"-> gl seg changed to: {gl_seg1.content} {gl_seg1.start}-{gl_seg1.end}\n---")
    merged = 0
    for n in range(len(gram_tier)-1):
        ind = n-merged
        gram_seg1 = gram_tier.elem[ind]
        gram_seg2 = gram_tier.elem[ind+1]
        if (gram_seg1.content in ["eve=","eve"]) & (gram_seg2.content in ["=he","he"]):
            gl_seg1 = gl_tier.getTime(gram_seg1.start)
            gl_seg2 = gl_tier.getTime(gram_seg2.start)
            if not "but" in gl_seg2.content:
                continue
            print(f"MERGE SEGMENTS\n---:")
            print(f"gram segs to be merged: {gram_seg1.content} {gram_seg1.start}-{gram_seg1.end} AND {gram_seg2.content} {gram_seg2.start}-{gram_seg2.end}")
            print(f"gl segs to be merged: {gl_seg1.content} {gl_seg1.start}-{gl_seg1.end} AND {gl_seg2.content} {gl_seg2.start}-{gl_seg2.end}")
            merged_gram_seg = merge_segments(gram_seg1,1)
            merged_gram_seg.content = "evehee"
            merged_gl_seg = merge_segments(gl_seg1,1)
            merged_gl_seg.content = "but"
            merged += 1
            print(f"-> gram segs merged to: {merged_gram_seg.content} {merged_gram_seg.start}-{merged_gram_seg.end}")
            print(f"-> gl segs merged to: {merged_gl_seg.content} {merged_gl_seg.start}-{merged_gl_seg.end}\n---")

    toElan.toElan(output_path+file_name,trans)