# In[1]:


# Import necessary packages
import pandas as pd
import numpy as np
import datetime
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import stats
import requests
import json

plt.style.use('seaborn')


# In[2]:


# Define a function to query data

def get_data_request(url, access_token, requestData):
    '''make HTTP GET request'''
    dResp = requests.get(url, headers = {'X-api-key': access_token}, params = requestData)      

    
    if dResp.status_code != 200:
        if False: print("Unable to get data. Code %s, Message: %s" % (dResp.status_code, dResp.text))
    else:
        if False: print("Data access successful")
        jResp = json.loads(dResp.text)
        return jResp


# In[3]:


# Define a function to retrieve data from Refinitiv Data Science Accelerator
# Default window time period is from 2016-11-01 to 2018-01-01

def query_refinitiv_data(ric,start_date='2016-11-01',end_date='2018-01-01'):
  access_token = 'Jjxmy4OMWB5t5osGMF5Ut7qkRipRRhPa4Ns86iiW'  # your personal key for Data Science Accelerator access to Pricing Data
  RESOURCE_ENDPOINT = "https://dsa-stg-edp-api.fr-nonprod.aws.thomsonreuters.com/data/historical-pricing/beta1/views/summaries/" + ric

  requestData = {
      "interval": "P1D",
      "start": start_date,
      "end": end_date,
      "fields": 'TRDPRC_1' #BID,ASK,OPEN_PRC,HIGH_1,LOW_1,TRDPRC_1,NUM_MOVES,TRNOVR_UNS
  }

  # Get the data from Refinitiv server
  jResp = get_data_request(RESOURCE_ENDPOINT, access_token, requestData)

  # Create a DataFrame from the retrieved data
  if jResp is not None:
      data = jResp[0]['data']
      headers = jResp[0]['headers']  
      names = [headers[x]['name'] for x in range(len(headers))]
      df = pd.DataFrame(data, columns=names )

      # Make DATE into DateTime object and make it the Index of df
      df.DATE = pd.to_datetime(df.DATE)
      df = df.set_index('DATE')

      df = df.rename(columns={'TRDPRC_1': 'Price'})
      df = df.sort_index()
      
      return df


# ## Query spot FX data

# In[4]:


# Query spot FX data and create a DataFrame from the data
GBP_USD_df = query_refinitiv_data('=GBP')
GBP_USD_df = GBP_USD_df.rename(columns={'Price':'GBP/USD'})
GBP_USD_df.tail()


# In[5]:


GBP_USD_df.plot(title= 'GBP Spot Price')
plt.xlabel('Date', fontsize=15)
plt.ylabel('Price', fontsize=15)


# ## Query Stock market indices
# 
# We choose the following Stock market index for US and UK
# 
# Country|Index
# -------|---
# US     |SPX
# GBP     |FTSE

# In[6]:


SPX_df = query_refinitiv_data('.SPX')
SPX_df = SPX_df.rename(columns={'Price': 'SPX'})
SPX_df.tail()


# In[7]:


FTSE_df = query_refinitiv_data('.FTSE')
FTSE_df = FTSE_df.rename(columns={'Price': 'FTSE'})
FTSE_df.tail()


# ## Prepare data for GBP/USD

# Combine GBP/USD, SPX and FTSE into 1 DataFrame

# In[8]:


GBP_USD_df = pd.merge(GBP_USD_df,SPX_df,how='outer',left_index=True,right_index=True)
GBP_USD_df = pd.merge(GBP_USD_df,FTSE_df,how='outer',left_index=True,right_index=True)
GBP_USD_df.fillna(method='ffill',inplace=True)
GBP_USD_df.tail()


# Calculate moving average of the indices, which provide a better estimate for the Intrinsic value of those indices

# In[9]:


