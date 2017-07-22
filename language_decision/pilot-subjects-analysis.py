
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


# ### Posterior of Drift Rate for Group Means

# In[22]:


v_SS, v_CP, v_CS, v_US = model.nodes_db.node[['v(SS)', 'v(CP)', 'v(CS)', 'v(US)']]

hddm.analyze.plot_posterior_nodes([v_SS, v_CP, v_CS, v_US])


# ### Checking for Model Convergence

# In[20]:


models = []
for i in range(5):
    m = hddm.HDDM(pilot_subjects, depends_on={'v': 'stim'})
    m.find_starting_values()
    m.sample(6000, burn=20)
    models.append(m)

hddm.analyze.gelman_rubin(models)


# ## Bias Analysis

# In[21]:


model_bias = hddm.HDDM(pilot_subjects, depends_on={'v': 'stim', 'z': 'stim'}, bias=True)
model_bias.find_starting_values()
model_bias.sample(6000, burn=20)

