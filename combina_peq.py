import pandas as pd
import numpy as np
import csv

precip = pd.read_csv('../dados/pme/pme_bacia_01.pd', index_col = 0, sep = ',')
precip.index = pd.to_datetime(precip.index)
precip.columns = ['pme']
data_inicial = precip.index[0]
data_final = precip.index[-1]

vazao = pd.read_csv('../dados/f_consist/Rio_Negro_HR.csv', index_col = 0, sep = ';')
vazao.index = pd.to_datetime(vazao.index)
vazao = vazao.drop(['h_m'], axis=1)
vazao.columns = ['qjus']
if vazao.index[0] > data_inicial:
    data_inicial = vazao.index[0]
if vazao.index[-1] < data_final:
    data_final = vazao.index[-1]

dados_peq = pd.merge(precip, vazao, how = 'outer',
                 left_index = True, right_index = True)
dados_peq = dados_peq.loc[data_inicial:data_final]

etp = pd.read_csv('../dados/etp/etpclim_01.txt', header = None)
etp['Mes'] = etp[0].str.slice(0,2)
etp['Dia'] = etp[0].str.slice(3,5)
etp['Hora'] = etp[0].str.slice(6,8)
etp['etp'] = pd.to_numeric(etp[0].str.slice(9,17))
etp = etp.drop([0], axis=1)
etp.index = etp['Mes'] + '-' + etp['Dia'] + '-' + etp['Hora']

dados_peq['data'] = dados_peq.index.strftime('%m-%d-%H')
dados_peq['etp'] = dados_peq['data'].map(etp['etp'])
dados_peq = dados_peq.drop(['data'], axis=1)
dados_peq = dados_peq[['pme', 'etp', 'qjus']]

dados_peq.loc['2014-06-10']

dados_peq['pme'] = dados_peq['pme'].apply('{:,.2f}'.format)
dados_peq['etp'] = dados_peq['etp'].apply('{:,.5f}'.format)

area = 3461

with open('../dados/peq/bacia_01.peq', 'w', newline = '') as file:
    writer = csv.writer(file)
    writer.writerow([area])
dados_peq.to_csv('../dados/peq/bacia_01.peq', mode = 'a')
