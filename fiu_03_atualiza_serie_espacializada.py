import numpy as np
import pandas as pd
import datetime as dt
import csv
import math
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

def haversine(lon1, lat1, lon2, lat2):
    rad = math.pi / 180  # degree to radian
    R = 6378.1  # earth average radius at equador (km)
    dlon = (lon2 - lon1) * rad
    dlat = (lat2 - lat1) * rad
    a = (math.sin(dlat / 2)) ** 2 + math.cos(lat1 * rad) * \
        math.cos(lat2 * rad) * (math.sin(dlon / 2)) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c #retorna distancia em km
    return(d)

#Lista postos de precipitacao com as seguintes informacoes
# Nome : [codigo simepar, codigo ANA, latitude, longitute, altitude]
postos_precip = {
    'Apucaraninha_Montante':['23735103', '2351079', '-23.73056', '-51.03778', '688'],
    'Barragem_PCH_Apucaraninha':['23745090', '2350015', '-23.75001', '-50.90772', '611'],
    'Reservatorio_Fiu':['23745094', '2350016', '-23.74906', '-50.94049', '430']
    }

## LEITURA DO ARQUIVO COM SERIE HISTORICA ESPACIALIZADA
pme_hist = pd.read_csv('/discolocal/bruno/Fiu/pme_fiu.csv', index_col='datahora')
pme_hist.index = pd.to_datetime(pme_hist.index, utc=True)

## LEITURA DA GRADE DA BACIA
arquivo_grade = '/discolocal/bruno/Fiu/pontos_grade_fiu.csv'
grade = pd.read_csv(arquivo_grade, sep=',')

## DEFINICAO DA DATA PARA ATUALIZAR
t_ini = pme_hist.index[-1] - dt.timedelta(days = 5)
t_fim = pd.Timestamp(dt.datetime.now(dt.timezone.utc))

## INICIALIZA DATAFRAMES DE ESPACIALIZACAO
DF_postos = pd.DataFrame()
DF_grade = pd.DataFrame()
DF_grade.index.name = 'datahora'
DF_dists = pd.DataFrame()


## REALIZA COLETA PARA CADA PONTO E ORGANIZA PARA ESPACIALIZACAO
posto_nome='Apucaraninha_Montante'
posto_informacoes=['23735103', '2351079', '-23.73056', '-51.03778', '688']


