
# coding: utf-8

# # Data Wrangling
# 
# Explore the experimental data & convert to HDDM-ready format (CSV)

# ## Fine-tune output for individual .mat files

# In[1]:

import scipy.io as scio

# Import .mat file as python object instead of numpy array to make life a little more bearable
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

# In[36]:

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

subject


# Now that the data is in a desirable format, we can dump it to a CSV file

# In[38]:

import csv

with open('../data/data_18333.csv', 'w') as f:
    w = csv.DictWriter(f, csv_keys)
    w.writeheader()
    w.writerows(subject)

