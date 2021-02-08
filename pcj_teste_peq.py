import sys
sys.path.append('../modelos/')
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from plotar_hidro import plotar_hidro
import matplotlib.pyplot as plt
import gr5i
import gr4j
import HydroErr as he


#Leitura das forçantes do modelo
arq = open('../dados/peq/bacia_274.peq')
areainc = float(arq.readline())
area = areainc
df = pd.read_csv('../dados/peq/bacia_274.peq', skiprows=[0],
                 index_col = 'data', parse_dates = True)

PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()
Qmon = df['qmon'].to_numpy()

df2 = df

##MODELO GR5i ##
dt = 24
# x1 = 66.7096
# x2 = -4.06384
# x3 = 295.446
# x4 = 1.7053
# x5 = 0.384637
x1 = 982.846
x2 = 0.22241
x3 = 17.7265
x4 = 2.56303
x5 = 0.1


resultado = gr5i.gr5i(dt=dt, area=area, PME=PME, ETP=ETP, Qmon=Qmon,
                      x1=x1, x2=x2, x3=x3, x4=x4, x5=x5)
df['q_gr5'] = pd.DataFrame(resultado, index=df.index)


## MODELO GR4J ##

#calibracao nash
x1 = 982.846
x2 = 1.22241
x3 = 17.7265
x4 = 2.56303
resultado = gr4j.gr4j(area=area, PME = PME, ETP = ETP, Qmon=Qmon,
                      x1 = x1, x2 = x2, x3 = x3, x4 = x4)
df['q_gr4'] = pd.DataFrame(resultado, index=df.index)


df2 = df.loc['2017']

Qsimulado2 = df2[['q_gr5', 'q_gr4']]

nash_gr5 = he.nse(df2['q_gr5'],df2['qjus'])
print('Nash GR5i = ' + str(nash_gr5))
nash_gr4 = he.nse(df2['q_gr4'],df2['qjus'])
print('Nash GR4J = ' + str(nash_gr4))

kge_gr5 = he.kge_2012(df2['q_gr5'],df2['qjus'])
print('KGE GR5i = ' + str(kge_gr5))
kge_gr4 = he.kge_2012(df2['q_gr4'],df2['qjus'])
print('KGE GR4J = ' + str(kge_gr4))

# Plotagem
fig = plotar_hidro(idx=df2.index, PME=df2['pme'], ETP=df2['etp'],
                   Qobs=df2['qjus'], Qmon=df2['qmon'], Qsims=Qsimulado2)
#plt.show()
fig.savefig('../dados/gr_pcj/pcj_completo.png', dpi = 300,
             bbox_inches = 'tight')