## REALIZA COLETA PARA CADA PONTO E ORGANIZA PARA ESPACIALIZACAO
for posto_nome, posto_informacoes in postos_precip.items():
    posto_codigo = posto_informacoes[0]
    posto_ana = posto_informacoes[1]
    posto_lat = float(posto_informacoes[2])
    posto_long = float(posto_informacoes[3])
    posto_alt = float(posto_informacoes[4])

    #Calcula a distancia (km) entre o posto e todos os pontos da grade
    for pi in grade.index:
        ponto_x = grade.loc[pi].x
        ponto_y = grade.loc[pi].y
        dist = haversine(posto_long, posto_lat, ponto_x, ponto_y)
        DF_dists.loc[pi,posto_nome] = dist

    #Coleta dados 15 min
    #coleta dados de precipitacao
    dados = coletar_dados(t_ini,t_fim, posto_codigo, '(7)')
    dados.columns = ['chuva_mm', 'sensor']
    dados = dados.drop('sensor', 1)
    dados.index = pd.to_datetime(dados.index, utc=True).rename('datahora')
    dados["chuva_mm"] = pd.to_numeric(dados["chuva_mm"], downcast = "float")

    #Trata serie 15 min
    #Dado sem valor
    dados['flag'] = np.where(dados['chuva_mm'].isnull(), 1, 0)

    #Cria DFs padrão de data, para serem preenchidas com os dados baixados
    # cria DFs padrão de data, para serem preenchidas com os dados baixados
    t_ini_15min = dados.index[0]
    t_fim_15min = dados.index[-1]
    date_rng_15min = pd.date_range(start=t_ini_15min, end=t_fim_15min,
                                   freq='15min',tz="UTC")
    table_15min = pd.DataFrame(date_rng_15min, columns=['datahora'])
    table_15min['datahora']= pd.to_datetime(table_15min['datahora'])
    table_15min = table_15min.set_index('datahora')
    df_15min = pd.merge(table_15min, dados, how='left',
                        left_index=True, right_index=True)
    df_15min = df_15min[~df_15min.index.duplicated(keep='first')]

    #Data sem registro na serie
    df_15min['flag'] = np.where(df_15min['flag'].isnull(), 2, df_15min['flag'])

    #Valores negativos e acumulados de 15min superiores a 45mm
    df_15min['flag'] = np.where((df_15min['chuva_mm'] < 0), 3, df_15min['flag'])
    df_15min['chuva_mm'] = np.where((df_15min['chuva_mm'] < 0
                                     ), np.nan, df_15min['chuva_mm'])
    df_15min['flag'] = np.where((df_15min['chuva_mm'] >45), 3, df_15min['flag'])
    df_15min['chuva_mm'] = np.where((df_15min['chuva_mm'] > 45
                                     ), np.nan, df_15min['chuva_mm'])

    #Persistencia de valores não nulos
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
    df_15min.drop(['flag'], axis=1, inplace = True)

    #Transforma em serie horaria
    #Cria DFs padrao horario
    t_ini_h = df_15min.index[0].round('1h')
    t_fim_h = df_15min.index[-1]
    date_rng_horario =pd.date_range(start=t_ini_h,end=t_fim_h,freq='H',tz="UTC")
    table_hor = pd.DataFrame(date_rng_horario, columns=['date'])
    table_hor['datahora']= pd.to_datetime(table_hor['date'])
    table_hor = table_hor.set_index('datahora')
    table_hor.drop(['date'], axis=1, inplace = True)

    # agrupa em dados horarios, com intervalo fechado à direita (acumulado/media da 0:01 a 1:00);
    df_15min['count'] = np.where(df_15min['chuva_mm'].notnull(), 1, 0)
    df_horario = (df_15min.resample("H", closed='right', label='right').
                  agg({'count' : np.sum, 'chuva_mm' : np.sum}))
    #df_horario.loc[df_horario['count'] < 4, ['q_m3s']] = np.nan
    #df_horario.loc[df_horario['count'] < 4, ['m']] = np.nan

    #Remove valores horarios superiores a 90mm
    df_horario['chuva_mm'] = np.where((df_horario['chuva_mm'] > 90
                                         ), np.nan, df_horario['chuva_mm'])

    # remove colunas 'count' dos dataframes e agrupa com data padrao
    df_horario.drop('count', axis=1, inplace=True)
    table_hor = pd.merge(table_hor, df_horario, left_index = True,
                         right_index = True, how = 'left')
    table_hor = table_hor[~table_hor.index.duplicated(keep='first')]
    table_hor['status'] = '1'

    #remove primeira linha do dataframe (hora incompleta)
    table_hor = table_hor[1:]

    #Concatena serie do posto em DF_postos
    sr_posto = table_hor['chuva_mm']
    sr_posto = sr_posto.rename(posto_nome)
    DF_postos = DF_postos.join(sr_posto, how='outer')

    print(posto_nome, ' acabou - ', list(postos_precip).index(posto_nome)+1,"/",
          len(postos_precip))

## REALIZA ESPACIALIZACAO DOS DADOS NOVOS
L = len(grade)
no_postos = len(DF_postos.columns)
for i,pi in enumerate(grade.index):
    D = np.array([DF_dists.loc[pi,i] for i in DF_postos.columns]) # vetor de distancias
    W = np.array([1/(di**2) for di in D]) # vetor de pesos
    for t in DF_postos.index:
        P_t = DF_postos.loc[t].values # vetor precipitacoes
        W_t = np.array([0 if np.isnan(P_t[i]) else W[i] for i in range(no_postos)])
        prec = np.sum(W_t * np.nan_to_num(P_t))/np.sum(W_t)
        DF_grade.loc[t, pi] = np.around(prec, decimals=2)
PME = DF_grade.mean(axis=1, skipna=True)
pme_att = pd.DataFrame(PME.rename('chuva_mm').round(2))
print('Espacialização finalizada.')

## ATUALIZACAO DA SERIE HISTORICA ESPACIALIZADA
pme_final = pd.concat([pme_hist, pme_att])
pme_final = pme_final[~pme_final.index.duplicated(keep='last')]
pme_final.to_csv('/discolocal/bruno/Fiu/pme_fiu.csv', index_label='datahora',
                 float_format='%.2f', date_format='%Y-%m-%dT%H:%M:%S+00:00')
print('Atualizacao Serie Historica finalizada.')
