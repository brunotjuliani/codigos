#BIBLIOTECAS
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import datetime as dt
from dateutil.relativedelta import relativedelta
gbl = globals()

#DEFINICAO PERIODO ANALISE
data_inicial = dt.datetime(2017, 1, 1,  0,  0) #YYYY, M, D, H, Min
data_final = dt.datetime(2017, 12, 31,  23,  59)

# dir_consistencia = "/discolocal/bruno/Observado/Pre_Consistencia"
# os.chdir(dir_consistencia)

dir_dados = '../Teste'
os.chdir(dir_dados)

serie_completa = pd.read_csv('vazao_fiu_HR.csv', sep =',', index_col = 0)
serie_completa.index = pd.to_datetime(serie_completa.index)

serie_completa

data_ini = data_inicial
data_fim = data_ini + relativedelta(days=+10)

while data_ini <= data_final:
    serie_observada = serie_completa.loc[str(data_ini) : str(data_fim)]

    plt.figure()
    plt.plot(serie_observada['qjus'], label = "Observado", linewidth = 0.6)
    plt.title('Serie Fiu', loc = 'left')
    plt.xlabel('Data')
    plt.ylabel('Vazao [m3s-1]')
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
