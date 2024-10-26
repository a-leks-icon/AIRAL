
# Basics of Corflow

This tutorial introduces the main concepts of Corflow and how to use it.

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
#Import the ELAN corflow modules.
from corflow import fromElan,toElan
#Path to the .eaf file.
file = "UUM-TXT-AN-00000-A01.eaf"
#Importing the .eaf file.
trans = fromElan.fromElan(file)
#Exporting the .eaf file.
toElan.toElan("new_file.eaf",trans)
```

By importing `toPraat` and using `toPraat.toPraat` instead of `toElan.toElan`, Corflow makes it possible to convert a file's format.

## Classes and Objects

Importing a file using Corflow creates a `Transcription` object. The following edited screenshot taken of the file `UUM-TXT-AN-00000-A01.eaf` in ELAN illustrates Corflow's model:

![Screenshot of the file 'UUM-TXT-AN-00000-A01.eaf' with added rectangles displaying Corflow classes and objects 'Transcription', 'Tier' and 'Segment'.](corflow_classes_elan_example.png)