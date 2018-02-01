
# coding: utf-8

# # Data Wrangling
# 
# Explore the experimental data & convert to HDDM-ready format (CSV)

# ## Fine-tune output for individual .mat files

# In[1]:


import scipy.io as scio

# Import .mat file as python object
data = scio.loadmat('../data/data_18333.mat', struct_as_record=False)


# For now, let's focus on the following:  
# - Reaction time (rt)  
# - Response (0/1)  
# - Stimulus (1-4 for now)  
# 
# This is similar to `examples/hddm_simple.csv`, used to play around with the HDDM library

# In[2]:


dat_struct = data['data'][0,0]  # Actual data structure, owns to matlab weirdness


# Before outputing to CSV, data for each subject will go in a python dictionary in the form of key --> array. The plan is to then create an array of dictionaries for all patients, with each dictionary representing the data gathered for an individual

# In[3]:


"""
Conversion from convoluted numpy array that scipy.io spits out to a more
pythonic data structure.
Leverage python instead of numpy for data manipulation, since the use of
numpy isn't really necessary for this data.
"""

#subject['rt'] = dat_struct.rt1.tolist()[0]
#subject['response'] = [x[0] for x in dat_struct.perf1.tolist()]
#subject['stim'] = [x[0] for x in dat_struct.conditions1.tolist()]

csv_keys = ['rt', 'response', 'stim']

reaction_times = dat_struct.rt1.tolist()[0]
responses = [x[0] for x in dat_struct.perf1.tolist()]
stimuli = [x[0] for x in dat_struct.conditions1.tolist()]

subject = []

for exp_run in list(zip(reaction_times, responses, stimuli)):
    trial = dict.fromkeys(csv_keys)
    trial['rt'], trial['response'], trial['stim'] = exp_run
    subject.append(trial)


# Now that the data is in a desirable format, we can dump it to a CSV file

# In[4]:


import csv

with open('../data/data_18333.csv', 'w') as f:
    w = csv.DictWriter(f, csv_keys)
    w.writeheader()
    w.writerows(subject)


# ## Convert all .mat files to .csv
# 
# Convert data from .mat files to .csv files for use by the HDDM library

# In[5]:


keys = ['rt', 'response', 'stim']


# In[6]:


def mat2py(mat_path):
    """
    Function to convert mat file to a pythonic data structure
    Returns list of dictionaries mapping to spectific attributes
    """
    data = scio.loadmat(mat_path, struct_as_record=False)
    
    dat_struct = data['data'][0,0]
    
    reaction_times = dat_struct.rt1.tolist()[0]
    responses = [x[0] for x in dat_struct.perf1.tolist()]
    stimuli = [x[0] for x in dat_struct.conditions1.tolist()]

    subject = []

    for exp_run in list(zip(reaction_times, responses, stimuli)):
        trial = dict.fromkeys(keys)
        trial['rt'], trial['response'], trial['stim'] = exp_run
        subject.append(trial)
    
    return subject


# In[7]:


def subject2csv(subject, mat_path):
    csv_path = mat_path.replace('.mat', '.csv')
    print(csv_path)
    with open(csv_path, 'w') as f:
        w = csv.DictWriter(f, keys)
        w.writeheader()
        w.writerows(subject)


# In[8]:


"""
Iterate through all .mat files in the data directory and 
convert them to csv format
"""

import glob

data_dir = '../data/pilot_subjects/'

mat_files = glob.glob(str(data_dir) + '*.mat')

for mat in mat_files:
    subject2csv(mat2py(mat), mat)


# A cleaned-up version of the above is found under `utils/matparser.py`

# In[10]:


dat_struct.__dict__

