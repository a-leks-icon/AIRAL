# Import the ELAN corflow modules.
from corflow import fromElan,toElan
# Path to the .eaf file.
file = "doreco_teop1238_Gol_01.eaf"
# Import the .eaf file.
trans = fromElan.fromElan(file)
# Export the .eaf file.
toElan.toElan("new_file.eaf",trans)

'''
# Call the help function on a Corflow object to
# get information about its attributes, methods
# and its relation to other objects:
# Call the help function on a transcription.
help(trans)
# Import Corflow classes, if you have not created the
respective object yet.
from corflow.Transcription import Transcription, Tier, Segment
# Create objects from that classes:
trans2 = Transcription()
tier = Tier()
seg = Segment()
# Call the help function on an object:
help(trans2)
help(tier)
help(segment)
print("---\n")
'''

# Shows how to access objects using '.elem[]':
# Get the first tier, its second segment.
tier = trans.elem[0]
seg = tier.elem[1]
# Print # the name of the transcription, the tier
print(f"transcription: {trans.name}")
print(f"first tier: {tier.name}")
# and the content of the second segment.
print(f"second segment: {seg.content}")
print("---\n")

# Shows how to access objects using regular expressions
# matching their name attribute:
# Find the word tier using one regular expression.
wd_tier = trans.findName("wd@")
# Find the morph and gloss tier using another regular expression.
mb_gl_tiers = trans.findAllName("(mb|gl)@")
# Print the names of all three tiers.
print(f"word tier: {wd_tier.name}")
print(f"morph and gloss tier:\n{[tier.name for tier in mb_gl_tiers]}")
print("---\n")

# Shows how to access the name attribute of transcriptions
# and tiers, and the content attribute of segments:
# Get the first tier and its second segment.
tier = trans.elem[0]
seg = tier.elem[1]
# Print the name of the transcription, tier and segment.
print(f"transcription: {trans.name}")
print(f"tier: {tier.name}")
print(f"segment name: {seg.name}")
# Print the content of the segment.
print(f"segment content: {seg.content}")
print("---\n")

# Access the start and end attributes of an object
# to get time information:
# Get the first tier, and its first and second segment.
tier = trans.elem[0]
seg1 = tier.elem[0]
seg2 = tier.elem[1]
# Print the start and end times of the transcription,
# the tier and its first two segments.
print(f"transcription: {trans.start} -- {trans.end}")
print(f"tier: {tier.start} -- {tier.end}")
print(f"first segment: {seg1.start} -- {seg1.end}")
print(f"second segment: {seg2.start} -- {seg2.end}")
print("---\n")

# Get the container (structure) of an object:
# Get the first tier and its first segment.
tier = trans.elem[0]
seg = tier.elem[0]
# Print the name of the transcription and first tier.
print(f"transcription: {trans.name}")
print(f"tier: {tier.name}")
# Print the name of the structure of the first tier
# and the name of structure of the first tier's first segment.
print(f"structure of the tier /{tier.name}/ is the transcription: {tier.struct.name}")
print(f"structure of the segment /{seg.content}/ is the tier: {seg.struct.name}")
print("---\n")

# The struct attribute can be used to check e.g. whether
# a segment belongs to a specific tier:
# Get the morph tier and its second segment.
mb_tier = trans.findName("mb@")
mb_seg = mb_tier.elem[1]
# Iterate through all child segments of the morph segment.
for child_seg in mb_seg.children():
    # Get the structure of the child segment.
    tier = child_seg.struct
    # Check, whether that child segment is a gloss (on the gloss tier).
    if tier.name.startswith("gl@"):
        # If so, print its content.
        print(f"gloss segment of /{mb_seg.content}/: {child_seg.content}")
print("---\n")

# Get the index of an object (its position inside
# the list of elements it belongs to):
# Get the phone tier.
ph_tier = trans.findName("ph@")
# Get the index of the phone tier.
ind = ph_tier.index()
# Print the index of the phone tier.
print(f"Index of tier /{ph_tier.name}/: {ind}")
# Check, whether the index of the phone tier is correct
# by accessing the respective tier based on that index.
print(f"Name of the tier with index {ind}: {trans.elem[ind].name}")
print("---\n")

# Remove and object (here: a segment) from its
# structure (here: a tier) by either using (1)
# the object itself or (2) the object's index:
# Get the word tier.
wd_tier = trans.findName("wd@")
# Print the first four words.
print(f"First four words: {[seg.content for seg in wd_tier.elem[:4]]}")
# Iterate through the first four words.
for wd in wd_tier:
    # Check, whether the content of a segment
    # matches the given string.
    if wd.content == "peho":
        # If so, remove that segment from its tier.
        wd_tier.remove(wd)