GBP_USD_df['GBP/USD 5D'] = GBP_USD_df['GBP/USD'].rolling(5).mean()
GBP_USD_df['SPX MA 5D'] = GBP_USD_df['SPX'].rolling(5).mean()
GBP_USD_df['FTSE MA 5D'] = GBP_USD_df['FTSE'].rolling(5).mean()
GBP_USD_df.tail()


# Plot for visualization

# In[10]:


GBP_USD_df.loc[:,['SPX','SPX MA 5D']].plot()
GBP_USD_df.loc[:,['FTSE','FTSE MA 5D']].plot()


# ## Calculating market return for 1 period
# 
# There are on average 30 days of in a month. We take 30 days to be our period duration for calculation

# In[11]:


duration = 30


# In[12]:


GBP_USD_df['SPX Returns 1M'] = GBP_USD_df['SPX MA 5D'].pct_change(duration)
GBP_USD_df['FTSE Returns 1M'] = GBP_USD_df['FTSE MA 5D'].pct_change(duration)
GBP_USD_df.tail()


# In[13]:


GBP_USD_df.reset_index(inplace=True)
GBP_USD_df.tail()


# ## Calculating Fair value of exchange rate using the proposed model
# 
# $$FX_2 = FX_1 \frac{1+r_{UK}}{1+r_{US}}$$

# In[14]:


GBP_USD_df['GBP/USD Fair value'] = np.nan
for i in np.arange(duration,len(GBP_USD_df)):
    GBP_USD_df.loc[i,'GBP/USD Fair value'] = GBP_USD_df.loc[i-duration,'GBP/USD 5D'] * (1 + GBP_USD_df.loc[i,'FTSE Returns 1M']) / (1 + GBP_USD_df.loc[i,'SPX Returns 1M'])


# In[15]:


GBP_USD_df.tail()


# In[16]:


plt.plot(GBP_USD_df['DATE'],GBP_USD_df['GBP/USD'])
plt.plot(GBP_USD_df['DATE'],GBP_USD_df['GBP/USD 5D'])
plt.plot(GBP_USD_df['DATE'],GBP_USD_df['GBP/USD Fair value'])


# ## Sharpe ratio and Backtesting
# 
# Take the risk free rate to be 1.4% and constant throughout our analysis.
# 
# We enter forward contracts for delivery in 1 month time. Thus, our **realized return** will be computed using *current spot exchange rate* and *spot exchange rate in 1 month later*.

# In[17]:


Ra = np.array([])
total_return = 0
threshold = 1


# In[18]:


for i in np.arange(len(GBP_USD_df)-duration):
    if GBP_USD_df.loc[i,'GBP/USD'] - GBP_USD_df.loc[i,'GBP/USD Fair value'] > threshold:              # long position
        Return = 1 - GBP_USD_df.loc[i+duration,'GBP/USD'] / GBP_USD_df.loc[i,'GBP/USD']               # realized return
        Ra = np.append(Ra, Return)    
        total_return += 100 * Return
    
    elif GBP_USD_df.loc[i,'GBP/USD'] - GBP_USD_df.loc[i,'GBP/USD Fair value'] < -threshold:           # short position
        Return = GBP_USD_df.loc[i+duration,'GBP/USD'] / GBP_USD_df.loc[i,'GBP/USD'] - 1               # realized return
        Ra = np.append(Ra, Return)    
        total_return += 100 * Return


# In[19]:


# convert to annual rate, compount the rate by 12 periods (there are 12 months in a year)
Ra = (Ra + 1)**12 - 1


# In[20]:


Ra.mean()


# In[21]:


sns.distplot(Ra)


# In[22]:


Sharpe_ratio = (Ra.mean() - 0.014) / Ra.std()
Sharpe_ratio


# ## Export estimated Fair value
# 
# For submission purpose

# In[23]:


FV_df = GBP_USD_df.loc[:,['DATE','GBP/USD Fair value']]
FV_df.tail()


# In[24]:


# FV_df.to_csv('Fair_value.csv',index=False)

print(total_return)