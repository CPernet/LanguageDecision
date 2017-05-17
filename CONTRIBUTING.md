# Contributing Guidelines for LanguageDecision

This document provides a set of guidelines to ensure the homogeneity of the project's codebase,
rendering the task of browsing through the code (either in scripts or Jupyter notebooks) relatively
straightforward and painless.

## Project Structure
Model development takes place in separate date-labelled notebooks under `develop/`, which are styled after 
lab notebooks and include both initial attempts as well as step-wise refinements that lead to the final model.
Each notebook should concern a particular, fairly specific aspect of the analysis, so that they do not get too
large (i.e. more than 8-10 code cells per notebook).

The files under `language-decision/` represent the final model and serve as a report on this project. Only refined
aspects of the model should be included under this directory.

All documentation should go under `docs/`. This project uses reStructuredText as the preferred file format for 
documentation. These files should aim to describe the more technical aspects of the project, and should include:  
- Function descriptions  
- Data structures  
- Descriptions of additional packages used  
- Justification for any assumptions made  
- Model evaluation  
- Identified limitations  
Note that this documentation should *complement* the accompanying text in Jupyter notebooks - not act as a substitute.

General utilities are found under `utils/`. 

Example usage of various model aspects is found under `examples/`, and can either take the form of python scripts or
Jupyter notebooks.

    .  
    |-- docs/  # Project documentation  
    |-- develop/  # Lab-notebook style notebooks for use during model development  
    + |-- [YYYY-MM-DD]-[short description].ipynb  
    + |-- 2017-05-16-control-ddm-fit.ipynb  
    + |-- [YYYY-MM-DD]-[short description].py (auto-generated)  
    + |-- 2017-05-16-control-ddm-fit.py  
    |-- language-decision/  # Final analysis/report  
    + |-- language-decision-model.ipynb  
    + |-- language-decision-model.py (auto-generated)  
    |-- utils/  
    + |-- jupyter-config/  
      + |-- post-save-hook.py  
      + |-- setup.sh  
    |-- data/  
    |-- tests/  
    |-- examples/  
    |-- LICENSE  
    |-- README.md  
    |-- requirements.txt  
    |-- CONTRIBUTING.md  


## Setting up a Development Environment
1. Install Anaconda, create & activate a new virtual environment as described in the README file
2. *(Optional)* To automatically generate python files from Jupyter notebooks every time a notebook is saved,
install the Jupyter post-save hook by running `utils/jupyter-config/setup.sh`. Note that this script only supports
MacOS and Linux hosts at the moment.

## Code Style
All Python code, including code found in Jupyter notebooks, should adhere to the [PEP-8 style guide](https://www.python.org/dev/peps/pep-0008/),
particularly with regards to the naming convention. 

In a nutshell:
- Functions and variables should be all lowercase, with words separated by underscores ("_"), `like_so`  
- No function or variable should consist of more than 3 words - use abbreviations instead  
- Constants should be `ALL_CAPS`  
- Classes should use the `CapWords` convention; for this project, prefer functions over classes  
- Modules should have short, all lowercase names  

## Documentation
Code in Jupyter notebooks should follow a logical structure, and should always be accompanied by explanatory text, 
ideally both before and after a particular analysis (that produces output).

Technical documentation should go under `docs/`, to avoid jeopardising clarity in individual Jupyter notebooks.