# Print the remaning three words after having removed
# a segment.
print(f"After removing the respective word: {[seg.content for seg in wd_tier.elem[:3]]}")
# Removes the first segment from the word tier
# using its index.
wd_tier.pop(0)
# Print the remaning two words after having removed
# a segment.
print(f"After removing the next word: {[seg.content for seg in wd_tier.elem[:2]]}")
print("---\n")

# Get an object's parent (here: a tier)
# and grandparent (the parent's parent) as well
# as all (direct and indirect) parents of an object:
# Get the phone tier.
ph_tier = trans.findName("ph@")
# Get the parent tier of the phone tier.
parent_tier = ph_tier.parent()
# Get the grandparent (parent of the parent) tier
# of the phone tier.
grandparent_tier = parent_tier.parent()
# Print the name of the phone tiers
# parent and grandparent tier.
print(f"direct parent tier of /phone tier/: {parent_tier.name}")
print(f"grandparent tier of /phone tier/: {grandparent_tier.name}")
# Get all parent tiers of the phone tier.
parent_tiers = ph_tier.parents()
# Print their names.
print(f"all parent tiers of /phone tier/: {[par.name for par in parent_tiers]}")
print("---\n")

# Check, whether an object has a direct parent,
# before accessing its attributes or methods
# to avoid an error:
# Get the first (root) tier and the second
# (non-root) tier.
root = trans.elem[0]
non_root = trans.elem[1]
for tier in [root,non_root]:
    #Print the name of the parent tier, if it exists.
    if tier.parent():
        print(f"The tier /{tier.name}/ has a parent, which is /{tier.parent().name}/.")
    #If the tier has no parent, print None.
    else:
        print(f"The tier /{tier.name}/ has no parent: {tier.parent()}.")
print("---\n")

# Check, whether an object has any parent,
# before accessing them and their attributes or methods
# to avoid an error:
# Get the root and gloss tier.
root = trans.elem[0]
gloss = trans.findName("gl@")
for tier in [root,gloss]:
    # Print the names of all parents of a tier,
    # if it has at least one parent.
    if tier.parents():
        print(f"The tier /{tier.name}/ has the following parents: {[par.name for par in tier.parents()]}.")
    # Print the empty list of parents, if a tier has no parents.
    else:
        print(f"The tier /{tier.name}/ has no parents: {tier.parents()}.")
print("---\n")

# Get an object's direct children or all
# its children and print their names.
# Get the reference tier.
ref_tier = trans.findName("ref@")
# Get only the direct child tiers of the ref tier.
direct_child_tiers = ref_tier.children()
# Print the names of the child tiers of the ref tier.
print(f"direct child tiers of /{ref_tier.name}/:")
print([tier.name for tier in direct_child_tiers])
# Get all child tiers of the ref tier.
all_child_tiers = ref_tier.allChildren()
# Print the names of all child tiers of the ref tier.
print(f"all child tiers of /{ref_tier.name}/")
print([tier.name for tier in all_child_tiers])
print("---\n")

# Get all child segments of the morph segment
# `peho' regardless to which tiers they belong
# and print their contents:
# Get the morph tier.
mb_tier = trans.findName("mb@")
# Get the morph `peho'.
mb_seg = mb_tier.elem[3]
# Get its direct child segments
children = mb_seg.children()
# and print their contents.
print(f"child segments of /{mb_seg.content}/")
print([seg.content for seg in children])
print("---\n")

# Get all direct child objects of an object
# as a list in a dictionary as a dictionary value
# using the structure they belong to as a dictionary key:
# Get the morph tier.
mb_tier = trans.findName("mb@")
# Get the morph `peho'.
mb_seg = mb_tier.elem[3]
# Get its direct child segments sorted in a dictionary.
children = mb_seg.childDict()
# Iterate through tiers (key) and lists of
# child segments (value) from that dictionary.
for tier,segs in children.items():
    # Print the name of the tier
    print(f"child segments belonging to child tier: {tier.name}")
    # and the content of each child segment belonging to that tier.
    print([seg.content for seg in segs])
print("---\n")

# Check, whether an object has children
# before trying to access them and their
# attributes and methods. Print their contents,
# if they exist.
# Get the morph tier.
mb_tier = trans.findName("mb@")
# Get the morph `peho'.
mb_seg = mb_tier.elem[3]
# Get the gloss tier.
gl_tier = trans.findName("gl@")
# Get its gloss (child segment) `INDEF3.SG'
# by using the gloss tier as a key in the
# dictionary containing all its direct child segments.
gl_seg = mb_seg.childDict()[gl_tier][0]
for seg in [mb_seg,gl_seg]:
    # Print the content of all direct child segments,
    # if a segment has child segments.
    if seg.children():
        print(f"The segment /{seg.content}/ has child segments: {[seg.content for seg in seg.children()]}")
    # Otherwise, print the empty list of child segments.
    else:
        print(f"The segment /{seg.content}/ has no child segments: {seg.children()}")
print("---\n")