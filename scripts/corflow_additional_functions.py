#Created: March 2023
#Latest Version: 2024-05-18
#Script written by Aleksandr Schamberger as part of the AIRAL project by Ludger Paschen at ZAS Berlin
#Corflow module created by François Delafontaine

'''
This script comprises a list of callable functions written for the python module 'corflow' to manipulate eaf-files.
'''

import re

def fill_gaps(transcription,referenced_tier_name,manipulated_tier_name,referenced_segment,inserted_segment):
    '''Creates for a given transcription and a referenced tier new segments with a given content on a second tier for all those segments with a given content on a referenced tier, which do not have a corresponding, time-aligned segment on the second tier. 
    
    Keyword arguments:

    transcription         -- the file loaded with the function fromElan

    referenced_tier_name  -- the string used to identify the referenced tier, whose segments are used as the base for adding new segments

    manipulated_tier_name -- the string used to identify the manipulated tier, where the new segments are added to

    referenced_segment    -- the content of the referenced segment, based on which time-aligned, new segments are added

    inserted_segment      -- the content of the new, time-aligned segments added on the manipulated tier
    '''
    referenced_tier_exists = False
    manipulated_tier_exists = False
    name_count = 1
    for tier in transcription:
        if referenced_tier_name in tier.name:
            referenced_tier = transcription.getName(tier.name)
            referenced_tier_exists = True
        elif manipulated_tier_name in tier.name:
            manipulated_tier = transcription.getName(tier.name)
            manipulated_tier_exists = True
        manipulated_tier_segment_times = []
        if referenced_tier_exists & manipulated_tier_exists:
            referenced_tier_exists = False
            manipulated_tier_exists = False
            for seg in manipulated_tier:
                manipulated_tier_segment_times.append(seg.start)
            for ref_seg in referenced_tier:
                if not ref_seg.start in manipulated_tier_segment_times:
                    if ref_seg.content == referenced_segment:
                        new_seg_added = False
                        for man_seg in manipulated_tier:
                            if man_seg.end < ref_seg.start:
                                if man_seg.index()+1 != len(manipulated_tier):
                                    if not (manipulated_tier.elem[man_seg.index()+1].end < ref_seg.start):
                                        if manipulated_tier.elem[man_seg.index()+1].end > ref_seg.start:
                                            manipulated_tier.add(man_seg.index()+1,ref_seg)
                                            manipulated_tier.elem[man_seg.index()+1].content = inserted_segment
                                            manipulated_tier.elem[man_seg.index()+1].setParent(ref_seg)
                                            manipulated_tier.elem[man_seg.index()+1].name = str(manipulated_tier.elem[man_seg.index()].name)+"_added"
                                            for man_seg_two in manipulated_tier:
                                                if (manipulated_tier.elem[man_seg.index()+1].name == man_seg_two.name) & (not manipulated_tier.elem[man_seg.index()+1].index() == man_seg_two.index()):
                                                    manipulated_tier.elem[man_seg.index()+1].name = str(manipulated_tier.elem[man_seg.index()+1].name)+"_"+str(name_count)
                                                    name_count += 1
                                        else:
                                            manipulated_tier.add(man_seg.index()+2,ref_seg)
                                            manipulated_tier.elem[man_seg.index()+2].content = inserted_segment
                                            manipulated_tier.elem[man_seg.index()+2].setParent(ref_seg)
                                            manipulated_tier.elem[man_seg.index()+2].name = str(manipulated_tier.elem[man_seg.index()+1].name)+"_added"
                                            new_seg_added = True
                                            for man_seg_two in manipulated_tier:
                                                if (manipulated_tier.elem[man_seg.index()+2].name == man_seg_two.name) & (not manipulated_tier.elem[man_seg.index()+2].index() == man_seg_two.index()):
                                                    manipulated_tier.elem[man_seg.index()+2].name = str(manipulated_tier.elem[man_seg.index()+2].name)+"_"+str(name_count)
                                                    name_count += 1
                                else:
                                    manipulated_tier.add(man_seg.index()+1,ref_seg)
                                    manipulated_tier.elem[man_seg.index()+1].content = inserted_segment
                                    manipulated_tier.elem[man_seg.index()+1].setParent(ref_seg)
                                    manipulated_tier.elem[man_seg.index()+1].name = str(manipulated_tier.elem[man_seg.index()].name)+"_added"
                                    for man_seg_two in manipulated_tier:
                                        if (manipulated_tier.elem[man_seg.index()+1].name == man_seg_two.name) & (not manipulated_tier.elem[man_seg.index()+1].index() == man_seg_two.index()):
                                            manipulated_tier.elem[man_seg.index()+1].name = str(manipulated_tier.elem[man_seg.index()+1].name)+"_"+str(name_count)
                                            name_count += 1
                            elif (man_seg.end == ref_seg.start) & (new_seg_added == False):
                                manipulated_tier.add(man_seg.index()+1,ref_seg)
                                manipulated_tier.elem[man_seg.index()+1].content = inserted_segment
                                manipulated_tier.elem[man_seg.index()+1].setParent(ref_seg)
                                manipulated_tier.elem[man_seg.index()+1].name = str(manipulated_tier.elem[man_seg.index()].name)+"_added"
                                for man_seg_two in manipulated_tier:
                                    if (manipulated_tier.elem[man_seg.index()+1].name == man_seg_two.name) & (not manipulated_tier.elem[man_seg.index()+1].index() == man_seg_two.index()):
                                        manipulated_tier.elem[man_seg.index()+1].name = str(manipulated_tier.elem[man_seg.index()+1].name)+"_"+str(name_count)
                                        name_count += 1
                            else:
                                new_seg_added = False
                                if man_seg.index() == 0:
                                    manipulated_tier.add(0,ref_seg)
                                    manipulated_tier.elem[0].content = inserted_segment
                                    manipulated_tier.elem[0].setParent(ref_seg)
                                    manipulated_tier.elem[0].name = str(manipulated_tier.elem[man_seg.index()].name)+"_addedbefore"
                                    for man_seg_two in manipulated_tier:
                                        if (manipulated_tier.elem[man_seg.index()+1].name == man_seg_two.name) & (not manipulated_tier.elem[man_seg.index()+1].index() == man_seg_two.index()):
                                            manipulated_tier.elem[man_seg.index()+1].name = str(manipulated_tier.elem[man_seg.index()+1].name)+"_"+str(name_count)
                                            name_count += 1

