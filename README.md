# LanguageDecision

[![Build Status](https://travis-ci.org/CPernet/LanguageDecision.svg?branch=master)](https://travis-ci.org/CPernet/LanguageDecision)


Repo for the analysis of a language related task in healthy participants and stroke patients

## Setup

1. Install Anaconda

2. Create a new Anaconda environment based on the model's requirements

		conda env create --name lang-dec --file=environment-linux.yml  # On Linux hosts
        conda env create --name lang-dec --file=environment-osx.yml    # On OSX hosts

3. Activate the new environment

		source activate lang-dec

4. Start the Jupyter Notebook main directory

		jupyter notebook language-decision/


### Using Vagrant

If Vagrant is already installed on your system, navigate to the project directory and simply run `vagrant up`.  
The jupyter server will come up on localhost:8080; tail the command output for the access token.
