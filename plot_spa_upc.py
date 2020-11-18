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

serie_previsao = pd.read_csv('/discolocal/bruno/SPAupc/previsao_1711.csv', sep =';',
                             index_col = 0)
serie_previsao
serie_previsao.index = pd.to_datetime(serie_previsao.index)
serie_previsao

plt.figure()
plt.plot(serie_previsao['Observado'], label = "Observado", linewidth = 2.0, color = 'k')
plt.plot(serie_previsao['Chuva_min'], label = "Simulacao 1", linewidth = 1.5, color = 'orangered')
plt.plot(serie_previsao['Chuva_med'], label = "Simulacao 2", linewidth = 1.5, color = 'blue')
plt.plot(serie_previsao['Chuva_max'], label = "Simulacao 3", linewidth = 1.5, color = 'green')
plt.grid(color = 'b', ls = 'dotted', lw = 0.4)
#plt.title('Simulação Pedra do Cavalo ', loc = 'left')
plt.ylabel('Vazão Diária Média [m3/s]')
plt.legend(loc="lower center", bbox_to_anchor=(0.5, -0.2), ncol = 4, fontsize = 8, fancybox = True)
# Format the date into months & days
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
# Change the tick interval
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=2))
# Puts x-axis labels on an angle
plt.gca().xaxis.set_tick_params(rotation = 0)
# Changes x-axis range
plt.gca().set_xbound(serie_previsao.index[0], serie_previsao.index[-1])
# data_texto = ('Data inicial: ' + str(data_ini.strftime("%Y-%m-%d")) + '\n' +
#               'Data final: ' + str(data_fim.strftime("%Y-%m-%d")))
# plt.annotate(data_texto, xy=(1,1), xytext=(-4,26), fontsize=10,
#              xycoords='axes fraction', textcoords='offset points',
#              bbox=dict(facecolor='white', alpha=0.8),
#              horizontalalignment='right', verticalalignment='top')
plt.savefig('/discolocal/bruno/SPAupc/previsao_1711.png', dpi = 300, bbox_inches = 'tight')
plt.show()
