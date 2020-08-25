# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os.path
import matplotlib.pyplot as plt
import matplotlib.dates as dt

path = os.getcwd()
lista = []

# cria DFs padrão de data, para serem preenchidas com os dados baixados
date_rng_horario = pd.date_range(start='01/01/1998', end='01/01/2020', freq='H')
table_hor = pd.DataFrame(date_rng_horario, columns=['date'])
table_hor['Datetime']= pd.to_datetime(table_hor['date'])
table_hor = table_hor.set_index('Datetime')
table_hor.drop(['date'], axis=1, inplace = True)

date_rng_diario = pd.date_range(start='01/01/1998', end='01/01/2020', freq='D')
table_dia = pd.DataFrame(date_rng_diario, columns=['date'])
table_dia['Datetime']= pd.to_datetime(table_dia['date'])
table_dia = table_dia.set_index('Datetime')
table_dia.drop(['date'], axis=1, inplace = True)


for filename in os.listdir(path):
    if filename.endswith(".txt"):
        cod = filename.strip("_flu.txt")
        lista.append(cod)
                
        df = pd.read_csv(cod + '_flu.txt', sep="|", skiprows=[i for i in range(1,2)])
        df.columns = ['data', cod]
        df.drop(df.tail(1).index, inplace=True)
        df['data'] = pd.to_datetime(df['data'])
        df.set_index('data', inplace=True)
        df['count'] = 1
        
        # agrupa em dados horarios, com intervalo fechado à direita (acumulado/media da 0:01 a 1:00);
        # coluna count resulta a soma (contagem) dos "1", coluna valor resulta na media dos valores;
        # para os valores de cont < 2, substitui o dado em 'valor' por NaN:
        df_horario = df.resample("H", closed='right').agg({'count' : np.sum, cod : np.mean})
        df_horario.loc[df_horario['count'] < 4, [cod]] = np.nan
        
        # cria coluna com valores 1;
        # agrupa em dados diarios, com intervalo fechado à direita (acumulado/media da 1:00 a 0:00);
        # coluna count resulta a soma (contagem) dos "1", coluna valor resulta na media dos valores;
        # para os valores de cont < 12, substitui o dado em 'valor' por NaN:
        df_horario['count'] = 1 						
        df_diario = df_horario.resample("D", closed='left').agg({'count':np.sum, cod : np.mean})
        df_diario.loc[df_diario['count'] < 24, [cod]] = np.nan		
        	
        # remove colunas 'count' dos dataframes
        df.drop(df_horario.columns[0], axis=1, inplace=True)								
        df_horario.drop(df_horario.columns[0], axis=1, inplace=True)
        df_diario.drop(df_diario.columns[0], axis=1, inplace=True)
        
        table_hor = pd.concat([table_hor, df_horario], axis=1)
        table_dia = pd.concat([table_dia, df_diario], axis=1)

table_dia.to_csv(r'D:\Mestrado\Dissertacao_Mestrado\QGIS\Projeto_Mestrado\Estações\Vazão\Processamento\DadosSimepar_Diario_4_24.csv', float_format = '%.2f')

# Looping feels like defeat. However, I'm not clever enough to avoid it 
good_ranges = []
for i in table_dia:
    col = table_dia[i]
    gauge_name = col.name

    # Start of good data block defined by a number preceeded by a NaN
    start_mark = (col.notnull() & col.shift().isnull())
    start = col[start_mark].index

    # End of good data block defined by a number followed by a Nan
    end_mark = (col.notnull() & col.shift(-1).isnull())
    end = col[end_mark].index

    for s, e in zip(start, end):
        good_ranges.append((gauge_name, s, e))

good_ranges = pd.DataFrame(good_ranges, columns=['gauge', 'start', 'end'])

# plotting
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, facecolor='#E6E6E6')
ax = ax.xaxis_date()
ax = plt.hlines(good_ranges['gauge'], 
                dt.date2num(good_ranges['start']), 
                dt.date2num(good_ranges['end']),
                colors='dodgerblue', linewidth = 15)

plt.grid(color='w', linestyle='solid')
plt.title("Disponibilidade de Dados Fluviométricos", loc='center', pad=15, fontsize = 18)

fig.tight_layout()

'''
def dados_flu(arq):
'''
