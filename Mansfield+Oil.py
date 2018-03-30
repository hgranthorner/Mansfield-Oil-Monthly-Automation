
# coding: utf-8

# In[19]:

import pandas as pd
import datetime
import numpy
from pandas.tseries.offsets import MonthEnd


# In[25]:

#Read in raw data (moraw)
moraw = pd.read_csv(r'C:\Users\HHORNER\Documents\My WMATA\Mansfield Oil\Current\Mansfield Oil New.csv')
moraw.head()


# In[27]:

moraw.tail()


# In[4]:

moraw.shape


# In[5]:

list(moraw)


# In[6]:

#Drop unused columns
moraw.drop(['DeliveryNumber','PONum','Location','DeptID','GLAccount','CarrierName','ReferenceNum','ProdCode','GrossGallons','NetGallons','SubTotal','Notes','DeliveryDate'],
          axis=1,
          level=None,
          inplace=True)


# In[7]:

#Add ACCT NO column
moraw['ACCT NO'] = '11094'
#Switch to new dataframe, remove duplicate header rows from dataframe
modata = moraw[~moraw.BOL.str.contains('BOL')]


# In[8]:

modata.shape


# In[9]:

list(modata)


# In[10]:

#Create Fuel Type column df['color'] = np.where(df['Set']=='Z', 'green', 'red')
modata['FuelType'] = numpy.where(modata['ProdDescription'].str[:4] == 'ULSD','D','G')
modata.head()


# In[11]:

#Rename ShipToAddress to Location
modata.rename(columns={'ShipToAddress' : 'Location'},inplace=True)
modata.head()


# In[12]:

#Load Tank ID file
df = pd.read_csv(r'C:\Users\HHORNER\Documents\My WMATA\Mansfield Oil\Current\Mansfield Oil VLOOKUP Table.csv')
tank = df[['Location','TANK']]
tank


# In[13]:

#Left join dataframes
left = modata
right = tank
mo = pd.merge(left,right,how='left',on='Location')
#Check null Tank IDs
mo['TANK'].isnull().values.any()


# In[14]:

#Double Check
mo['TANK'].unique()


# In[15]:

#Create EMSys Account Numbers
mo['EMSys Account Number'] = mo['ACCT NO'] + '-' + mo['TANK'] + '-' + mo['FuelType']
mo['EMSys Account Number']


# In[16]:

#Create Start and End Dates
mo['StartDate'] = pd.to_datetime(mo['InvoiceDate'].str.split('/').str[0] + '/1/' + mo['InvoiceDate'].str.split('/').str[2])
mo['EndDate'] = mo['StartDate'] + MonthEnd(1)
mo.head()


# In[17]:

#Export Diesel
mo[mo.FuelType.str.contains('D')].to_csv(r'C:\Users\HHORNER\Documents\My WMATA\Mansfield Oil\Current\Mansfield Oil Diesel.csv')


# In[18]:

#Export Gasoline
mo[mo.FuelType.str.contains('G')].to_csv(r'C:\Users\HHORNER\Documents\My WMATA\Mansfield Oil\Current\Mansfield Oil Gasoline.csv')

