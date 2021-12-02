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


# In[216]:


df_aero["OPERATOR_CD"]=pd.to_numeric(df_aero["SERIAL_NUMBER"])


# In[217]:


df_aero['OPERATOR_CD'].astype(str).astype(int)


# In[213]:


cph = CoxPHFitter()
cph.fit(df_aero_new, "TIME_SINCE_INSTALL_CYCLES", event_col="PART_REMOVAL")
cph.print_summary()


# In[177]:


index_names = ['SERIAL_NUMBER', 'TIME_SINCE_INSTALL_CYCLES']


# In[228]:


data = df_aero[index_names+['PART_REMOVAL']].groupby('SERIAL_NUMBER').last()

plt.figure(figsize=(15,7))
survival = KaplanMeierFitter()
survival.fit(data['TIME_SINCE_INSTALL_CYCLES'], data['PART_REMOVAL'])


# In[291]:


data


# In[221]:


get_ipython().run_line_magic('pylab', 'inline')
figsize(12,6)


# In[222]:


survival.plot


# In[229]:


from matplotlib import pyplot as plt


survival.plot_survival_function()
plt.title('Survival function of Parts');


# In[ ]:





# In[264]:


df_aero['TIME_SINCE_INSTALL_CYCLES'][1]


# In[ ]:


df_aero_new = df_aero[index_names+['PART_REMOVAL']].groupby('SERIAL_NUMBER')


# In[265]:


for i in range(len(df_aero)):
    print(i)


# In[288]:


df_aero


# In[ ]:


#check whether air craft age depends on the removal


df_age

df['age'] > 


# In[299]:


df_aero.AIRCRAFT_AGE.unique()


# In[290]:


df_aero.loc[df_aero['SERIAL_NUMBER'] == 'S3TRZMY']


# In[269]:


df_aero['PROBABILITY_OF_REMOVAL']= survival.survival_function_at_times(df_aero['TIME_SINCE_INSTALL_CYCLES'][1])


# In[270]:


df_aero


# In[267]:


df_aero


# In[286]:


s = survival.survival_function_at_times(2325).tolist()


# In[306]:


s.tolist()


# In[305]:


import pickle

pickle_out= open("survival_aero.pkl","wb")
pickle.dump(survival,pickle_out)
pickle_out.close()


# In[ ]:


from flask import Flask

app = Flask(__name__)

@app.route('/getpro', methods=['POST'])
def predict():
     json_ = request.json
     query_df = pd.DataFrame(json_)
     query = pd.get_dummies(query_df)
    
     survival_res = joblib.load('survival.pkl')
     survival_prob= survival_res.survival_function_at_times(query)
     return jsonify({'probability': list(survival_prob)})


if __name__ == '__main__':
     app.run(port=8080)


# In[285]:


s[0]


# In[283]:


pd.to_numeric(s)


# In[282]:


s[0]


# In[274]:


s


# In[275]:





# In[235]:


results = logrank_test(df_aero['TIME_SINCE_INSTALL_CYCLES'], df_aero['PART_REMOVAL'])
results.print_summary()


# In[237]:



results = pairwise_logrank_test(df_aero['TIME_SINCE_INSTALL_CYCLES'], df_aero['PART_REMOVAL'])
results.print_summary()


# In[176]:


df_aero.loc[df_aero['SERIAL_NUMBER'] == 'SZZSF5K']


# In[241]:


df = survival.survival_function_


# In[249]:


df


# In[248]:


df["timeline"]


# In[243]:


df.loc[df['timeline']=='3.0']


# In[ ]:


data


# In[9]:


survival.plot()
plt.ylabel("Probability of survival")
plt.show()
plt.close()

