
# coding: utf-8

# In[ ]:


# I will be using these packages over the course of the week
get_ipython().magic(u'matplotlib inline')
import os
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('bmh')
from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
import numpy as np
from sklearn.decomposition import TruncatedSVD # dimensionality reduction for sparse data. 

from geopandas import GeoSeries, GeoDataFrame;
from shapely.wkt import loads
import lightgbm # machine learning library gradient boosted models useful for regression, classifications and other tasks
#import keras super intuitive deep learning library that uses the super-quick tensorflow as a backend.


# In[186]:


trails = gpd.read_file('pud_results_hex.shp')
df_trails = pd.DataFrame(trails)
#os.getcwd()
background = gpd.read_file('rainierNP_boundary.shp')

df_trails['log_PUD_JAN'] = np.log(df_trails['PUD_JAN'])
#PUD_JAN.max()
#length of the columns

# def log_each_column(trails):
#     log_df = []
#     for i in len(df_trails.columns):
#         log_df = np.log(df_trails[i])

#df_trails.head()
# I want to create a function that returns the log transformation for each column to try to assuage the skewedness of the data.
# I see that I am getting negative infinity for the values, 
df_trails.columns[1]
def normalize(geodf, column_index):
     return np.log(geodf.columns[column_index])


# In[187]:


trails.plot(cmap='inferno', figsize =(20,20)); # very pretty graph that I don't really understand. 


# Ideas... chloropleuth plot, results. log transformation to balance the data, omit columns that are not giving good information, maybe some form of regularization, . ML? 
# PCA, dimensionality reduction.
# Binary, where a certain criteria returns a one otherwise a zero to reduce the sparsity in the data. 
# 
# 
# #np.log(trails)
# 

# In[ ]:


print(background.crs); print(background.size)
print(trails.crs); print(trails.size)


# In[ ]:


trails.crs


# In[ ]:


#trails.geometry.area
trails.crs
#trails.geometry.bounds

background.plot(ax=trails.plot(cmap='Set2', figsize=(10, 10)), facecolor='gray'); # Not very informative...


# I have some numpy conversions below that are totally tangential, I thought I might be able to repurpose my deep learning code and try to make a multi-layer perceptron. I dont know this is a good use-case... If anyone is interested in deep learning there is an online course by a world renowned AI expert that goes into detail on this.

# In[ ]:




array = np.array(trails['PUD_JAN'])#trails['PUD_FEB'])#trails['PUD_MAR'],trails['PUD_MAR']) #trails['PUD_APR'], trails['PUD_MAY']) # trails['PUD_JUN'],trails['PUD_JUL'],trails['PUD_AUG'],trails['PUD_SEP'],trails['PUD_OCT'],trails['PUD_NOV'],trails['PUD_DEC'] )


# In[ ]:


array


# In[ ]:


np.log(array)


# In[ ]:


average = np.sum(array)/len(array) # Another way to normalize the data is to find the zscore: (column_sample - column_mean) / column_standard_deviation


# In[ ]:


array.shape


# In[ ]:




