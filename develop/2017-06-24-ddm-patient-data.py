
# coding: utf-8

# # DDM for Patient Data
# 
# Same as before, parse .mat files to CSV, then attempt to fit data to the hierarchical drift decision model, with 

# In[23]:


get_ipython().magic('matplotlib inline')
import warnings; warnings.filterwarnings('ignore')


# ## Prepare Data

# In[2]:


import sys
sys.path.append('../')


# In[16]:


from utils import matparser
import glob

data_dir = '../data/patients_data/'

matparser.matparser(data_dir)


# In[21]:


# TODO - Place in utils
import csv

def parse_condition(stim_num):
    if stim_num == '1':
        return 'SS'
    if stim_num == '2':
        return 'CP'
    if stim_num == '3':
        return 'CS'
    if stim_num == '4':
        return 'US'

csv_dir = '../data/patients_data/'
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

with open('../data/patients.csv', 'w') as out:
        writer = csv.DictWriter(out, keys)
        writer.writeheader()
        for subj in subjects:
            writer.writerows(subj)


# ## Fit to HDDM model

# In[28]:


import hddm

data = hddm.load_csv('../data/patients_clean.csv')

model = hddm.HDDM(data, depends_on={'v': 'stim', 'z': 'stim'}, bias=True)
model.find_starting_values()
model.sample(6000, burn=20)


# In[29]:


model.print_stats()


# In[30]:


model.plot_posteriors()


# In[31]:


v_SS, v_CP, v_CS, v_US = model.nodes_db.node[['v(SS)', 'v(CP)', 'v(CS)', 'v(US)']]

hddm.analyze.plot_posterior_nodes([v_SS, v_CP, v_CS, v_US])


# In[33]:


print('P(SS > US) = ' + str((v_SS.trace() > v_US.trace()).mean()))
print('P(CP > SS) = ' + str((v_CP.trace() > v_SS.trace()).mean()))
print('P(CS > SS) = ' + str((v_CS.trace() > v_SS.trace()).mean()))
print('P(CP > CS) = ' + str((v_CP.trace() > v_CS.trace()).mean()))


# ### Check Convergence 

# In[32]:


models = []
for i in range(5):
    m = hddm.HDDM(data, depends_on={'v': 'stim'})
    m.find_starting_values()
    m.sample(6000, burn=20)
    models.append(m)

hddm.analyze.gelman_rubin(models)

