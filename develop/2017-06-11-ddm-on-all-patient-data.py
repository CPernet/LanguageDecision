
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


# In[31]:

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

with open('../data/all_subjects.csv', 'w') as out:
        writer = csv.DictWriter(out, keys)
        writer.writeheader()
        for subj in subjects:
            writer.writerows(subj)


# ## First stab at hddm model fit

# In[43]:

import hddm

data = hddm.load_csv('../data/all_subjects_clean.csv')

model = hddm.HDDM(data, depends_on={'v': 'stim'})
model.find_starting_values()
model.sample(6000, burn=20)


# In[44]:

model.print_stats()


# #### Plot posteriors

# In[45]:

get_ipython().magic('matplotlib inline')
model.plot_posteriors()


# #### Plot posterior of drift rate for group means

# In[46]:

v_SS, v_CP, v_CS, v_US = model.nodes_db.node[['v(SS)', 'v(CP)', 'v(CS)', 'v(US)']]

hddm.analyze.plot_posterior_nodes([v_SS, v_CP, v_CS, v_US])


# Calculate the proportion of the posteriors in which the drift rate for one condition is greater than the other

# In[54]:

print('P(SS > US) = ' + str((v_SS.trace() > v_US.trace()).mean()))
print('P(CP > SS) = ' + str((v_CP.trace() > v_SS.trace()).mean()))
print('P(CS > SS) = ' + str((v_CS.trace() > v_SS.trace()).mean()))
print('P(CP > CS) = ' + str((v_CP.trace() > v_CS.trace()).mean()))


# Therefore:  
# - The drift rate for CP is significantly lower than all other conditions  
# - The drift rate for CS is significantly 

# #### Check for model convergence 

# In[48]:

models = []
for i in range(5):
    m = hddm.HDDM(data, depends_on={'v': 'stim'})
    m.find_starting_values()
    m.sample(6000, burn=20)
    models.append(m)

hddm.analyze.gelman_rubin(models)


# Models converge!
