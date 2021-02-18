import sys
sys.path.append('../modelos/')
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import gr5i
from plotar_hidro import plotar_hidro
import matplotlib.pyplot as plt
import HydroErr as he

#Leitura das forçantes do modelo
arq = open('/discolocal/bruno/Fiu/peq_Fiu_6hrs.csv')
areainc = float(arq.readline())
area = areainc
df = pd.read_csv('/discolocal/bruno/Fiu/peq_Fiu_6hrs.csv', skiprows=[0],
                 index_col = 'datahora_UTC', parse_dates = True)
df['qmon'] = 0
cmb = df['pme']
etp = df['etp']
qmont = df['qmon']
qobs = df['qjus']
Q0 = qobs[0]
dt = 6

PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()
Qmon = df['qmon'].to_numpy()


##MODELO GR5i ##
x1 = 478.654
x2 = 0.426158
x3 = 474.276
x4 = 4.22446
x5 = 0.417908

resultado = gr5i.gr5i(dt=dt, area=area, PME=PME, ETP=ETP, Qmon=Qmon,
                      x1=x1, x2=x2, x3=x3, x4=x4, x5=x5)
df['q_gr5'] = pd.DataFrame(resultado, index=df.index)

## GR5i 2a calibracao ##
x1 = 1101.37
x2 = -0.123209
x3 = 176.285
x4 = 3.49818
x5 = 0.622437


resultado2 = gr5i.gr5i(dt=dt, area=area, PME=PME, ETP=ETP, Qmon=Qmon,
                      x1=x1, x2=x2, x3=x3, x4=x4, x5=x5)
df['gr5i_2'] = pd.DataFrame(resultado2, index=df.index)

##CORTE DE TEMPO PARA NASH E PLOTAGEM##
df2 = df
df2.index
Qsimulado2 = df2[['q_gr5', 'gr5i_2']]

nash_gr = he.nse(df2['q_gr5'],df2['qjus'])
print('Nash GR5i = ' + str(nash_gr))
nash_gr2 = he.nse(df2['gr5i_2'],df2['qjus'])
print('Nash GR5i_2 = ' + str(nash_gr2))

data_texto = (f'Nash GR5i = {nash_gr:.2f}' + '\n' +
              f'Nash GR5i_2 = {nash_gr2:.2f}')

# Plotagem
fig = plotar_hidro(idx=df2.index, PME=df2['pme'], ETP=df2['etp'],
                   Qobs=df2['qjus'], Qmon=None, Qsims=Qsimulado2)
plt.annotate(data_texto, xy=(1,1), xytext=(-4,100), fontsize=10,
             xycoords='axes fraction', textcoords='offset points',
             bbox=dict(facecolor='white', alpha=0.8),
             horizontalalignment='right', verticalalignment='top')
#fig.savefig('../Teste/prints/fiu_2020_manual.png', dpi = 300,
#             bbox_inches = 'tight')
