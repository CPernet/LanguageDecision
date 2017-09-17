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


### Using Docker

1. Make sure you've installed the docker engine for your OS

2. Build the docker environment

		docker build -t langdec .

3. Run the docker image

		docker run -d -p 5000:5000 langdec

4. The jupyter notebook should now be running at localhost:5000.  
   If prompted for a password by jupyter, type "langdec" to log in


Alternatively, you can skip building the docker image locally and run from the Docker registry using `docker run -d -p 5000:5000 celefthe/langdec`
