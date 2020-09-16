#BIBLIOTECAS
import pandas as pd
import numpy as np
import os
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats


#DEFINICAO PERIODO ANALISE
data_ini = dt.datetime(2020, 7, 1,  0,  0) #YYYY, M, D, H, Min
data_fim = dt.datetime(2020, 7, 31,  23,  59)

dir_usinas = "/discolocal/bruno/Coleta_Dados/Dados_Usinas"
dir_observado = "/discolocal/bruno/Observado"

os.chdir(dir_observado)


nome_bacia = 'Uniao_da_Vitoria'

serie_observada = pd.read_csv('vazao_'+nome_bacia+'.csv', index_col=0)
serie_observada.index = pd.to_datetime(serie_observada.index)
serie_observada = serie_observada.loc[str(data_ini) : str(data_fim)]

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
plt.savefig("vazao_"+nome_bacia+"_"+data_ini.strftime("%Y%m%d")+"_"+
            data_fim.strftime("%Y%m%d")+".png", dpi = 300)