def fill_gaps_match(transcription,referenced_tier_name,manipulated_tier_name,referenced_segment,inserted_segment):
    '''Creates for a given transcription and a referenced tier new segments with a given content on a second tier for all those segments with a given content on a referenced tier, which do not have a corresponding, time-aligned segment on the second tier. 
    
    Keyword arguments:

    transcription         -- the file loaded with the function fromElan

    referenced_tier_name  -- the string used to identify the referenced tier, whose segments are used as the base for adding new segments

    manipulated_tier_name -- the string used to identify the manipulated tier, where the new segments are added to

    referenced_segment    -- the content of the referenced segment, based on which time-aligned, new segments are added

    inserted_segment      -- the content of the new, time-aligned segments added on the manipulated tier
    '''
    referenced_tier_exists = False
    manipulated_tier_exists = False
    name_count = 1
    for tier in transcription:
        if referenced_tier_name == tier.name:
            referenced_tier = transcription.getName(tier.name)
            referenced_tier_exists = True
        elif manipulated_tier_name == tier.name:
            manipulated_tier = transcription.getName(tier.name)
            manipulated_tier_exists = True
        manipulated_tier_segment_times = []
        if referenced_tier_exists & manipulated_tier_exists:
            referenced_tier_exists = False
            manipulated_tier_exists = False
            for seg in manipulated_tier:
                manipulated_tier_segment_times.append(seg.start)
            for ref_seg in referenced_tier:
                if not ref_seg.start in manipulated_tier_segment_times:
                    if ref_seg.content == referenced_segment:
                        new_seg_added = False
                        for man_seg in manipulated_tier:
                            if man_seg.end < ref_seg.start:
                                if man_seg.index()+1 != len(manipulated_tier):
                                    if not (manipulated_tier.elem[man_seg.index()+1].end < ref_seg.start):
                                        if manipulated_tier.elem[man_seg.index()+1].end > ref_seg.start:
                                            manipulated_tier.add(man_seg.index()+1,ref_seg)
                                            manipulated_tier.elem[man_seg.index()+1].content = inserted_segment
                                            manipulated_tier.elem[man_seg.index()+1].setParent(ref_seg)
                                            manipulated_tier.elem[man_seg.index()+1].name = str(manipulated_tier.elem[man_seg.index()].name)+"_added"
                                            for man_seg_two in manipulated_tier:
                                                if (manipulated_tier.elem[man_seg.index()+1].name == man_seg_two.name) & (not manipulated_tier.elem[man_seg.index()+1].index() == man_seg_two.index()):
                                                    manipulated_tier.elem[man_seg.index()+1].name = str(manipulated_tier.elem[man_seg.index()+1].name)+"_"+str(name_count)
                                                    name_count += 1
                                        else:
                                            manipulated_tier.add(man_seg.index()+2,ref_seg)
                                            manipulated_tier.elem[man_seg.index()+2].content = inserted_segment
                                            manipulated_tier.elem[man_seg.index()+2].setParent(ref_seg)
                                            manipulated_tier.elem[man_seg.index()+2].name = str(manipulated_tier.elem[man_seg.index()+1].name)+"_added"
                                            new_seg_added = True
                                            for man_seg_two in manipulated_tier:
                                                if (manipulated_tier.elem[man_seg.index()+2].name == man_seg_two.name) & (not manipulated_tier.elem[man_seg.index()+2].index() == man_seg_two.index()):
                                                    manipulated_tier.elem[man_seg.index()+2].name = str(manipulated_tier.elem[man_seg.index()+2].name)+"_"+str(name_count)
                                                    name_count += 1
                                else:
                                    manipulated_tier.add(man_seg.index()+1,ref_seg)
                                    manipulated_tier.elem[man_seg.index()+1].content = inserted_segment
                                    manipulated_tier.elem[man_seg.index()+1].setParent(ref_seg)
                                    manipulated_tier.elem[man_seg.index()+1].name = str(manipulated_tier.elem[man_seg.index()].name)+"_added"
                                    for man_seg_two in manipulated_tier:
                                        if (manipulated_tier.elem[man_seg.index()+1].name == man_seg_two.name) & (not manipulated_tier.elem[man_seg.index()+1].index() == man_seg_two.index()):
                                            manipulated_tier.elem[man_seg.index()+1].name = str(manipulated_tier.elem[man_seg.index()+1].name)+"_"+str(name_count)
                                            name_count += 1
                            elif (man_seg.end == ref_seg.start) & (new_seg_added == False):
                                manipulated_tier.add(man_seg.index()+1,ref_seg)
                                manipulated_tier.elem[man_seg.index()+1].content = inserted_segment
                                manipulated_tier.elem[man_seg.index()+1].setParent(ref_seg)
                                manipulated_tier.elem[man_seg.index()+1].name = str(manipulated_tier.elem[man_seg.index()].name)+"_added"
                                for man_seg_two in manipulated_tier:
                                    if (manipulated_tier.elem[man_seg.index()+1].name == man_seg_two.name) & (not manipulated_tier.elem[man_seg.index()+1].index() == man_seg_two.index()):
                                        manipulated_tier.elem[man_seg.index()+1].name = str(manipulated_tier.elem[man_seg.index()+1].name)+"_"+str(name_count)
                                        name_count += 1
                            else:
                                new_seg_added = False
                                if man_seg.index() == 0:
                                    manipulated_tier.add(0,ref_seg)
                                    manipulated_tier.elem[0].content = inserted_segment
                                    manipulated_tier.elem[0].setParent(ref_seg)
                                    manipulated_tier.elem[0].name = str(manipulated_tier.elem[man_seg.index()].name)+"_addedbefore"
                                    for man_seg_two in manipulated_tier:
                                        if (manipulated_tier.elem[man_seg.index()+1].name == man_seg_two.name) & (not manipulated_tier.elem[man_seg.index()+1].index() == man_seg_two.index()):
                                            manipulated_tier.elem[man_seg.index()+1].name = str(manipulated_tier.elem[man_seg.index()+1].name)+"_"+str(name_count)
                                            name_count += 1

def fix_affixes(transcription,referenced_tier_name,manipulated_tier_name):
    '''Fixes for a given transcription on a given tier the content of all those segments, whose corresponding, time-aligned segments on a referenced tier are marked as affixes (prefixes, suffixes or infixes), so that they are marked as affixes as well.
    
    Keyword arguments:

    transcription         -- the file loaded with the function fromElan

    referenced_tier_name  -- the string used to identify the referenced tier, whose segments contents are used as the base

    manipulated_tier_name -- the string used to identify the manipulated tier, whose segments contents are changed in order to match the status as affixes of their time-aligned segments on the referenced tier
    '''
    referenced_tier_exists = False
    manipulated_tier_exists = False
    for tier in transcription:
        if referenced_tier_name in tier.name:
            referenced_tier = transcription.getName(tier.name)
            referenced_tier_exists = True
        elif manipulated_tier_name in tier.name:
            manipulated_tier = transcription.getName(tier.name)
            manipulated_tier_exists = True
        if referenced_tier_exists & manipulated_tier_exists:
            referenced_tier_exists = False
            manipulated_tier_exists = False
            for ref_seg in referenced_tier:
                if ref_seg.content.startswith("-") & ref_seg.content.endswith("-"):
                    for man_seg in manipulated_tier:
                        if (ref_seg.start == man_seg.start) & (ref_seg.end == man_seg.end):
                            if (not man_seg.content.startswith("-")) & (not man_seg.content == ""):
                                man_seg.content = "-" + man_seg.content
                            if (not man_seg.content.endswith("-")) & (not man_seg.content == ""):
                                man_seg.content += "-"
                elif ref_seg.content.endswith("-"):
                    for man_seg in manipulated_tier:
                        if (ref_seg.start == man_seg.start) & (ref_seg.end == man_seg.end):
                            if (not man_seg.content.endswith("-")) & (not man_seg.content == ""):
                                man_seg.content += "-"
                elif ref_seg.content.startswith("-"):
                    for man_seg in manipulated_tier:
                        if (ref_seg.start == man_seg.start) & (ref_seg.end == man_seg.end):
                            if (not man_seg.content.startswith("-")) & (not man_seg.content == ""):
                                man_seg.content = "-" + man_seg.content



def remove_segments(transcription,segment_content,manipulated_tier_name=""):
    '''Removes all segments on either all or only on specified tiers of a transcription.
    
    Keyword arguments:
    
    transcription   -- the file loaded with the function fromElan

    segment_content -- the content by which segments, which are to be removed, are identified
    
    Optional keyword argument:

    manipulated_tier_name -- the string used to identify the manipulated tier, where segments are to be removed
    '''
    if manipulated_tier_name == "":
        for tier in transcription:
            for seg in tier:
                if segment_content == seg.content:
                    if seg.children():
                        for child in seg.children():
                            for tier2 in transcription:
                                if child in tier2:
                                    tier2.remove(child)
                                    break
                    if seg.parent():
                        if (seg.start != seg.parent().start) & (seg.end != seg.parent().end):
                            if (seg.end == seg.parent().end) | ((seg.start > seg.parent().start) & (seg.end < seg.parent().end)):
                                tier.elem[seg.index()-1].end = seg.end
                            elif (seg.start == seg.parent().start):
                                tier.elem[seg.index()+1].start = seg.start
                    tier.pop(seg.index())
    else:
        manipulated_tier_exists = False
        for tier in transcription:
            if manipulated_tier_name in tier.name:
                manipulated_tier = transcription.getName(tier.name)
                manipulated_tier_exists = True
            if manipulated_tier_exists:
                manipulated_tier_exists = False
                for seg in manipulated_tier:
                    if segment_content == seg.content:
                        for child in seg.children():
                            for tier2 in transcription:
                                if child in tier2:
                                    tier2.remove(child)
                                    break
                        if seg.parent():
                            if (seg.start != seg.parent().start) & (seg.end != seg.parent().end):
                                if (seg.end == seg.parent().end) | ((seg.start > seg.parent().start) & (seg.end < seg.parent().end)):
                                    manipulated_tier.elem[seg.index()-1].end = seg.end
                                elif (seg.start == seg.parent().start):
                                    manipulated_tier.elem[seg.index()+1].start = seg.start
                        manipulated_tier.pop(seg.index())


