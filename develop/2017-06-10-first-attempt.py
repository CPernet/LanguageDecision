
# coding: utf-8

# # First Attempt
# 
# Initial attempt to fit data to DDM, following the HDDM quick-start tutorial

# In[8]:

get_ipython().magic('matplotlib inline')


# In[4]:

import hddm

data = hddm.load_csv('../data/data_18333.csv')

model = hddm.HDDM(data, depends_on={'v': 'stim'})

model.sample(2000, burn=20)

model.print_stats()



# In[9]:

model.plot_posteriors()


# Looks promising!

# In[ ]:



