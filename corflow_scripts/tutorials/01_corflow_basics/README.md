
# Basics of Corflow

This tutorial introduces the main concepts and classes of Corflow. Each code snipped can be used in its own .py file. All code snippets are included in [`01_corflow_basics.py`](01_corflow_basics.py) as one script.

## Importing and Exporting Files

Corflow is both a tool to (1) manipulate a file and (2) to change a file's format. Corflow currently supports the linguistic formats of the following linguistic tools:

|Tool|Format|
|---|---|
|ELAN|.eaf|
|Praat|.TextGrid|
|EXMARaLDA|.xml|
|Pangloss|.xml|
|Transcriber|.trs|

To either import or export a file containing linguistic data, import the module, whose name is made up of (1) the name of the tool (2) prefixed with either _from_ or _to_, and use the module's function with the same name. E.g. to import and export an .eaf file, create a Python script with the following code:

```python
# Import the ELAN corflow modules.
from corflow import fromElan,toElan
# Path to the .eaf file.
file = "doreco_teop1238_Gol_01.eaf"
# Importing the .eaf file.
trans = fromElan.fromElan(file)
# Exporting the .eaf file.
toElan.toElan("new_file.eaf",trans)
```

Importing e.g. the module `toPraat` and using `toPraat.toPraat` instead of `toElan.toElan` when importing an .eaf file with `fromElan.fromElan`, Corflow makes it possible to convert a file's format.

