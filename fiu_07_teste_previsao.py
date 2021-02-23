import sys
sys.path.append('../modelos/')
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import gr5i
import matplotlib.pyplot as plt
import HydroErr as he

def plotar_hidro(idx, PME, ETP, Qobs, Qmon=None, Qsims=None):

    fig, (ax1, ax2) = plt.subplots(2, 1,sharex='all',gridspec_kw={'height_ratios': [1, 3]})

    ax1.bar( idx, PME, label='PME', color='blue')
    ax1.plot(idx, ETP, label='etp', color='red')
    ax1.invert_yaxis()
    ax1.set_ylabel('Altura de precipitação (mm)', fontsize=8)
    ax1.legend(loc='upper right', fontsize=8)


    ax2.plot(idx, Qobs, label='Qobs', color='black')
    ax2.set_ylabel('Vazão (m3/s)')
    if Qmon is not None:
        ax2.plot(idx, Qmon, label='Qmon', color='black', linestyle='--')

    if Qsims is not None:
        for chave in Qsims.keys():
            ax2.plot(idx, Qsims[chave], label=chave)
            ax2.legend(loc='upper right', fontsize=8)

    return fig

#Leitura das forçantes do modelo
arq = open('/discolocal/bruno/Fiu/peq_previsao0625_Fiu.csv')
areainc = float(arq.readline())
area = areainc
df = pd.read_csv('/discolocal/bruno/Fiu/peq_previsao0625_Fiu.csv', skiprows=[0],
                  index_col = 'datahora_UTC', parse_dates = True)

df['qmon'] = 0
dt = 6

PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()
Qmon = df['qmon'].to_numpy()


## GR5i 2a calibracao ##
x1 = 1480
x2 = -0.1
x3 = 94
x4 = 2.6
x5 = 0.41

resultado2 = gr5i.gr5i(dt=dt, area=area, PME=PME, ETP=ETP, Qmon=Qmon,
                      x1=x1, x2=x2, x3=x3, x4=x4, x5=x5)
df['gr5i_previsao'] = pd.DataFrame(resultado2, index=df.index)

##CORTE DE TEMPO PARA NASH E PLOTAGEM##
df2 = df.loc['2020-06-25':'2020-07-01']
df2.index
Qsimulado2 = df2[['gr5i_previsao']]

nash_gr = he.nse(df2['gr5i_previsao'],df2['qjus'])
print('Nash GR5i = ' + str(nash_gr))

data_texto = (f'Nash GR5i = {nash_gr:.2f}')

# Plotagem
fig = plotar_hidro(idx=df2.index,
                   PME=df2['pme'],
                   ETP=df2['etp'],
                   Qobs=df2['qjus'],
                   Qmon=df2['qmon'],
                   Qsims=Qsimulado2)
# plt.annotate(data_texto, xy=(1,1), xytext=(-4,100), fontsize=10,
#              xycoords='axes fraction', textcoords='offset points',
#              bbox=dict(facecolor='white', alpha=0.8),
#              horizontalalignment='right', verticalalignment='top')
#fig.savefig('../Teste/prints/fiu_2020_manual.png', dpi = 300,
#             bbox_inches = 'tight')
