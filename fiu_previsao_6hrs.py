import pandas as pd
import numpy as np
import csv
import sys
import datetime as dt
import pytz
sys.path.append('../modelos/')
from plotar_hidro import plotar_hidro


bacia = 'XX'
nome = 'Fiu'
area = 534

## DIA DISPARO (MODIFICAR PARA DATETIME TODAY)
hoje = dt.date.today()
ano = hoje.year
mes = hoje.month
dia = hoje.day
dispara = dt.datetime(ano, mes, dia,  00)
t_ini = dispara - dt.timedelta(days=365)
t_fim = dispara + dt.timedelta(days=5)

#cria DF padrao horario para ser preenchido com os dados
date_rng_horario = pd.date_range(start=t_ini, end=t_fim, freq='H', tz = "UTC")
dados_peq = pd.DataFrame(date_rng_horario, columns=['date'])
dados_peq['datahora_UTC']= pd.to_datetime(dados_peq['date'])
dados_peq = dados_peq.set_index('datahora_UTC')
dados_peq.drop(['date'], axis=1, inplace = True)
dados_peq

# ## GERA SERIE PADRAO DE ETP PARA FIU ##
# etp_bruto = pd.read_csv('/discolocal/bruno/Fiu/etp_londrina_horario.csv',
#                   index_col = 0, sep = ',')
# etp_bruto.index = pd.to_datetime(etp_bruto.index)
# etp_bruto.index = etp_bruto.index.tz_localize('UTC')
# etp_bruto.columns = ['etp']
# etp_bruto['etp'] = etp_bruto['etp'].fillna(0)
#
# etp_padrao = etp_bruto.groupby([etp_bruto.index.month, etp_bruto.index.day, etp_bruto.index.hour]).mean()
# etp_padrao.index = etp_padrao.index.set_names(['Mes', 'Dia', 'Hora'])
# etp_padrao.reset_index(inplace = True)
# etp_padrao['Mes'] = etp_padrao.Mes.map('{:02}'.format)
# etp_padrao['Dia'] = etp_padrao.Dia.map('{:02}'.format)
# etp_padrao['Hora'] = etp_padrao.Hora.map('{:02}'.format)
# etp_padrao['etp'] = etp_padrao.etp.map('{:.5f}'.format)
# etp_padrao.to_csv('/discolocal/bruno/Fiu/etp_londrina_padrao.csv', sep = ',',
#               index = False)

#Carrega dados etp padrao
etp = pd.read_csv('/discolocal/bruno/Fiu/etp_londrina_padrao.csv', sep = ',')
etp.index = (etp['Mes'].map('{:02}'.format) + '-' +
             etp['Dia'].map('{:02}'.format) + '-' +
             etp['Hora'].map('{:02}'.format))

dados_peq['data'] = dados_peq.index.strftime('%m-%d-%H')
dados_peq['etp'] = dados_peq['data'].map(etp['etp'])
dados_peq = dados_peq.drop(['data'], axis=1)



dados_peq = pd.merge(dados_peq, etp, how = 'outer',
                 left_index = True, right_index = True)
dados_peq = dados_peq.loc[data_inicial:data_final]
dados_6hrs = (dados_peq.resample("6H", closed='right', label = 'right').
              agg({'pme' : np.sum, 'etp' : np.sum, 'qjus' : np.mean}))


dados_6hrs['pme'] = dados_6hrs['pme'].apply('{:,.2f}'.format)
dados_6hrs['qjus'] = dados_6hrs['qjus'].apply('{:,.3f}'.format)
dados_6hrs['etp'] = dados_6hrs['etp'].apply('{:,.3f}'.format)

# df = dados_peq.loc['2019']
#
# PME = df['pme'].to_numpy()
# ETP = df['etp'].to_numpy()
# Qjus = df['qjus'].to_numpy()
#
# fig = plotar_hidro(idx=df.index, PME=PME, ETP=ETP, Qobs=Qjus, Qmon=None,
#                    Qsims=None)
# fig.savefig('../Teste/observadofiu_2019.png', dpi = 300,
#             bbox_inches = 'tight')
with open('../dados/peq/bacia_fiu_6hrs.peq', 'w', newline = '') as file:
    writer = csv.writer(file)
    writer.writerow([area])
dados_6hrs.to_csv('../dados/peq/bacia_fiu_6hrs.peq', mode = 'a',
                 index_label='datahora_UTC')
