import numpy as np
import pandas as pd
import datetime as dt
import time
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

# PARA COLETA DOS DADOS DE ESTACOES SELECIONADAS
postos = pd.read_csv(f'dados_selecao.csv', index_col=0)
t_ini = dt.datetime(1990,1,1)
t_fim = dt.datetime.now()

#postos com dados
dfselecao = pd.DataFrame()

#Cria DF padrao horario para ser preenchido
date_rng = pd.date_range(start=t_ini, end=t_fim, freq='D', tz='utc')
table_d = pd.DataFrame(date_rng, columns=['date'])
table_d['data']= pd.to_datetime(table_d['date'])
table_d = table_d.set_index('data')
table_d= table_d[[]]

## COLETA DADOS VENTO
for idx, row in postos.iterrows():
    start1 = time.time()
    estcodigo = row['estcodigo']
    estnome = row['estnome']
    orgsigla = row['orgsigla']

    print(f'{idx+1}/{len(postos)} - Coletando dados brutos - {estnome}')
    #coleta dados de vento e temperatura
    vel_rajada = coletar_dados(t_ini,t_fim, estcodigo, '(9)')
    vel_rajada.columns = ['v_rajada', 'sensor']
    temp_max = coletar_dados(t_ini,t_fim, estcodigo,'(4)')
    temp_max.columns = ['t_max', 'sensor']
    dados = pd.merge(vel_rajada['v_rajada'],temp_max['t_max'],how='outer',
                     left_index=True,right_index=True)
    temp_min = coletar_dados(t_ini,t_fim, estcodigo,'(5)')
    temp_min.columns = ['t_min', 'sensor']
    dados = pd.merge(dados,temp_min['t_min'],how='outer',
                     left_index=True,right_index=True)

    if dados.empty:
        #nao armazena dados vazios, e passa para proxima estacao
        end1 = time.time()
        print('Tempo decorrido ', end1-start1)
        print(f'{idx+1}/{len(postos)} - {estcodigo} - {orgsigla} - Sem dados disponíveis')
        continue

    #converte indice para formato DATETIME ISO UTC
    dados.index = pd.to_datetime(dados.index, utc=True).rename('datahora')
    dados['v_rajada'] = pd.to_numeric(dados['v_rajada'], downcast="float")
    dados['t_max'] = pd.to_numeric(dados['t_max'], downcast="float")
    dados['t_min'] = pd.to_numeric(dados['t_min'], downcast="float")

    #Agrupa em serie horaria, com intervalo fechado à direita (acumulado 0:01 a 1:00)
    dados_dia = (dados.resample("D", closed='right').
                 agg({'v_rajada':np.max, 't_max':np.max, 't_min':np.min}))

    #Unifica dados no DF padrao
    #Se dado vazio, entao preenche com nan
    try:
        df_dia = pd.merge(table_d, dados_dia, left_index = True,
                          right_index = True, how = 'left')
    except:
        df_dia = table_d.copy()
        df_dia['v_rajada'] = np.nan
        df_dia['t_max'] = np.nan
        df_dia['t_min'] = np.nan
    df_dia = df_dia[~df_dia.index.duplicated(keep='first')]

    #define inicio da serie como primeiro dado observado, seja vento ou temperatura
    inicio = dados_dia.first_valid_index()
    df_dia = df_dia.loc[inicio:]

    #Le serie de temperatura e vento medio, e une com maximos/minimos
    df_anterior = pd.read_csv(f'./Dados/{orgsigla}_{estcodigo}.csv',
                              index_col='data', parse_dates=True)
    df_anterior.index = df_anterior.index.tz_localize('utc')
    df_exporta = pd.merge(df_anterior,df_dia,how='outer',
                          left_index=True,right_index=True)

    #Exporta dados completos
    df_exporta.index = df_exporta.index.strftime('%Y-%m-%d')
    df_exporta.to_csv(f'./Dados_Novo/{orgsigla}_{estcodigo}.csv', float_format='%.2f')

    #Atualiza df com estacoes com dados
    dfselecao = dfselecao.append(row)
    end1 = time.time()
    print('Tempo decorrido ', end1-start1)
    print(f'{idx+1}/{len(postos)} - {estcodigo} - {orgsigla} - Início em {df_dia.index[0]}')
