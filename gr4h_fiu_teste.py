import sys
sys.path.append('../modelos/')
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import gr4h
import sacramento2020 as sac
from plotar_hidro import plotar_hidro
import matplotlib.pyplot as plt
import HydroErr as he

#Leitura das forçantes do modelo
arq = open('../dados/peq/bacia_fiu.peq')
areainc = float(arq.readline())
area = areainc
df = pd.read_csv('../dados/peq/bacia_fiu.peq', skiprows=[0],
                 index_col = 'datahora_UTC', parse_dates = True)
df['qmon'] = 0
cmb = df['pme']
etp = df['etp']
qmont = df['qmon']
qobs = df['qjus']
Q0 = qobs[0]

PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()
Qmon = df['qmon'].to_numpy()

# ##MODELO SACRAMENTO AUTOMATICO##
# TZWM = 53.0693
# UZFWM = 33.8188
# LZTWM = 301.566
# LZFPM = 761.563
# LZFSM = 75.0766
# ADIMP = 0.043635
# PCTIM = 0.0509886
# PFREE = 0.473211
# UZK = 0.34619
# LZPK = 0.00100104
# LZSK = 0.022452
# ZPERC = 132.15
# REXP = 3.28576
# k = 6.05251
# n = 6.57516
# resultado = sac.simulacao(area=area, PME=PME, ETP=ETP, UZTWM=TZWM, UZFWM=UZFWM,
#                           LZTWM=LZTWM, LZFPM=LZFPM, LZFSM=LZFSM, ADIMP=ADIMP,
#                           PCTIM=PCTIM, PFREE=PFREE, UZK=UZK, LZPK=LZPK,
#                           LZSK=LZSK, ZPERC=ZPERC, REXP=REXP, k=k, n=n)
# df['q_sac'] = pd.DataFrame(resultado[2], index=df.index)


##MODELO GR4H AUTOMATICO##
x1 = 1498.88
x2 = 1.25387
x3 = 289.684
x4 = 3.84673
k = 4.10347
n = 3.95573
resultado = gr4h.gr4h_nash(area=area, PME=PME, ETP=ETP, Qmon=Qmon,
                      x1=x1, x2=x2, x3=x3, x4=x4, k=k, n=n)
df['q_gr4h'] = pd.DataFrame(resultado, index=df.index)

##MODELO GR4H MANUAL##
x1 =  1494.87
x2 = 0.179334
x3 = 355.515
x4 = 3.36178
k = 3.41246
n = 4.62699

# x1 = 1498.62
# x2 = 2
# x3 = 216.087
# x4 = 2.01744
# k = 2
# n = 4.13935

resultado = gr4h.gr4h_nash(area=area, PME=PME, ETP=ETP, Qmon=Qmon,
                      x1=x1, x2=x2, x3=x3, x4=x4, k=k, n=n)
df['q_manual'] = pd.DataFrame(resultado, index=df.index)

##CORTE DE TEMPO PARA NASH E PLOTAGEM##
df2 = df.loc['2015-12':'2016-01']

Qsimulado2 = df2[['q_manual', 'q_gr4h']]


nash_manual = he.nse(df2['q_manual'],df2['qjus'])
print('Nash GR4H Manual = ' + str(nash_manual))

nash_gr = he.nse(df2['q_gr4h'],df2['qjus'])
print('Nash GR4H = ' + str(nash_gr))

data_texto = (f'Nash GR4H Manual = {nash_manual:.2f}' + '\n' +
              f'Nash GR4H Auto = {nash_gr:.2f}')

# Plotagem
fig = plotar_hidro(idx=df2.index, PME=df2['pme'], ETP=df2['etp'],
                   Qobs=df2['qjus'], Qmon=None, Qsims=Qsimulado2)
plt.annotate(data_texto, xy=(1,1), xytext=(-4,100), fontsize=10,
             xycoords='axes fraction', textcoords='offset points',
             bbox=dict(facecolor='white', alpha=0.8),
             horizontalalignment='right', verticalalignment='top')
#fig.savefig('../Teste/prints/fiu_2020_manual.png', dpi = 300,
#             bbox_inches = 'tight')
