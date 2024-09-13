# AIRAL

**[AIRAL](https://www.leibniz-zas.de/en/research/research-areas/laboratory-phonology/airal)** "***A****coustic* ***I****nsights into the* ***R****oot-****A****ffix asymmetry across****L****anguages*" is an ongoing **research project** by [Ludger Paschen](http://www.ludgerpaschen.de/) at [ZAS](https://www.leibniz-zas.de/en/) Berlin (*Leibniz-Zentrum Allgemeine Sprachwissenschaft*) funded by the German Research Foundation [DFG](https://www.dfg.de/en) (*Deutsche Forschungsgemeinschaft*). AIRAL investigates the acoustic properties of complex words in a diverse sample of the world's mostly **small and endangered** languages. AIRAL analyzes annotated datasets from the [DoReCo](https://doreco.info/) corpus created at ZAS between 2019 and 2022.

## Aim of this Repository

This **repository** contains the python scripts written for and used in the research project **AIRAL**. The aim of this repository is to collect, document and maintain the scripts written for the project and for the various datasets of the DoReCo corpus. Another aim is to provide users (researchers) with useful scripts, which they can either apply directly to their datasets or use them as templates for writing their own scripts.

While most scripts are well documented in the project's internal documentation, they are currently not well documented in the files themselves. A first objective is to provide the scripts and functions with sufficient information and comments.

Please note that the quality and readability of the scripts vary significantly. This is because I (Aleks) developed and improved my programming skills during the time I was writing the scripts. Because I want to preserve their functionality, it is very likely that it will stay this way.

## Scripts

The scripts are divided into **four** different subdirectories. Most of them manipulate language datasets from the DoReCo corpus published in the [DoReCo database](https://doreco.huma-num.fr/). The manipulated data consists of **.eaf**-files used in [ELAN](https://archive.mpi.nl/tla/elan). The scripts utilize the **[Corflow](https://github.com/DoReCo/corflow)** tool/python library (more information on that down below). The four subdirectories are:

1. **doreco_lang_scripts**: Scripts written to manipulate and clean the data of *specific* languages from the DoReCo corpus. Some examples:
    - collect and resolve **misalignments** between segments (units) from multiple, different tiers
    - manipulate segments (**merge, split, move** them, **define** their content) depending on their **content, time, relation** and/or **position**
2. **general_scripts**: Scripts written to manipulate the data of *multiple, different* languages or to extract information from the data. Some examples:
    - **import** translations as tiers with time-aligned segments
    - collect **duplicated, overlapping** or **misaligned** segments
3. **debug_scripts**: Script mainly written to review datasets and files before finalizing and publishing them. Some examples:
    - check, whether the structure of an .eaf (.xml)-file is **well-formed**
    - check, whether (hierarchical) **relations** between objects (segments, tiers, etc.) specific to .eaf-files **hold**
4. **airal_scripts**: A few scripts written for tasks within the AIRAL project other than manipulating datasets from to DoReCo corpus intended to be published later on. Some examples:
    - import a .csv-file containing language data and **create** a .txt-file with **useful statistical data**, e.g. token frequencies of individual glosses, morphs and pos tags, or tuples of them.

## Corflow

Most scripts (those in the subdirectories 1.-3.) utilize the **[Corflow](https://github.com/DoReCo/corflow)** python library. Corflow is a tool to *manipulate* files and/or *change* a file's format, mainly applying to files used in the context of corpus linguistics. The tool was created by François Delafontaine as part of the [DoReCo](https://doreco.info/) project. Currently, the following file formats are supported:

* ELAN: .eaf
* Praat: .textgrid
* Pangloss: .xml

 Corflow is still in development. While there are currently no UI nor any detailed error messages available, the tool already enables users to manipulate corpus data in an easy, customizable and reliable way. Future releases will (hopefully) for example enable the user to work with data created within [ANNIS](https://corpus-tools.org/annis/).

## DoReCo Languages

The language specific scripts were written to manipulate data from the DoReCo corpus for the following languages:

* Arapaho
* Bora
* Daakie
* English (Southern England)
* Gubeeher
* Komnzo
* Nafsan
* Texistepec Popoluca
* Savosavo
* Sümi
* Teop
* Urum
* Yongningna

## Contact

If you have questions, want to make comments, note issues or if you need help with scripts or functions, feel free to contact [Aleksandr Schamberger](mailto:mail@aleksandrschamberger.de).

## Maintainer and Authors

This repository is created and maintained by [Aleksandr Schamberger](https://github.com/a-leks-icon/).

Scripts were written by Michelle Elizabeth Throssell Balagué and Aleksandr Schamberger.