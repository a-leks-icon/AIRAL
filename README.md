# AIRAL

**[AIRAL](https://www.leibniz-zas.de/en/research/research-areas/laboratory-phonology/airal)** "***A****coustic* ***I****nsights into the* ***R****oot-****A****ffix asymmetry across* ***L****anguages*" is an ongoing research project by [Ludger Paschen](http://www.ludgerpaschen.de/) at [ZAS](https://www.leibniz-zas.de/en/) Berlin (*Leibniz-Zentrum Allgemeine Sprachwissenschaft*) funded by the German Research Foundation [DFG](https://www.dfg.de/en) (*Deutsche Forschungsgemeinschaft*).

AIRAL investigates the acoustic properties of complex words in a diverse sample of the world's mostly **small and endangered** languages. AIRAL analyzes annotated datasets from the [DoReCo](https://doreco.huma-num.fr) corpus to test if and how the internal structure of words leaves acoustic traces, in particular with regard to the distinction between roots and affixes.

## Quick Info

- [Corflow Scripts](./corflow_scripts/): Scripts and functions written in Python augmenting the [Corflow](https://github.com/DoReCo/corflow) tool working with linguistic datasets e.g. .eaf ([ELAN](https://archive.mpi.nl/tla/elan)) files (located in the [corflow_scripts](./corflow_scripts/) subdirectory).
- [AIRAL Scripts](./airal_archive/): Scripts and functions written in Python for the AIRAL project manipulating datasets of the DoReCo corpus (located in the [airal_archive](./airal_archive/) subdirectory).

To **get started** with Corflow or AIRAL scripts, visit the [first tutorial](./corflow_scripts/tutorials/00_getting_started/).

## Aim and Structure of this Repository

### Corflow Scripts

The main aim of this repository is to provide users (researchers) with useful Python scripts and functions located in the **[corflow_scripts](./corflow_scripts/)** subdirectory extracted from those scripts written for the **ARIAL** project utilizing the [Corflow](https://github.com/DoReCo/corflow) tool. Users can use these scripts for their own projects applying them directly to their own datasets or use them as templates for writing their own scripts.

**Corflow** is a tool (Python library) to *manipulate* files or *change* a file's format, mainly applying to files used in the context of **corpus linguistics** and **multi-layered annotated corpora**. The tool was created by François Delafontaine as part of the [DoReCo](https://doreco.huma-num.fr) project. Currently, the following file formats are supported:

* [ELAN](https://archive.mpi.nl/tla/elan): .eaf
* [Praat](https://www.fon.hum.uva.nl/praat/): .textgrid
* [Pangloss](https://github.com/CNRS-LACITO/Pangloss_website): .xml

### AIRAL Scripts

A secondary aim of this repository is to document and maintain the Python scripts written for the **AIRAL** project manipulating and cleaning various datasets of the DoReCo corpus.

The archived scripts written for the **AIRAL** project located in the **[airal_archive](./airal_archive/)** subdirectory are divided into four subsubdirectories. Most of them manipulate language datasets from the DoReCo corpus published in the [DoReCo database](https://doreco.huma-num.fr/). The manipulated data consists of **.eaf**-files used in ELAN. The four subsubdirectories are:

1. **[doreco_lang_scripts](./airal_archive/doreco_lang_scripts/)**: Scripts written to manipulate and clean the data of *specific* languages from the DoReCo corpus. Some examples:
    - collect and resolve **misalignments** between segments (units) from multiple, different tiers
    - manipulate segments (**merge, split, move** them, **define** their content) depending on their **content, time, relation** and/or **position**
2. **[general_scripts](./airal_archive/general_scripts/)**: Scripts written to manipulate the data of *multiple, different* languages or to extract information from the data. Some examples:
    - **import** translations as tiers with time-aligned segments
    - collect **duplicated, overlapping** or **misaligned** segments
3. **[debug_scripts](./airal_archive/debug_scripts/)**: Scripts mainly written to review datasets and files before finalizing and publishing them. Some examples:
    - check, whether the structure of an .eaf (.xml)-file is **well-formed**
    - check, whether (hierarchical) **relations** between objects (segments, tiers, etc.) specific to .eaf-files **hold**
4. **[airal_scripts](./airal_archive/airal_scripts/)**: A few scripts written for tasks within the AIRAL project other than manipulating datasets from the DoReCo corpus. Some examples:
    - import a .csv-file containing linguistic information of a dataset and **create** a .txt-file with **useful statistical data**, e.g. token frequencies of glosses, morphs and part-of-speech tags

#### DoReCo Languages

Languages, for which specific AIRAL scripts were written, are the following:

* Arapaho
* Bora
* Daakie
* English (Southern England)
* Baïnounk Gubëeher
* Komnzo
* Nafsan (South Efate)
* Texistepec Popoluca
* Savosavo
* Sümi
* Teop
* Urum
* Yongning Na

## Contact

If you have questions, want to make comments, note issues or if you need help with scripts or functions, feel free to contact [Aleksandr Schamberger](mailto:mail@aleksandrschamberger.de).

## Maintainers and Authors

This repository was created and is maintained by [Aleksandr Schamberger](https://github.com/a-leks-icon/).

Scripts were written by [Michelle Elizabeth Throssell Balagué](https://github.com/michellethr), [Ludger Paschen](https://github.com/LuPaschen) and Aleksandr Schamberger.