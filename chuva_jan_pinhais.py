import numpy as np
import pandas as pd
import datetime as dt
import csv
import seaborn as sns
import matplotlib.pyplot as plt
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

posto_nome = 'Pinhais'
posto_codigo = '25254905'

########## SERIES 15 MIN ##########
print('Coletando dados brutos',posto_nome)
t_ini = dt.datetime(1997, 1, 1,  0,  0) #AAAA, M, D, H, Min
t_fim = dt.datetime.now()

#coleta dados de precipitacao
dados = coletar_dados(t_ini,t_fim, posto_codigo, '(7)')
dados.columns = ['chuva_mm', 'sensor']
dados = dados.drop('sensor', 1)

#converte indice para formato DATETIME ISO UTC
dados.index = pd.to_datetime(dados.index, utc=True).rename('datahora')
dados["chuva_mm"] = pd.to_numeric(dados["chuva_mm"], downcast = "float")

########## TRATA SERIES 15 MIN ##########

#DADOS BRUTOS -> FLAG 0
#DADO BRUTO BAIXADO SEM VALOR -> FLAG 1
dados['flag'] = np.where(dados['chuva_mm'].isnull(), 1, 0)

# cria DFs padrão de data, para serem preenchidas com os dados baixados
t_ini = dados.index[0]
t_fim = dados.index[-1]

date_rng_15min = pd.date_range(start=t_ini, end=t_fim,freq='15min',tz="UTC")
table_15min = pd.DataFrame(date_rng_15min, columns=['datahora'])
table_15min['datahora']= pd.to_datetime(table_15min['datahora'])
table_15min = table_15min.set_index('datahora')
df_15min = pd.merge(table_15min, dados, how='left',
                    left_index=True, right_index=True)
df_15min = df_15min[~df_15min.index.duplicated(keep='first')]

#DATA SEM REGISTRO NA SERIE DE DADOS BRUTOS -> FLAG 2
df_15min['flag'] = np.where(df_15min['flag'].isnull(), 2, df_15min['flag'])

#SINALIZA A OCORRENCIA DE VALORES NEGATIVOS -> FLAG 3
#SINALIZA A OCORRENCIA DE VALORES SUPERIORES A 45 MM -> FLAG 3
#REMOVE VALORES DE COTA NEGATIVOS
df_15min['flag'] = np.where((df_15min['chuva_mm'] < 0), 3, df_15min['flag'])
df_15min['chuva_mm'] = np.where((df_15min['chuva_mm'] < 0
                                 ), np.nan, df_15min['chuva_mm'])
df_15min['flag'] = np.where((df_15min['chuva_mm'] >45), 3, df_15min['flag'])
df_15min['chuva_mm'] = np.where((df_15min['chuva_mm'] > 45
                                 ), np.nan, df_15min['chuva_mm'])

#SINALIZA PERSISTENCIA DE VALORES NAO NULOS -> FLAG 4
# H <= 2MM <- 6 HORAS = 24 REGISTROS
# H > 2MM <- 1 HORA = 4 REGISTROS
dados2 = df_15min.groupby((df_15min['chuva_mm'].
                           shift()!=df_15min['chuva_mm']).cumsum()
                          ).filter(lambda x: len(x) >= 24)
dados2 = dados2[dados2['chuva_mm']>0]
dados2 = dados2[dados2['chuva_mm']<=2]
dados3 = df_15min.groupby((df_15min['chuva_mm'].
                           shift()!=df_15min['chuva_mm']).cumsum()
                          ).filter(lambda x: len(x) >= 4)
dados3 = dados3[dados3['chuva_mm']>0]
dados3 = dados3[dados3['chuva_mm']>2]
df_15min['flag'] = np.where(df_15min.index.isin(dados2.index),
                            4, df_15min['flag'])
df_15min['flag'] = np.where(df_15min.index.isin(dados3.index),
                            4, df_15min['flag'])
df_15min['chuva_mm'] = np.where(df_15min.index.isin(dados2.index),
                            np.nan, df_15min['chuva_mm'])
df_15min['chuva_mm'] = np.where(df_15min.index.isin(dados3.index),
                            np.nan, df_15min['chuva_mm'])

#COLUNA FLAG PARA INTEIRO
df_15min['flag'] = df_15min['flag'].astype(int)

########## TRANSFORMA SERIE MENSAL ##########

df_15min.drop(['flag'], axis=1, inplace = True)

df_15min['count'] = np.where(df_15min['chuva_mm'].notnull(), 1, 0)
df_mensal = (df_15min.resample("M", closed='right', label='right').
              agg({'count' : np.sum, 'chuva_mm' : np.sum}))

df_mensal.drop('count', axis=1, inplace=True)

df_mensal

df_mensal[df_mensal.index.month == 1]

plt.figure(figsize=(8.3,3))
sns.boxplot(x="chuva_mm", data=df_mensal[df_mensal.index.month == 1])
sns.stripplot(x="chuva_mm", color='black',alpha=0.5,data=df_mensal[df_mensal.index.month == 1])
sns.stripplot(x=[134.6], color='red',alpha=1)
plt.xlabel("Precipitacao Janeiro [mm]", size=10)
plt.savefig('../boxplot_janeiro.png', dpi = 300,
            bbox_inches = 'tight')
