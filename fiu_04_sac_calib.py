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
arq = open('/discolocal/bruno/Fiu/peq_Fiu_6hrs.csv')
area = float(arq.readline())
df = pd.read_csv('/discolocal/bruno/Fiu/peq_Fiu_6hrs.csv', skiprows=[0],
                 index_col = 'datahora_UTC', parse_dates = True)
#df = df.loc['2019':'2020']
df['qmon'] = 0
Qmon = df['qmon'].to_numpy()
PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()
idx = df.index.to_numpy()
dt = 6



### CALIBRAR
spot_setup = sac.spot_setup(dt = dt, area = area, PME = PME, ETP = ETP, Qjus = Qjus, Qmon = Qmon, h_aq=360, fobj='NSE')
sampler = sceua(spot_setup)
sampler.sample(5000, ngs=10, kstop=3, peps=0.1, pcento=0.1)
results = sampler.getdata()
params = get_best_parameterset(results,maximize=False)
bestindex, bestobjf = get_minlikeindex(results)
simulation_fields = get_simulation_fields(results)
Qsim = {}
Qsim['best_NSE'] = list(results[simulation_fields][bestindex])
