import sys
sys.path.append('/home/bruno/github/modelos_arlan/gr4j/')

import pandas as pd
import numpy as np
import HydroErr as he
import spotpy
import gr4j

arq = open('/discolocal/bruno/Observado/Teste/Reservatorio_Fiu.peq')
area = float(arq.readline())
area
df = pd.read_csv('/discolocal/bruno/Observado/Teste/Reservatorio_Fiu.peq',
                 skiprows=1)
df = df.dropna()
idx = df['data']
PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qobs = df['qjus'].to_numpy()

x1 = 5000
x2 = 0.1
x3 = 1850
x4 = 2.3
# fconv
Qsim = gr4j.sim(PME, ETP, area, x1, x2, x3, x4)

nash = he.nse(Qsim, Qobs)
print('Nash = ' + str(nash))

import matplotlib.pyplot as plt
plt.plot(idx, Qobs)
plt.plot(idx, Qsim)
plt.show()
