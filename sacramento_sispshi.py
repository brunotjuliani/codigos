import sys
sys.path.append('../modelos/')
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sacramento2020 as sac
import sacramento_antigo as sac0
from plotar_hidro import plotar_hidro
import HydroErr as he

#Leitura das forçantes do modelo
arq = open('../dados/peq/bacia_01.peq')
areainc = float(arq.readline())
area = areainc
df = pd.read_csv('../dados/peq/bacia_01.peq', skiprows=[0],
                 index_col = 'datahora_UTC', parse_dates = True)
df = df.loc['2019':'2020']
df['qmon'] = 0
cmb = df['pme']
etp = df['etp']
qmont = df['qmon']
qobs = df['qjus']
Q0 = qobs[0]

PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()

##MODELO ANTIGO##

codigo = 26064948
nome = 'Rio Negro'
Hmed = 1.84
Hdp = 1.46
Hmax = 13.10
Hmin = 0.15
DH15M = 0.27
DH60M = 0.34
NDAC = 25
Qmed = 76.1
Qdp = 70.9
Qmax = 712.0
Qalta2 = 106.9
Qbaixa2 = 32.2
Qmin = 11.2
DQ15M = 10.0
DQ60M = 15.2


# Ordem obrigatória dos parâmetros:
# param[0] =  UZWM: capacidade máxima de armazenamento da camada superior do solo (mm);
# param[1] =  LZWM: capacidade máxima de armazenamento da camada inferior do solo (mm);
# param[2] =   UZK: taxa de transferência lateral da camada superior do solo (%/dia);
# param[3] =   LZK: taxa de transferência lateral da camada inferior do solo (%/dia);
# param[4] = ZPERC: coeficiente da equação de percolação (adim.);
# param[5] =  IMPX: expoente da equação de escoamento direto proveniente da área impermeável (adim.);
# param[6] =  REXP: expoente da equação de percolação (adim.);
# param[7] =  TRNX: expoente da equação para cálculo da transpiração (adim.)
# param[8] =  SIDE: fração do escoamento subterrâneo que chega ao canal (%);
# param[9] =  beta: fração do volume do reservatório de canal que escoa por passo de tempo (%);
# param[10]=   NRC: número de reservatórios conceituais (inteiro).

PARAM1 = { 1:
             {'MEDIA':
                      { 1: [ 206.540,  189.260, 0.18190, 0.01160, 297.000, 5.99990, 1.00010, 4.22680, 1.00000, 0.03831,  4],
                        2: [ 458.980,  817.550, 0.10000, 0.00280, 794.140, 0.55370, 1.02500, 0.91850, 0.81350, 0.04260, 15],
                        3: [ 423.990,  718.830, 0.10000, 0.00650, 620.500, 5.88330, 1.00070, 1.27730, 0.35840, 0.11435, 15],
                        4: [ 157.210,  204.720, 0.21170, 0.00770, 899.140, 5.99910, 2.67440, 1.04060, 1.00000, 0.02650,  3],
                        5: [ 237.480,  264.290, 0.15020, 0.00460, 893.100, 5.99940, 1.00000, 5.98900, 0.00010, 0.04628,  4],
                        6: [ 348.050,   94.550, 0.10730, 0.03300, 772.090, 1.71650, 4.57060, 0.14750, 0.78960, 0.22610, 15],
                        7: [ 118.740,   39.300, 0.18880, 0.19970, 801.070, 5.81300, 1.00030, 0.91950, 0.11880, 0.21294, 15],
                        8: [ 189.890,  178.510, 0.14480, 0.00790, 899.700, 5.99750, 1.11680, 3.66210, 0.99990, 0.04945,  4],
                        9: [ 100.930,  698.510, 0.26160, 0.00120, 819.900, 2.12060, 4.34020, 0.70760, 1.00000, 0.00730,  1],
                       10: [ 164.040,  197.660, 0.22130, 0.00910, 899.860, 5.98870, 3.06970, 1.07110, 1.00000, 0.03302,  4]
                      }}}

# Tríade de conjuntos de parâmetros para cada classe de vazão
aux = [ PARAM1[1]['MEDIA'][5],
        PARAM1[1]['MEDIA'][6],
        PARAM1[1]['MEDIA'][7]]
parametros = aux[:]

# Lista das variáveis datahora do período de modelagem
t = df.index[0]
tN = df.index[-1]
datas = []
while t <= tN:
    datas.append(t)
    t += timedelta(hours = 1)

# Simulação com parâmetros para vazão alta
estados = [parametros[0][0]*0.5, parametros[0][1]*0.5]
aux = Q0 * 3600 / parametros[0][9]
for i in range(parametros[0][10]):
    estados.append(aux)
