import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import pytz
import json
import psycopg2, psycopg2.extras


#postos_vazao = {
#                'Rio_Negro':'26064948',
#                'Porto_Amazonas':'25334953',
#                'Sao_Bento':'25564947',
#                'Pontilhao':'25555031',
#                'Santa_Cruz_Timbo':'26125049',
#                'Sao_Mateus_Sul':'25525023',
#                'Divisa':'26055019',
#                'Fluviopolis':'26025035',
#                'Uniao_da_Vitoria':'26145104',
#                'Madereira_Gavazzoni':'25485116',
#                'Jangada':'26225115',
#                'Solais_Novo':'26055155',
#                'Porto_Santo_Antonio':'25235306',
#                'Aguas_do_Vere':'25465256',
#                'Porto_Capanema':'25345435',
#                'Hotel_Cataratas':'25685442'
#            }

posto_nome = 'Porto_Amazonas'
posto_codigo = '25334953'

########## SERIES HORARIAS ##########

#le arquivo com serie de 15 minutos
bruto_15min = pd.read_csv('../dados/'+posto_nome+'FC.csv', index_col=0, sep=';')
bruto_15min.index = pd.to_datetime(bruto_15min.index)
bruto_15min.drop(['flag'], axis=1, inplace = True)

#cria DFs padrao horario para ser preenchido com os dados de 15 min
t_ini = bruto_15min.index[0].round('1h')
t_fim = bruto_15min.index[-1]
date_rng_horario = pd.date_range(start=t_ini, end=t_fim, freq='H', tz = "UTC")
table_hor = pd.DataFrame(date_rng_horario, columns=['date'])
table_hor['datahora_UTC']= pd.to_datetime(table_hor['date'])
table_hor = table_hor.set_index('datahora_UTC')
table_hor.drop(['date'], axis=1, inplace = True)


# agrupa em dados horarios, com intervalo fechado à direita (acumulado/media da 0:01 a 1:00);
# coluna count resulta a soma (contagem) dos "1", coluna valor resulta na media dos valores;
# para os valores de cont < 4, substitui o dado em 'valor' por NaN:
bruto_15min['count'] = np.where(bruto_15min['q_m3s'].notnull(), 1, 0)
df_horario = (bruto_15min.resample("H", closed='right', label='right').
              agg({'count' : np.sum, 'q_m3s' : np.mean, 'h_m' : np.mean}))
#df_horario.loc[df_horario['count'] < 4, ['q_m3s']] = np.nan
#df_horario.loc[df_horario['count'] < 4, ['m']] = np.nan

# remove colunas 'count' dos dataframes e agrupa com data padrao
df_horario.drop('count', axis=1, inplace=True)
table_hor = pd.merge(table_hor, df_horario, left_index = True,
                     right_index = True, how = 'left')
table_hor = table_hor[~table_hor.index.duplicated(keep='first')]

#exporta observado para csv
table_hor.to_csv('../dados/f_consist/'+posto_nome+'_HR.csv',
                 date_format='%Y-%m-%dT%H:%M:%SZ', sep = ";",
                 float_format = '%.3f')

#exporta plot serie historica
plt.figure()
plt.plot(table_hor['h_m'], label = "Cota", linewidth = 0.3)
plt.title('Serie ' + posto_nome)
#plt.xlabel('Data')
plt.ylabel('h[m]')
# Format the date into months & days
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
# Change the tick interval
plt.gca().xaxis.set_major_locator(mdates.YearLocator(5))
# Puts x-axis labels on an angle
plt.gca().xaxis.set_tick_params(rotation = 30)
# Changes x-axis range
#plt.gca().set_xbound(data_ini, data_fim)
plt.savefig('../dados/f_consist/'+posto_nome+'_HR.png', dpi = 300,
            bbox_inches = 'tight')
plt.close()
