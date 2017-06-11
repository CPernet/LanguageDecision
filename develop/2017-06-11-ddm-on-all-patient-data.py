
# coding: utf-8

# # DDM for All Patient Data
# 
# Parse all patient data to a single CSV, then check if subject data can fit a hierarchical drift decision model for different stimuli types

# Experimental stimuli are as follows:  
# - Condition 1: Same stimuli (see cat / hear cat) -- `SS`  
# - Condition 2: Phonologically congruent (see cat / hear hat) -- `CP`  
# - Condition 3: Semantically congruent (see cat / hear dog) -- `CS`  
# - Condition 4: Unrelated stimuli (see house / hear cat)  -- `US`  

# ### Parse all subject data to single csv
# 
# Generate a single csv for all data, using `subject_idx` as a unique patient identifier. 
# Also give conditions (`stim`) a 2-character descriptive instead of a number.
# 
# CSV fields are as follows:  
# - `subj_idx`: Unique subject identifier  
# - `rt`: Reaction time  
# - `stim`: Stimulus (SS/CP/CS/US)  
# - `response`: Response to stimulus (True(1)/False(0))  

# In[21]:

def parse_condition(stim_num):
    if stim_num == '1':
        return 'SS'
    if stim_num == '2':
        return 'CP'
    if stim_num == '3':
        return 'CS'
    if stim_num == '4':
        return 'US'


# In[29]:

import csv
import glob 


csv_dir = '../data/pilot_subjects/'
subjects = []

for csv_file in glob.glob(csv_dir + 'data*.csv'):
    subject = []
    subj_idx = csv_file[-9:-4]  # Use id from filename
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for trial in reader:
            trial['subj_idx'] = subj_idx
            trial['stim'] = parse_condition(trial['stim'])
            subject.append(trial)
    subjects.append(subject)
    
keys = subject[0].keys()
print(keys)


with open('../data/all_subjects.csv', 'w') as out:
        writer = csv.DictWriter(out, keys)
        writer.writeheader()
        for subj in subjects:
            writer.writerows(subj)
        
print(subjects)

