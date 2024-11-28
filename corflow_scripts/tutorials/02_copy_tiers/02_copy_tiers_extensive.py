# Importing the ELAN corflow modules.
from corflow import fromElan,toElan
# Path to .eaf file.
eaf = "doreco_teop1238_Gol_01.eaf"
# Creating a transcription object (importing the .eaf file).
trans = fromElan.fromElan(eaf,encoding="utf-8")
# Get the morph tier.
mb_tier = trans.findName("mb@")
# Get the gloss tier.
gl_tier = trans.findName("gl@")
# Print the names of the morph and gloss tier.
print(f"mb tier: {mb_tier.name}")
print(f"gl tier: {gl_tier.name}")
#Copy and add the morph tier.
new_mb_tier = trans.add(-1,mb_tier)
# Split the name of the morph tier into three parts:
# (1) "mb", (2) "@" and (2) the speaker "Gol".
mb_tier_name_split = mb_tier.name.partition("@")
# Add the suffix "_tok" to "mb".
new_name = mb_tier_name_split[0] + "_tok"
# Add the remaining parts of the original name
# and change the name of the new morph tier.
new_mb_tier.name = new_name + mb_tier_name_split[1] + mb_tier_name_split[2]
# Copy and add the gloss tier.
new_gl_tier = trans.add(-1,gl_tier,new_mb_tier)
# Split the name of the gloss tier into three parts:
# (1) "gl", (2) "@" and (2) the speaker "Gol".
gl_tier_name_split = gl_tier.name.partition("@")
# Add the suffix "_tok" to "gl".
new_name = gl_tier_name_split[0] + "_tok"
# Add the remaining parts of the original name
# and change the name of the new gloss tier.
new_gl_tier.name = new_name + gl_tier_name_split[1] + gl_tier_name_split[2]
# Renaming the annotation ID of all segments
# to make sure, that every segment has a
# unique annotation ID.
incr = 0
for tier in trans:
    incr = tier.renameSegs("a",incr)
# Exporting the transcription as a new .eaf file.
toElan.toElan(trans.name + "_tok" + ".eaf",trans)