
# coding: utf-8

# # Pilot Subjects Analysis

# Experimental stimuli are as follows:  
# - Condition 1: Same stimuli (see cat / hear cat) -- `SS`  
# - Condition 2: Phonologically congruent (see cat / hear hat) -- `CP`  
# - Condition 3: Semantically congruent (see cat / hear dog) -- `CS`  
# - Condition 4: Unrelated stimuli (see house / hear cat)  -- `US`  

# In[14]:


"""
Environment setup
"""
get_ipython().magic('matplotlib inline')
get_ipython().magic('cd ~/Programming/projects/language_decision/')
import warnings; warnings.filterwarnings('ignore')
import hddm


# In[16]:


pilot_subjects = hddm.load_csv('data/pilot_clean.csv')

model = hddm.HDDM(pilot_subjects, depends_on={'v': 'stim'})
model.find_starting_values()
model.sample(6000, burn=20)


# ### Model Statistics

# In[17]:


model.print_stats()


# ### Plotting Posteriors

# In[18]:


model.plot_posteriors()


# ### Checking for Model Convergence

# In[20]:


models = []
for i in range(5):
    m = hddm.HDDM(pilot_subjects, depends_on={'v': 'stim'})
    m.find_starting_values()
    m.sample(6000, burn=20)
    models.append(m)

hddm.analyze.gelman_rubin(models)

