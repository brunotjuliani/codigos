import pandas as pd
import numpy as np

df = pd.read_csv('timbu.csv', parse_dates=True, skiprows=12, header=None, dtype=str)
df


df2 = pd.DataFrame()
df2['temperatura_C'] = pd.to_numeric(df[3] + '.' + df[4])
df2['pressao_M'] = pd.to_numeric(df[5] + '.' + df[6])
df2.index = (pd.to_datetime(df[1], dayfirst=True) + pd.to_timedelta(df[2])).rename('datahora')

print(df2)

df3 = pd.read_csv('dados_20190525.csv', index_col='datahora', parse_dates=True)

df3
