import numpy as np
import pandas as pd
import datetime as dt
import psycopg2, psycopg2.extras


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

posto_nome = 'apucaraninha_montante'
posto_codigo = '23735103'

# posto_nome = 'reservatorio_fiu'
# posto_codigo = '23745094'

# ## COLETA DADOS PRECIP
#
# ########## SERIES 15 MIN ##########
# print('Coletando dados brutos',posto_nome)
# t_ini = dt.datetime(2010, 1, 1,  0,  0) #AAAA, M, D, H, Min
# t_fim = dt.datetime.now()
#
# #coleta dados de precipitacao
# dados = coletar_dados(t_ini,t_fim, posto_codigo, '(7)')
# dados.columns = ['pme', 'sensor_prec']
#
# #converte indice para formato DATETIME ISO UTC
# dados.index = pd.to_datetime(dados.index).rename('datahora_UTC')
# dados["pme"] = pd.to_numeric(dados["pme"], downcast = "float")
# dados['count'] = 1
#
# # cria DFs padrão de data, para serem preenchidas com os dados baixados
# date_rng_diario = pd.date_range(start=t_ini, end=t_fim, freq='D')
# table_dia = pd.DataFrame(date_rng_diario, columns=['data'])
# table_dia['data']= pd.to_datetime(table_dia['data'])
# table_dia = table_dia.set_index('data')
#
# # agrupa em dados horarios, com intervalo fechado à direita (acumulado/media da 0:01 a 1:00);
# # coluna count resulta a soma (contagem) dos "1", coluna valor resulta na media dos valores;
# # para os valores de cont < 2, substitui o dado em 'valor' por NaN:
# df_horario = dados.resample("H", closed='right').agg({'count' : np.sum,
#                                                       'pme' : np.sum})
# #df_horario.loc[df_horario['count'] < 4, ['pme']] = np.nan
#
# # cria coluna com valores 1;
# # agrupa em dados diarios, com intervalo fechado à direita (acumulado/media da 1:00 a 0:00);
# # coluna count resulta a soma (contagem) dos "1", coluna valor resulta na media dos valores;
# # para os valores de cont < 12, substitui o dado em 'valor' por NaN:
# df_horario['count'] = 1
# df_diario = df_horario.resample("D", closed='left').agg({'count':np.sum,
#                                                          'pme' : np.sum})
# #df_diario.loc[df_diario['count'] < 24, ['pme']] = np.nan
#
# # remove colunas 'count' dos dataframes
# df_horario.drop(df_horario.columns[0], axis=1, inplace=True)
# df_diario.drop(df_diario.columns[0], axis=1, inplace=True)
#
# table_dia = pd.concat([table_dia, df_diario], axis=1)
# table_dia['pme'] = np.where((table_dia['pme'] > 250), 0, table_dia['pme'])
#
# #exporta observado para csv
# table_dia.to_csv('/discolocal/bruno/Observado/Teste/'+posto_nome+'_plu_diario.csv',
#                 date_format='%Y-%m-%dT%H:%M:%SZ', sep = ";",
#                 float_format = '%.3f')
#
# print(posto_nome, 'acabou - ')

## COLETA DADOS VAZAO

########## SERIES 15 MIN ##########
print('Coletando dados brutos',posto_nome)
t_ini = dt.datetime(2015, 1, 1,  0,  0) #AAAA, M, D, H, Min
t_fim = dt.datetime.now()

#coleta dados de precipitacao
dados = coletar_dados(t_ini,t_fim, posto_codigo, '(33)')
dados.columns = ['q_m3s', 'sensor_prec']

#converte indice para formato DATETIME ISO UTC
dados.index = pd.to_datetime(dados.index).rename('datahora_UTC')
dados["q_m3s"] = pd.to_numeric(dados["q_m3s"], downcast = "float")
dados['count'] = 1

# cria DFs padrão de data, para serem preenchidas com os dados baixados
date_rng_diario = pd.date_range(start=t_ini, end=t_fim, freq='D')
table_dia = pd.DataFrame(date_rng_diario, columns=['data'])
table_dia['data']= pd.to_datetime(table_dia['data'])
table_dia = table_dia.set_index('data')

# agrupa em dados horarios, com intervalo fechado à direita (acumulado/media da 0:01 a 1:00);
# coluna count resulta a soma (contagem) dos "1", coluna valor resulta na media dos valores;
# para os valores de cont < 2, substitui o dado em 'valor' por NaN:
df_horario = dados.resample("H", closed='right').agg({'count' : np.sum,
                                                      'q_m3s' : np.mean})
#df_horario.loc[df_horario['count'] < 4, ['q_m3s']] = np.nan

# cria coluna com valores 1;
# agrupa em dados diarios, com intervalo fechado à direita (acumulado/media da 1:00 a 0:00);
# coluna count resulta a soma (contagem) dos "1", coluna valor resulta na media dos valores;
# para os valores de cont < 12, substitui o dado em 'valor' por NaN:
df_horario['count'] = 1
df_diario = df_horario.resample("D", closed='left').agg({'count':np.sum,
                                                         'q_m3s' : np.mean})
#df_diario.loc[df_diario['count'] < 24, ['q_m3s']] = np.nan

# remove colunas 'count' dos dataframes
df_horario.drop(df_horario.columns[0], axis=1, inplace=True)
df_diario.drop(df_diario.columns[0], axis=1, inplace=True)

table_dia = pd.concat([table_dia, df_diario], axis=1)

#exporta observado para csv
table_dia.to_csv('/discolocal/bruno/Observado/Teste/'+posto_nome+'_flu_diario.csv',
                date_format='%Y-%m-%dT%H:%M:%SZ', sep = ";",
                float_format = '%.3f')

print(posto_nome, 'acabou - ')
