#############################################################################
# DEFINICOES
#############################################################################
import pandas as pd
import datetime as dt
import numpy as np
from scipy.stats import gamma, expon
posto = 'uniao_da_vitoria'


################################################################################
# FUNCOES
################################################################################
def thresholds(srq, percs):
    tuplas_idx = list(zip(srq.index.month, srq.index.day))
    cols = ['q'+str(i) for i in percs]
    df_qrefs = pd.DataFrame(columns=['mes','dia'] + cols)
    df_qrefs.index.names = ['dia_juliano']
    for t in pd.date_range(dt.date(1900,1,1), dt.date(1900,12,31)):
        janela = pd.date_range(t - dt.timedelta(days=15), t + dt.timedelta(days=15))
        tuplas_janela = list(zip(janela.month, janela.day))
        idx_t = [ i in tuplas_janela for i in tuplas_idx ]
        linha = [t.month, t.day]
        for perc in percs:
            q = np.percentile(srq.loc[idx_t].to_numpy(),100-perc)
            linha.append(round(q,2))
        df_qrefs.loc[t.dayofyear,:] = linha
    return df_qrefs

################################################################################
# ALGORITMO
################################################################################

print('Processando {}'.format(posto))
# 1 - Aquisicao da serie de vazoes do posto
srq = pd.read_csv('../dados/{}_completo.csv'.format(posto)
        , parse_dates=True, index_col='data')['q_m3s']

# 2 - Calculo das vazoes de referencia (thresholds)
percs = range(100)
df_qrefs = thresholds(srq, percs)
df_qrefs.to_csv('../dados/{}_quantis.csv'.format(posto))

# 3 - Calculo do percentil atual
ontem = srq.index[-1]
if (ontem.month==2) & (ontem.day==29):
    diadoano=df_qrefs[(df_qrefs["mes"]==2) & (df_qrefs['dia']==28)]
else:
    diadoano =df_qrefs[(df_qrefs["mes"]==ontem.month) & (df_qrefs['dia']==ontem.day)]
diadoano2 = diadoano.drop(['mes', 'dia'], axis=1)

for q in diadoano2.columns:
    if (diadoano2.loc[:,q].values[0] > srq[-1]):
        continue
    if (diadoano2.loc[:,q].values[0] <= srq[-1]):
        valor_referencia = diadoano2.loc[:,'q95'].values[0]
        print('Vazao atual = ', str(srq[-1]), ' m3/s\n',
              'Excedencia (q%) = ', q, '\n',
              'Vazao de referencia (q95)= ', str(valor_referencia), 'm3/s')
        break


# 4 - Criacao do DataFrame contendo os deficits e qrefs de cada intervalo
df_deficits = srq.to_frame()
qref=95
qref = 'q{}'.format(qref)
df_deficits[qref] = df_deficits.apply(lambda x:
                    df_qrefs.loc[(df_qrefs['mes']==x.name.month)&
                    (df_qrefs['dia']==x.name.day),qref].values[0]
                    if x.name.day != 29 else
                    df_qrefs.loc[(df_qrefs['mes']==x.name.month)&
                    (df_qrefs['dia']==28),qref].values[0], axis=1)
df_deficits['di'] = df_deficits[qref] - df_deficits['q_m3s']
df_deficits['q50'] = df_deficits.apply(lambda x:
                    df_qrefs.loc[(df_qrefs['mes']==x.name.month)&
                    (df_qrefs['dia']==x.name.day),'q50'].values[0]
                    if (x.name.month != 2) & (x.name.day != 29) else
                    df_qrefs.loc[(df_qrefs['mes']==x.name.month)&
                    (df_qrefs['dia']==28),'q50'].values[0], axis=1)

df_deficits


df_deficits.to_csv('../dados-saida/{}_serie.csv'.format(posto))
