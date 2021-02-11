#BIBLIOTECAS
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import datetime as dt
from dateutil.relativedelta import relativedelta
import glob
gbl = globals()

DF = pd.DataFrame()
path_pd = '/discolocal/bruno/PCJ/'
arquivos_pd = glob.glob(path_pd+'*.csv')
for arquivo_pd in arquivos_pd:
    nome_posto = arquivo_pd.split('/')[-1].split('.csv')[0]
    serie_completa = pd.read_csv(arquivo_pd, skiprows=3, index_col='datahora')
    DF[nome_posto] = serie_completa['chuva_mm']
DF.index = pd.to_datetime(DF.index)
DF

#DEFINICAO PERIODO ANALISE
data_inicial = dt.datetime(2018, 1, 1,  0,  0) #YYYY, M, D, H, Min
data_final = dt.datetime(2018, 12, 31,  23,  59)

data_ini = data_inicial
data_fim = data_ini + relativedelta(days=+10)

while data_ini <= data_final:
    recorte = DF.loc[str(data_ini) : str(data_fim)]
    plt.figure()
    x= mdates.date2num(recorte.index)
    for column in recorte:
        plt.bar(x, recorte[column], label = column, width = 0.05)
        x = x+0.06
    plt.xlabel('Data')
    plt.ylabel('Cota [m]')
    # Format the date into months & days
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    # Change the tick interval
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    # Puts x-axis labels on an angle
    plt.gca().xaxis.set_tick_params(rotation = 30)
    plt.legend(bbox_to_anchor=(1.04,1))
    plt.show()
    data_ini = data_fim
    data_fim = data_ini + relativedelta(days=+10)
