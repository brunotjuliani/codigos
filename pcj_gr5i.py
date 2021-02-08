import sys
sys.path.append('../modelos/')
import pandas as pd
import numpy as np
import funcoes_objetivo
import gr5i
from spotpy.analyser import *
from spotpy.algorithms import sceua
from spotpy.parameter import Uniform
from plotar_hidro import plotar_hidro

# Leitura das forcantes
arq = open('../dados/peq/bacia_274.peq')
area = float(arq.readline())
df = pd.read_csv('../dados/peq/bacia_274.peq', skiprows=[0],
                 index_col = 'data', parse_dates = True)
#df = df.loc['2019':'2020']
Qmon = df['qmon'].to_numpy()
PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()
idx = df.index.to_numpy()
dt = 24

### CALIBRAR
spot_setup = gr5i.spot_setup(dt = dt, area = area, PME = PME, ETP = ETP, Qjus = Qjus, Qmon = Qmon, h_aq=360, fobj='NSE')
sampler = sceua(spot_setup)
sampler.sample(5000, ngs=10, kstop=3, peps=0.1, pcento=0.1)
results = sampler.getdata()
params = get_best_parameterset(results,maximize=False)
bestindex, bestobjf = get_minlikeindex(results)
simulation_fields = get_simulation_fields(results)
Qsim = {}
Qsim['best_NSE'] = list(results[simulation_fields][bestindex])



# Plotagem
fig = plotar_hidro(idx=df.index, PME=PME, ETP=ETP, Qobs=Qjus, Qmon=Qmon,
                   Qsims=Qsim)
fig.savefig('../dados/peq/bacia_274_gr5i.png', dpi = 300,
            bbox_inches = 'tight')
