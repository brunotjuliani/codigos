import numpy as np
import pandas as pd
import datetime as dt
import psycopg2, psycopg2.extras
import pyet


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

#posto_nome = 'Apucaraninha_Montante'
#posto_codigo = '23735103'

posto_nome = 'Londrina'
posto_codigo = '23185109'


## COLETA DADOS VAZAO

########## SERIES 15 MIN ##########
print('Iniciando ',posto_nome)
t_ini = dt.datetime(1997, 1, 1,  0,  0) #AAAA, M, D, H, Min
t_fim = dt.datetime.now()

#Temperatura maxima
print('Coletando Temperatura Maxima de ',posto_nome)
tempmax = coletar_dados(t_ini,t_fim, posto_codigo, '(4)')
tempmax.columns = ['Tmax', 'sensor']
tempmax

#Temperatura minima
print('Coletando Temperatura Minima de ',posto_nome)
tempmin = coletar_dados(t_ini,t_fim, posto_codigo, '(5)')
tempmin.columns = ['Tmin', 'sensor']
tempmin

#Velocidade media do vento
print('Coletando Velocidade Media de ',posto_nome)
vento = coletar_dados(t_ini,t_fim, posto_codigo, '(8)')
vento.columns = ['Vento', 'sensor']
vento

#Radiacao Solar
print('Coletando Radiacao Solar de ',posto_nome)
solar = coletar_dados(t_ini,t_fim, posto_codigo, '(6)')
solar.columns = ['Rad_Solar', 'sensor']
solar

#Umidade Relativa
print('Coletando Umidade Relativa de ',posto_nome)
rh = coletar_dados(t_ini,t_fim, posto_codigo, '(2)')
rh.columns = ['Rh', 'sensor']
rh

#concatena dataframes
dados = pd.merge(tempmax['Tmax'],tempmin['Tmin'],how='outer',
                 left_index=True,right_index=True)
dados = pd.merge(dados,vento['Vento'],how='outer',
                 left_index=True,right_index=True)
dados = pd.merge(dados,solar['Rad_Solar'],how='outer',
                 left_index=True,right_index=True)
dados = pd.merge(dados,rh['Rh'],how='outer',
                 left_index=True,right_index=True)
dados

#converte indice para formato DATETIME ISO UTC
dados.index = pd.to_datetime(dados.index).rename('datahora_UTC')
dados["Tmax"] = pd.to_numeric(dados["Tmax"], downcast = "float")
dados["Tmin"] = pd.to_numeric(dados["Tmin"], downcast = "float")
dados["Vento"] = pd.to_numeric(dados["Vento"], downcast = "float")
dados["Rad_Solar"] = pd.to_numeric(dados["Rad_Solar"], downcast = "float")
dados["Rh"] = pd.to_numeric(dados["Rh"], downcast = "float")

# cria DFs padrão de data, para serem preenchidas com os dados baixados
date_rng_diario = pd.date_range(start=t_ini, end=t_fim, freq='D')
table_dia = pd.DataFrame(date_rng_diario, columns=['data'])
table_dia['data']= pd.to_datetime(table_dia['data'])
table_dia = table_dia.set_index('data')

# agrupa em dados horarios, com intervalo fechado à direita (acumulado/media da 0:01 a 1:00);
# coluna count resulta a soma (contagem) dos "1", coluna valor resulta na media dos valores;
# para os valores de cont < 2, substitui o dado em 'valor' por NaN:
dados['count'] = 1
df_horario = dados.resample("H", closed='right'
                            ).agg({'count':np.sum, 'Tmax':np.mean,
                                   'Tmin':np.mean, 'Vento':np.mean,
                                   'Rad_Solar':np.sum, 'Rh':np.mean})
#df_horario.loc[df_horario['count'] < 4, ['pme']] = np.nan

# cria coluna com valores 1;
# agrupa em dados diarios, com intervalo fechado à direita (acumulado/media da 1:00 a 0:00);
# coluna count resulta a soma (contagem) dos "1", coluna valor resulta na media dos valores;
# para os valores de cont < 12, substitui o dado em 'valor' por NaN:
df_horario['count'] = 1
df_diario = df_horario.resample("D", closed='left'
                                ).agg({'count':np.sum, 'Tmax':np.mean,
                                       'Tmin':np.mean, 'Vento':np.mean,
                                       'Rad_Solar':np.sum, 'Rh':np.mean})
#df_diario.loc[df_diario['count'] < 24, ['pme']] = np.nan

# remove colunas 'count' dos dataframes
df_horario.drop(df_horario.columns[0], axis=1, inplace=True)
df_diario.drop(df_diario.columns[0], axis=1, inplace=True)
table_dia = pd.concat([table_dia, df_diario], axis=1)

table_dia['Rad_Solar'] = table_dia['Rad_Solar']*15*60/1000000

#exporta observado para csv
table_dia.to_csv('/discolocal/bruno/Observado/Teste/'+posto_nome+
                 '_dados_etp.csv',date_format='%Y-%m-%dT%H:%M:%SZ',
                 sep = ";",float_format = '%.3f')

print(posto_nome, 'acabou - ')

table_dia
