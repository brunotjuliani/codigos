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
postos = pd.read_csv(f'dados_selecao_direcao.csv', index_col=0)
postos = postos.iloc[-1:]
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
    vel_vento = coletar_dados(t_ini,t_fim, estcodigo, '(8)')
    vel_vento.columns = ['vel_vento', 'sensor']
    dir_vento = coletar_dados(t_ini,t_fim, estcodigo,'(10)')
    dir_vento.columns = ['dir_vento', 'sensor']
    dados = pd.merge(vel_vento['vel_vento'],dir_vento['dir_vento'],how='outer',
                     left_index=True,right_index=True)

    if dados.empty:
        #nao armazena dados vazios, e passa para proxima estacao
        end1 = time.time()
        print('Tempo decorrido ', end1-start1)
        print(f'{idx+1}/{len(postos)} - {estcodigo} - {orgsigla} - Sem dados disponíveis')
        continue

    #converte indice para formato DATETIME ISO UTC
    dados.index = pd.to_datetime(dados.index, utc=True).rename('datahora')
    dados['dir_vento'] = pd.to_numeric(dados['dir_vento'], downcast="float")
    dados['vel_vento'] = pd.to_numeric(dados['vel_vento'], downcast="float")

    #Exporta dados completos
    dados.to_csv(f'./Direcao_Vento/{orgsigla}_{estcodigo}.csv', float_format='%.2f')

    #Atualiza df com estacoes com dados
    dfselecao = dfselecao.append(row)
    end1 = time.time()
    print('Tempo decorrido ', end1-start1)
    print(f'{idx+1}/{len(postos)} - {estcodigo} - {orgsigla}')
