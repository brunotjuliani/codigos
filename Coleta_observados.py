import os

##DEFINE FUNCOES
'''
    Realiza coleta - agregacao - CQD dos dados do banco do Simepar
    entre t_ini e t_fim
    Boas praticas de programacao em
    https://towardsdatascience.com/data-scientists-your-variable-names-are-awful-heres-how-to-fix-them-89053d2855be
    # Obs:
    # - label = 'left' fara com que a precipitacao do dia 2019/05/30 seja entre 2019/05/29 7:00 e 2019/05/30 7:00
    # - base = 10 significa que o dia vai de 10 as 10 UTC, ou seja, 7 as 7 BRT
    # Todos os horarios sao UTC
'''

import pandas as pd, numpy as np
import psycopg2, psycopg2.extras
from datetime import datetime


### FUNCOES

'''
    ADAPTADO PARA AS ESTACOES DO SIMEPAR NO IGUACU
'''


def coletar_dados(t_ini,t_fim,posto_codigo,sensores):
        # Montagem do texto
    t_ini_string = t_ini.strftime('%Y-%m-%d %H:%M')
    t_fim_string = t_fim.strftime('%Y-%m-%d %H:%M')
    texto_psql = "select hordatahora at time zone 'UTC' as hordatahora, \
                  horleitura, horsensor \
                  from horaria where hordatahora >= '{}' and hordatahora <= '{}' \
                  and horestacao in ({}) \
                  and horsensor in {} \
                  order by horestacao, horsensor, hordatahora; \
                  ".format(t_ini_string, t_fim_string, posto_codigo,sensores)
    # Execução da consulta no banco do Simepar
    conn = psycopg2.connect(dbname='clim', user='hidro', password='hidrologia', host='tornado', port='5432')
    consulta = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    consulta.execute(texto_psql)
    consulta_lista = consulta.fetchall()
    df_consulta = pd.DataFrame(consulta_lista, columns=['tempo','valor','sensor'])
    df_consulta.set_index('tempo', inplace=True)
    return df_consulta

def funcao_coleta_banco(t_ini, t_fim, posto_codigo):
    # Montagem do texto
    t_ini_string = t_ini.strftime('%Y-%m-%d %H:%M')
    t_fim_string = t_fim.strftime('%Y-%m-%d %H:%M')
    texto_psql = "select hordatahora at time zone 'UTC' as hordatahora, \
                  horleitura, horsensor \
                  from horaria where hordatahora >= '{}' and hordatahora <= '{}' \
                  and horestacao in ({}) \
                  and horsensor in (7,33) \
                  order by horestacao, horsensor, hordatahora; \
                  ".format(t_ini_string, t_fim_string, posto_codigo)
    # Execução da consulta no banco do Simepar
    conn = psycopg2.connect(dbname='clim', user='hidro', password='hidrologia', host='tornado', port='5432')
    consulta = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    consulta.execute(texto_psql)
    consulta_lista = consulta.fetchall()
    df_consulta = pd.DataFrame(consulta_lista, columns=['tempo','valor','sensor'])
    df_consulta.set_index('tempo', inplace=True)

    # Vazao
    sr_vazao = df_consulta.loc[df_consulta['sensor'] == 33]['valor']
    sr_vazao = pd.to_numeric(sr_vazao)
    sr_vazao.name = 'vazao (m3/s)'

    # Chuva
    sr_chuva = df_consulta.loc[df_consulta['sensor'] == 7]['valor']
    sr_chuva = pd.to_numeric(sr_chuva)
    sr_chuva.name = 'chuva acumulada (mm)'

    return sr_vazao, sr_chuva

def agrega_vazao(sr_vazao, base_agregacao, tolerancia_vazao):
    sr = sr_vazao
    # Limpar duplicados
    sr = sr.loc[~sr.index.duplicated(keep='first')]
    # Resample - 1º para dadoos horarios, preenchendo vazios com NaN
    sr = sr.resample('H', label='left', closed='right').apply(lambda x: x.mean(skipna=True))
    # Resample - 2º para dados diarios
    sr = sr.resample('24H', base=base_agregacao, label='left', closed='right') \
                .apply(lambda x: x.mean(skipna=True) if (x.isnull().sum() <= tolerancia_vazao) else np.nan )
    # Pos-processamento
    sr = pd.Series(sr.round(decimals=3).to_numpy(), index = sr.index.floor('D'), name='vazao (m3/s)')
    return sr

