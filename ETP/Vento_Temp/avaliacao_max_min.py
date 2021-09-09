import pandas as pd
pd.options.mode.chained_assignment = None
import datetime as dt
import numpy as np

postos_def = pd.read_csv('./dados_selecao.csv')
info_estacoes = pd.DataFrame()

for idx, row in postos_def.iterrows():
    estcodigo = row['estcodigo']
    orgsigla = row['orgsigla']
    dados = pd.read_csv(f'./Dados_Novo/{orgsigla}_{estcodigo}.csv', index_col=0, parse_dates=True)
    row['ini_serie'] = dados.first_valid_index().strftime('%Y-%m-%d')
    row['fim_serie'] = dados.last_valid_index().strftime('%Y-%m-%d')

    dados = dados[['v_rajada', 't_max', 't_min']]
    dados.v_rajada = np.where(dados.v_rajada < 0, np.nan, dados.v_rajada)
    dados.v_rajada = np.where(dados.v_rajada > 50, np.nan, dados.v_rajada)
    dados.t_max = np.where(dados.t_max < -50, np.nan, dados.t_max)
    dados.t_max = np.where(dados.t_max > 50, np.nan, dados.t_max)
    dados.t_min = np.where(dados.t_min < -20, np.nan, dados.t_min)
    dados.t_min = np.where(dados.t_min > 50, np.nan, dados.t_min)
    dados['c_rajada'] = np.where(dados.v_rajada.isnull(), 0, 1)
    dados['c_tmax'] = np.where(dados.t_max.isnull(), 0, 1)
    dados['c_tmin'] = np.where(dados.t_min.isnull(), 0, 1)

    dados_anual = dados.resample("Y", closed='right').agg(
        {'v_rajada':np.max, 't_max':np.max, 't_min':np.min,
         'c_rajada':np.sum, 'c_tmax':np.sum, 'c_tmin':np.sum})
    dados_anual.loc[dados_anual['c_rajada'] < 210, ['v_rajada']] = np.nan
    dados_anual.loc[dados_anual['c_tmax'] < 210, ['t_max']] = np.nan
    dados_anual.loc[dados_anual['c_tmin'] < 210, ['t_min']] = np.nan

    row['v_rajada_max'] = dados_anual['v_rajada'].mean()
    row['t_max_med'] = dados_anual['t_max'].mean()
    row['t_min_med'] = dados_anual['t_min'].mean()

    info_estacoes = info_estacoes.append(row)
    print(f'{idx+1}/{len(postos_def)}')

lista_atualizada = info_estacoes[['estcodigo', 'estnome', 'orgsigla',
                                  'estlongitude', 'estlatitude', 'estaltitude',
                                  't_med_medio', 't_max_med', 't_min_med',
                                  'v_vento_medio', 'v_rajada_max',
                                  'ini_serie', 'fim_serie']]
lista_atualizada['estcodigo'] = lista_atualizada['estcodigo'].apply(np.int64)

lista_atualizada.to_csv('dados_selecao_maxmin.csv')

lista_atualizada
