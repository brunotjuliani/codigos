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
data_ini = dt.datetime(2019, 6, 1,  0,  0) #YYYY, M, D, H, Min
data_fim = dt.datetime(2019, 6, 15,  23,  59)

dir_usinas = "/discolocal/bruno/Coleta_Dados/Dados_Usinas"
dir_observado = "/discolocal/bruno/Observado"
os.chdir(dir_observado)


nome_bacia = 'Santa_Cruz_Timbo'

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


os.chdir(dir_observado)
estacao_nome = 'Santa_Cruz_Timbo'
vazao_observado = pd.read_csv("vazao_"+estacao_nome+".csv",
                              index_col = 0).rename(columns = {
                                  'q_m3s':'vazao_obs'})
vazao_observado

gbl["Cod_"+str(calibracao_cod)+'_Horizonte_'+str(horizonte)] = gbl[
    "Cod_"+str(calibracao_cod)+'_Horizonte_'+str(horizonte)].merge(
        vazao_observado['vazao_obs'],how='left', left_index=True,
        right_index=True)

os.chdir(dir_usinas)
estacao_nome = 'DRJ'
vazao_observado = pd.read_csv(estacao_nome+".txt", header = None, skiprows = 1)
vazao_observado['Year'] = vazao_observado[0].str.slice(0,4)
vazao_observado['Month'] = vazao_observado[0].str.slice(5,7)
vazao_observado['Day'] = vazao_observado[0].str.slice(8,10)
vazao_observado['Hora'] = vazao_observado[0].str.slice(11,13).astype(str).astype(int)
vazao_observado['vazao_obs'] = pd.to_numeric(vazao_observado[0].str.slice(14,22), errors = 'coerce')
vazao_observado['Data'] = pd.to_datetime(vazao_observado[['Year', 'Month', 'Day']]) + pd.to_timedelta(vazao_observado['Hora'], unit = 'h')
vazao_observado = vazao_observado.set_index('Data')
vazao_observado = vazao_observado.drop([0, 'Year', 'Month', 'Day', 'Hora'], 1)

vazao_observado
vazao_observado
