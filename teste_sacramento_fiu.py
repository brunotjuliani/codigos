import sys
sys.path.append('../modelos/')
import pandas as pd
import numpy as np
import funcoes_objetivo
import sacramento2020 as sac
from spotpy.analyser import *
from spotpy.algorithms import sceua
from spotpy.parameter import Uniform
from plotar_hidro import plotar_hidro

# Leitura das forcantes
#arq = open('/discolocal/bruno/Observado/Teste/bacia_fiu.peq')
arq = open('../dados/bacia_fiu.peq')
area = float(arq.readline())
#df = pd.read_csv('/discolocal/bruno/Observado/Teste/bacia_fiu.peq',
#                 skiprows=[0], index_col = 'data', parse_dates = True)
df = pd.read_csv('../dados/bacia_fiu.peq', skiprows=[0], index_col = 'data',
                 parse_dates = True)

PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()
idx = df.index.to_numpy()

### CALIBRAR
spot_setup = sac.spotpy(area = area, PME = PME, ETP = ETP, Qjus = Qjus,
                              h_aq=180, fobj='NSE')
sampler = sceua(spot_setup)
sampler.sample(10, ngs=10, kstop=3, peps=0.1, pcento=0.1)
results = sampler.getdata()
params = get_best_parameterset(results,maximize=False)
bestindex, bestobjf = get_minlikeindex(results)
simulation_fields = get_simulation_fields(results)
Qsim = {}
Qsim['best_NSE'] = list(results[simulation_fields][bestindex])


# Plotagem
fig = plotar_hidro(idx=df.index, PME=PME, ETP=ETP, Qobs=Qjus, Qmon=None,
                   Qsims=Qsim)
fig.savefig('../dados/teste.png', dpi = 300,
            bbox_inches = 'tight')