**Note**: Importing and exporting an .eaf file will change the .xml structure and/or the number of .xml elements of the imported file. This mainly results in the size of the file being reduced. The overall structure of the file as well as its content are still intact. However, it might be the case that certain programs return an error, when importing the new .eaf file. To avoid such errors, the file has to be (1) opened in ELAN, (2) changed in some way (e.g. changing a segment's content/string) and (3) saved. As a result, the size of the file is restored and no error should occur anymore. This issue will hopefully be completely gone in future releases of Corflow.

## Classes and Objects

The following edited screenshot taken of the file `doreco_teop1238_Gol_01.eaf` in ELAN illustrates Corflow's model:

![Screenshot of the file 'doreco_teop1238_Gol_01.eaf' with added rectangles displaying Corflow classes and objects 'Transcription', 'Tier' and 'Segment'.](corflow_classes_elan_example_03.png)

Importing a file using Corflow creates a `Transcription` object. A `Transcription` object contains (multiple) `Tier` objects and a `Tier` object contains (multiple) `Segment` objects. `Transcriptions`, `Tiers` and `Segments` relate (1) linearly and (2) hierarchically to each other as well as share a number of attributes and methods (as they all belong to the root class `Conteneur`. In what follows, I illustrate common attributes and methods used in Corflow.

## Help

To get information about an object's attributes and methods call the `help` function with the respective object as an argument or read the [Corflow GitHub Wiki](https://github.com/DoReCo/corflow/wiki).

```python
# Import the respective class.
from corflow.Transcription import Transcription, Tier, Segment
# Create an object from that class.
trans = Transcription()
tier = Tier()
seg = Segment()
# Call the help function.
help(trans)
help(tier)
help(seg)
```

## Common Attributes and Methods

The following table shows which common attributes and methods to use on which objects to obtain meaningful information:

|Attribute/Method|Transcription|Tier|Segment|
|---|---|---|---|
|elem|x|x||
|name|x|x|x|
|content|||x|
|start|x|x|x|
|end|x|x|x|
|struct||x|x|
|metadata|x|x|x|
|index()||x|x|
|parent()||x|x|
|children()|x|x|x|
|findName()|x|x|x|
|getIndex()|x|x||
|getTime()|x|x||
|remove()|x|x||
|setParent()||x|x|

### Accessing Objects by their Index

The `.elem` attribute is a list containing all objects belonging to an object. The following example accesses the first tier and its second segment of the transcription `trans`:

```python
from corflow import fromElan
file = "doreco_teop1238_Gol_01.eaf"
trans = fromElan.fromElan(file)
# Get the first tier.
tier = trans.elem[0]
# Get the second segment of the first tier.
seg = tier.elem[1]
print(f"transcription: {trans.name}")
print(f"first tier: {tier.name}")
print(f"second segment: {seg.content}")
```

Output:

```console
transcription: doreco_teop1238_Gol_01
first tier: ref@Gol
second segment: 0001_DoReCo_doreco_teop1238_Gol_01
```

### Accessing Objects by their Name (regular expression)

The methods `.findName` and `.findAllName` return one or all objects, whose `.name` attribute match a given regular expression. The following example accesses (1) the word tier only and (2) the morph and gloss tier:

```python
from corflow import fromElan
file = "doreco_teop1238_Gol_01.eaf"
trans = fromElan.fromElan(file)
# Get the word tier.
wd_tier = trans.findName("wd@")
# Get the morph and the gloss tier.
mb_gl_tiers = trans.findAllName("(mb|gl)@")
print(f"word tier: {wd_tier.name}")
print(f"morph and gloss tier:\n{[tier.name for tier in mb_gl_tiers]}")
```

Output:

```console
word tier: wd@Gol
morph and gloss tier:
['mb@Gol', 'gl@Gol']
```

To access a `Segment` object based on their `.content` attribute, you can use the `get_segs` function from the [general_functions](../../general_functions.py) script (more on that in the [third tutorial]()).

### Name and Content

`.name` contains an object's name. If it's a `Transcription`, `.name` contains the file's name without the file extension. If it's a `Segment`, `.name` contains the unique ID of that segment. To access a segment's string, use `.content` instead:

```python
from corflow import fromElan
file = "doreco_teop1238_Gol_01.eaf"
trans = fromElan.fromElan(file)
tier = trans.elem[0]
seg = tier.elem[1]
print(f"transcription: {trans.name}")
print(f"tier: {tier.name}")
print(f"segment name: {seg.name}")
print(f"segment content: {seg.content}")
```

Output:

```console
transcription: doreco_teop1238_Gol_01
tier: ref@Gol
segment name: a1
segment content: 0001_DoReCo_doreco_teop1238_Gol_01
```

### Time

`.start` and `.end` contain an object's start and end time respectively (in seconds):

```python
from corflow import fromElan
file = "doreco_teop1238_Gol_01.eaf"
trans = fromElan.fromElan(file)
tier = trans.elem[0]
seg1 = tier.elem[0]
seg2 = tier.elem[1]
print(f"transcription: {trans.start} -- {trans.end}")
print(f"tier: {tier.start} -- {tier.end}")
print(f"first segment: {seg1.start} -- {seg1.end}")
print(f"second segment: {seg2.start} -- {seg2.end}")
```

Output:

```console
transcription: 0.0 -- 116.0
tier: 0.0 -- 116.0
first segment: 0.0 -- 0.06
second segment: 0.06 -- 2.84
```

### Structure

`.struct` refers to the container of an object (the object of which an object is an element of). The structure of a `Segment` object is the `Tier` object it is an element of. The structure of a `Tier` object is the `Transcription` object it is an element of:

```python
from corflow import fromElan
file = "doreco_teop1238_Gol_01.eaf"
trans = fromElan.fromElan(file)
tier = trans.elem[0]
seg = tier.elem[0]
print(f"transcription: {trans.name}")
print(f"tier: {tier.name}")
print(f"structure of the tier /{tier.name}/ is the transcription: {tier.struct.name}")
print(f"structure of the segment /{seg.content}/ is the tier: {seg.struct.name}")
```

Output:

```console
transcription: doreco_teop1238_Gol_01
tier: ref@Gol
structure of the tier /ref@Gol/ is the transcription: doreco_teop1238_Gol_01
structure of the segment /<p:>/ is the tier: ref@Gol
```

`.struct` is useful e.g. when checking whether a child segment belongs to a specific tier (more on child and parent objects later):

```python
from corflow import fromElan
file = "doreco_teop1238_Gol_01.eaf"
trans = fromElan.fromElan(file)
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
```

Output:

```console
gloss segment of /Te=/: PREP=
```

### Index

`.index()` returns the index an object has in the list of elements of the object it belongs to:

```python
from corflow import fromElan
file = "doreco_teop1238_Gol_01.eaf"
trans = fromElan.fromElan(file)
ph_tier = trans.findName("ph@")
# Get the object's index.
ind = ph_tier.index()
print(f"Index of tier /{ph_tier.name}/: {ind}")
print(f"Name of the tier with index {ind}: {trans.elem[ind].name}")
```

Output:

```console
Index of tier /ph@Gol/: 6
Name of the tier with index 6: ph@Gol
```

### Remove an Object

`.remove()` removes an object from its structure. `.pop()` does the same, but uses the index of the object instead of the object itself:

```python
from corflow import fromElan
file = "doreco_teop1238_Gol_01.eaf"
trans = fromElan.fromElan(file)
wd_tier = trans.findName("wd@")
print(f"First four words: {[seg.content for seg in wd_tier.elem[:4]]}")
# Iterate through the first four words.
for wd in wd_tier:
    # Remove the segment, whose content matches a given string.
    if wd.content == "peho":
        wd_tier.remove(wd)
print(f"After removing the respective word: {[seg.content for seg in wd_tier.elem[:3]]}")
# Removes the first word segment from its
# (word) tier using its index.
wd_tier.pop(0)
print(f"After removing the next word: {[seg.content for seg in wd_tier.elem[:2]]}")
```

Output:

```console
First four words: ['<p:>', 'Teo', 'peho', 'vuri']
After removing the respective word: ['<p:>', 'Teo', 'vuri']
After removing the next word: ['Teo', 'vuri']
```

### Parents and Children

#### Parents

`.parent()` returns an object's direct parent object. It can be used recursively. `.parents()` returns a list containing all (direct and indirect) parents an object has:

```python
from corflow import fromElan
file = "doreco_teop1238_Gol_01.eaf"
trans = fromElan.fromElan(file)
ph_tier = trans.findName("ph@")
# Get the parent tier of the phone tier.
parent_tier = ph_tier.parent()
# Get the grandparent (parent of the parent) tier
# of the phone tier.
grandparent_tier = parent_tier.parent()
print(f"direct parent tier of /phone tier/: {parent_tier.name}")
print(f"grandparent tier of /phone tier/: {grandparent_tier.name}")
# Get all parent tiers of the phone tier.
parent_tiers = ph_tier.parents()
print(f"all parent tiers of /phone tier/: {[par.name for par in parent_tiers]}")
```

Output:

```console
direct parent tier of /phone tier/: mb@Gol
grandparent tier of /phone tier/: wd@Gol
all parent tiers of /phone tier/: ['ref@Gol', 'wd@Gol', 'mb@Gol']
```

If an object does not have a parent object (e.g. because it is the root tier), Python throws out an error, if the attribute of method of that non-existing object is accessed:

```python
from corflow import fromElan
file = "doreco_teop1238_Gol_01.eaf"
trans = fromElan.fromElan(file)
# Get the first (root) tier.
tier = trans.elem[0]
# Get its (none-existing) parent.
parent = tier.parent()
# Print the name of the parent tier.
print(parent.name)
```

Possible output:

```console
Traceback (most recent call last):
  File "/home/user/corflow_scripts/tutorials/01_corflow_basics/test.py", line 9, in <module>
    print(parent.name)
          ^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'name'
```

Avoid such errors by checking, whether (1) `.parent()` returns an object instead of None and whether (2) `.parents()` returns a non-empty list before trying to access objects of that list.

```python
from corflow import fromElan
file = "doreco_teop1238_Gol_01.eaf"
trans = fromElan.fromElan(file)
# Get the first (root) tier and the second
# (non-root) tier.
root = trans.elem[0]
non_root = trans.elem[1]
for tier in [root,non_root]:
    # Print the name of the tier's existing parent.
    if tier.parent():
        print(f"The tier /{tier.name}/ has a parent, which is /{tier.parent().name}/.")
    # Print the type of the non-existing parent.
    else:
        print(f"The tier /{tier.name}/ has no parent: {tier.parent()}.")
```

Output:

```console
The tier /ref@Gol/ has no parent: None.
The tier /tx@Gol/ has a parent, which is /ref@Gol/.
```

```python
from corflow import fromElan
file = "doreco_teop1238_Gol_01.eaf"
trans = fromElan.fromElan(file)
# Get the root and gloss tier.
root = trans.elem[0]
gloss = trans.findName("gl@")
for tier in [root,gloss]:
    #Print the names of all parents of a tier,
    # if it has at least one parent.
    if tier.parents():
        print(f"The tier /{tier.name}/ has the following parents: {[par.name for par in tier.parents()]}.")
    #Print the empty list of parents, if a tier has no parents.
    else:
        print(f"The tier /{tier.name}/ has no parents: {tier.parents()}.")
```

Output:

```console
The tier /ref@Gol/ has no parents: [].
The tier /gl@Gol/ has the following parents: ['ref@Gol', 'wd@Gol', 'mb@Gol'].
```

#### Children

`.children()` returns a list containing each direct child object of an object. `.allChildren()` returns a list containing all (direct and indirect) child objects:

```python
from corflow import fromElan
file = "doreco_teop1238_Gol_01.eaf"
trans = fromElan.fromElan(file)
ref_tier = trans.findName("ref@")
# Get only the direct child tiers of the ref tier.
direct_child_tiers = ref_tier.children()
print(f"direct child tiers of /{ref_tier.name}/:")
print([tier.name for tier in direct_child_tiers])
# Get all child tiers of the ref tier.
all_child_tiers = ref_tier.allChildren()
print(f"all child tiers of /{ref_tier.name}/")
print([tier.name for tier in all_child_tiers])
```

Output:

```console
direct child tiers of /ref@Gol/:
['tx@Gol', 'ft@Gol', 'wd@Gol']
all child tiers of /ref@Gol/
['tx@Gol', 'ft@Gol', 'wd@Gol', 'mb@Gol', 'gl@Gol', 'ph@Gol', 'doreco-mb-algn@Gol', 'gloss', 'mc-zero']
```

`.children()` and `.allChildren()` collect child objects regardless to which structures these belong to. The following code returns a list with all child segments of the morph segment `peho` regardless to which tiers (gloss, phone or align tier) these segments belong to:

```python
from corflow import fromElan
file = "doreco_teop1238_Gol_01.eaf"
trans = fromElan.fromElan(file)
mb_tier = trans.findName("mb@")
# Get the morph `peho'.
mb_seg = mb_tier.elem[3]
# Get its direct child segments and print their contents.
children = mb_seg.children()
print(f"child segments of /{mb_seg.content}/")
print([seg.content for seg in children])
```

Output:

```console
child segments of /peho/
['INDEF3.SG', 'p', 'e', 'h', 'o', '****']
```

`.childDict()` and `.allChildDict()` return a dictionary, where child objects are sorted: each child object belonging to the same structure is put into the same list as a _dictionary value_. This list of child objects can be accessed using the structure object they belong to as the _dictionary key_. The following code sorts all child segments of the morph `peho` by printing (1) the name of the tier and (2) the content of all child segments belonging to that tier.

```python
from corflow import fromElan
file = "doreco_teop1238_Gol_01.eaf"
trans = fromElan.fromElan(file)
mb_tier = trans.findName("mb@")
# Get the morph `peho'.
mb_seg = mb_tier.elem[3]
# Get its direct child segments sorted in a dictionary.
children = mb_seg.childDict()
for tier,segs in children.items():
    # Print the name of the tier
    print(f"child segments belonging to child tier: {tier.name}")
    # and the content of each child object belonging to that tier.
    print([seg.content for seg in segs])
```

Output:

```console
child segments belonging to child tier: gl@Gol
['INDEF3.SG']
child segments belonging to child tier: ph@Gol
['p', 'e', 'h', 'o']
child segments belonging to child tier: doreco-mb-algn@Gol
['****']
```

If an object has no child objects, `.children()` and `.allChildren()` will return empty lists and `.childDict()` and `.allChildDict()` empty dictionaries. Python throws out an IndexError when trying to access an object from an empty list:

```python
from corflow import fromElan
file = "doreco_teop1238_Gol_01.eaf"
trans = fromElan.fromElan(file)
gl_tier = trans.findName("gl@")
# Get the gloss `INDEF3.SG'.
gl_seg = gl_tier.elem[3]
# Get its first direct child segment.
seg = gl_seg.children()[0]
# Print the content of this child segment.
print(seg.content)
```

Possible Output:

```console
Traceback (most recent call last):
  File "/home/user/corflow_scripts/tutorials/01_corflow_basics/test.py", line 8, in <module>
    seg = gl_seg.children()[0]
          ~~~~~~~~~~~~~~~~~^^^
IndexError: list index out of range
```

Either iterate through lists or dictionaries, or check, whether a list or dictionary is non-empty before accessing objects:

```python
from corflow import fromElan
file = "doreco_teop1238_Gol_01.eaf"
trans = fromElan.fromElan(file)
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
```

Output:

```console
The segment /peho/ has child segments: ['INDEF3.SG', 'p', 'e', 'h', 'o', '****']
The segment /INDEF3.SG/ has no child segments: []
```

## References

The .eaf file used in this tutorial belongs to **Teop** from DoReCo:

* Mosel, Ulrike. 2022. Teop DoReCo dataset. In Seifart, Frank, Ludger Paschen and Matthew Stave (eds.). Language Documentation Reference Corpus (DoReCo) 1.2. Berlin & Lyon: Leibniz-Zentrum Allgemeine Sprachwissenschaft & laboratoire Dynamique Du Langage (UMR5596, CNRS & Université Lyon 2). https://doreco.huma-num.fr/languages/teop1238 (Accessed on 02/11/2024). DOI:10.34847/nkl.9322sdf2

DoReCo database:

* Seifart, Frank, Ludger Paschen & Matthew Stave (eds.). 2022. Language Documentation Reference Corpus (DoReCo) 1.2. Berlin & Lyon: Leibniz-Zentrum Allgemeine Sprachwissenschaft & laboratoire Dynamique Du Langage (UMR5596, CNRS & Université Lyon 2). DOI:10.34847/nkl.7cbfq779