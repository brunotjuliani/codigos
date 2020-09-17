#BIBLIOTECAS
import os
import HydroErr as he
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import requests
import pytz
gbl = globals()

#DEFINICAO PERIODO ANALISE
data_ini = dt.datetime(2017, 5, 1,  0,  0) #YYYY, M, D, H, Min
data_fim = dt.datetime(2017, 5, 31,  23,  59)

dir_usinas = "/discolocal/bruno/Coleta_Dados/Dados_Usinas"
dir_observado = "/discolocal/bruno/Observado"
dir_bacias = "/discolocal/bruno/Coleta_Dados/Dados_Bacias"
dir_usinas = "/discolocal/bruno/Coleta_Dados/Dados_Usinas"
os.chdir(dir_observado)


nome_bacia = 'Rio_Negro'

erros = []
try:
    erros = np.hstack(erros)
except ValueError:
    pass

serie_observada = pd.read_csv('vazao_'+nome_bacia+'.csv', index_col=0)
serie_observada.index = pd.to_datetime(serie_observada.index)
serie_observada.loc[pd.to_datetime(erros), 'q_m3s'] = np.nan
serie_observada = serie_observada.loc[str(data_ini) : str(data_fim)]
serie_observada

plt.figure()
plt.plot(serie_observada['q_m3s'], label = "Observado", linewidth = 0.5)
plt.title('Serie ' + nome_bacia, loc = 'left')
plt.xlabel('Data')
plt.ylabel('Q [m3s-1]')
data_texto = ('Data inicial: ' + str(data_ini.strftime("%Y-%m-%d")) + '\n' +
              'Data final: ' + str(data_fim.strftime("%Y-%m-%d")))
plt.annotate(data_texto, xy=(1,1), xytext=(-4,26), fontsize=10,
             xycoords='axes fraction', textcoords='offset points',
             bbox=dict(facecolor='white', alpha=0.8),
             horizontalalignment='right', verticalalignment='top')
