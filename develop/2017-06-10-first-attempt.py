
# coding: utf-8

# # First Attempt
# 
# Initial attempt to fit data from a single subject to DDM, following the HDDM tutorial for a single subject

# In[8]:

get_ipython().magic('matplotlib inline')


# In[14]:

import hddm

data = hddm.load_csv('../data/data_18333.csv')

model = hddm.HDDM(data, depends_on={'v': 'stim'})

model.find_starting_values()

model.sample(2000, burn=20)


# In[9]:

model.plot_posteriors()


# Looks promising!
# 
# Let's formally check for convergence using the Gelman-Rubin R statistic

# In[13]:

models = []

# Generate 5 models
for i in range(5):
    m = hddm.HDDM(data, depends_on={'v': 'stim'})
    m.find_starting_values()
    m.sample(5000, burn=20)
    models.append(m)
    
hddm.analyze.gelman_rubin(models)


# Values are close to 1 and not larger than 1.02, therefore models converge successfully!

# In[15]:

model.print_stats()


# Compare the posterior for different drift-rate conditions

# In[17]:

v_1, v_2, v_3, v_4 = model.nodes_db.node[['v(1)', 'v(2)', 'v(3)', 'v(4)']]

hddm.analyze.plot_posterior_nodes([v_1, v_2, v_3, v_4])

