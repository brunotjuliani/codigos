import pandas as pd
import numpy as np
import csv
import sys
import datetime
import pytz
sys.path.append('../modelos/')
from plotar_hidro import plotar_hidro


bacia = 'XX'
nome = 'Fiu'
area = 534

precip = pd.read_csv('/discolocal/bruno/Fiu/pme_fiu.csv', index_col = 0, sep = ',')
precip.index = pd.to_datetime(precip.index)
precip.columns = ['pme']
data_inicial = precip.index[0]
data_final = precip.index[-1]

vazao = pd.read_excel('/discolocal/bruno/Fiu/dados_horarios_fiu.xlsx')
vazao.index = (pd.to_datetime(vazao.Data) + pd.to_timedelta(vazao.Hora, unit = 'h'))
vazao.index = vazao.index.tz_localize('UTC')
vazao['qjus'] = np.where((vazao['Afluente'] == 'S/L'), np.nan, vazao['Afluente'])
vazao = vazao[['qjus']]
vazao['qjus'] = pd.to_numeric(vazao['qjus'])
vazao['qjus'] = np.where((vazao['qjus'] < 0), np.nan, vazao['qjus'])
if vazao.index[0] > data_inicial:
    data_inicial = vazao.index[0]
if vazao.index[-1] < data_final:
    data_final = vazao.index[-1]

dados_peq = pd.merge(precip, vazao, how = 'outer',
                 left_index = True, right_index = True)

#Carrega dados etp padrao
etp = pd.read_csv('/discolocal/bruno/Fiu/etp_londrina_padrao.csv', sep = ',')
etp.index = (etp['Mes'].map('{:02}'.format) + '-' +
             etp['Dia'].map('{:02}'.format) + '-' +
             etp['Hora'].map('{:02}'.format))
dados_peq['data'] = dados_peq.index.strftime('%m-%d-%H')
dados_peq['etp'] = dados_peq['data'].map(etp['etp'])
dados_peq = dados_peq.drop(['data'], axis=1)

#DEFINE PERIODOS E AGRUPA 6 HRS
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
with open('/discolocal/bruno/Fiu/peq_Fiu_6hrs.csv', 'w', newline = '') as file:
    writer = csv.writer(file)
    writer.writerow([area])
dados_6hrs.to_csv('/discolocal/bruno/Fiu/peq_Fiu_6hrs.csv', mode = 'a',
                 index_label='datahora_UTC')
