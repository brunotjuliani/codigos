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
arq = open('../dados/peq/bacia_01.peq')
area = float(arq.readline())
df = pd.read_csv('../dados/peq/bacia_01.peq', skiprows=[0],
                 index_col = 'datahora_UTC', parse_dates = True)
df = df.loc['2010':'2020']
PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()
idx = df.index.to_numpy()


### CALIBRAR
spot_setup = sac.spotpy(area = area, PME = PME, ETP = ETP, Qjus = Qjus,
                              h_aq=4520, fobj='NSE')
sampler = sceua(spot_setup)
sampler.sample(5000, ngs=10, kstop=3, peps=0.1, pcento=0.1)
results = sampler.getdata()
params = get_best_parameterset(results,maximize=False)
bestindex, bestobjf = get_minlikeindex(results)
simulation_fields = get_simulation_fields(results)
Qsim = {}
Qsim['best_NSE'] = list(results[simulation_fields][bestindex])


# Plotagem
fig = plotar_hidro(idx=df.index, PME=PME, ETP=ETP, Qobs=Qjus, Qmon=None,
                   Qsims=Qsim)
fig.savefig('../dados/peq/bacia_01.png', dpi = 300,
            bbox_inches = 'tight')

#Minimal objective value: 1.88585
#Best parameter set:
#UTZWM=56.58360674864332
#UZFWM=35.580001986855876
#LZTWM=78.85340743089148
#LZFPM=781.403493307761
#LZFSM=72.88056072756544
#ADIMP=0.12820809527236016
#PCTIM=0.0959405860061334
#PFREE=0.14750748723645518
#UZK=0.3024198894185668
#LZPK=0.012493614293406204
#LZSK=0.044529097826248656
#ZPERC=90.96501735957224
#REXP=2.2843797425788566
#k=8.994715632019345
#n=8.505781879112629
