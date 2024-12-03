# Importing the ELAN corflow modules.
from corflow import fromElan,toElan
# Path to .eaf file.
import os
eaf = "doreco_teop1238_Gol_01.eaf"
current_directory = os.path.dirname(os.path.abspath(__file__))
eaf_path = os.path.join(current_directory, eaf)
# Creating a transcription object (importing the .eaf file).
trans = fromElan.fromElan(eaf_path,encoding="utf-8")
# Get the morph tier.
mb_tier = trans.findName("mb@")
# Get the gloss tier.
gl_tier = trans.findName("gl@")
# Print the names of the morph and gloss tier.
print(f"mb tier: {mb_tier.name}")
print(f"gl tier: {gl_tier.name}")
# Copy and add the morph tier, and rename it.
new_mb_tier = trans.add(-1,mb_tier)
new_mb_tier.name = "mb_legacy@Gol"
# Copy and add the gloss tier, and rename it.
new_gl_tier = trans.add(-1,gl_tier,new_mb_tier)
new_gl_tier.name = "gl_legacy@Gol"
# Renaming the annotation ID of all segments
# to make sure, that every segment has a
# unique annotation ID.
incr = 0
for tier in trans:
    incr = tier.renameSegs("a",incr)
# Exporting the transcription as a new .eaf file.
toElan.toElan(trans.name + "_copied_legacy_tiers" + ".eaf",trans)
