import sys
sys.path.append('../modelos/')
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import gr4h
import sacramento_antigo as sac0
from plotar_hidro import plotar_hidro
import matplotlib.pyplot as plt
import HydroErr as he

#Leitura das forçantes do modelo
arq = open('../dados/peq/bacia_01.peq')
areainc = float(arq.readline())
area = areainc
df = pd.read_csv('../dados/peq/bacia_01.peq', skiprows=[0],
                 index_col = 'datahora_UTC', parse_dates = True)
df = df.loc['2010':'2020']
df['qmon'] = 0
cmb = df['pme']
etp = df['etp']
qmont = df['qmon']
qobs = df['qjus']
Q0 = qobs[0]

PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()
Qmon = df['qmon'].to_numpy()

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
# x1 = 908
# #x2 = 2.3
# x2 = 1.5
# x3 = 310
# x4 = 4.0
# k = 9.9
# n = 7

x1=570
x2=1.26
x3=304
x4=3.63
k=9.87
n=6


resultado = gr4h.gr4h_nash(area=area, PME=PME, ETP=ETP, Qmon=Qmon,
                      x1=x1, x2=x2, x3=x3, x4=x4, k=k, n=n)
df['q_sim'] = pd.DataFrame(resultado, index=df.index)


##CORTE DE TEMPO PARA NASH E PLOTAGEM##
df2 = df.loc['2020']

Qsimulado2 = df2[['q_sim', 'sim_ant']]


nash = he.nse(df2['q_sim'],df2['qjus'])
print('Nash = ' + str(nash))

nash_ant = he.nse(df2['sim_ant'],df2['qjus'])
print('Nash Antigo = ' + str(nash_ant))


# Plotagem
fig = plotar_hidro(idx=df2.index, PME=df2['pme'], ETP=df2['etp'],
                   Qobs=df2['qjus'], Qmon=None, Qsims=Qsimulado2)
fig.savefig('../dados/peq/teste_calib_bacia_01_full.png', dpi = 300,
            bbox_inches = 'tight')


##CORTE DE TEMPO PARA NASH E PLOTAGEM##
df2015 = df.loc['2015']
Qsimulado2015 = df2015[['q_sim', 'sim_ant']]
nash2015 = he.nse(df2015['q_sim'],df2015['qjus'])
print('Nash 2015 = ' + str(nash2015))
nash_ant2015 = he.nse(df2015['sim_ant'],df2015['qjus'])
print('Nash Antigo 2015 = ' + str(nash_ant2015))
# Plotagem
fig2015 = plotar_hidro(idx=df2015.index, PME=df2015['pme'], ETP=df2015['etp'],
                   Qobs=df2015['qjus'], Qmon=None, Qsims=Qsimulado2015)
fig2015.savefig('../dados/peq/teste_calib_bacia_01_2015.png', dpi = 300,
            bbox_inches = 'tight')

df2016 = df.loc['2016']
Qsimulado2016 = df2016[['q_sim', 'sim_ant']]
nash2016 = he.nse(df2016['q_sim'],df2016['qjus'])
print('Nash 2016 = ' + str(nash2016))
nash_ant2016 = he.nse(df2016['sim_ant'],df2016['qjus'])
print('Nash Antigo 2016 = ' + str(nash_ant2016))
# Plotagem
fig2016 = plotar_hidro(idx=df2016.index, PME=df2016['pme'], ETP=df2016['etp'],
                   Qobs=df2016['qjus'], Qmon=None, Qsims=Qsimulado2016)
fig2016.savefig('../dados/peq/teste_calib_bacia_01_2016.png', dpi = 300,
            bbox_inches = 'tight')

df2017 = df.loc['2017']
Qsimulado2017 = df2017[['q_sim', 'sim_ant']]
nash2017 = he.nse(df2017['q_sim'],df2017['qjus'])
print('Nash 2017 = ' + str(nash2017))
nash_ant2017 = he.nse(df2017['sim_ant'],df2017['qjus'])
print('Nash Antigo 2017 = ' + str(nash_ant2017))
# Plotagem
fig2017 = plotar_hidro(idx=df2017.index, PME=df2017['pme'], ETP=df2017['etp'],
                   Qobs=df2017['qjus'], Qmon=None, Qsims=Qsimulado2017)
fig2017.savefig('../dados/peq/teste_calib_bacia_01_2017.png', dpi = 300,
            bbox_inches = 'tight')

df2018 = df.loc['2018']
Qsimulado2018 = df2018[['q_sim', 'sim_ant']]
nash2018 = he.nse(df2018['q_sim'],df2018['qjus'])
print('Nash 2018 = ' + str(nash2018))
nash_ant2018 = he.nse(df2018['sim_ant'],df2018['qjus'])
print('Nash Antigo 2018 = ' + str(nash_ant2018))
# Plotagem
fig2018 = plotar_hidro(idx=df2018.index, PME=df2018['pme'], ETP=df2018['etp'],
                   Qobs=df2018['qjus'], Qmon=None, Qsims=Qsimulado2018)
fig2018.savefig('../dados/peq/teste_calib_bacia_01_2018.png', dpi = 300,
            bbox_inches = 'tight')

df2019 = df.loc['2019']
Qsimulado2019 = df2019[['q_sim', 'sim_ant']]
nash2019 = he.nse(df2019['q_sim'],df2019['qjus'])
print('Nash 2019 = ' + str(nash2019))
nash_ant2019 = he.nse(df2019['sim_ant'],df2019['qjus'])
print('Nash Antigo 2019 = ' + str(nash_ant2019))
# Plotagem
fig2019 = plotar_hidro(idx=df2019.index, PME=df2019['pme'], ETP=df2019['etp'],
                   Qobs=df2019['qjus'], Qmon=None, Qsims=Qsimulado2019)
fig2019.savefig('../dados/peq/teste_calib_bacia_01_2019.png', dpi = 300,
            bbox_inches = 'tight')

df2020 = df.loc['2020']
Qsimulado2020 = df2020[['q_sim', 'sim_ant']]
nash2020 = he.nse(df2020['q_sim'],df2020['qjus'])
print('Nash 2020 = ' + str(nash2020))
nash_ant2020 = he.nse(df2020['sim_ant'],df2020['qjus'])
print('Nash Antigo 2020 = ' + str(nash_ant2020))
# Plotagem
fig2020 = plotar_hidro(idx=df2020.index, PME=df2020['pme'], ETP=df2020['etp'],
                   Qobs=df2020['qjus'], Qmon=None, Qsims=Qsimulado2020)
fig2020.savefig('../dados/peq/teste_calib_bacia_01_2020.png', dpi = 300,
            bbox_inches = 'tight')
