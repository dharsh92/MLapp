#!/usr/bin/env python
# coding: utf-8

# In[308]:


import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter, CoxTimeVaryingFitter
from lifelines.statistics import logrank_test,pairwise_logrank_test


# In[309]:


#read the csv file
df_aero=pd.read_csv("removals.csv")


# In[310]:


df_aero.head(10)


# In[311]:


#checking the number of records

df_aero.shape


# In[312]:


#check for missing values

print("missing values")
df_aero.isnull().sum()


# In[313]:


#check for outliers

import seaborn as sns

sns.boxplot(x=df_aero['MEL_QTY'])


# In[314]:


#since MEL_QTY has outliers missing values will be filled with median

df_aero['MEL_QTY']= df_aero['MEL_QTY'].fillna(df_aero['MEL_QTY'].median())


# In[315]:


df_aero.isnull().sum()


# In[316]:


df_aero.head(10)


# In[317]:


#since delay qty is a time series data, missing values will be handled using forward fill

df_aero['DELAY_QTY']= df_aero['DELAY_QTY'].fillna(method='ffill')


# In[318]:


df_aero.isnull().sum()


# In[319]:


#dropping the first row as forward fill refers to the previous value
df_aero = df_aero.dropna(axis=0)


# In[320]:


df_aero.shape


# In[321]:


#adding the event column

df_aero['PART_REMOVAL'] = 0

#cosider part removes at the last cycle
idx_last_record = df_aero.reset_index().groupby(by='SERIAL_NUMBER')['index'].last()
df_aero.at[idx_last_record, 'PART_REMOVAL'] = 1


# In[322]:


df_aero


# In[323]:


#create object for KaplanMeierFitter

kmf = KaplanMeierFitter()

#fit the values

kmf.fit(durations = df_aero['TIME_SINCE_INSTALL_CYCLES'], event_observed = df_aero['PART_REMOVAL'])


# In[324]:


#event table

kmf.event_table


# In[325]:


from matplotlib import pyplot as plt


kmf.plot_survival_function()
plt.title('Survival function of Parts');


# In[326]:


#get all the probabilities

kmf.survival_function_


# In[327]:


#add the probabilities to the dataframe

for i in range(len(df_aero)):
    df_aero['PROBABILITY_OF_REMOVAL'] = kmf.survival_function_at_times(df_aero['TIME_SINCE_INSTALL_CYCLES']).tolist()
    


# In[328]:


df_aero


# In[332]:


df_aero.dtypes


# In[329]:


#add the model to pickel

import pickle

with open('survival_pkl', 'wb') as files:
    pickle.dump(kmf, files)


# In[330]:


with open('survival_pkl' , 'rb') as f:
    lr = pickle.load(f)


# In[331]:


lr.survival_function_at_times(20).tolist()

