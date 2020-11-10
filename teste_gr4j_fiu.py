
import sys
sys.path.append('/home/bruno/github/modelos/')
import spot_setup
import pandas as pd
import spotpy
import numpy as np
import gr4j
import sacramento
import hymod
import matplotlib.pyplot as plt
import HydroErr as he
from matplotlib import gridspec
from spotpy.analyser import *
from spotpy.algorithms import sceua
from plotar_hidro import plotar_hidro

# Leitura das forcantes
arq = open('/discolocal/bruno/Observado/Teste/bacia_fiu.peq')
area = float(arq.readline())
df = pd.read_csv('/discolocal/bruno/Observado/Teste/bacia_fiu.peq',
                 skiprows=[0], index_col = 'data', parse_dates = True)
#df = df.loc['2020']
PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()
idx = df.index.to_numpy()

### CALIBRAR
spot_setup = spot_setup.setup_sacramento(area = area, PME = PME, ETP = ETP,
                                             Qjus = Qjus, h_aq=180, fobj='NSE')
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

#####---------------#####---------------#####---------------#####---------------

#####---------------#####---------------#####---------------#####---------------

# arq = open('/discolocal/bruno/Observado/Teste/bacia_fiu.peq')
# area = float(arq.readline())
# df = pd.read_csv('/discolocal/bruno/Observado/Teste/bacia_fiu.peq',
#                  skiprows=[0], index_col = 'data', parse_dates = True)
# PME = df['pme'].to_numpy()
# ETP = df['etp'].to_numpy()
# Qjus = df['qjus'].to_numpy()
# idx = df.index.to_numpy()
#
# tipo_calib = 'CALIBRACAO AUTOMATICA'
# tipo_modelo = 'HYMOD'
# cmax=438.45746561527324
# bexp=0.23003730393937155
# alpha=0.33632717076940544
# Rs=0.012351725032362048
# Rq=0.6618310537529434
# k=3.4582317170538985
# n=0.27960124032773115
#
# Qsimulado = hymod.hymod_nash(area = area, Precip = PME, PET = ETP, cmax = cmax,
#                              bexp = bexp, alpha = alpha, Rs = Rs, Rq = Rq,
#                              k = k, n = n, Qmon=None)
# df['qsim'] = Qsimulado
# nash = he.nse(df['qsim'][365:],df['qjus'][365:])
# kge_2009 = he.kge_2009(df['qsim'][365:],df['qjus'][365:])
# kge_2009
# kge_2012 = he.kge_2012(df['qsim'][365:],df['qjus'][365:])
# kge_2012
# print('SIMULACAO FIU' +
#       '\n' + tipo_calib +
#       '\n' + tipo_modelo +
#       '\nNash = ' + str(nash) +
#       '\nKGE-2009 = ' + str(kge_2009) +
#       '\nKGE-2012 = ' + str(kge_2012))
# fig = plotar_hidro(idx=df.index, PME=PME, ETP=ETP, Qobs=df['qjus'],
#                    Qmon=None, Qsim=df['qsim'])


#####---------------#####---------------#####---------------#####---------------
arq = open('/discolocal/bruno/Observado/Teste/bacia_fiu.peq')
area = float(arq.readline())
df = pd.read_csv('/discolocal/bruno/Observado/Teste/bacia_fiu.peq',
                 skiprows=[0], index_col = 'data', parse_dates = True)
PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()
idx = df.index.to_numpy()

##CALIBRACAO GERAL
tipo_calib = 'CALIBRACAO AUTOMATICA'
tipo_modelo = 'GR4J CABECEIRA'
#calibracao nash
x1=1497
x2=1.71
x3=107
x4=1.62

# #picos cheias
# x1=1363
# x2=1.20
# x3=52
# x4=1.21
Qsimulado = gr4j.gr4j(area=area, PME = PME, ETP = ETP, x1 = x1, x2 = x2,
                           x3 = x3, x4 = x4)
df['qsim_auto'] = Qsimulado

##CALIBRACAO SACRAMENTO
tipo_calib = 'CALIBRACAO AUTOMATICA'
tipo_modelo = 'SACRAMENTO'
#calibracao nash
UZTWM = 67.35561585313553
UZFWM = 46.49076023113198
LZTWM = 108.52822928348942
LZFSM = 131.7976977056543
LZFPM = 935.7724280949543
UZK = 0.28475381808434785
LZSK = 0.1739609266459105
LZPK = 0.008091203322176218
PFREE = 0.43073101444253814
ZPERC = 27.914896239755194
REXP = 2.455054545586011
PCTIM = 0.07966861009792477
ADIMP = 0.05599504554449504
k = 0.9025977944095924
n = 1.69397002081278


Qsimulado2 = sacramento.sacramento_nash(area = area, PME = PME, ETP = ETP,
                    UZTWM = UZTWM, UZFWM = UZFWM, LZTWM = LZTWM, LZFSM = LZFSM,
                    LZFPM = LZFPM, UZK = UZK, LZSK = LZSK, LZPK = LZPK,
                    PFREE = PFREE, ZPERC = ZPERC, REXP = REXP, PCTIM = PCTIM,
                    ADIMP = ADIMP, k = k, n = n, Qmon=None, RIVA=0, SIDE=0,
                    RSERV=0.3)
df['qsim_auto2'] = Qsimulado2

# ##CALIBRACAO GR PICOS
# tipo_calib = 'CALIBRACAO AUTOMATICA'
# tipo_modelo = 'GR4J CABECEIRA'
# x1=750
# x2=1.53
# x3=60
# x4=1.0
# Qsimulado2 = gr4j.gr4j_cabeceira(area=area, PME = PME, ETP = ETP, x1 = x1, x2 = x2,
#                            x3 = x3, x4 = x4)
# df['qsim_auto2'] = Qsimulado2

# ##CALIBRACAO KGE
# tipo_calib2 = 'CALIBRACAO AUTOMATICA'
# tipo_modelo2 = 'GR4J CABECEIRA'
# x1=1363
# x2=1.20
# x3=52
# x4=1.21
# Qsimulado2 = gr4j.gr4j(area=area, PME = PME, ETP = ETP, x1 = x1, x2 = x2,
#                            x3 = x3, x4 = x4)
# df['qsim_auto2'] = Qsimulado2


df = df.loc['2020']

nash_auto = he.nse(df['qsim_auto'],df['qjus'])
nash_auto2 = he.nse(df['qsim_auto2'],df['qjus'])

print('SIMULACAO FIU' +
      '\nNash GR4J - Automatico = ' + str(nash_auto) +
      '\nNash Sacramento - Automatico = ' + str(nash_auto2))
fig = plotar_hidro(idx=df.index, PME=df['pme'], ETP=df['etp'], Qobs=df['qjus'],
                   Qmon=None, Qsim=df['qsim_auto'], Qsim2=df['qsim_auto2'])
fig.savefig('/discolocal/bruno/Observado/Teste/2020_completo.png')
