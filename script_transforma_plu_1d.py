import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime as dt
import pytz
import json
import psycopg2, psycopg2.extras

dir_klabin = '/discolocal/bruno/Consist_Klabin'
os.chdir(dir_klabin)
lista = []

postos = {
                'Jusante':'Jusante',
                'Montante':'Montante',
            }

########## SERIES HORARIAS ##########
for posto_nome, posto_codigo in postos.items():
    #le arquivo com serie de 15 minutos
    bruto_15min = pd.read_csv(posto_nome+'.csv', index_col = 0)
    bruto_15min.index = pd.to_datetime(bruto_15min.index)
    bruto_15min = bruto_15min[~bruto_15min.index.duplicated(keep='first')]

    #cria DFs padrao horario para ser preenchido com os dados de 15 min
    t_ini = bruto_15min.index[0].normalize()
    t_fim = bruto_15min.index[-1].normalize()

    date_rng_horario = pd.date_range(start=t_ini, end=t_fim, freq='H')
    table_hor = pd.DataFrame(date_rng_horario, columns=['date'])
    table_hor['Datetime']= pd.to_datetime(table_hor['date'])
    table_hor = table_hor.set_index('Datetime')
    table_hor.drop(['date'], axis=1, inplace = True)

    date_rng_diario = pd.date_range(start=t_ini, end=t_fim, freq='D')
    table_dia = pd.DataFrame(date_rng_diario, columns=['date'])
    table_dia['Datetime']= pd.to_datetime(table_dia['date'])
    table_dia = table_dia.set_index('Datetime')
    table_dia.drop(['date'], axis=1, inplace = True)

    df = bruto_15min
    df.columns = ['valor', 'sensor']
    df.drop(df.tail(1).index, inplace=True)
    df[df['valor'] < 0] = np.nan
    df = df.dropna()
    df['count'] = 1
    df.index = pd.to_datetime(df.index)

    # agrupa em dados horarios, com intervalo fechado à direita (acumulado/media da 0:01 a 1:00);
    # coluna count resulta a soma (contagem) dos "1", coluna valor resulta na media dos valores;
    # para os valores de cont < 4, substitui o dado em 'valor' por NaN:
    df_horario = (df.resample("H", closed='left').
                  agg({'count' : np.sum, 'valor' : np.sum}))
    df_horario.loc[df_horario['count'] < 4, ['valor']] = np.nan

    # cria coluna com valores 1;
    # agrupa em dados diarios, com intervalo fechado à direita (acumulado/media da 1:00 a 0:00);
    # coluna count resulta a soma (contagem) dos "1", coluna valor resulta na media dos valores;
    # para os valores de cont < 24, substitui o dado em 'valor' por NaN:
    df_horario['count'] = 1
    df_diario = (df_horario.resample("D", closed='left').
                 agg({'count':np.sum, 'valor' : np.sum}))
    df_diario.loc[df_diario['count'] < 24, ['valor']] = np.nan

    # remove colunas 'count' dos dataframes
    df_diario.drop('count', axis=1, inplace=True)
    table_dia = pd.concat([table_dia, df_diario], axis=1)


    #exporta observado para csv
    table_dia.to_csv(posto_nome+'_diario.csv')


    print(posto_nome, 'acabou - ', list(postos).index(posto_nome)+1,"/",
          len(postos))
