import pandas as pd
import datetime as dt
import numpy as np

simepar = pd.read_csv('info_Simepar.csv', index_col=0)
simepar['estcodigo'] = simepar['estcodigo'].apply(np.int64)

inmet = pd.read_csv('info_Inmet.csv', index_col=0)
inmet['estcodigo'] = inmet['estcodigo'].apply(np.int64)


selecao = pd.concat([simepar, inmet]).reset_index()
selecao = selecao.drop(['index', 'esttipo', 'estiniciooperacao'], axis=1)

info_estacoes = pd.DataFrame()

for idx, row in selecao.iterrows():
    estcodigo = row['estcodigo']
    orgsigla = row['orgsigla']
    dados = pd.read_csv(f'./Dados/{orgsigla}_{estcodigo}.csv', index_col=0, parse_dates=True)
    dados.v_vento = np.where(dados.v_vento < 0, np.nan, dados.v_vento)
    dados.v_vento = np.where(dados.v_vento > 50, np.nan, dados.v_vento)
    dados.t_med = np.where(dados.t_med < -50, np.nan, dados.t_med)
    dados.t_med = np.where(dados.t_med > 50, np.nan, dados.t_med)
    row['ini_vento'] = dados['v_vento'].first_valid_index()
    row['fim_vento'] = dados['v_vento'].last_valid_index()
    row['ini_temp'] = dados['t_med'].first_valid_index()
    row['fim_temp'] = dados['t_med'].last_valid_index()
    s_padrao = dados.groupby([dados.index.month, dados.index.day]).mean()
    row['v_vento_medio'] = s_padrao['v_vento'].mean()
    row['t_med_medio'] = s_padrao['t_med'].mean()
    info_estacoes = info_estacoes.append(row)
    print(f'{idx+1}/{len(selecao)}')

lista_temp_vento = info_estacoes[['estcodigo', 'estnome', 'orgsigla',
                                  'estlongitude', 'estlatitude', 'estaltitude',
                                  't_med_medio', 'v_vento_medio',
                                  'ini_temp', 'fim_temp', 'ini_vento', 'fim_vento']]
lista_temp_vento['estcodigo'] = lista_temp_vento['estcodigo'].apply(np.int64)

lista_temp_vento.to_csv('dados_selecao.csv')

lista_temp_vento[lista_temp_vento['v_vento_medio']>50]
