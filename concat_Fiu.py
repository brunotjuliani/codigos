import pandas as pd
import numpy as np
import csv

data_inicial = '2015-09-23'
data_final = '2020-09-30'

posto_nome = 'reservatorio_fiu'

#posto_plu = 'apucaraninha_montante'
#posto_codigo = '23735103'

posto_plu = 'reservatorio_fiu'
# posto_codigo = '23745094'
posto_area = 588.003

plu_diario = pd.read_csv('/discolocal/bruno/Observado/Teste/' + posto_plu +
                         '_plu_diario.csv', index_col = 0, sep = ';')
plu_diario.index = pd.to_datetime(plu_diario.index).tz_localize(None)
plu_diario.columns = ['pme']


evp_diario = pd.read_csv('/discolocal/bruno/Observado/Teste/evp_londrina_inmet.csv',
                         index_col = 0, sep = ',')
evp_diario.index = pd.to_datetime(evp_diario.index)
evp_diario.columns = ['etp']


vazao_diario = pd.read_excel('/discolocal/bruno/Observado/Teste/' + posto_nome +
                             '_flu_diario.xlsx', index_col = 0, skiprows = 2)
vazao_diario.index = pd.to_datetime(vazao_diario.index)
vazao_diario.columns = ['qjus']

dados = pd.merge(plu_diario, evp_diario, how = 'outer',
                 left_index = True, right_index = True)
dados = pd.merge(dados, vazao_diario, how = 'outer',
                 left_index = True, right_index = True)
dados.index.name = 'data'
dados['pme'] = dados['pme'].apply('{:,.2f}'.format)
dados['etp'] = dados['etp'].apply('{:,.2f}'.format)
dados['qjus'] = dados['qjus'].apply('{:,.3f}'.format)

dados = dados.loc[data_inicial:data_final]

with open('/discolocal/bruno/Observado/Teste/' + posto_plu + '.peq',
          'w', newline = '') as file:
    writer = csv.writer(file)
    writer.writerow([posto_area])
dados.to_csv('/discolocal/bruno/Observado/Teste/' + posto_plu + '.peq',
             mode = 'a')
