# Corflow Scripts

Python functions build on top of the **[Corflow](https://github.com/DoReCo/corflow)** tool complementing it when working with .eaf (ELAN) files.

All functions specifically build for the scripts in this directory are located in `general_functions.py`.

## Getting Started

To use the scripts and functions in this repository, install Corflow: Open your terminal, navigate to your virtual environment and activate it, and enter the following command:

```shell
pip install corflow
```

To learn **how to use** Corflow and the additional scripts and functions, take a look at the [tutorials](./tutorials/).

## Useful scripts 

Here are short scripts that illustrate some base functionalities of Corflow, and provide minimal working examples for common tasks related to processing and manipulating ELAN .eaf files. These scripts are fully commented and guide the user through each processing step.

1. Load and save files: How to open and save 
2. Copy tiers: How to create copies of tiers as either stand-alone tiers or as daughter tiers
3. Substitute content: How to search and replace (sub)strings on designated tiers based on regular expressions
4. Delete and create segments: How to delete and create annotation units based on a set of conditions
5. ...

## Sanity checks

With the function XXX provided by YYY.py, you can easily check one or multiple .eaf files for common issues that may 
The script checks for 

1. adherence to the EAFv3.0 XML schema ("validation")
2. inconsistent time codes (e.g. negative time codes or units with negative durations) 
4. overlaps between annotation units
5. duplicate tiers or annoation units
6. ...

We recommend integrating this function into your workflow and calling it as often as possible, ideally before and after each processing step.
