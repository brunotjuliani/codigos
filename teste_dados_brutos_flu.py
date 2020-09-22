# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime as dt
import pytz
import json
import psycopg2, psycopg2.extras
import sys
np.set_printoptions(threshold=sys.maxsize)
pd.set_option("display.max_rows", None, "display.max_columns", None)

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
    t_ini = dt.datetime(2020, 9, 1,  0,  0) #AAAA, M, D, H, Min
    t_fim = dt.datetime(2020, 9, 22, 23, 59)

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


    lista.append(posto_nome)

    # cria DFs padrão de data, para serem preenchidas com os dados baixados
    date_rng_horario = pd.date_range(start=t_ini, end=t_fim, freq='H')
    table_hor = pd.DataFrame(date_rng_horario, columns=['date'])
    table_hor['Datetime']= pd.to_datetime(table_hor['date'])
    table_hor = table_hor.set_index('Datetime')
    table_hor.drop(['date'], axis=1, inplace = True)

    date_rng_diario = pd.date_range(start=t_ini, end=t_fim, freq='D')
    table_dia = pd.DataFrame(date_rng_diario, columns=['date'])
    table_dia['Datetime']= pd.to_datetime(table_dia['date'])
    table_dia = table_dia.set_index('Datetime')
    table_dia.drop(['date'], axis=1, inplace = True)

    df = dados
    df.columns = ['m', 'q_m3s']
    df.drop(df.tail(1).index, inplace=True)
    df['count'] = 1
    df.index = pd.to_datetime(df.index)
    #converte para hora local - GMT-3 - timezone('America/Sao_Paulo')
    df.index = (df.index.tz_localize(pytz.utc).
                tz_convert(pytz.timezone('America/Sao_Paulo')).
                strftime("%Y-%m-%d %X"))
    df.index = pd.to_datetime(df.index)
    df["q_m3s"] = pd.to_numeric(df["q_m3s"], downcast="float")
    df["m"] = pd.to_numeric(df["m"], downcast = "float")


    # agrupa em dados horarios, com intervalo fechado à direita (acumulado/media da 0:01 a 1:00);
    # coluna count resulta a soma (contagem) dos "1", coluna valor resulta na media dos valores;
    # para os valores de cont < 2, substitui o dado em 'valor' por NaN:
    df_horario = (df.resample("H", closed='right', label='right').
                  agg({'count' : np.sum, 'q_m3s' : np.mean, 'm' : np.mean}))
    df_horario.loc[df_horario['count'] < 2, ['q_m3s']] = np.nan
    df_horario.loc[df_horario['count'] < 2, ['m']] = np.nan

    # cria coluna com valores 1;
    # agrupa em dados diarios, com intervalo fechado à direita (acumulado/media da 1:00 a 0:00);
    # coluna count resulta a soma (contagem) dos "1", coluna valor resulta na media dos valores;
    # para os valores de cont < 12, substitui o dado em 'valor' por NaN:
    df_horario['count'] = 1
    df_diario = (df_horario.resample("D", closed='left').
                 agg({'count':np.sum, 'q_m3s' : np.mean, 'm' : np.mean}))
    df_diario.loc[df_diario['count'] < 12, ['q_m3s']] = np.nan
    df_diario.loc[df_diario['count'] < 12, ['m']] = np.nan

    # remove colunas 'count' dos dataframes
    df.drop(df_horario.columns[0], axis=1, inplace=True)
    df_horario.drop(df_horario.columns[0], axis=1, inplace=True)
    df_diario.drop(df_diario.columns[0], axis=1, inplace=True)

    table_hor = pd.concat([table_hor, df_horario], axis=1)
    table_dia = pd.concat([table_dia, df_diario], axis=1)

    #remove dados negativos
    table_hor[table_hor['q_m3s'] < 0] = np.nan
    table_hor[table_hor['m'] < 0] = np.nan
    table_dia[table_dia['q_m3s'] < 0] = np.nan
    table_dia[table_dia['m'] < 0] = np.nan

#    #importa dicionario de erros grosseiros e escolhe estacao
#    dicionario_erros = json.load(open('erros_grosseiros.txt'))
#    erros_estacao = dicionario_erros[posto_nome]
#    #trata a matriz de erros
#    try:
#        erros_estacao = np.hstack(erros_estacao)
#    except ValueError:
#        pass
#    #remove erros grosseiros da serie observada
#    table_hor.loc[pd.to_datetime(erros_estacao), 'q_m3s'] = np.nan

    #exporta observado para csv
#    table_hor.to_csv('vazao_'+posto_nome+'.csv')
    #table_dia.to_csv(posto_nome+'_telemetrica.csv')

    plt.figure()
    plt.plot(table_hor['q_m3s'], label = "Observado", linewidth = 0.3)
    plt.title('Serie ' + posto_nome)
    plt.xlabel('Data')
    plt.ylabel('Q [m3s-1]')
#    plt.savefig('vazao_'+posto_nome+'.png', dpi = 300)
    plt.close()

    print(posto_nome, 'acabou - ', list(postos_vazao).index(posto_nome)+1,"/",
          len(postos_vazao))
print(df)
df

#REMOVE COTAS CONSTANTES ------ AQUI APLICADO PARA 96 OBSERVACOES DE 15 MIN - 24 HORAS
df2 = df.groupby((df['m'].shift()!=df['m']).cumsum()).filter(lambda x: len(x) >= 96)
df['m'] = np.where(df.index.isin(df2.index),np.nan,df['m'])
df.dropna()
