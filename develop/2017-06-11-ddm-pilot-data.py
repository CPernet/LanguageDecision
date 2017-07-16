
# coding: utf-8

# # DDM for All Control Data
# 
# Parse all control data to a single CSV, then check if subject data can fit a hierarchical drift decision model for different stimuli types

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

# In[1]:


def parse_condition(stim_num):
    if stim_num == '1':
        return 'SS'
    if stim_num == '2':
        return 'CP'
    if stim_num == '3':
        return 'CS'
    if stim_num == '4':
        return 'US'


# In[2]:


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

with open('../data/controls.csv', 'w') as out:
        writer = csv.DictWriter(out, keys)
        writer.writeheader()
        for subj in subjects:
            writer.writerows(subj)


# ## First stab at hddm model fit

# In[57]:


import hddm

data = hddm.load_csv('../data/all_subjects_clean.csv')

model = hddm.HDDM(data, depends_on={'v': 'stim'})
model.find_starting_values()
model.sample(6000, burn=20)


# In[4]:


model.print_stats()


# ##### Parameters of Interest
# 
# - Mean of *a* = 2.39576 (std = 0.152745)  
# - Mean of *t* = 0.576694 s  
# - Dift rate (v) mean values:  
#     - CP = 1.47559  
#     - CS = 1.95786  
#     - SS = 2.37192  
#     - US = 2.28449

# #### Plot posteriors

# In[5]:


get_ipython().magic('matplotlib inline')
model.plot_posteriors()


# #### Plot posterior of drift rate for group means

# In[6]:


v_SS, v_CP, v_CS, v_US = model.nodes_db.node[['v(SS)', 'v(CP)', 'v(CS)', 'v(US)']]

hddm.analyze.plot_posterior_nodes([v_SS, v_CP, v_CS, v_US])


# Calculate the proportion of the posteriors in which the drift rate for one condition is greater than the other

# In[7]:


print('P(SS > US) = ' + str((v_SS.trace() > v_US.trace()).mean()))
print('P(CP > SS) = ' + str((v_CP.trace() > v_SS.trace()).mean()))
print('P(CS > SS) = ' + str((v_CS.trace() > v_SS.trace()).mean()))
print('P(CP > CS) = ' + str((v_CP.trace() > v_CS.trace()).mean()))


# Therefore:  
# - The drift rate for **CP** is significantly lower than all other conditions  
# - The drift rate for **CS** is significantly lower than **SS** and **US**, but significantly higher than **CP**  
# - The drift rates for **SS** and **US** are not significantly different  

# #### Check for model convergence 

# In[8]:


models = []
for i in range(5):
    m = hddm.HDDM(data, depends_on={'v': 'stim'})
    m.find_starting_values()
    m.sample(6000, burn=20)
    models.append(m)

hddm.analyze.gelman_rubin(models)


# Models converge!

# ## Explore Bias

# In[65]:


model_bias = hddm.HDDM(data, depends_on={'v': 'stim', 'z': 'stim'}, bias=True)
model_bias.find_starting_values()
model_bias.sample(6000, burn=20)


# In[67]:


model_bias.plot_posteriors()


# In[66]:


model_bias.print_stats()


# In[70]:


model_bias.print_stats()


# z values don't appear to significantly vary
