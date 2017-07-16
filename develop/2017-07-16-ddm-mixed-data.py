
# coding: utf-8

# # Mixed Data DDM
# 
# DDM using both patient and matched control data

# In[2]:


get_ipython().magic('matplotlib inline')
get_ipython().magic('cd ..')

import warnings; warnings.filterwarnings('ignore')


# #### Start by parsing the .mat files from the matched controls

# In[2]:


from utils import matparser, data_compiler
import glob

data_dir = 'data/controls/'

matparser.parse_dir(data_dir)

out_dir = "data/controls.csv"
data_compiler.compile_dir(data_dir, out_dir)


# Clean up - remove *nan* entries as these cause hddm to fail

# In[3]:


get_ipython().system('cat data/controls.csv | grep -v nan > data/controls_clean.csv ')


# Merge patient and matched control data to single .csv file
# 
# First, create tagged versions of the csv files - include "tag" column to differentiate between patient and control

# In[36]:


get_ipython().system('cat data/patients_clean.csv | sed 1d | awk -v d="patient" -F"," \'BEGIN { OFS = "," } {$5=d; print}\' | tr -d $\'\\r\' > data/patients_tagged.csv')
get_ipython().system('cat data/controls_clean.csv | sed 1d | awk -v d="control" -F"," \'BEGIN { OFS = "," } {$5=d; print}\' | tr -d $\'\\r\' > data/controls_tagged.csv')

get_ipython().system('echo "response,rt,subj_idx,stim,subj_type" > data/combined_clean.csv')
get_ipython().system('cat data/patients_tagged.csv >> data/combined_clean.csv; sed 1d data/controls_tagged.csv >> data/combined_clean.csv')


# ## Build HDDM model

# In[3]:


import hddm

data = hddm.load_csv('data/combined_clean.csv')

model = hddm.HDDM(data, depends_on={'v': ['stim', 'subj_type'], 'a': 'subj_type'})
model.find_starting_values()
model.sample(6000, burn=20)