Qalta = sac0.ExecutaSACSIMPLES(parametros[0], datas, etp, cmb, qmont, areainc,
                          estados)

# Simulação com parâmetros para vazão média
estados = [parametros[1][0]*0.5, parametros[1][1]*0.5]
aux = Q0 * 3600 / parametros[1][9]
for i in range(parametros[1][10]):
    estados.append(aux)
Qmedia = sac0.ExecutaSACSIMPLES(parametros[1], datas, etp, cmb, qmont, areainc,
                           estados)


# Simulação com parâmetros para vazão baixa
estados = [parametros[2][0]*0.5, parametros[2][1]*0.5]
aux = Q0 * 3600 / parametros[2][9]
for i in range(parametros[2][10]):
    estados.append(aux)
Qbaixa = sac0.ExecutaSACSIMPLES(parametros[2], datas, etp, cmb, qmont, areainc,
                           estados)

# Vazão modelada com ponderação pela classe da vazão
Qmod = sac0.Fracionamento(datas, qobs, Qalta, Qmedia, Qbaixa, Qbaixa2, Qmin,
                          Qalta2)
del Qalta, Qmedia, Qbaixa, estados
df['sim_ant'] = pd.DataFrame.from_dict(Qmod, orient = 'index')
Qsimulado = df[['sim_ant']]


##MODELO CALIBRACAO##

# TZWM = 16.748
# UZFWM = 59.2835
# LZTWM = 135.795
# LZFPM = 916.621
# LZFSM = 42.7809
# ADIMP = 0.023229
# PCTIM = 0.0566524
# PFREE = 0.441261
# UZK = 0.283859
# LZPK = 0.00270224
# LZSK = 0.0475308
# ZPERC = 131.84
# REXP = 2.35218
# k = 9.83349
# n = 9.09199
TZWM= 14.4217
UZFWM= 47.6533
LZTWM= 189.411
LZFPM= 787.69
LZFSM= 16.8398
ADIMP= 0.0891221
PCTIM= 0.0610251
PFREE= 0.402377
UZK= 0.263238
LZPK= 0.00214846
LZSK= 0.0492473
ZPERC= 146.337
REXP= 2.25878
k= 8.20777
n= 9.60026


resultado = sac.simulacao(area=area, PME=PME, ETP=ETP, UZTWM=TZWM, UZFWM=UZFWM,
                          LZTWM=LZTWM, LZFPM=LZFPM, LZFSM=LZFSM, ADIMP=ADIMP,
                          PCTIM=PCTIM, PFREE=PFREE, UZK=UZK, LZPK=LZPK,
                          LZSK=LZSK, ZPERC=ZPERC, REXP=REXP, k=k, n=n)

df['q_sim'] = pd.DataFrame(resultado[2], index=df.index)


#CALIBRACAO MANUAL#

TZWM= 36.2586
UZFWM= 44.9155
LZTWM= 50
LZFPM= 600
LZFSM= 50
ADIMP= 0.00322059
PCTIM= 0.05
PFREE= 0.371737
UZK= 0.527345
LZPK= 0.000372
LZSK= 0.022755
ZPERC= 153.023
REXP= 1.39687
k= 4.38886
n= 7.39993

resultado2014 = sac.simulacao(area=area, PME=PME, ETP=ETP, UZTWM=TZWM, UZFWM=UZFWM,
                          LZTWM=LZTWM, LZFPM=LZFPM, LZFSM=LZFSM, ADIMP=ADIMP,
                          PCTIM=PCTIM, PFREE=PFREE, UZK=UZK, LZPK=LZPK,
                          LZSK=LZSK, ZPERC=ZPERC, REXP=REXP, k=k, n=n)

df['sim_manual'] = pd.DataFrame(resultado2014[2], index=df.index)

##CORTE DE TEMPO PARA NASH E PLOTAGEM##
df2 = df.loc['2019']
#Qsimulado2 = df2[['sim_ant', 'q_sim', 'sim_manual']]
Qsimulado2 = df2[['sim_ant', 'sim_manual']]


nash_ant = he.nse(df2['sim_ant'],df2['qjus'])
print('Nash antigo = ' + str(nash_ant))

nash_novo = he.nse(df2['q_sim'],df2['qjus'])
print('nash calibracao = ' + str(nash_novo))


# Plotagem
fig = plotar_hidro(idx=df2.index, PME=df2['pme'], ETP=df2['etp'],
                   Qobs=df2['qjus'], Qmon=None, Qsims=Qsimulado2)
#fig.savefig('../dados/peq/teste_calib_bacia_01.png', dpi = 300,
#            bbox_inches = 'tight')
