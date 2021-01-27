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

precip = pd.read_csv('../dados/pme/pme_fiu_horario.csv', index_col = 0, sep = ',')
precip.index = pd.to_datetime(precip.index)
precip.columns = ['pme']
data_inicial = precip.index[0]
data_final = precip.index[-1]

vazao = pd.read_excel('../Teste/dados_horarios_fiu.xlsx')
vazao.index = (pd.to_datetime(vazao.Data) + pd.to_timedelta(vazao.Hora, unit = 'h'))
vazao.index = vazao.index.tz_localize('UTC')
vazao['qjus'] = np.where((vazao['Afluente'] == 'S/L'), np.nan, vazao['Afluente'])
vazao = vazao[['qjus']]
vazao['qjus'] = pd.to_numeric(vazao['qjus'])
vazao['qjus'] = np.where((vazao['qjus'] < 0), np.nan, vazao['qjus'])
vazao['qjus'] = vazao['qjus'].rolling(window=4, min_periods=1).mean()
vazao.to_csv('../Teste/vazao_fiu_HR.csv',
                 date_format='%Y-%m-%dT%H:%M:%SZ', sep = ",",
                 float_format = '%.3f', index_label='data')

if vazao.index[0] > data_inicial:
    data_inicial = vazao.index[0]
if vazao.index[-1] < data_final:
    data_final = vazao.index[-1]

dados_peq = pd.merge(precip, vazao, how = 'outer',
                 left_index = True, right_index = True)

etp = pd.read_csv('../Teste/evp_londrina_horario.csv', index_col = 0, sep = ',')
etp.index = pd.to_datetime(etp.index)
etp.index = etp.index.tz_localize('UTC')
etp.columns = ['etp']
etp['etp'] = etp['etp'].fillna(0)
if etp.index[0] > data_inicial:
    data_inicial = etp.index[0]
if etp.index[-1] < data_final:
    data_final = etp.index[-1]

dados_peq = pd.merge(dados_peq, etp, how = 'outer',
                 left_index = True, right_index = True)
dados_peq = dados_peq.loc[data_inicial:data_final]


dados_peq['pme'] = dados_peq['pme'].apply('{:,.2f}'.format)
dados_peq['qjus'] = dados_peq['qjus'].apply('{:,.3f}'.format)
dados_peq['etp'] = dados_peq['etp'].apply('{:,.3f}'.format)

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
with open('../dados/peq/bacia_fiu.peq', 'w', newline = '') as file:
    writer = csv.writer(file)
    writer.writerow([area])
dados_peq.to_csv('../dados/peq/bacia_fiu.peq', mode = 'a',
                 index_label='datahora_UTC')
