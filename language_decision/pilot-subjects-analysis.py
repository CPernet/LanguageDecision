
# coding: utf-8

# # Pilot Subjects Analysis
# 
# Dataset gathered from pilot subjects. All subjects were healthy adults. **TODO - ADD DESCRIPTION FOR PILOT SUBJECTS**
# 
# <img src="./ddm_desc.jpeg" width="600">
# 
# Here, we use the `hddm` (Python) library$^1$ to model language-based decision making based on response-time & accuracy data from a binary forced-choice decision task. During each trial, subjects were presented with a digital image of an item (visual stimulus) and a verbal description (auditory stimulus). At the end of each trial, subjects were asked to indicate whether the two types of stimuli agreed (i.e. visual and auditory stimulus pointed to the same object) or were different (i.e. non-matching sound and image). Auditory and visual stimuli pairs fell under four distinct categories, as summarised below:  
# - Condition 1 (**SS**): Same stimuli (see cat / hear cat)
# - Condition 2 (**CP**): Phonologically congruent (see cat / hear hat)
# - Condition 3 (**CS**): Semantically congruent (see cat / hear dog)
# - Condition 4 (**US**): Unrelated stimuli (see house / hear cat)

# In[40]:


"""
Environment setup
"""
get_ipython().magic('matplotlib inline')
get_ipython().magic('cd ~/Programming/projects/language_decision/')
import warnings; warnings.filterwarnings('ignore')
import hddm
import numpy as np
import matplotlib.pyplot as plt


# In[38]:


"""
Plot Drift Diffusion Model for pilot subjects data
"""

pilot_subjects = hddm.load_csv('data/pilot_clean.csv')

# Test if stimulus type affects drift rate
model = hddm.HDDM(pilot_subjects, depends_on={'v': 'stim'})
model.find_starting_values()
model.sample(6000, burn=20)


# ## Dataset & Model Statistics

# In[39]:


model.print_stats() # Dump statistics


# | Variable            | Mean (3 dp) | Standard Deviation (3 dp) | 
# | ------------------- | ----------- | ------------------------- | 
# | Threshold (a)       |    2.396    |           0.565           |
# | SS Drift Rate (vSS) |    2.376    |           0.112           |
# | CP Drift Rate (vCP) |    1.474    |           0.102           |
# | CS Drift Rate (vCS) |    1.956    |           0.110           |
# | US Drift Rate (vUS) |    2.285    |           0.109           |
# | Reaction Time (t)   |    0.578    |           0.339           |

# In[71]:


us = pilot_subjects.loc[pilot_subjects['stim'] == 'US']
ss = pilot_subjects.loc[pilot_subjects['stim'] == 'SS']
cp = pilot_subjects.loc[pilot_subjects['stim'] == 'CP']
cs = pilot_subjects.loc[pilot_subjects['stim'] == 'CS']

plt.boxplot([.rt.values, cp.rt.values, ss.rt.values, us.rt.values], 
            labels=('CS', 'CP', 'SS', 'US'),)
plt.title('Comparison of Reaction Time Differences Between Stimuli Groups')
plt.show()


# ## Model Posteriors Analysis

# In[35]:


model.plot_posteriors()


# ### Posterior of Drift Rate for Group Means

# In[36]:


v_SS, v_CP, v_CS, v_US = model.nodes_db.node[['v(SS)', 'v(CP)', 'v(CS)', 'v(US)']]

hddm.analyze.plot_posterior_nodes([v_SS, v_CP, v_CS, v_US])


# ## Bias Analysis

# In[21]:


model_bias = hddm.HDDM(pilot_subjects, depends_on={'v': 'stim', 'z': 'stim'}, bias=True)
model_bias.find_starting_values()
model_bias.sample(6000, burn=20)


# ## Checking for Model Convergence

# In[23]:


models = []
for i in range(5):
    m = hddm.HDDM(pilot_subjects, depends_on={'v': 'stim'})
    m.find_starting_values()
    m.sample(6000, burn=20)
    models.append(m)

hddm.analyze.gelman_rubin(models)


# ## Conclusions

# ## References
# 
# [1] Wiecki TV, Sofer I and Frank MJ (2013). HDDM: Hierarchical Bayesian estimation of the Drift-Diffusion Model in Python. Front. Neuroinform. 7:14. doi: 10.3389/fninf.2013.00014
