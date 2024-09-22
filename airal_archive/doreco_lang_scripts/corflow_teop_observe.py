#Created: 2024-05-12
#Latest Version: 2024-05-17
#Script written by Aleksandr Schamberger (GitHub: JLEKS) as part of the AIRAL project by Ludger Paschen at ZAS Berlin.
#Corflow module created by François Delafontaine

from corflow import fromElan,toElan
import glob

input_path = "../../input_files/"
output_path = "../../output_files/"
eaf_files = glob.glob(input_path+"*.eaf")

count = 0
for file in eaf_files:
    file_name = file.replace(input_path,"")
    print(f"Processing file: {file_name}")
    trans = fromElan.fromElan(file,encoding="utf-8")
    gram_tier = trans.getName("grammatical_words_mtok")
    gl_tier = trans.getName("gloss_mtok")
    old_gram_tier = trans.getName("grammatical_words")
    if old_gram_tier == None:
        raise Exception("No grammatical words tier.")

    for ind in range(len(gl_tier)-2):
        gl_seg = gl_tier.elem[ind]
        gl_seg2 = gl_tier.elem[ind+1]
        gl_seg3 = gl_tier.elem[ind+2]
        gram_seg = gram_tier.getTime(gl_seg.start)
        gram_seg2 = gram_tier.getTime(gl_seg2.start)
        gram_seg3 = gram_tier.getTime(gl_seg3.start)
        o_seg = old_gram_tier.getTime(gl_seg.start)
        o_seg2 = old_gram_tier.getTime(gl_seg2.start)
        o_seg3 = old_gram_tier.getTime(gl_seg3.start)
        o_segs = [o_seg,o_seg2,o_seg3]
        if (not gl_seg.content.startswith(("=","-"))) & (not gl_seg.content.endswith(("=","-"))) & (gl_seg2.content.endswith(("=","-"))) & (gl_seg3.content.startswith(("=","-"))):
            if gl_seg.content == "":
                continue
            same = True
            for seg in o_segs:
                for seg2 in o_segs:
                    if seg != seg2:
                        same = False
                        break
            if same:
                count += 1
                print(f"---\ncase: {count} | file: {file_name} | tier: {gl_tier.name}\ngl_seg1: {gl_seg.content}: {gl_seg.start}-{gl_seg.end}\ngl_seg2: {gl_seg2.content}: {gl_seg2.start}-{gl_seg2.end}\ngl_seg3: {gl_seg3.content}: {gl_seg3.start}-{gl_seg3.end}")
                print(f"gram_seg1: {gram_seg.content}: {gram_seg.start}-{gram_seg.end}\ngram_seg2: {gram_seg2.content}: {gram_seg2.start}-{gram_seg2.end}\ngram_seg3: {gram_seg3.content}: {gram_seg3.start}-{gram_seg3.end}\n---\n")
        elif (not gl_seg3.content.startswith(("=","-"))) & (not gl_seg3.content.endswith(("=","-"))) & (gl_seg.content.endswith(("=","-"))) & (gl_seg2.content.startswith(("=","-"))):
            same = True
            for seg in o_segs:
                for seg2 in o_segs:
                    if seg != seg2:
                        same = False
                        break
            if same:
                count += 1
                print(f"---\ncase: {count} | file: {file_name} | tier: {gl_tier.name}\ngl_seg1: {gl_seg.content}: {gl_seg.start}-{gl_seg.end}\ngl_seg2: {gl_seg2.content}: {gl_seg2.start}-{gl_seg2.end}\ngl_seg3: {gl_seg3.content}: {gl_seg3.start}-{gl_seg3.end}")
                print(f"gram_seg1: {gram_seg.content}: {gram_seg.start}-{gram_seg.end}\ngram_seg2: {gram_seg2.content}: {gram_seg2.start}-{gram_seg2.end}\ngram_seg3: {gram_seg3.content}: {gram_seg3.start}-{gram_seg3.end}\n---\n")
        '''
        if (gl_seg.content.endswith(("=","-"))) & (gl_seg2.content.startswith(("=","-"))):
            count += 1
            print(f"case: {count} | file: {file_name} | tier: {gl_tier.name}\ngl_seg1: {gl_seg.content}: {gl_seg.start}-{gl_seg.end}\ngl_seg2: {gl_seg2.content}: {gl_seg2.start}-{gl_seg2.end}")
            print(f"gram_seg1: {gram_seg.content}: {gram_seg.start}-{gram_seg.end}\ngram_seg2: {gram_seg2.content}: {gram_seg2.start}-{gram_seg2.end}\n---")
        elif (gl_seg.content.endswith("-")) & (gl_seg2.content.endswith("=")):
            count += 1
            print(f"case: {count} | file: {file_name} | tier: {gl_tier.name}\ngl_seg1: {gl_seg.content}: {gl_seg.start}-{gl_seg.end}\ngl_seg2: {gl_seg2.content}: {gl_seg2.start}-{gl_seg2.end}")
            print(f"gram_seg1: {gram_seg.content}: {gram_seg.start}-{gram_seg.end}\ngram_seg2: {gram_seg2.content}: {gram_seg2.start}-{gram_seg2.end}\n---")
        elif (gl_seg.content.startswith("=")) & (gl_seg2.content.startswith("-")):
            count += 1
            print(f"case: {count} | file: {file_name} | tier: {gl_tier.name}\ngl_seg1: {gl_seg.content}: {gl_seg.start}-{gl_seg.end}\ngl_seg2: {gl_seg2.content}: {gl_seg2.start}-{gl_seg2.end}")
            print(f"gram_seg1: {gram_seg.content}: {gram_seg.start}-{gram_seg.end}\ngram_seg2: {gram_seg2.content}: {gram_seg2.start}-{gram_seg2.end}\n---")
        '''