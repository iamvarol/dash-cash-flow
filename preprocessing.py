import pandas as pd
import numpy as np
from datetime import datetime

def preprocess(dataframe, export_status):
    
    # drop unnecessary columns
    dataframe.drop(['Firma', 'Donem', 'GelirGider', 'Yil', 'AyNo', 'Hafta'], axis=1, inplace=True)
    
    dataframe['Tarih'] = dataframe['Vade']
    dataframe['Tarih'] = dataframe.apply(lambda x: x['Aciklama1'] if ((x['Grup']=='Banka')|(x['Grup']=='Kasa'))  else x['Tarih'], axis=1)
    dataframe['Tarih']= pd.to_datetime(dataframe['Tarih']) 
   
    print('before sort :\n', dataframe.dtypes)
    dataframe['timestamp'] = dataframe['Tarih'] # .copy(deep=True) # generate timestamp for the time-window-slider and other graphs
    dataframe['Tarih'] = dataframe['Tarih'].dt.date
    
    # dataframe = dataframe.sort_values("Tarih").set_index("Tarih")
    dataframe.sort_values(by=['Tarih'], inplace=True, ascending=False)
    
    # print('after sort :\n', dataframe.dtypes)
    
    # dataframe.drop(['timestamp'], axis=1, inplace=True)
    # dataframe['A'] = dataframe.apply(lambda x: x['B'] if x['A']==0 else x['A'], axis=1)
    
    dataframe['Yil'] = dataframe['Ay'] = dataframe['Haftanin_Gunu'] = dataframe['Tarih']
    
    dataframe['Yil'] = dataframe['Yil'].apply(lambda x: datetime.strftime(x, '%Y'))  # Datetime -> year string
    dataframe['Ay'] = dataframe['Ay'].apply(lambda x: datetime.strftime(x, '%m'))  # Datetime -> month string
    dataframe['Haftanin_Gunu'] = dataframe['Haftanin_Gunu'].apply(lambda x: datetime.strftime(x, '%A'))  # Datetime -> weekday string
    
    dataframe['Islem Tipi'] = ['Tahsilat' if x > 0 else 'Ödeme' for x in dataframe['Tutar']]
    #df['color'] = ['red' if x == 'Z' else 'green' for x in df['Set']]
    
    if export_status:
        export_csv = dataframe.to_csv (f'data/gimas_db.zip', index = None, header=True)
    # print(dataframe.head())
    # print(dataframe.tail())
    
    return dataframe


if __name__ == '__main__':
    preprocess()
    