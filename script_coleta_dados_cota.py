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
dir_cota = "/discolocal/bruno/Dados_Cota"
os.chdir(dir_cota)
lista = []

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
    conn = psycopg2.connect(dbname='clim', user='hidro', password='hidrologia',
                            host='tornado', port='5432')
    consulta = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    consulta.execute(texto_psql)
    consulta_lista = consulta.fetchall()
    df_consulta =pd.DataFrame(consulta_lista,columns=['tempo','valor','sensor'])
    df_consulta.set_index('tempo', inplace=True)
    return df_consulta

postos_cota = {
                'Balsa_Nova':'25584963'
            }


## COLETA DADOS VAZAO


for posto_nome, posto_codigo in postos_cota.items():
    print('Coletando cota',posto_nome)
    t_ini = dt.datetime(1990, 1, 1,  0,  0) #AAAA, M, D, H, Min
    t_fim = dt.datetime(2020, 9, 11, 23, 59)
    dados=coletar_dados(t_ini,t_fim,posto_codigo,'(18)') #07 precip e 33 vazao

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
    df.columns = ['q_m3s', 'sensor']
    df.drop(df.tail(1).index, inplace=True)
    df['count'] = 1
    df.index = pd.to_datetime(df.index)
    #converte para hora local - GMT-3 - timezone('America/Sao_Paulo')
    df.index = df.index.tz_localize(pytz.utc).tz_convert(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %X")
    df.index = pd.to_datetime(df.index)
    df["q_m3s"] = pd.to_numeric(df["q_m3s"], downcast="float")


    # agrupa em dados horarios, com intervalo fechado à direita (acumulado/media da 0:01 a 1:00);
    # coluna count resulta a soma (contagem) dos "1", coluna valor resulta na media dos valores;
    # para os valores de cont < 2, substitui o dado em 'valor' por NaN:
    df_horario = df.resample("H", closed='right').agg({'count' : np.sum,
                                                       'q_m3s' : np.mean})
    #df_horario.loc[df_horario['count'] < 2, ['q_m3s']] = np.nan

    # cria coluna com valores 1;
    # agrupa em dados diarios, com intervalo fechado à direita (acumulado/media da 1:00 a 0:00);
    # coluna count resulta a soma (contagem) dos "1", coluna valor resulta na media dos valores;
    # para os valores de cont < 12, substitui o dado em 'valor' por NaN:
    df_horario['count'] = 1
    df_diario = df_horario.resample("D", closed='left').agg({'count':np.sum,
                                                             'q_m3s' : np.mean})
    df_diario.loc[df_diario['count'] < 12, ['q_m3s']] = np.nan

    # remove colunas 'count' dos dataframes
    df.drop(df_horario.columns[0], axis=1, inplace=True)
    df_horario.drop(df_horario.columns[0], axis=1, inplace=True)
    df_diario.drop(df_diario.columns[0], axis=1, inplace=True)

    table_hor = pd.concat([table_hor, df_horario], axis=1)
    table_dia = pd.concat([table_dia, df_diario], axis=1)

    #remove dados negativos
    table_hor[table_hor['q_m3s'] < 0] = np.nan
    table_dia[table_dia['q_m3s'] < 0] = np.nan

    #exporta observado para csv
    #table_hor.to_csv('cota_'+posto_nome+'.csv')
    table_dia.to_csv(posto_nome+'_cota.csv')

    print(posto_nome, 'acabou - ', list(postos_cota).index(posto_nome)+1,"/",
          len(postos_vazao))
