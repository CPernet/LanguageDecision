
# coding: utf-8

# # Mixed Data DDM
# 
# DDM using both patient and matched control data

# In[1]:


get_ipython().magic('matplotlib inline')
get_ipython().magic('cd ..')
import warnings; warnings.filterwarnings('ignore')


# In[2]:


from utils import matparser, data_compiler
import glob

data_dir = 'data/controls/'

matparser.parse_dir(data_dir)

out_dir = "data/controls.csv"
data_compiler.compile_dir(data_dir, out_dir)

