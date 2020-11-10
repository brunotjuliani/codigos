
import sys
sys.path.append('/home/bruno/github/modelos/')
import spot_setup
import pandas as pd
import spotpy
import numpy as np
import gr4j
import matplotlib.pyplot as plt
import HydroErr as he
from matplotlib import gridspec
from spotpy.analyser import *
from spotpy.algorithms import sceua
from plotar_hidro import plotar_hidro

# Leitura das forcantes
arq = open('/discolocal/bruno/Observado/Teste/apucaraninha_montante.peq')
area = float(arq.readline())
df = pd.read_csv('/discolocal/bruno/Observado/Teste/apucaraninha_montante.peq',
                 skiprows=[0], index_col = 'data', parse_dates = True)
df = df.loc['2016-07-08':]
PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()
idx = df.index.to_numpy()

### CALIBRAR
spot_setup = spot_setup.setup_gr4j_nash(area, PME, ETP, Qjus, h_aq=365, fobj='LSE')
sampler = sceua(spot_setup)
sampler.sample(5000, ngs=10, kstop=3, peps=0.1, pcento=0.1)
results = sampler.getdata()
params = get_best_parameterset(results,maximize=False)
bestindex, bestobjf = get_minlikeindex(results)
simulation_fields = get_simulation_fields(results)
Qsim = {}
Qsim['best_NSE'] = list(results[simulation_fields][bestindex][0])

# Plotagem
fig = plotar_hidro(idx=df.index, PME=PME, ETP=ETP, Qobs=Qjus, Qmon=None, Qsim=Qsim['best_NSE'])

arq = open('/discolocal/bruno/Observado/Teste/apucaraninha_montante.peq')
area = float(arq.readline())
df = pd.read_csv('/discolocal/bruno/Observado/Teste/apucaraninha_montante.peq',
                 skiprows=[0], index_col = 'data', parse_dates = True)
df = df.loc['2016-07-08':]
PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()
idx = df.index.to_numpy()
x1 = 1199.59
x2 = 2.98
x3 = 197.49
x4 = 1.53
k = 0.49
n = 0.52
Qsimulado = gr4j.gr4j_nash(area=area, PME = PME, ETP = ETP, x1 = x1, x2 = x2,
                           x3 = x3, x4 = x4, k = k, n = n)
df['qsim'] = Qsimulado
nash = he.nse(df['qsim'][365:],df['qjus'][365:])
kge_2009 = he.kge_2009(df['qsim'][365:],df['qjus'][365:])
kge_2009
kge_2012 = he.kge_2012(df['qsim'][365:],df['qjus'][365:])
kge_2012
print('SIMULACAO BEST KGE' +
      '\nNash = ' + str(nash) +
      '\nKGE-2009 = ' + str(kge_2009) +
      '\nKGE-2012 = ' + str(kge_2012))
fig = plotar_hidro(idx=df.index, PME=PME, ETP=ETP, Qobs=df['qjus'],
                   Qmon=None, Qsim=df['qsim'])


#HYMOD
# Leitura das forcantes
arq = open('/discolocal/bruno/Observado/Teste/apucaraninha_montante.peq')
area = float(arq.readline())
df = pd.read_csv('/discolocal/bruno/Observado/Teste/apucaraninha_montante.peq',
                 skiprows=[0], index_col = 'data', parse_dates = True)
df = df.loc['2016-07-08':]
PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()
idx = df.index.to_numpy()

### CALIBRAR
spot_setup = spot_setup.hymod_teste(area, PME, ETP, Qjus)
sampler = sceua(spot_setup)
sampler.sample(5000, ngs=10, kstop=3, peps=0.1, pcento=0.1)
results = sampler.getdata()
params = get_best_parameterset(results,maximize=False)
bestindex, bestobjf = get_minlikeindex(results)
simulation_fields = get_simulation_fields(results)
Qsim = {}
Qsim['best_NSE'] = list(results[simulation_fields][bestindex][0])
