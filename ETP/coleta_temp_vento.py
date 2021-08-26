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

postos = pd.read_excel('inventario_banco_simepar_jul2021.xlsx')

# ORGAOS QUE FALTAM COLETAR
# orgaos = ['SAISP', 'CEMADEN', 'Simepar', 'PETROBRAS', 'ELEJOR', 'Inmet',
#        'Epagri/Ciram', 'Águas Paraná', 'Mascarenhas', 'Maua',
#        'Testes Laboratório', 'PCH Verde 4A', 'PCH Arturo Andreoli',
#        'UHE Pedra do Cavalo', 'SANEPAR', 'Orbcopel', 'Ro',
#        'PCH São Francisco', 'Caminhos do Paraná', 'ValeES', 'Duke',
#        'UHE Colíder', 'Klabin', 'INVESTCO', 'Suderhsa', 'Santa Fé',
#        'FEPAGRO', 'Lactec', 'Iapar', 'LIGHT', 'Ludesa', 'Bocaiuva',
#        'Rio Bonito', 'ECOVIA', 'COMPERJ', 'UHE Queimado',
#        'PCH Novo Horizonte', 'PCH Cavernoso II', 'PCH Alto Sucuriú',
#        'PCH Figueirópolis', 'Copel', 'Simepar CampoE', 'Porto Primavera',
#        'OrbSrh', 'Constremac', 'Ta', 'Corumba', 'SimeparTorres',
#        'ENERPEIXE', 'Tractebel']
orgao = 'Simepar'
postos_orgao = postos[postos.orgsigla == orgao].reset_index()

#postos com dados
dfselecao = pd.DataFrame()

#define manualmente início da serie a ser coletada
t_ini = dt.datetime(1990,1,1)
t_fim = dt.datetime.now()
#Cria DF padrao horario para ser preenchido
date_rng = pd.date_range(start=t_ini, end=t_fim, freq='D', tz='utc')
table_d = pd.DataFrame(date_rng, columns=['date'])
table_d['data']= pd.to_datetime(table_d['date'])
table_d = table_d.set_index('data')
table_d= table_d[[]]

## COLETA DADOS VENTO
for idx, row in postos_orgao.iterrows():
    start1 = time.time()
    estcodigo = row['estcodigo']
    estnome = row['estnome']
    orgsigla = row['orgsigla']

    ########## SERIES 15 MIN ##########
    print(f'{idx+1}/{len(postos_orgao)} - Coletando dados brutos - {estnome}')
    #coleta dados de vento e temperatura
    vel_vento = coletar_dados(t_ini,t_fim, estcodigo, '(8)')
    vel_vento.columns = ['v_vento', 'sensor']
    temp_media = coletar_dados(t_ini,t_fim, estcodigo,'(1)')
    temp_media.columns = ['t_med', 'sensor']
    dados = pd.merge(vel_vento['v_vento'],temp_media['t_med'],how='outer',
                     left_index=True,right_index=True)

    if dados.empty:
        #nao armazena dados vazios, e passa para proxima estacao
        end1 = time.time()
        print('Tempo decorrido ', end1-start1)
        print(f'{idx+1}/{len(postos_orgao)} - {estcodigo} - {orgsigla} - Sem dados disponíveis')
        continue

    #converte indice para formato DATETIME ISO UTC
    dados.index = pd.to_datetime(dados.index, utc=True).rename('datahora')
    dados['v_vento'] = pd.to_numeric(dados['v_vento'], downcast="float")
    dados['t_med'] = pd.to_numeric(dados['t_med'], downcast="float")

    #Agrupa em serie horaria, com intervalo fechado à direita (acumulado 0:01 a 1:00)
    dados_hor = (dados.resample("H", closed='right', label='right').
                 agg({'v_vento':np.mean, 't_med':np.mean}))

    dados_dia = (dados_hor.resample("D", closed='right').
                 agg({'v_vento':np.mean, 't_med':np.mean}))

    #Unifica dados no DF padrao
    #Se dado vazio, entao preenche com nan
    try:
        df_dia = pd.merge(table_d, dados_dia, left_index = True,
                          right_index = True, how = 'left')
    except:
        df_dia = table_d.copy()
        df_dia['v_vento'] = np.nan
        df_dia['t_med'] = np.nan

    df_dia = df_dia[~df_dia.index.duplicated(keep='first')]
    #Exporta serie
    #define inicio da serie como primeiro dado observado, seja vento ou temperatura
    inicio = dados_dia['v_vento'].first_valid_index()
    if dados_dia['t_med'].first_valid_index() < inicio:
        inicio = dados_dia['t_med'].first_valid_index()
    df_dia = df_dia.loc[inicio:]
    df_dia.index = df_dia.index.strftime('%Y-%m-%d')
    df_dia.to_csv(f'./Dados/{orgsigla}_{estcodigo}.csv', float_format='%.2f')

    #Atualiza df com estacoes com dados
    dfselecao = dfselecao.append(row)
    end1 = time.time()
    print('Tempo decorrido ', end1-start1)
    print(f'{idx+1}/{len(postos_orgao)} - {estcodigo} - {orgsigla} - Início em {df_dia.index[0]}')

#exporta df com dados das estacoes com dados
dfselecao.to_csv(f'./info_{orgao}.csv')
