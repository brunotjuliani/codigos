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
data_inicial = dt.datetime(2016, 1, 1,  0,  0) #YYYY, M, D, H, Min
data_final = dt.datetime(2020, 12, 31,  23,  59)

dir_usinas = "/discolocal/bruno/Coleta_Dados/Dados_Usinas"
dir_observado = "/discolocal/bruno/Observado"
dir_bacias = "/discolocal/bruno/Coleta_Dados/Dados_Bacias"
dir_usinas = "/discolocal/bruno/Coleta_Dados/Dados_Usinas"
os.chdir(dir_observado)


nome_bacia = 'Rio_Negro'

data_ini = data_inicial
data_fim = data_ini + relativedelta(days=+10)
while data_ini <= data_final:
    serie_observada = pd.read_csv('vazao_'+nome_bacia+'_1h.csv', index_col=0)
    serie_observada.index = pd.to_datetime(serie_observada.index)
    serie_observada = serie_observada.loc[str(data_ini) : str(data_fim)]
    serie_observada

    plt.figure()
    plt.plot(serie_observada['q_m3s'], label = "Observado", linewidth = 0.5)
    plt.title('Serie ' + nome_bacia, loc = 'left')
    plt.xlabel('Data')
    plt.ylabel('Q [m3s-1]')
    # Format the date into months & days
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%Y'))
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