def define_content_old_version(transcription,referenced_tier_name,manipulated_tier_name,referenced_segment_content,defined_segment_content,manipulated_segment_content=""):
    if not isinstance(referenced_tier_name,str):
        raise Exception("Your given value for the parameter 'referenced_tier_name' is not a string. It has to be.")
    elif not isinstance(manipulated_tier_name,str):
        raise Exception("Your given value for the parameter 'manipulated_tier_name' is not a string. It has to be.")
    elif not isinstance(referenced_segment_content,str):
        raise Exception("Your given value for the parameter 'referenced_segment_content' is not a string. It has to be.")
    elif not isinstance(defined_segment_content,(str,list)):
        raise Exception("Your given value for the parameter 'defined_segment_content' is neither a string nor a list. It has to be.")
    elif not isinstance(manipulated_segment_content,(str,list)):
        raise Exception("Your given value for the parameter 'manipulated_segment_content' is neither a string nor a list. It has to be.")
    elif ((isinstance(defined_segment_content,list)) & (len(defined_segment_content) < 2)) | ((isinstance(manipulated_segment_content,list)) & (len(manipulated_segment_content) < 2)):
        raise Exception("At least one of the lists for the parameters 'defined_segment_content' and 'manipulated_segment_content' contains only one item. If so, write strings instead.")
    elif (isinstance(defined_segment_content,list) & isinstance(manipulated_segment_content,list)) & (len(defined_segment_content) != len(manipulated_segment_content)):
        raise Exception("The two parameters 'defined_segment_content' and 'manipulated_segment_content' have to have the same number of items, which they currently do not.")
    elif isinstance(defined_segment_content,list):
        if (not isinstance(manipulated_segment_content,list)) & (not manipulated_segment_content == ""):
            raise Exception("The arguments for the parameters 'defined_segment_content' and 'manipulated_segment_content' have to be both either lists or strings if both are specified. They are currently not.")
        else:
            for item in defined_segment_content:
                if not isinstance(item,str):
                    raise Exception("Your list for the parameter 'defined_segment_content' contains an item, which is not a string. It has to be.")
    elif isinstance(manipulated_segment_content,list):
        if not isinstance(defined_segment_content,list):
            raise Exception("The arguments for the parameters 'defined_segment_content' and 'manipulated_segment_content' have to be both either lists or strings. They are currently not.")
        else:
            for item in manipulated_segment_content:
                if not isinstance(item,str):
                    raise Exception("Your list for the parameter 'manipulated_segment_content' contains an item, which is not a string. It has to be.")

    referenced_tier_exists = False
    manipulated_tier_exists = False
    for tier in transcription:
        if referenced_tier_name in tier.name:
            referenced_tier = transcription.getName(tier.name)
            referenced_tier_exists = True
        if manipulated_tier_name in tier.name:
            manipulated_tier = transcription.getName(tier.name)
            manipulated_tier_exists = True
        if referenced_tier_exists & manipulated_tier_exists:
            referenced_tier_exists = False
            manipulated_tier_exists = False
            if manipulated_segment_content == "":
                if isinstance(defined_segment_content,str):
                    for ref_seg in referenced_tier:
                        if ref_seg.content == referenced_segment_content:
                            for man_seg in manipulated_tier:
                                if (man_seg.start == ref_seg.start) & (man_seg.end == ref_seg.end):
                                    man_seg.content = defined_segment_content
                elif isinstance(defined_segment_content,list):
                    for ref_seg in referenced_tier:
                        man_segs_index_of_ref_seg = []
                        number_of_items = 0
                        if ref_seg.content == referenced_segment_content:
                            for man_seg in manipulated_tier:
                                if ((man_seg.start == ref_seg.start) | ((man_seg.start > ref_seg.start) & (man_seg.end < ref_seg.end))) | (man_seg.end == ref_seg.end):
                                    man_segs_index_of_ref_seg.append((man_seg.index(),number_of_items))
                                    number_of_items += 1
                            if len(man_segs_index_of_ref_seg) == len(defined_segment_content):
                                for man_seg in manipulated_tier:
                                    for (man_seg_index,man_seg_count) in man_segs_index_of_ref_seg:
                                        if man_seg.index() == man_seg_index:
                                            man_seg.content = defined_segment_content[man_seg_count]

            elif isinstance(manipulated_segment_content,str):
                for ref_seg in referenced_tier:
                    if ref_seg.content == referenced_segment_content:
                        for man_seg in manipulated_tier:
                            if (man_seg.start == ref_seg.start) & (man_seg.end == ref_seg.end) & (man_seg.content == manipulated_segment_content):
                                man_seg.content = defined_segment_content

            elif isinstance(manipulated_segment_content,list):
                for ref_seg in referenced_tier:
                    man_segs_index_of_ref_seg = []
                    man_segs_content_of_ref_seg = []
                    number_of_items = 0
                    if ref_seg.content == referenced_segment_content:
                        for man_seg in manipulated_tier:
                            if ((man_seg.start == ref_seg.start) | ((man_seg.start > ref_seg.start) & (man_seg.end < ref_seg.end))) | (man_seg.end == ref_seg.end):
                                man_segs_index_of_ref_seg.append((man_seg.index(),number_of_items))
                                man_segs_content_of_ref_seg.append((man_seg.content,number_of_items))
                                number_of_items += 1
                        if len(man_segs_index_of_ref_seg) == len(defined_segment_content):
                            if all(man_seg_content == manipulated_segment_content[man_seg_count] for (man_seg_content,man_seg_count) in man_segs_content_of_ref_seg):
                                for man_seg in manipulated_tier:
                                    for (man_seg_index,man_seg_count) in man_segs_index_of_ref_seg:
                                        if man_seg.index() == man_seg_index:
                                            man_seg.content = defined_segment_content[man_seg_count]

