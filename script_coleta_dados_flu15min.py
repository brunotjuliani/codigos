# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime as dt
import pytz
import json
import psycopg2, psycopg2.extras

dir_seca = '/discolocal/bruno/Seca_Iguacu/Dados_Estacoes'
dir_dados = "/discolocal/bruno/Coleta_Dados"
dir_observado = "/discolocal/bruno/Observado"
os.chdir(dir_observado)
lista = []

def coletar_dados(t_ini,t_fim,posto_codigo,sensores):
        # Montagem do texto
    t_ini_string = t_ini.strftime('%Y-%m-%d %H:%M')
    t_fim_string = t_fim.strftime('%Y-%m-%d %H:%M')
    texto_psql = "select hordatahora at time zone 'UTC' as hordatahora, \
                  horleitura, horsensor, horqualidade \
                  from horaria where hordatahora >= '{}' and hordatahora <= '{}' \
                  and horestacao in ({}) \
                  and horsensor in {} \
                  order by horestacao, horsensor, hordatahora; \
                  ".format(t_ini_string, t_fim_string, posto_codigo,sensores)
    # Execução da consulta no banco do Simepar
    conn = psycopg2.connect(dbname='clim', user='hidro', password='hidrologia',
                            host='tornado', port='5432')
    consulta = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    consulta.execute(texto_psql)
    consulta_lista = consulta.fetchall()
    df_consulta =pd.DataFrame(consulta_lista,columns=['tempo','valor','sensor',
                                                      'qualidade'])
    df_consulta.set_index('tempo', inplace=True)
    return df_consulta

postos_vazao = {
                'Rio_Negro':'26064948',
#                'Porto_Amazonas':'25334953',
#                'Sao_Bento':'25564947',
#                'Pontilhao':'25555031',
#                'Santa_Cruz_Timbo':'26125049',
#                'Sao_Mateus_Sul':'25525023',
#                'Divisa':'26055019',
#                'Fluviopolis':'26025035',
#                'Uniao_da_Vitoria':'26145104',
#                'Madereira_Gavazzoni':'25485116',
#                'Jangada':'26225115',
                ### Foz_do_Areia':'GBM',
#                'Solais_Novo':'26055155',
#                'Porto_Santo_Antonio':'25235306',
#                'Aguas_do_Vere':'25465256',
                ### 'Segredo':'SGD',
                ### 'Foz_do_Chopim':'FCH',
                ### 'Santa_Clara':'SCL',
                ### 'Salto_Caxias':'SCX',
#                'Porto_Capanema':'25345435',
#                'Hotel_Cataratas':'25685442'
            }


## COLETA DADOS VAZAO


for posto_nome, posto_codigo in postos_vazao.items():
    print('Coletando vazao',posto_nome)
    t_ini = dt.datetime(1997, 1, 1,  0,  0) #AAAA, M, D, H, Min
    t_fim = dt.datetime(2020, 9, 28, 23, 59)

    #coleta dados de cota para verificacao qualidade
    dados_cota = coletar_dados(t_ini,t_fim, posto_codigo, '(18)')
    dados_cota.columns = ['cota', 'sensor_cota', 'quali_cota']
    #coleta dados de vazao
    dados_vazao = coletar_dados(t_ini,t_fim, posto_codigo, '(33)')
    dados_vazao.columns = ['vazao', 'sensor_vazao', 'quali_vazao']
    #concatena vazao e cota, filtrando apenas cotas aprovadas no banco de dados
    dados = pd.merge(dados_cota,dados_vazao['vazao'],how='inner',
                     left_index=True,right_index=True)
    dados = dados[dados['quali_cota'] == 0].drop(['sensor_cota', 'quali_cota'],
                                                 axis = 1)
    #REMOVE COTAS CONSTANTES ------ AQUI APLICADO PARA 96 OBSERVACOES DE 15 MIN - 24 HORAS
    dados2 = dados.groupby((dados['cota'].shift()!=dados['cota']).cumsum()
                           ).filter(lambda x: len(x) >= 96)
    dados['cota'] = np.where(dados.index.isin(dados2.index),np.nan,dados['cota'])
    dados = dados.dropna()
    dados.columns = ['m', 'q_m3s']
    #REMOVE DADOS NEGATIVOS
    dados[dados['q_m3s'] < 0] = np.nan
    dados[dados['m'] < 0] = np.nan
    #converte para hora local - GMT-3 - timezone('America/Sao_Paulo')
    dados.index = pd.to_datetime(dados.index)
    dados.index = (dados.index.tz_localize(pytz.utc).
                   tz_convert(pytz.timezone('America/Sao_Paulo')).
                   strftime("%Y-%m-%d %X"))
    dados.index = pd.to_datetime(dados.index)
    dados["q_m3s"] = pd.to_numeric(dados["q_m3s"], downcast="float")
    dados["m"] = pd.to_numeric(dados["m"], downcast = "float")

    # cria DFs padrão de data, para serem preenchidas com os dados baixados
    date_rng_15min = pd.date_range(start=t_ini, end=t_fim, freq='15min')
    table_15min = pd.DataFrame(date_rng_15min, columns=['date'])
    table_15min['Datetime']= pd.to_datetime(table_15min['date'])
    table_15min = table_15min.set_index('Datetime')
    table_15min.drop(['date'], axis=1, inplace = True)

    df_15min = pd.merge(table_15min, dados, how='left',
                        left_index=True, right_index=True)

    #importa dicionario de erros grosseiros e escolhe estacao
    dicionario_erros = json.load(open('erros_grosseiros_15min.txt'))
    erros_estacao = dicionario_erros[posto_nome]
    #trata a matriz de erros
    try:
        erros_estacao = np.hstack(erros_estacao)
    except ValueError:
        pass
    #remove erros grosseiros da serie observada
    df_15min.loc[pd.to_datetime(erros_estacao), 'q_m3s'] = np.nan
    df_15min.loc[pd.to_datetime(erros_estacao), 'm'] = np.nan

    #exporta observado para csv
    df_15min.to_csv('vazao_'+posto_nome+'_15min.csv')

    print(posto_nome, 'acabou - ', list(postos_vazao).index(posto_nome)+1,"/",
          len(postos_vazao))
