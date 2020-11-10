import pandas as pd
import numpy as np
import csv

data_inicial = '2015-09-23'
data_final = '2020-08-31'

# cria DFs padrão de data, para serem preenchidas com os dados baixados
date_rng_diario = pd.date_range(start=data_inicial, end=data_final, freq='D')

#1- Sao Jose
plu_1 = pd.read_csv('/discolocal/bruno/Observado/Teste/sao_jose.pds',
                    skiprows = [0,1,2], index_col = 'Data', parse_dates = True,
                    na_values=['-'], sep = ',')
plu_1.index = pd.to_datetime(plu_1.index).tz_localize(None)
plu_1.columns = ['p_1']
plu_1["p_1"] = pd.to_numeric(plu_1["p_1"], downcast = "float")
plu_1['count'] = 1
dados_1 = pd.DataFrame(date_rng_diario, columns=['data'])
dados_1['data']= pd.to_datetime(dados_1['data'])
dados_1 = dados_1.set_index('data')
df_diario_1 = plu_1.resample("D", closed='left').agg({'count' : np.sum,
                                                      'p_1' : np.sum})
df_diario_1.drop(df_diario_1.columns[0], axis=1, inplace=True)
dados_1 = pd.concat([dados_1, df_diario_1], axis=1)
area_1 = 243.172

coordenadas = pd.read_csv('/discolocal/bruno/Observado/Teste/sao_jose.pds',
                          sep = ',')
lat = coordenadas.iloc[0,0]
lgt = coordenadas.iloc[0,1]
d1 = dados_1
d1.columns = ['p']
d1.index.name = 'data'
with open('/discolocal/bruno/Observado/Teste/Estacoes_plu/sao_jose.pd',
          'w', newline = '') as file:
    writer = csv.writer(file)
    writer.writerow([lat, lgt])
d1.to_csv('/discolocal/bruno/Observado/Teste/Estacoes_plu/sao_jose.pd',
             mode = 'a')

#2 - Apucaraninha Montante
plu_2 = pd.read_csv('/discolocal/bruno/Observado/Teste/apucaraninha_montante_plu_diario.csv',
                    index_col = 0, sep = ';')
plu_2.index = pd.to_datetime(plu_2.index).tz_localize(None)
plu_2.columns = ['p_2']
dados_2 = plu_2
area_2 = 260.826

lat = -23.730556
lgt = -51.037778
d2 = dados_2
d2.columns = ['p']
d2.index.name = 'data'
with open('/discolocal/bruno/Observado/Teste/Estacoes_plu/apucaraninha_montante.pd',
          'w', newline = '') as file:
    writer = csv.writer(file)
    writer.writerow([lat, lgt])
d2.to_csv('/discolocal/bruno/Observado/Teste/Estacoes_plu/apucaraninha_montante.pd',
             mode = 'a')

#3 - Montante barragem fiu
plu_3 = pd.read_csv('/discolocal/bruno/Observado/Teste/montante_fiu.pds',
                    skiprows = [0,1,2], index_col = 'Data', parse_dates = True,
                    na_values=['-'], sep = ',')
plu_3.index = pd.to_datetime(plu_3.index).tz_localize(None)
plu_3.columns = ['p_3']
plu_3["p_3"] = pd.to_numeric(plu_3["p_3"], downcast = "float")
plu_3['count'] = 1
dados_3 = pd.DataFrame(date_rng_diario, columns=['data'])
dados_3['data']= pd.to_datetime(dados_3['data'])
dados_3 = dados_3.set_index('data')
df_diario_3 = plu_3.resample("D", closed='left').agg({'count' : np.sum,
                                                      'p_3' : np.sum})
df_diario_3.drop(df_diario_3.columns[0], axis=1, inplace=True)
dados_3 = pd.concat([dados_3, df_diario_3], axis=1)
area_3 = 71.807

coordenadas = pd.read_csv('/discolocal/bruno/Observado/Teste/montante_fiu.pds',
                          sep = ',')
