
import sys
sys.path.append('/home/bruno/github/modelos/')
import pandas as pd
import spotpy
import numpy as np
import matplotlib.pyplot as plt
import HydroErr as he
import funcoes_objetivo
import gr4j
import hymod
import sacramento
from matplotlib import gridspec
from spotpy.analyser import *
from spotpy.algorithms import sceua
from spotpy.parameter import Uniform
from plotar_hidro import plotar_hidro

class setup_sacramento(object):
    #UZTWM = Uniform(low=10, high=150)
    UZTWM = Uniform(low=32.496313384479365, high=32.496313384479365)
    #UZFWM = Uniform(low=10, high=75)
    UZFWM = Uniform(low=33.75650084208516, high=33.75650084208516)
    #LZTWM = Uniform(low=75, high=400)
    LZTWM=Uniform(low=118.14876592791606,high=118.14876592791606)
    #LZFSM = Uniform(low=10, high=300)
    LZFSM = Uniform(low=37.07446042127618, high=37.07446042127618)
    #LZFPM = Uniform(low=50, high=1000)
    LZFPM = Uniform(low=941.526246986471, high=941.526246986471)
    #UZK   = Uniform(low=0.2, high=0.4)
    UZK   = Uniform(low=0.26010702761760773, high=0.26010702761760773)
    #LZSK  = Uniform(low=0.020, high=0.250)
    LZSK  = Uniform(low=0.23265250576359764, high=0.23265250576359764)
    #LZPK  = Uniform(low=0.001, high=0.020)
    LZPK  = Uniform(low=0.00951492307831019, high=0.00951492307831019)
    PFREE = Uniform(low=0, high=0.6)
    #PFREE = Uniform(low=0.4055012014217911, high=0.4055012014217911)
    ZPERC = Uniform(low=5, high=250)
    #ZPERC = Uniform(low=180.22656808426035, high=180.22656808426035)
    REXP  = Uniform(low=1.1, high=4)
    #REXP  = Uniform(low=2.513628327347164, high=2.513628327347164)
    PCTIM = Uniform(low=0, high=0.1)
    #PCTIM = Uniform(low=0.0335690584170161, high=0.0335690584170161)
    ADIMP = Uniform(low=0, high=0.2)
    #ADIMP = Uniform(low=0.07288925887564152, high=0.07288925887564152)
    k     = Uniform(low=0.01, high=10)
    #k = Uniform(low=1, high=1)
    n     = Uniform(low=0.01, high=10)
    #n = Uniform(low=1, high=1)

    def __init__(self, area, PME, ETP, Qjus, Qmon=None, h_aq=0, fobj='KGE'):
        self.area = area
        self.PME  = PME
        self.ETP  = ETP
        self.Qjus = Qjus
        self.Qmon = Qmon
        self.h_aq = h_aq
        self.fobj = fobj

    def simulation(self, x):
        Qsim = sacramento.sacramento_nash(self.area, self.PME, self.ETP,  \
                            x[0], x[1], x[2], x[3], x[4], \
                            x[5], x[6], x[7], x[8], x[9], x[10], x[11], x[12], \
                            x[13], x[14], Qmon=self.Qmon)
        return Qsim

    def evaluation(self):
        Qobs = self.Qjus
        return Qobs

    def objectivefunction(self, simulation, evaluation):
        criterio = getattr(funcoes_objetivo, self.fobj)(simulation, evaluation, self.h_aq)
        fmin = 1 - criterio
        return fmin

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
spot_setup = setup_sacramento(area = area, PME = PME, ETP = ETP, Qjus = Qjus,
                              h_aq=180, fobj='NSE')
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
arq = open('/discolocal/bruno/Observado/Teste/bacia_fiu.peq')
area = float(arq.readline())
df = pd.read_csv('/discolocal/bruno/Observado/Teste/bacia_fiu.peq',
                 skiprows=[0], index_col = 'data', parse_dates = True)
PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()
idx = df.index.to_numpy()

##CALIBRACAO MANUAL
tipo_calib = 'CALIBRACAO MANUAL'
tipo_modelo = 'SACRAMENTO'
#calibracao nash
UZTWM=32.496313384479365
UZFWM=33.75650084208516
LZTWM=118.14876592791606
LZFSM=37.07446042127618
LZFPM=941.526246986471
UZK=0.26010702761760773
LZSK=0.23265250576359764
LZPK=0.00951492307831019
PFREE=0.3586677583632592
ZPERC=236.43878081332315
REXP=2.8680883773291184
PCTIM=0.03529309788158186
ADIMP=0.18701345689813623
k=0.6921226103309257
n=2.4187268870185195


Qsimulado = sacramento.sacramento_nash(area = area, PME = PME, ETP = ETP,
                    UZTWM = UZTWM, UZFWM = UZFWM, LZTWM = LZTWM, LZFSM = LZFSM,
                    LZFPM = LZFPM, UZK = UZK, LZSK = LZSK, LZPK = LZPK,
                    PFREE = PFREE, ZPERC = ZPERC, REXP = REXP, PCTIM = PCTIM,
                    ADIMP = ADIMP, k = k, n = n, Qmon=None, RIVA=0, SIDE=0,
                    RSERV=0.3)
df['qsim_auto'] = Qsimulado

##CALIBRACAO SACRAMENTO
tipo_calib2 = 'CALIBRACAO AUTOMATICA'
tipo_modelo2 = 'SACRAMENTO'
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



#df = df.loc['2020']

nash_auto = he.nse(df['qsim_auto'],df['qjus'])
nash_auto2 = he.nse(df['qsim_auto2'],df['qjus'])

print('SIMULACAO FIU' +
      '\n' + tipo_modelo + ' ' + tipo_calib + ' = ' + str(nash_auto) +
      '\n' + tipo_modelo2 + ' ' + tipo_calib2 + ' = ' + str(nash_auto2))
fig = plotar_hidro(idx=df.index, PME=df['pme'], ETP=df['etp'], Qobs=df['qjus'],
                   Qmon=None, Qsim=df['qsim_auto'], Qsim2=df['qsim_auto2'])