def define_content_old_version_tier_match(transcription,referenced_tier_name,manipulated_tier_name,referenced_segment_content,defined_segment_content,manipulated_segment_content=""):
    if not isinstance(referenced_tier_name,str):
        raise Exception("Your given value for the parameter 'referenced_tier_name' is not a string. It has to be.")
    elif not isinstance(manipulated_tier_name,str):
        raise Exception("Your given value for the parameter 'manipulated_tier_name' is not a string. It has to be.")
    elif not isinstance(referenced_segment_content,str):
        raise Exception("Your given value for the parameter 'referenced_segment_content' is not a string. It has to be.")
    elif not isinstance(defined_segment_content,(str,list)):
        raise Exception("Your given value for the parameter 'defined_segment_content' is neither a string nor a list. It has to be.")
    elif not isinstance(manipulated_segment_content,(str,list)):
        raise Exception("Your given value for the parameter 'manipulated_segment_content' is neither a string nor a list. It has to be.")
    elif ((isinstance(defined_segment_content,list)) & (len(defined_segment_content) < 2)) | ((isinstance(manipulated_segment_content,list)) & (len(manipulated_segment_content) < 2)):
        raise Exception("At least one of the lists for the parameters 'defined_segment_content' and 'manipulated_segment_content' contains only one item. If so, write strings instead.")
    elif (isinstance(defined_segment_content,list) & isinstance(manipulated_segment_content,list)) & (len(defined_segment_content) != len(manipulated_segment_content)):
        raise Exception("The two parameters 'defined_segment_content' and 'manipulated_segment_content' have to have the same number of items, which they currently do not.")
    elif isinstance(defined_segment_content,list):
        if (not isinstance(manipulated_segment_content,list)) & (not manipulated_segment_content == ""):
            raise Exception("The arguments for the parameters 'defined_segment_content' and 'manipulated_segment_content' have to be both either lists or strings if both are specified. They are currently not.")
        else:
            for item in defined_segment_content:
                if not isinstance(item,str):
                    raise Exception("Your list for the parameter 'defined_segment_content' contains an item, which is not a string. It has to be.")
    elif isinstance(manipulated_segment_content,list):
        if not isinstance(defined_segment_content,list):
            raise Exception("The arguments for the parameters 'defined_segment_content' and 'manipulated_segment_content' have to be both either lists or strings. They are currently not.")
        else:
            for item in manipulated_segment_content:
                if not isinstance(item,str):
                    raise Exception("Your list for the parameter 'manipulated_segment_content' contains an item, which is not a string. It has to be.")

    referenced_tier_exists = False
    manipulated_tier_exists = False
    for tier in transcription:
        if referenced_tier_name == tier.name:
            referenced_tier = transcription.getName(tier.name)
            referenced_tier_exists = True
        if manipulated_tier_name == tier.name:
            manipulated_tier = transcription.getName(tier.name)
            manipulated_tier_exists = True
        if referenced_tier_exists & manipulated_tier_exists:
            referenced_tier_exists = False
            manipulated_tier_exists = False
            if manipulated_segment_content == "":
                if isinstance(defined_segment_content,str):
                    for ref_seg in referenced_tier:
                        if ref_seg.content == referenced_segment_content:
                            for man_seg in manipulated_tier:
                                if (man_seg.start == ref_seg.start) & (man_seg.end == ref_seg.end):
                                    man_seg.content = defined_segment_content
                elif isinstance(defined_segment_content,list):
                    for ref_seg in referenced_tier:
                        man_segs_index_of_ref_seg = []
                        number_of_items = 0
                        if ref_seg.content == referenced_segment_content:
                            for man_seg in manipulated_tier:
                                if ((man_seg.start == ref_seg.start) | ((man_seg.start > ref_seg.start) & (man_seg.end < ref_seg.end))) | (man_seg.end == ref_seg.end):
                                    man_segs_index_of_ref_seg.append((man_seg.index(),number_of_items))
                                    number_of_items += 1
                            if len(man_segs_index_of_ref_seg) == len(defined_segment_content):
                                for man_seg in manipulated_tier:
                                    for (man_seg_index,man_seg_count) in man_segs_index_of_ref_seg:
                                        if man_seg.index() == man_seg_index:
                                            man_seg.content = defined_segment_content[man_seg_count]

            elif isinstance(manipulated_segment_content,str):
                for ref_seg in referenced_tier:
                    if ref_seg.content == referenced_segment_content:
                        for man_seg in manipulated_tier:
                            if (man_seg.start == ref_seg.start) & (man_seg.end == ref_seg.end) & (man_seg.content == manipulated_segment_content):
                                man_seg.content = defined_segment_content

            elif isinstance(manipulated_segment_content,list):
                for ref_seg in referenced_tier:
                    man_segs_index_of_ref_seg = []
                    man_segs_content_of_ref_seg = []
                    number_of_items = 0
                    if ref_seg.content == referenced_segment_content:
                        for man_seg in manipulated_tier:
                            if ((man_seg.start == ref_seg.start) | ((man_seg.start > ref_seg.start) & (man_seg.end < ref_seg.end))) | (man_seg.end == ref_seg.end):
                                man_segs_index_of_ref_seg.append((man_seg.index(),number_of_items))
                                man_segs_content_of_ref_seg.append((man_seg.content,number_of_items))
                                number_of_items += 1
                        if len(man_segs_index_of_ref_seg) == len(defined_segment_content):
                            if all(man_seg_content == manipulated_segment_content[man_seg_count] for (man_seg_content,man_seg_count) in man_segs_content_of_ref_seg):
                                for man_seg in manipulated_tier:
                                    for (man_seg_index,man_seg_count) in man_segs_index_of_ref_seg:
                                        if man_seg.index() == man_seg_index:
                                            man_seg.content = defined_segment_content[man_seg_count]