def agrega_chuva(sr_chuva, base_agregacao, tolerancia_chuva):
    sr = sr_chuva
    # Limpar duplicados
    sr = sr.loc[~sr.index.duplicated(keep='first')]
    # Resample - 1º para dadoos horarios, preenchendo vazios com NaN
    sr = sr.resample('H', label='left', closed='right').apply(lambda x: x.sum(skipna=False))
    # Resample - 2º para dados diarios
    sr = sr.resample('24H', base=base_agregacao, label='left', closed='right') \
                .apply(lambda x: x.sum(skipna=True) if (x.isnull().sum()<=tolerancia_chuva) else np.nan )
    # Pos-processamento
    sr = pd.Series(sr.round(decimals=1).to_numpy(), index = sr.index.floor('D'), name = 'chuva (mm)')
    return sr



import datetime as dt, pandas as pd


## LISTA POSTOS VAZAO

postos_vazao = {
                #'Rio_Negro':'26064948',
                #'Porto_Amazonas':'25334953',
                #'Sao_Bento':'25564947',
                'Pontilhao':'25555031',
                #'Santa_Cruz_Timbo':'26125049',
                #'Sao_Mateus_Sul':'25525023',
                #'Divisa':'26055019',
                #'Fluviopolis':'26025035',
                #'Uniao_da_Vitoria':'26145104',
                #'Madereira_Gavazzoni':'25485116',
                #'Jangada':'26225115',
                ### Foz_do_Areia':'GBM',
                #'Solais_Novo':'26055155',
                #'Porto_Santo_Antonio':'25235306',
                #'Aguas_do_Vere':'25465256',
                ### 'Segredo':'SGD',
                ### 'Foz_do_Chopim':'FCH',
                ### 'Santa_Clara':'SCL',
                ### 'Salto_Caxias':'SCX',
                #'Porto_Capanema':'25345435',
                #'Hotel_Cataratas':'25685442'

            }


## LISTA POSTOS PRECIPITACAO

postos_precip = {
                'Rio_Negro':'26064948', #hidrologica
                #'Porto_Amazonas':'25334953', #hidrologica
                # Sao_Bento':'25564947', #hidrologica
                # Pontilhao':'25555031', #hidrologica
                # Santa_Cruz_Timbo':'26125049', #hidrologica
                # Sao_Mateus_Sul':'25525023', #hidrologica
                # Divisa':'26055019', #hidrologica
                # Fluviopolis':'26025035', #hidrologica
                # Uniao_da_Vitoria':'26145104', #hidrologica
                # Madereira_Gavazzoni':'25485116', #hidrologica
                # Jangada':'26225115', #hidrologica
                ### Foz_do_Areia':'26005139', #hidrologica
                # Solais_Novo':'26055155', #hidrologica
                # Porto_Santo_Antonio':'25235306', #hidrologica
                # Aguas_do_Vere':'25465256', #hidrologica
                ### 'Segredo':'25475206', #hidrologica
                ### 'Foz_do_Chopim':'FCH',
                ### 'Santa_Clara':'25385157', #meteorologica - estacao Pinhao
                ### 'Salto_Caxias':'25325330', #hidrologica
                # 'Porto_Capanema':'25345435', #hidrologica
                # 'Hotel_Cataratas':'25685442' #hidrologica

            }



## DEFINE DIRETORIOS

dir_dados = "/discolocal/bruno/Coleta_Dados"
dir_observado = "/discolocal/bruno/Observado"
dir_seca = '/discolocal/bruno/Seca_Iguacu/Dados_Estacoes'


## COLETA DADOS VAZAO

os.chdir(dir_seca)

for posto_nome, posto_codigo in postos_vazao.items():
    print('Coletando vazao',posto_nome)
    t_ini = dt.datetime(1990, 1, 1,  0,  0) #AAAA, M, D, H, Min
    t_fim = dt.datetime(2020, 8, 26, 23, 59)
    dados=coletar_dados(t_ini,t_fim,posto_codigo,'(33)') #07 p precip e 33 p vazao
    dados.to_csv(f'{posto_nome}_telemetrica.csv')
    print(posto_nome, 'acabou - ',list(postos_vazao).index(posto_nome)+1,"/",len(postos_vazao))


## COLETA DADOS PRECIPITACAO

os.chdir(dir_observado)

for posto_nome, posto_codigo in postos_precip.items():
    print('Coletando precipitacao',posto_nome)
    t_ini = dt.datetime(2015, 9, 3,  0,  0) #AAAA, M, D, H, Min
    t_fim = dt.datetime(2020, 8, 12, 23, 59)
    dados=coletar_dados(t_ini,t_fim,posto_codigo,'(7)') #07 p precip e 33 p vazao
    dados.to_csv(f'precip_{posto_nome}.csv')
    print(posto_nome, 'acabou - ',list(postos_precip).index(posto_nome),"/",len(postos_precip))
