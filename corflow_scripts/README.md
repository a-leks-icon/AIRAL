# Corflow Scripts

All functions specifically build for the scripts in this directory are in `corflow_functions.py`.

# Useful scripts 

Here are short scripts that illustrate some of the base functionalities of corflow, and provide minimal working examples for common tasks related to processing and manipulating ELAN .eaf files. These scripts are fullly commented and guide the user through each processing step.

1. Load and save files: How to open and save 
2. Copy tiers: How to create copies of tiers as either stand-alone tiers or as daughter tiers
3. Substitute content: How to search and replace (sub)strings on designated tiers based on regular expressions
4. Delete and create segments: How to delete and create annotation units based on a set of conditions
5. ...

# Sanity checks

With the function XXX provided by YYY.py, you can easily check one or multiple .eaf files for common issues that may 
The script checks for 

1. adherence to the EAFv3.0 XML schema ("validation")
2. inconsistent time codes (e.g. negative time codes or units with negative durations) 
4. overlaps between annotation units
5. duplicate tiers or annoation units
6. ...

We recommend integrating this function into your workflow and calling it as often as possible, ideally before and after each processing step.
