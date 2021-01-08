import numpy as np
import pandas as pd
import datetime as dt
import csv


########## SERIES ORIGINAL ##########
arquivo_pd14 = '../dados/brutos_pcj/14_ssdpcj_20201228.csv'
codigo_posto14 = arquivo_pd14.split('/')[-1].split('_')[0]
lat_long14 = pd.read_csv(arquivo_pd14, skiprows=2, nrows=1, header=None,
                       sep = ',').iloc[0]
long14 = lat_long14[0]
lat14  = lat_long14[1]
alt14 = lat_long14[2]
sr_posto14 = pd.read_csv(arquivo_pd14, skiprows=3, parse_dates=True,
                       index_col='datahora', sep=',')
sr_posto14.drop('status', axis=1, inplace=True)
t_ini = sr_posto14.index[0].round('1h')
t_fim = sr_posto14.index[-1]
df_horario14 = (sr_posto14.resample("H", closed='right', label='right').
              agg({'chuva_mm' : np.sum}))
df_diario14 = (sr_posto14.resample("D", closed='right', label='right').
              agg({'chuva_mm' : np.sum}))
df_mensal14 = (sr_posto14.resample("M", closed='right', label='right').
              agg({'chuva_mm' : np.sum}))
df_anual14 = (sr_posto14.resample("Y", closed='right', label='right').
              agg({'chuva_mm' : np.sum}))

df_anual14

arquivo_pd84 = '../dados/brutos_pcj/84_ssdpcj_20201228.csv'
codigo_posto84 = arquivo_pd84.split('/')[-1].split('_')[0]
lat_long84 = pd.read_csv(arquivo_pd84, skiprows=2, nrows=1, header=None,
                       sep = ',').iloc[0]
long84 = lat_long84[0]
lat84  = lat_long84[1]
alt84 = lat_long84[2]
sr_posto84 = pd.read_csv(arquivo_pd84, skiprows=3, parse_dates=True,
                       index_col='datahora', sep=',')
sr_posto84.drop('status', axis=1, inplace=True)
if sr_posto84.index[0] < t_ini:
    t_ini = sr_posto84.index[0].round('1h')
if sr_posto84.index[-1] > t_fim:
    t_fim = sr_posto84.index[-1]
df_horario84 = (sr_posto84.resample("H", closed='right', label='right').
              agg({'chuva_mm' : np.sum}))
df_diario84 = (sr_posto84.resample("D", closed='right', label='right').
              agg({'chuva_mm' : np.sum}))
df_mensal84 = (sr_posto84.resample("M", closed='right', label='right').
              agg({'chuva_mm' : np.sum}))
df_anual84 = (sr_posto84.resample("Y", closed='right', label='right').
              agg({'chuva_mm' : np.sum}))

arquivo_pd43 = '../dados/brutos_pcj/43_ssdpcj_20201228.csv'
codigo_posto43 = arquivo_pd43.split('/')[-1].split('_')[0]
lat_long43 = pd.read_csv(arquivo_pd43, skiprows=2, nrows=1, header=None,
                       sep = ',').iloc[0]
long43 = lat_long43[0]
lat43  = lat_long43[1]
alt43 = lat_long43[2]
sr_posto43 = pd.read_csv(arquivo_pd43, skiprows=3, parse_dates=True,
                       index_col='datahora', sep=',')
sr_posto43.drop('status', axis=1, inplace=True)
if sr_posto43.index[0] < t_ini:
    t_ini = sr_posto43.index[0].round('1h')
if sr_posto43.index[-1] > t_fim:
    t_fim = sr_posto43.index[-1]
sr_posto43 = sr_posto43.loc['2015':]
df_horario43 = (sr_posto43.resample("H", closed='right', label='right').
              agg({'chuva_mm' : np.sum}))
df_diario43 = (sr_posto43.resample("D", closed='right', label='right').
              agg({'chuva_mm' : np.sum}))
df_mensal43 = (sr_posto43.resample("M", closed='right', label='right').
              agg({'chuva_mm' : np.sum}))
df_anual43 = (sr_posto43.resample("Y", closed='right', label='right').
              agg({'chuva_mm' : np.sum}))
df_anual43

arquivo_pd42 = '../dados/brutos_pcj/42_ssdpcj_20201228.csv'
codigo_posto42 = arquivo_pd42.split('/')[-1].split('_')[0]
lat_long42 = pd.read_csv(arquivo_pd42, skiprows=2, nrows=1, header=None,
                       sep = ',').iloc[0]
long42 = lat_long42[0]
lat42  = lat_long42[1]
alt42 = lat_long42[2]
sr_posto42 = pd.read_csv(arquivo_pd42, skiprows=3, parse_dates=True,
                       index_col='datahora', sep=',')
sr_posto42.drop('status', axis=1, inplace=True)
if sr_posto42.index[0] < t_ini:
    t_ini = sr_posto42.index[0].round('1h')
if sr_posto42.index[-1] > t_fim:
    t_fim = sr_posto42.index[-1]
df_horario42 = (sr_posto42.resample("H", closed='right', label='right').
              agg({'chuva_mm' : np.sum}))
df_diario42 = (sr_posto42.resample("D", closed='right', label='right').
              agg({'chuva_mm' : np.sum}))
df_mensal42 = (sr_posto42.resample("M", closed='right', label='right').
              agg({'chuva_mm' : np.sum}))
df_anual42 = (sr_posto42.resample("Y", closed='right', label='right').
              agg({'chuva_mm' : np.sum}))
df_anual42

########## TRANSFORMA SERIE HORARIA ##########

#cria DFs padrao horario para ser preenchido com os dados de 15 min
date_rng_horario = pd.date_range(start=t_ini, end=t_fim, freq='H', tz="UTC")
table_hor = pd.DataFrame(date_rng_horario, columns=['date'])
table_hor['datahora']= pd.to_datetime(table_hor['date'])
table_hor = table_hor.set_index('datahora')
table_hor.drop(['date'], axis=1, inplace = True)



# remove colunas 'count' dos dataframes e agrupa com data padrao
df_horario.drop('count', axis=1, inplace=True)
table_hor = pd.merge(table_hor, df_horario, left_index = True,
                     right_index = True, how = 'left')
table_hor = table_hor[~table_hor.index.duplicated(keep='first')]
table_hor['status'] = '1'

print(posto_nome, ' acabou - ', list(postos_precip).index(posto_nome)+1,"/",
      len(postos_precip))
