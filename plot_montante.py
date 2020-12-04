#BIBLIOTECAS
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import datetime as dt
from dateutil.relativedelta import relativedelta
gbl = globals()

dir_dados = '../dados'
os.chdir(dir_dados)

posto_exutoria= 'Uniao_da_Vitoria'
serie_exutoria = pd.read_csv(posto_exutoria+'_HR.csv', sep =';', index_col = 0)
serie_exutoria.index = pd.to_datetime(serie_exutoria.index)
serie_exutoria = serie_exutoria.rename(columns={'q_m3s':'q_jus'})

posto_mont1 = 'Fluviopolis'
serie_mont1 = pd.read_csv(posto_mont1+'_HR.csv', sep=';', index_col = 0)
serie_mont1.index = pd.to_datetime(serie_mont1.index)
serie_mont1 = serie_mont1.rename(columns={'q_m3s':'q_'+posto_mont1})

posto_mont2 = 'Santa_Cruz_Timbo'
serie_mont2 = pd.read_csv(posto_mont2+'_HR.csv', sep=';', index_col = 0)
serie_mont2.index = pd.to_datetime(serie_mont2.index)
serie_mont2 = serie_mont2.rename(columns={'q_m3s':'q_'+posto_mont2})
serie_mont2

vazoes_montante = pd.merge(serie_exutoria['q_jus'], serie_mont1['q_'+posto_mont1],
                           left_index = True, right_index = True, how = "outer")
vazoes_montante = pd.merge(vazoes_montante, serie_mont2['q_'+posto_mont2],
                           left_index = True, right_index = True, how = "outer")
vazoes_montante['q_montante'] = vazoes_montante['q_'+posto_mont1] + vazoes_montante['q_'+posto_mont2]

vazoes_montante.to_csv('../dados/'+posto_exutoria+'_montantes.csv',
                       date_format='%Y-%m-%dT%H:%M:%SZ', sep = ";",
                       float_format = '%.3f')


data_ini = dt.datetime(2014, 1, 1,  0,  0)
data_fim = dt.datetime(2020, 12, 31,  23,  59)

vazoes_montante = vazoes_montante.loc[str(data_ini) : str(data_fim)]

plt.figure()
plt.plot(vazoes_montante['q_jus'], label = "Uniao da Vitoria", linewidth = 0.6)
plt.plot(vazoes_montante['q_Fluviopolis'], label = "Fluviopolis", linewidth = 0.6)
plt.plot(vazoes_montante['q_Santa_Cruz_Timbo'], label = "Santa Cruz do Timbo", linewidth = 0.6)
plt.plot(vazoes_montante['q_montante'], label = "Q Montante", linewidth = 0.6)
plt.title('Serie ' + posto_exutoria, loc = 'left')
#plt.xlabel('Data')
plt.ylabel('Vazao [m3s]')
plt.legend()
# Format the date into months & days
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
# Change the tick interval
plt.gca().xaxis.set_major_locator(mdates.YearLocator(1))
# Puts x-axis labels on an angle
plt.gca().xaxis.set_tick_params(rotation = 30)
# Changes x-axis range
plt.gca().set_xbound(data_ini, data_fim)
#data_texto = ('Data inicial: ' + str(data_ini.strftime("%Y-%m-%d")) + '\n' +
#              'Data final: ' + str(data_fim.strftime("%Y-%m-%d")))
#plt.annotate(data_texto, xy=(1,1), xytext=(-4,26), fontsize=10,
#             xycoords='axes fraction', textcoords='offset points',
#             bbox=dict(facecolor='white', alpha=0.8),
#             horizontalalignment='right', verticalalignment='top')
plt.savefig('../dados/'+posto_exutoria+'_montantes.png',
            dpi = 300, bbox_inches = 'tight')
plt.show()
