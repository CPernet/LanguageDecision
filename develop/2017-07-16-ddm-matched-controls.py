
# coding: utf-8

# # DDM for matched controls
# 
# Check how controls fit DDM

# In[1]:


get_ipython().magic('matplotlib inline')
get_ipython().magic('cd ..')

import warnings; warnings.filterwarnings('ignore')


# In[6]:


import hddm

data = hddm.load_csv('data/controls_clean.csv')

model = hddm.HDDM(data, depends_on={'v': 'stim'})
model.find_starting_values()
model.sample(6000, burn=20)


# In[7]:


model.print_stats()


# In[8]:


model.plot_posteriors()


# In[9]:


v_SS, v_CP, v_CS, v_US = model.nodes_db.node[['v(SS)', 'v(CP)', 'v(CS)', 'v(US)']]

hddm.analyze.plot_posterior_nodes([v_SS, v_CP, v_CS, v_US])


# In[11]:


print('P(SS > US) = ' + str((v_SS.trace() > v_US.trace()).mean()))
print('P(CP > SS) = ' + str((v_CP.trace() > v_SS.trace()).mean()))
print('P(CS > SS) = ' + str((v_CS.trace() > v_SS.trace()).mean()))
print('P(CP > CS) = ' + str((v_CP.trace() > v_CS.trace()).mean()))

