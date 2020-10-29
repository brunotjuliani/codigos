#BIBLIOTECAS
import os
import HydroErr as he
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import datetime as dt
import requests
import pytz
from dateutil.relativedelta import relativedelta
gbl = globals()

#DEFINICAO PERIODO ANALISE
data_inicial = dt.datetime(1999, 1, 1,  0,  0) #YYYY, M, D, H, Min
data_final = dt.datetime(1999, 12, 31,  23,  59)

dir_usinas = "/discolocal/bruno/Coleta_Dados/Dados_Usinas"
dir_observado = "/discolocal/bruno/Observado"
dir_bacias = "/discolocal/bruno/Coleta_Dados/Dados_Bacias"
dir_usinas = "/discolocal/bruno/Coleta_Dados/Dados_Usinas"
dir_consistencia = "/discolocal/bruno/Observado/Pre_Consistencia"
os.chdir(dir_consistencia)


posto_nome = 'Rio_Negro'
posto_codigo = '26064948'


data_ini = data_inicial
data_fim = data_ini + relativedelta(days=+10)
while data_ini <= data_final:
#    serie_observada = pd.read_csv('vazao_'+nome_bacia+'_1h.csv', index_col=0)
    serie_observada = pd.read_csv(posto_codigo+'FC.csv', sep =';', index_col = 0)
    serie_observada.index = pd.to_datetime(serie_observada.index)
    serie_observada = serie_observada.loc[str(data_ini) : str(data_fim)]
    serie_observada

    plt.figure()
    plt.plot(serie_observada['h_m'], label = "Observado", linewidth = 0.5)
    plt.title('Serie ' + posto_nome, loc = 'left')
    plt.xlabel('Data')
    plt.ylabel('Nivel [m]')
    # Format the date into months & days
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # Change the tick interval
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    # Puts x-axis labels on an angle
    plt.gca().xaxis.set_tick_params(rotation = 30)
    # Changes x-axis range
    plt.gca().set_xbound(data_ini, data_fim)
    data_texto = ('Data inicial: ' + str(data_ini.strftime("%Y-%m-%d")) + '\n' +
                  'Data final: ' + str(data_fim.strftime("%Y-%m-%d")))
    plt.annotate(data_texto, xy=(1,1), xytext=(-4,26), fontsize=10,
                 xycoords='axes fraction', textcoords='offset points',
                 bbox=dict(facecolor='white', alpha=0.8),
                 horizontalalignment='right', verticalalignment='top')
    plt.show()
    data_ini = data_fim
    data_fim = data_ini + relativedelta(days=+10)