lat = coordenadas.iloc[0,0]
lgt = coordenadas.iloc[0,1]
d3 = dados_3
d3.columns = ['p']
d3.index.name = 'data'
with open('/discolocal/bruno/Observado/Teste/Estacoes_plu/montante_fiu.pd',
          'w', newline = '') as file:
    writer = csv.writer(file)
    writer.writerow([lat, lgt])
d3.to_csv('/discolocal/bruno/Observado/Teste/Estacoes_plu/montante_fiu.pd',
             mode = 'a')

#4 - Reservatorio Fiu
plu_4 = pd.read_csv('/discolocal/bruno/Observado/Teste/reservatorio_fiu_plu_diario.csv',
                    index_col = 0, sep = ';')
plu_4.index = pd.to_datetime(plu_4.index).tz_localize(None)
plu_4.columns = ['p_4']
dados_4 = plu_4
area_4 = 10.883

lat = -23.745833
lgt = -50.940278
d4 = dados_4
d4.columns = ['p']
d4.index.name = 'data'
with open('/discolocal/bruno/Observado/Teste/Estacoes_plu/reservatorio_fiu.pd',
          'w', newline = '') as file:
    writer = csv.writer(file)
    writer.writerow([lat, lgt])
d4.to_csv('/discolocal/bruno/Observado/Teste/Estacoes_plu/reservatorio_fiu.pd',
             mode = 'a')


dados = pd.merge(dados_1, dados_2, how = 'outer',
                 left_index = True, right_index = True)
dados = pd.merge(dados, dados_3, how = 'outer',
                 left_index = True, right_index = True)
dados = pd.merge(dados, dados_4, how = 'outer',
                 left_index = True, right_index = True)
dados.index.name = 'data'
# dados['p_1'] = dados['p_1'].apply('{:,.2f}'.format)
# dados['p_2'] = dados['p_2'].apply('{:,.2f}'.format)
# dados['p_3'] = dados['p_3'].apply('{:,.2f}'.format)
# dados['p_4'] = dados['p_4'].apply('{:,.2f}'.format)

dados = dados.loc[data_inicial:data_final]

area_total = area_1 + area_2 + area_3 + area_4

dados['pme'] = (dados['p_1']*area_1/area_total + dados['p_2']*area_2/area_total+
                dados['p_3']*area_3/area_total + dados['p_4']*area_4/area_total)
dados_pme = pd.DataFrame(dados['pme'])

dados_pme.to_csv('/discolocal/bruno/Observado/Teste/bacia_fiu.pd',
                 float_format = '%.2f', sep = ';')



plu_diario = pd.read_csv('/discolocal/bruno/Observado/Teste/pme_bacia_fiu.pd',
                         index_col = 0, sep = ',')
plu_diario.index = pd.to_datetime(plu_diario.index).tz_localize(None)
plu_diario.columns = ['pme']

evp_diario = pd.read_csv('/discolocal/bruno/Observado/Teste/evp_londrina_inmet.csv',
                         index_col = 0, sep = ',')
evp_diario.index = pd.to_datetime(evp_diario.index)
evp_diario.columns = ['etp']

vazao_diario = pd.read_excel('/discolocal/bruno/Observado/Teste/reservatorio_fiu_flu_diario.xlsx',
                             index_col = 0, skiprows = 2)
vazao_diario.index = pd.to_datetime(vazao_diario.index)
vazao_diario.columns = ['qjus']

dados_peq = pd.merge(plu_diario, evp_diario, how = 'outer',
                 left_index = True, right_index = True)
dados_peq = pd.merge(dados_peq, vazao_diario, how = 'outer',
                 left_index = True, right_index = True)
dados_peq.index.name = 'data'
dados_peq['pme'] = dados_peq['pme'].apply('{:,.2f}'.format)
dados_peq['etp'] = dados_peq['etp'].apply('{:,.2f}'.format)
dados_peq['qjus'] = dados_peq['qjus'].apply('{:,.3f}'.format)

dados_peq = dados_peq.loc[data_inicial:data_final]

area = 534

with open('/discolocal/bruno/Observado/Teste/bacia_fiu.peq',
          'w', newline = '') as file:
    writer = csv.writer(file)
    writer.writerow([area])
dados_peq.to_csv('/discolocal/bruno/Observado/Teste/bacia_fiu.peq',
             mode = 'a')
