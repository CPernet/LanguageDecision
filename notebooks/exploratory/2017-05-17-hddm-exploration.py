
# coding: utf-8

# # Exploring hddm

# In[25]:

get_ipython().magic('matplotlib inline')


# ## Quick-Start Tutorial
# 
# As found in the hddm repo README file - see https://github.com/hddm-devs/hddm

# In[11]:

import hddm

# Load csv data - converted to numpy array
data = hddm.load_csv('../examples/hddm_simple.csv')

# Create hddm model object
model = hddm.HDDM(data, depends_on={'v': 'difficulty'})

# Markov chain Monte Carlo sampling
model.sample(2000, burn=20)


# Notes on MCMC sampling:

# In[19]:

# Model fitted parameters & summary stats
model.print_stats()

model.print_stats().__class__


# `print_stats()` is literally just a printer - it doesn't return a data structure. Could parse this info in a nice python data structure?

# In[27]:

# Fit posterior RT distributions
model.plot_posteriors()


# In[28]:

# Plot theoretical RT distributions
model.plot_posterior_predictive()


# -------

# ## Demo
# 
# As found at http://ski.clps.brown.edu/hddm_docs/tutorial_python.html
