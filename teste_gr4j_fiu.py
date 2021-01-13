
import sys
sys.path.append('..//modelos/')
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
arq = open('../Teste/bacia_fiu.peq')
area = float(arq.readline())
df = pd.read_csv('../Teste/bacia_fiu.peq',
                 skiprows=[0], index_col = 'data', parse_dates = True)
#df = df.loc['2020']
PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()
idx = df.index.to_numpy()
df


#####---------------#####---------------#####---------------#####---------------
arq = open('../Teste/bacia_fiu.peq')
area = float(arq.readline())
df = pd.read_csv('../Teste/bacia_fiu.peq',
                 skiprows=[0], index_col = 'data', parse_dates = True)
PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()
idx = df.index.to_numpy()

#CALIBRACAO GR AUTOMATICA
tipo_calib = 'CALIBRACAO AUTOMATICA'
tipo_modelo = 'GR4J CABECEIRA'
#calibracao nash
x1=1497
x2=1.71
x3=107
x4=1.62
Qsimulado_auto = gr4j.gr4j(area=area, PME = PME, ETP = ETP, x1 = x1, x2 = x2,
                           x3 = x3, x4 = x4)
df['qsim_auto'] = Qsimulado_auto



##CALIBRACAO 01
tipo_calib = 'CALIBRACAO MANUAL 01'
x1=750
x2=1.53
x3=60
x4=1.0
Qsimulado_01 = gr4j.gr4j(area=area, PME = PME, ETP = ETP, x1 = x1, x2 = x2,
                           x3 = x3, x4 = x4)
df['qsim_01'] = Qsimulado_01

##CALIBRACAO KGE
tipo_calib2 = 'CALIBRACAO MANUAL 02'
x1=1363
x2=1.20
x3=52
x4=1.21
Qsimulado_02 = gr4j.gr4j(area=area, PME = PME, ETP = ETP, x1 = x1, x2 = x2,
                           x3 = x3, x4 = x4)
df['qsim_02'] = Qsimulado_02

df = df.loc['2020-06':'2020-07']
df2 = df[['qsim_auto', 'qsim_01', 'qsim_02']]

nash_auto = he.nse(df['qsim_auto'],df['qjus'])
print('Nash Calib. Automatica = ', nash_auto)

nash_01 = he.nse(df['qsim_01'],df['qjus'])
print('Nash Calib. Manual 01 = ', nash_01)

nash_02 = he.nse(df['qsim_02'],df['qjus'])
print('Nash Calib. Manual 02 = ', nash_02)



fig = plotar_hidro(idx=df.index, PME=df['pme'], ETP=df['etp'], Qobs=df['qjus'],
                   Qmon=None, Qsims=df2)
fig.savefig('../Teste/teste_calib_fiu_2020.png', dpi = 300,
            bbox_inches = 'tight')