def define_content(transcription,manipulated_tier_name: str | tuple,defined_segment_content: str | list | tuple,**conditions_on_tiers: tuple):
    '''Defines the content of all those segments on a tier, which either a) have a certain content and/or b) are time-aligned with segments on other tiers, which fulfill certain conditions regarding their content.

    Keyword arguments:

    - transcription -- The file loaded with the function 'fromElan'

    - manipulated_tier_name -- The string used to identify the name of the tier, whose segments are to be manipulated. By default, the condition is that the string is IN the tier name. Alternatively, using a tuple with the second argument being the string 'MATCH', the string has to match the tier name; e.g. (<tier.name>,"MATCH"); options are "MATCH", "IN".

    - defined_segment_content -- How the segments of a tier should be changed. If only a string is given, it defines the content of every found segment. If a tuple is given, additional operations are possible; e.g. (<content>,"ADD_TO_END") adds <content> to the end of the string of the current content of a segment. options are "ADD_TO_END", "ADD_TO_START", "REPLACE_BY_INDEX", "REPLACE_BY_SIGN" (here, the third and optionally fourth element in the tuple specify the index or the sign to be replaced)

    - **conditions_on_tiers -- The dict to specify the conditions for which segments are to be changed. The key name is irrelevant, as long as it is unique for every condition. The value has to be a tuple; (<tier.name>,<option1>,<string>,<option2>,<bool>). <option1>, <option2> and <bool> are optional. <option1> can be "MATCH", "IN" (for the tier name). <string> is either a string (while <option2> can be "MATCH", "IN" or "REGEX") or the name of a string method (as a string) (while <option2> is a string with the methods argument) or a custom function which takes the segment content as input and returns either True or False (while <option2> is a list with additional arguments of that function).
    
    '''

    manipulated_tier_exists = False
    found_tiers = []

    for tier in transcription:

        if isinstance(manipulated_tier_name,str):
            if manipulated_tier_name in tier.name:
                manipulated_tier = transcription.getName(tier.name)
                manipulated_tier_exists = True
        elif isinstance(manipulated_tier_name,tuple):
            if manipulated_tier_name[1] == "MATCH":
                if manipulated_tier_name[0] == tier.name:
                    manipulated_tier = transcription.getName(tier.name)
                    manipulated_tier_exists = True
            elif manipulated_tier_name[1] == "IN":
                if manipulated_tier_name[0] in tier.name:
                    manipulated_tier = transcription.getName(tier.name)
                    manipulated_tier_exists = True

        for number,cond_value in enumerate(conditions_on_tiers.values()):
            if cond_value[1] == "MATCH":
                if cond_value[0] == tier.name:
                    found_tiers.append((number,tier.name))
            elif cond_value[0] in tier.name:
                found_tiers.append((number,tier.name))

        if (len(found_tiers) == len(conditions_on_tiers)) & manipulated_tier_exists:

            found_tiers.sort()

            found_tiers_sorted = []
            for (number,tier_name) in found_tiers:
                found_tiers_sorted.append(tier_name)

            manipulated_tier_exists = False
            met_conditions_times = {}
            met_conditions_times_lists = {}

            for number,cond_value in enumerate(conditions_on_tiers.values()):

                if any(isinstance(item,list) for item in cond_value):
                    met_conditions_times_lists[number] = []
                else:
                    met_conditions_times[number] = []


                if len(cond_value) == 2:

                    if isinstance(cond_value[1],str):
                        if (cond_value[1] != "MATCH") & (cond_value[1] != "IN"):
                            if hasattr("test",cond_value[1]):
                                for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                    if getattr(cond_seg.content,cond_value[1])():
                                        met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                            elif cond_value[1] == ">.<":
                                for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                    met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                            elif cond_value[1] != ">.<":

                                for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                    if cond_seg.content == cond_value[1]:
                                        met_conditions_times[number].append((cond_seg.start,cond_seg.end))


                    elif callable(cond_value[1]):
                        for cond_seg in transcription.getName(found_tiers_sorted[number]):
                            if cond_value[1](cond_seg.content):
                                met_conditions_times[number].append((cond_seg.start,cond_seg.end))

                    elif isinstance(cond_value[1],list):
                        
                        if ">...<" in cond_value[1]:
                            print

                        elif not ">...<" in cond_value[1]:
                            indices_without_var_seg = []
                            for index,seg in enumerate(cond_value[1]):
                                if seg != ">.<":
                                    indices_without_var_seg.append(index)
                            for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                cond_seg_sublist_content = []
                                cond_seg_sublist_times = []
                                for seg in transcription.getName(found_tiers_sorted[number]).elem[cond_seg.index():cond_seg.index()+len(cond_value[1])]:
                                    cond_seg_sublist_content.append(seg.content)
                                    cond_seg_sublist_times.append((seg.start,seg.end))
                                if len(cond_value[1]) == len(cond_seg_sublist_content):
                                    if all(cond_value[1][index] == cond_seg_sublist_content[index] for index in indices_without_var_seg):
                                        met_conditions_times_lists[number].append(tuple(cond_seg_sublist_times))

                elif len(cond_value) == 3:

                    if isinstance(cond_value[1],str):

                        if isinstance(cond_value[2],bool):
                            if hasattr("test",cond_value[1]):
                                for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                    if getattr(cond_seg.content,cond_value[1])() == cond_value[2]:
                                        met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                            else:
                                for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                    if (cond_seg.content == cond_value[1]) == cond_value[2]:
                                        met_conditions_times[number].append((cond_seg.start,cond_seg.end))

                        elif (cond_value[1] != "MATCH") & (cond_value[1] != "IN"):
                            if hasattr("test",cond_value[1]):
                                if isinstance(cond_value[2],tuple):
                                    for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                        if getattr(cond_seg.content,cond_value[1])(*cond_value[2]):
                                            met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                                else:
                                    for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                        if getattr(cond_seg.content,cond_value[1])(cond_value[2]):
                                            met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                            elif cond_value[2] == "IN":
                                for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                    if cond_value[1] in cond_seg.content:
                                        met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                            elif cond_value[2] == "REGEX":
                                for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                    if re.search(str(cond_value[1]),cond_seg.content):
                                        met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                            elif cond_value[2] == "MATCH":
                                for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                    if cond_value[1] == cond_seg.content:
                                        met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                        elif (cond_value[1] == "MATCH") | (cond_value[1] == "IN"):
                            if isinstance(cond_value[2],str):
                                if hasattr("test",cond_value[2]):
                                    for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                        if getattr(cond_seg.content,cond_value[2])():
                                            met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                                elif cond_value[2] == ">.<":
                                    for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                        met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                                elif cond_value[2] != ">.<":
                                    for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                        if cond_seg.content == cond_value[2]:
                                            met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                            elif callable(cond_value[2]):
                                for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                    if cond_value[2](cond_seg.content):
                                        met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                            elif isinstance(cond_value[2],list):

                                if ">...<" in cond_value[2]:
                                    print

                                elif not ">...<" in cond_value[2]:
                                    indices_without_var_seg = []
                                    for index,seg in enumerate(cond_value[2]):
                                        if seg != ">.<":
                                            indices_without_var_seg.append(index)
                                    for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                        cond_seg_sublist_content = []
                                        cond_seg_sublist_times = []
                                        for seg in transcription.getName(found_tiers_sorted[number]).elem[cond_seg.index():cond_seg.index()+len(cond_value[2])]:
                                            cond_seg_sublist_content.append(seg.content)
                                            cond_seg_sublist_times.append((seg.start,seg.end))
                                        if len(cond_value[2]) == len(cond_seg_sublist_content):
                                            if all(cond_value[2][index] == cond_seg_sublist_content[index] for index in indices_without_var_seg):
                                                met_conditions_times_lists[number].append(cond_seg_sublist_times)

                    elif callable(cond_value[1]):
                        if isinstance(cond_value[2],str):
                            for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                if cond_value[1](cond_seg.content,cond_value[2]):
                                    met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                        elif isinstance(cond_value[2],tuple):
                            for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                if cond_value[1](cond_seg.content,*cond_value[2]):
                                    met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                        elif isinstance(cond_value[2],bool):
                            for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                if (cond_value[1](cond_seg.content)) == cond_value[2]:
                                    met_conditions_times[number].append((cond_seg.start,cond_seg.end))

                elif len(cond_value) == 4:

                    if isinstance(cond_value[1],str):
                        
                        if (cond_value[1] == "MATCH") | (cond_value[1] == "IN"):
                            if isinstance(cond_value[2],str):
                                if hasattr("test",cond_value[2]):
                                    if isinstance(cond_value[3],bool):
                                        for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                            if (getattr(cond_seg.content,cond_value[2])()) == cond_value[3]:
                                                met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                                    elif isinstance(cond_value[3],tuple):
                                        for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                            if getattr(cond_seg.content,cond_value[2])(*cond_value[3]):
                                                met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                                    else:
                                        for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                            if getattr(cond_seg.content,cond_value[2])(cond_value[3]):
                                                met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                                elif isinstance(cond_value[3],bool):
                                    for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                        if (cond_value[2] == cond_seg.content) == cond_value[3]:
                                            met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                                elif cond_value[3] == "IN":
                                    for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                        if cond_value[2] in cond_seg.content:
                                            met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                                elif cond_value[3] == "REGEX":
                                    for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                        if re.search(str(cond_value[2]),cond_seg.content):
                                            met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                                elif cond_value[3] == "MATCH":
                                    for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                        if cond_value[2] == cond_seg.content:
                                            met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                            elif callable(cond_value[2]):
                                if isinstance(cond_value[3],bool):
                                    for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                        if (cond_value[2](cond_seg.content)) == cond_value[3]:
                                            met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                                elif isinstance(cond_value[3],tuple):
                                    for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                        if cond_value[2](cond_seg.content,*cond_value[3]):
                                            met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                                else:
                                    for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                        if cond_value[2](cond_seg.content,cond_value[3]):
                                            met_conditions_times[number].append((cond_seg.start,cond_seg.end))

                        elif (cond_value[1] != "MATCH") & (cond_value[1] != "IN"):
                            if hasattr("test",cond_value[1]):
                                if isinstance(cond_value[2],tuple) & isinstance(cond_value[3],bool):
                                    for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                        if (getattr(cond_seg.content,cond_value[1])(*cond_value[2])) == cond_value[3]:
                                            met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                                elif isinstance(cond_value[3],bool):
                                    for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                        if (getattr(cond_seg.content,cond_value[1])(cond_value[2])) == cond_value[3]:
                                            met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                            elif (cond_value[2] == "IN") & isinstance(cond_value[3],bool):
                                for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                    if (cond_value[1] in cond_seg.content) == cond_value[3]:
                                        met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                            elif (cond_value[2] == "REGEX") & isinstance(cond_value[3],bool):
                                for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                    if bool(re.search(str(cond_value[1]),cond_seg.content)) == cond_value[3]:
                                        met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                            elif (cond_value[2] == "MATCH") & isinstance(cond_value[3],bool):
                                for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                    if (cond_value[1] == cond_seg.content) == cond_value[3]:
                                        met_conditions_times[number].append((cond_seg.start,cond_seg.end))

                    elif callable(cond_value[1]):
                        if isinstance(cond_value[2],tuple) & isinstance(cond_value[3],bool):
                            for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                if (cond_value[1](cond_seg.content,*cond_value[2])) == cond_value[3]:
                                    met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                        elif isinstance(cond_value[3],bool):
                            for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                if (cond_value[1](cond_seg.content,cond_value[2])) == cond_value[3]:
                                    met_conditions_times[number].append((cond_seg.start,cond_seg.end))

                elif (len(cond_value) == 5) & ((cond_value[1] == "MATCH") | (cond_value[1] == "IN")):

                    if isinstance(cond_value[2],str) & isinstance(cond_value[4],bool):
                        if hasattr("test",cond_value[2]):
                            if isinstance(cond_value[3],tuple):
                                for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                    if (getattr(cond_seg.content,cond_value[2])(*cond_value[3])) == cond_value[4]:
                                        met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                            else:
                                for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                    if (getattr(cond_seg.content,cond_value[2])(cond_value[3])) == cond_value[4]:
                                        met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                        elif cond_value[3] == "IN":
                            for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                if (cond_value[2] in cond_seg.content) == cond_value[4]:
                                    met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                        elif cond_value[3] == "REGEX":
                            for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                if bool(re.search(str(cond_value[2]),cond_seg.content)) == cond_value[4]:
                                    met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                        elif cond_value[3] == "MATCH":
                            for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                if (cond_value[2] == cond_seg.content) == cond_value[4]:
                                    met_conditions_times[number].append((cond_seg.start,cond_seg.end))

                    elif callable(cond_value[2]) & isinstance(cond_value[4],bool):
                        if isinstance(cond_value[3],tuple):
                            for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                if (cond_value[2](cond_seg.content,*cond_value[3])) == cond_value[4]:
                                    met_conditions_times[number].append((cond_seg.start,cond_seg.end))
                        else:
                            for cond_seg in transcription.getName(found_tiers_sorted[number]):
                                if (cond_value[2](cond_seg.content,cond_value[3])) == cond_value[4]:
                                    met_conditions_times[number].append((cond_seg.start,cond_seg.end))



            if len(met_conditions_times) > 0:

                final_met_conditions_times = list(set.intersection(*map(set,met_conditions_times.values())))
                final_met_conditions_times.sort()

            if len(met_conditions_times_lists) > 0:

                final_met_conditions_times_lists = list(set.intersection(*map(set,met_conditions_times_lists.values())))
                final_met_conditions_times_lists.sort()

                for index2,structure in enumerate(final_met_conditions_times_lists):
                    final_met_conditions_times_lists[index2] = list(structure)

                if len(final_met_conditions_times_lists) == 0:
                    final_met_conditions_times_lists_length = 0
                elif len(final_met_conditions_times_lists) > 0:
                    final_met_conditions_times_lists_length = len(final_met_conditions_times_lists[0])

            if (len(met_conditions_times) > 0) & (len(met_conditions_times_lists) <= 0):
                #ONLY SIMPLE STRINGS

                man_seg_sublist = []

                if isinstance(defined_segment_content,str):

                    for man_seg in manipulated_tier:
                        if (man_seg.start,man_seg.end) in final_met_conditions_times:
                            man_seg.content = defined_segment_content
                        elif any(man_seg.start == cond_seg_start for cond_seg_start,cond_seg_end in final_met_conditions_times):
                            man_seg_sublist = []
                            man_seg_sublist.append(man_seg.index())
                        elif any((man_seg.start > cond_seg_start) & (man_seg.end < cond_seg_end) for cond_seg_start,cond_seg_end in final_met_conditions_times):
                            man_seg_sublist.append(man_seg.index())
                        elif any(man_seg.end == cond_seg_end for cond_seg_start,cond_seg_end in final_met_conditions_times):
                            man_seg_sublist.append(man_seg.index())
                            for man_seg_index in man_seg_sublist:
                                manipulated_tier.elem[man_seg_index].content = defined_segment_content
                            man_seg_sublist = []

                elif isinstance(defined_segment_content,tuple):
                    
                    if len(defined_segment_content) == 2:

                        if defined_segment_content[1] == "MATCH":
                            for man_seg in manipulated_tier:
                                if (man_seg.start,man_seg.end) in final_met_conditions_times:
                                    man_seg.content = defined_segment_content[0]
                                elif any(man_seg.start == cond_seg_start for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist = []
                                    man_seg_sublist.append(man_seg.index())
                                elif any((man_seg.start > cond_seg_start) & (man_seg.end < cond_seg_end) for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist.append(man_seg.index())
                                elif any(man_seg.end == cond_seg_end for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist.append(man_seg.index())
                                    for man_seg_index in man_seg_sublist:
                                        manipulated_tier.elem[man_seg_index].content = defined_segment_content[0]
                                    man_seg_sublist = []

                        elif defined_segment_content[1] == "ADD_TO_START":
                            for man_seg in manipulated_tier:
                                if (man_seg.start,man_seg.end) in final_met_conditions_times:
                                    man_seg.content = defined_segment_content[0] + man_seg.content
                                elif any(man_seg.start == cond_seg_start for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist = []
                                    man_seg_sublist.append(man_seg.index())
                                elif any((man_seg.start > cond_seg_start) & (man_seg.end < cond_seg_end) for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist.append(man_seg.index())
                                elif any(man_seg.end == cond_seg_end for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist.append(man_seg.index())
                                    for man_seg_index in man_seg_sublist:
                                        manipulated_tier.elem[man_seg_index].content = defined_segment_content[0] + man_seg.content
                                    man_seg_sublist = []

                        elif defined_segment_content[1] == "ADD_TO_END":
                            for man_seg in manipulated_tier:
                                if (man_seg.start,man_seg.end) in final_met_conditions_times:
                                    man_seg.content += defined_segment_content[0]
                                elif any(man_seg.start == cond_seg_start for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist = []
                                    man_seg_sublist.append(man_seg.index())
                                elif any((man_seg.start > cond_seg_start) & (man_seg.end < cond_seg_end) for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist.append(man_seg.index())
                                elif any(man_seg.end == cond_seg_end for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist.append(man_seg.index())
                                    for man_seg_index in man_seg_sublist:
                                        manipulated_tier.elem[man_seg_index].content += defined_segment_content[0]
                                    man_seg_sublist = []

                        elif defined_segment_content[1] == "ALL":
                            for man_seg in manipulated_tier:
                                if (man_seg.start,man_seg.end) in final_met_conditions_times:
                                    man_seg.content = defined_segment_content[0]
                                elif any(man_seg.start == cond_seg_start for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist = []
                                    man_seg_sublist.append(man_seg.index())
                                elif any((man_seg.start > cond_seg_start) & (man_seg.end < cond_seg_end) for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist.append(man_seg.index())
                                elif any(man_seg.end == cond_seg_end for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist.append(man_seg.index())
                                    for man_seg_index in man_seg_sublist:
                                        manipulated_tier.elem[man_seg_index].content = defined_segment_content[0]
                                    man_seg_sublist = []

                        elif defined_segment_content[1] == "ONLY_TIME-ALIGNED":
                            for man_seg in manipulated_tier:
                                if (man_seg.start,man_seg.end) in final_met_conditions_times:
                                    man_seg.content = defined_segment_content[0]

                    elif len(defined_segment_content) == 3:

                        if defined_segment_content[1] == "REPLACE_BY_INDEX":
                            for man_seg in manipulated_tier:
                                if (man_seg.start,man_seg.end) in final_met_conditions_times:
                                    man_seg_content_list = list(man_seg.content)
                                    man_seg_content_list[defined_segment_content[2]] = defined_segment_content[0]
                                    man_seg.content = "".join(man_seg_content_list) 
                                elif any(man_seg.start == cond_seg_start for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist = []
                                    man_seg_sublist.append(man_seg.index())
                                elif any((man_seg.start > cond_seg_start) & (man_seg.end < cond_seg_end) for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist.append(man_seg.index())
                                elif any(man_seg.end == cond_seg_end for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist.append(man_seg.index())
                                    for man_seg_index in man_seg_sublist[defined_segment_content[2]]:
                                        manipulated_tier.elem[man_seg_index].content = defined_segment_content[0]
                                    man_seg_sublist = []

                        elif defined_segment_content[1] == "REPLACE_BY_SIGN":
                            for man_seg in manipulated_tier:
                                if (man_seg.start,man_seg.end) in final_met_conditions_times:
                                    man_seg.content = man_seg.content.replace(defined_segment_content[2],defined_segment_content[0])
                                elif any(man_seg.start == cond_seg_start for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist = []
                                    man_seg_sublist.append(man_seg.index())
                                elif any((man_seg.start > cond_seg_start) & (man_seg.end < cond_seg_end) for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist.append(man_seg.index())
                                elif any(man_seg.end == cond_seg_end for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist.append(man_seg.index())
                                    for man_seg_index in man_seg_sublist:
                                        manipulated_tier.elem[man_seg_index].content = manipulated_tier.elem[man_seg_index].content.replace(defined_segment_content[2],defined_segment_content[0])
                                    man_seg_sublist = []

                    elif len(defined_segment_content) == 4:

                        if defined_segment_content[1] == "REPLACE_BY_INDEX":
                            for man_seg in manipulated_tier:
                                if (man_seg.start,man_seg.end) in final_met_conditions_times:
                                    man_seg_content_list = list(man_seg.content)
                                    man_seg_content_list[defined_segment_content[2]:defined_segment_content[3]] = defined_segment_content[0]
                                    man_seg.content = "".join(man_seg_content_list) 
                                elif any(man_seg.start == cond_seg_start for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist = []
                                    man_seg_sublist.append(man_seg.index())
                                elif any((man_seg.start > cond_seg_start) & (man_seg.end < cond_seg_end) for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist.append(man_seg.index())
                                elif any(man_seg.end == cond_seg_end for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg_sublist.append(man_seg.index())
                                    for man_seg_index in man_seg_sublist[defined_segment_content[2]:defined_segment_content[3]]:
                                        manipulated_tier.elem[man_seg_index].content = defined_segment_content[0]
                                    man_seg_sublist = []

                elif isinstance(defined_segment_content,list):

                    for man_seg in manipulated_tier:
                        man_seg_sublist_times = []
                        man_seg_sublist = []
                        for seg in manipulated_tier.elem[man_seg.index():man_seg.index()+len(defined_segment_content)]:
                            man_seg_sublist_times.append((seg.start,seg.end))
                            man_seg_sublist.append(seg.index())
                        if any((man_seg_sublist_times[0][0] == cond_seg_start) & (man_seg_sublist_times[-1][-1] == cond_seg_end) for cond_seg_start,cond_seg_end in final_met_conditions_times):
                               for def_seg_index,man_seg_index in enumerate(man_seg_sublist):
                                   manipulated_tier.elem[man_seg_index].content = defined_segment_content[def_seg_index]

            elif (len(met_conditions_times) <= 0) & (len(met_conditions_times_lists) > 0):
                #ONLY LISTS

                if isinstance(defined_segment_content,str):

                    for man_seg in manipulated_tier:
                        man_seg_sublist_times = []
                        man_seg_sublist = []
                        for seg in manipulated_tier.elem[man_seg.index():man_seg.index()+final_met_conditions_times_lists_length]:
                            man_seg_sublist_times.append((seg.start,seg.end))
                            man_seg_sublist.append(seg.index())
                        if man_seg_sublist_times in final_met_conditions_times_lists:
                            for man_seg_index in man_seg_sublist:
                                manipulated_tier.elem[man_seg_index].content = defined_segment_content
                        elif any((man_seg.start == cond_list[0][0]) & (man_seg.end == cond_list[-1][-1]) for cond_list in final_met_conditions_times_lists):
                            man_seg.content = defined_segment_content

                elif isinstance(defined_segment_content,list):

                    for man_seg in manipulated_tier:
                        man_seg_sublist_times = []
                        man_seg_sublist = []
                        for seg in manipulated_tier.elem[man_seg.index():man_seg.index()+len(defined_segment_content)]:
                            man_seg_sublist_times.append((seg.start,seg.end))
                            man_seg_sublist.append(seg.index())
                        if man_seg_sublist_times in final_met_conditions_times_lists:
                            for def_seg_index,man_seg_index in enumerate(man_seg_sublist):
                                if defined_segment_content[def_seg_index] != ">.<":
                                    manipulated_tier.elem[man_seg_index].content = defined_segment_content[def_seg_index]
                        #elif any((man_seg.start == cond_list[0][0]) & (man_seg.end == cond_list[-1][-1]) for cond_list in final_met_conditions_times_lists):
                            #man_seg.content = defined_segment_content[0]

                elif isinstance(defined_segment_content,tuple):

                    if len(defined_segment_content) == 3:

                        if defined_segment_content[1] == "REPLACE_BY_INDEX":
                            for man_seg in manipulated_tier:
                                man_seg_sublist_times = []
                                man_seg_sublist = []
                                for seg in manipulated_tier.elem[man_seg.index():man_seg.index()+final_met_conditions_times_lists_length]:
                                    man_seg_sublist_times.append((seg.start,seg.end))
                                    man_seg_sublist.append(seg.index())
                                if man_seg_sublist_times in final_met_conditions_times_lists:
                                    for man_seg_index in man_seg_sublist:
                                        if man_seg_index == man_seg_sublist[defined_segment_content[2]]:
                                            manipulated_tier.elem[man_seg_index].content = defined_segment_content[0]

            elif (len(met_conditions_times) > 0) & (len(met_conditions_times_lists) > 0):
                #STRINGS AND LISTS

                if isinstance(defined_segment_content,str):
                    
                    for man_seg in manipulated_tier:
                        if (man_seg.start,man_seg.end) in final_met_conditions_times:
                            if any((man_seg.start == cond_list[0][0]) & (man_seg.end == cond_list[-1][-1]) for cond_list in final_met_conditions_times_lists):
                                man_seg.content = defined_segment_content
                        else:
                            man_seg_sublist_times = []
                            man_seg_sublist = []
                            for seg in manipulated_tier.elem[man_seg.index():man_seg.index()+final_met_conditions_times_lists_length]:
                                man_seg_sublist_times.append((seg.start,seg.end))
                                man_seg_sublist.append(seg.index())
                            if man_seg_sublist_times in final_met_conditions_times_lists:
                                if any((man_seg_sublist_times[0][0] == cond_seg_start) & (man_seg_sublist_times[-1][-1] == cond_seg_end) for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                    man_seg.content = defined_segment_content

                elif isinstance(defined_segment_content,list):

                    for man_seg in manipulated_tier:
                        man_seg_sublist_times = []
                        man_seg_sublist = []
                        for seg in manipulated_tier.elem[man_seg.index():man_seg.index()+len(defined_segment_content)]:
                            man_seg_sublist_times.append((seg.start,seg.end))
                            man_seg_sublist.append(seg.index())
                        if man_seg_sublist_times in final_met_conditions_times_lists:
                            if any((man_seg_sublist_times[0][0] == cond_seg_start) & (man_seg_sublist_times[-1][-1] == cond_seg_end) for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                for def_seg_index,man_seg_index in enumerate(man_seg_sublist):
                                    if defined_segment_content[def_seg_index] != ">.<":
                                        manipulated_tier.elem[man_seg_index].content = defined_segment_content[def_seg_index]

                elif isinstance(defined_segment_content,tuple):

                    if len(defined_segment_content) == 3:

                        if defined_segment_content[1] == "REPLACE_BY_INDEX":

                            for man_seg in manipulated_tier:
                                if (man_seg.start,man_seg.end) in final_met_conditions_times:
                                    if any((man_seg.start == cond_list[0][0]) & (man_seg.end == cond_list[-1][-1]) for cond_list in final_met_conditions_times_lists):
                                        man_seg_content_list = list(man_seg.content)
                                        man_seg_content_list[defined_segment_content[2]] = defined_segment_content[0]
                                        man_seg.content = "".join(man_seg_content_list)
                                else:
                                    man_seg_sublist_times = []
                                    man_seg_sublist = []
                                    for seg in manipulated_tier.elem[man_seg.index():man_seg.index()+final_met_conditions_times_lists_length]:
                                        man_seg_sublist_times.append((seg.start,seg.end))
                                        man_seg_sublist.append(seg.index())
                                    if man_seg_sublist_times in final_met_conditions_times_lists:
                                        if any((man_seg_sublist_times[0][0] == cond_seg_start) & (man_seg_sublist_times[-1][-1] == cond_seg_end) for cond_seg_start,cond_seg_end in final_met_conditions_times):
                                            for man_seg_index in man_seg_sublist:
                                                if man_seg_index == man_seg_sublist[defined_segment_content[2]]:
                                                    manipulated_tier.elem[man_seg_index].content = defined_segment_content[0]

            manipulated_tier_exists = False
            found_tiers = []

def find_tiers(transcription,string):
    '''Returns a list with all tiers in the *transcription* whose names match the given regex *string*.'''
    found_tiers = []
    for tier in transcription:
        if re.search(string,tier.name):
            found_tiers.append(tier)
    return found_tiers

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

def test():
    print("Could be imported.")

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

def get_duplicated_segments_old_version(transcription):
    '''Returns for a given *transcription* a dictionary with tiers as keys and lists as values. Those lists contain tuples of segments of the same tier, which either share their start and/or end time, or fall in between each others times.'''
    duplicated_segments = {}
    for tier in transcription:
        duplicated_segments[tier] = []
        duplicated_segments[tier].append(set())
        for seg1 in tier:
            seg_set = set()
            for seg2 in tier:
                if (seg1.start == seg2.start) | (seg1.end == seg2.end) | ((seg1.start > seg2.start) & (seg1.end < seg2.end)):
                    if seg1 != seg2:
                        seg_set.add(seg1)
                        seg_set.add(seg2)
            if not seg_set in duplicated_segments[tier]:
                duplicated_segments[tier].append(seg_set)
                #This more strict condition is for cases, where one segment overlaps with at least two other duplicated segments, which themselves do not overlap with each other.
                for ind,added_seg_set in enumerate(duplicated_segments[tier][:-1]):
                    if any(seg in added_seg_set for seg in seg_set):
                        if len(seg_set) > len(added_seg_set):
                            duplicated_segments[tier].pop(ind)
                        else:
                            duplicated_segments[tier].pop(-1)
                        break
        for index,segs in enumerate(duplicated_segments[tier]):
            indexed_segs = [(seg.index(),seg) for seg in segs]
            ordered_segs = sorted(indexed_segs)
            segs_l = [seg for index,seg in ordered_segs]
            duplicated_segments[tier][index] = tuple(segs_l)
    return duplicated_segments

def get_overlapping_segments(transcription):
    '''Returns for a given *transcription* a dictionary with tiers as keys and lists as values. Those lists contain pairs of segments of the same tier, where the first segments overlaps with the second segment (this means that a) the first segments end time is greater than the second segments start time AND b) that the first segments end time is smaller than the second segments end time. Duplicates are intentionally excluded). This function only works correctly, if the segments of a tier are ordered correctly based on their (start) times.'''
    overlapping_segments = {}
    for tier in transcription:
        overlapping_segments[tier] = []
        tier_segs = [seg for seg in tier]
        for ind,seg in enumerate(tier_segs[:-1]):
            overlap_segs_group = [seg]
            for next_seg in tier_segs[ind+1:]:
                if (seg.start == next_seg.start) | (seg.end == next_seg.end) | ((seg.start > next_seg.start) & (seg.end < next_seg.end)):
                    continue
                elif (seg.end > next_seg.start) & (seg.end < next_seg.end):
                    overlap_segs_group.append(next_seg)
            if len(overlap_segs_group) > 1:
                overlapping_segments[tier].append(tuple(overlap_segs_group))
    return overlapping_segments

def get_duplicated_segments(transcription):
    '''Returns for a given *transcription* a dictionary with tiers as keys and lists as values. Those lists contain tuples of segments of the same tier, which either share their start and/or end time, or fall in between each others times.'''
    duplicated_segments = {}
    for tier in transcription:
        duplicated_segments[tier] = []
        duplicated_segments[tier].append(set())
        for seg1 in tier:
            seg_set = set()
            for seg2 in tier:
                if (seg1.start == seg2.start) | (seg1.end == seg2.end) | ((seg1.start > seg2.start) & (seg1.end < seg2.end)):
                    if seg1 != seg2:
                        seg_set.add(seg1)
                        seg_set.add(seg2)
            similar_set_exists = False
            for added_seg_set in duplicated_segments[tier]:
                if any(seg in added_seg_set for seg in seg_set):
                    similar_set_exists = True
                    for seg in seg_set:
                        added_seg_set.add(seg)
            if not similar_set_exists:
                if not seg_set in duplicated_segments[tier]:
                    duplicated_segments[tier].append(seg_set)
        for index,segs in enumerate(duplicated_segments[tier]):
            indexed_segs = [(seg.index(),seg) for seg in segs]
            ordered_segs = sorted(indexed_segs)
            segs_l = [seg for index,seg in ordered_segs]
            duplicated_segments[tier][index] = tuple(segs_l)
    return duplicated_segments

'''
def merge_segments_inactive(segment,n:int=-1):
    #Merges a *segment*s content and structure (e.g. times) with a number of *n* segments on the same tier. If *n* is negative, the merged segments are to the left. If *n* is positive, the merged segments are to the right. All segments to be merged must be right next to each other. Returns additionally the changed segment object.
    if n < 0:
        seg_range = range(-1,n-1,-1)
        segment.start = segment.struct.elem[segment.index()+n].start
        for num in seg_range:
            current_seg = segment.struct.elem[segment.index()+num+1]
            next_seg = next_seg = segment.struct.elem[segment.index()+num]
            if current_seg.start == next_seg.end:
                segment.content = next_seg.content + segment.content
            if next_seg.children():
                for child_seg in next_seg.children():
                    child_seg.setParent(segment)
        for num in seg_range:
            next_seg = segment.struct.elem[segment.index()-1]
            segment.struct.remove(next_seg)

    elif n > 0:
        seg_range = range(1,n+1)
        segment.end = segment.struct.elem[segment.index()+n].end
        for num in seg_range:
            current_seg = segment.struct.elem[segment.index()+num-1]
            next_seg = next_seg = segment.struct.elem[segment.index()+num]
            if current_seg.end == next_seg.start:
                segment.content += next_seg.content
            if next_seg.children():
                for child_seg in next_seg.children():
                    child_seg.setParent(segment)
        for num in seg_range:
            next_seg = segment.struct.elem[segment.index()+1]
            segment.struct.remove(next_seg)

    return segment
'''

def copy_tier(transcription,tier,new_tier_name,parent_tier,char_num=1):
    '''Copies an existing *tier* and adds it to a *transcription* with its *new_tier_name* and newly assigned *parent_tier*. All segments of the newly added tier get renamed based on their first characters letter and the number *char_num* given. By default, this number euqals 1 meaning that if e.g. the first character in a segments name is 'a', it gets substituted by 'b'. If char_num equals 2 and the first character is again 'a', it gets substituted by the character 'c', and so on. Returns the newly added tier.'''
    transcription.add(-1,tier)
    new_tier = transcription.elem[-1]
    new_tier.name = new_tier_name
    for seg in new_tier:
        seg.name = chr(ord(seg.name[0])+char_num) + seg.name[1:]
    new_tier.setParent(parent_tier)
    for seg in new_tier:
        seg.setParent(parent_tier.getTime(seg.start))
    return new_tier