
# coding: utf-8

# # Exploring hddm

# In[25]:

get_ipython().magic('matplotlib inline')


# ## Following the Quick-Start Tutorial
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


# With regards to sampling:  
# - This guy offers a condensed version of what MCMC sampling is about https://jeremykun.com/2015/04/06/markov-chain-monte-carlo-without-all-the-bullshit/ ; it looks straight-forward enough  
# - Trodding through the docs may provide may provide more insight into why they use 2000 sampling points (my guess is it's a good performance/accuracy tradeoff), and why their burn-in is 20 => **TODO**  
# - More info about the whole burn-in business here http://users.stat.umn.edu/~geyer/mcmc/burn.html => **TODO**  
# 
# Also - pymc throws a bunch of depreciation warnings, might be worth contacting their mailing list & maybe try to fix it? => **TODO**

# In[19]:

# Model fitted parameters & summary stats
model.print_stats()

model.print_stats().__class__


# `print_stats()` is literally just a printer - it doesn't return a data structure. Find out how to get this info in a nice python data structure => **TODO**

# In[27]:

# Fit posterior distributions
model.plot_posteriors()


# In[ ]:



