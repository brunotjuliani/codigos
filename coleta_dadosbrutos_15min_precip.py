import numpy as np
import pandas as pd
import datetime as dt
import csv
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

postos_precip = {
            'Aguas_do_Vere':['25465256', '-25.7737', '-52.9329'],
            'Balsa_Jaracatia':['25345816', '-25.5832', '-53.2668'],
            'Bituruna':['26065150', '-26.0639', '-51.5083'],
            'Boa_Vista_da_Aparecida':['25315021', '-25.5225', '-53.3558'],
            'Cascavel':['24535333', '-24.8845', '-53.5547'],
            'Coronel_Domingos_Soares':['25825217', '-26.03729', '-51.98156'],
            'Curitiba':['25264916', '-25.44817', '-49.23033'],
            'Derivacao_do_Rio_Jordao':['25755210', '-25.75922', '-52.10889'],
            'Divisa':['26055019', '-26.0833', '-50.3166'],
            'Entre_Rios':['25335129', '-25.5459', '-51.4884'],
            'Fernandes_Pinheiro':['25275035', '-25.4532', '-50.5839'],
            'Fluviopolis':['26025035', '-26.0333', '-50.5833'],
            'Foz_do_Areia_Hid':['26005139', '-26.00639', '-51.66754'],
            'Foz_do_Areia_Met':['26055139', '-26.0037', '-51.6679'],
            'Foz_do_Cachoeira':['26355045', '-26.5833', '-50.75'],
            'Foz_do_Chopim':['25345306', '-25.5713', '-53.1135'],
            'Foz_do_Iguacu':['25245437', '-25.4059', '-54.6167'],
            'Foz_do_Timbo':['26105047', '-26.29452', '-50.89522'],
            'Fragosos':['26094923', '-26.15', '-49.3833'],
            'Francisco_Beltrao':['26055305', '-26.0593', '-53.06548'],
            'Guarapuava':['25215130', '-25.3845', '-51.4935'],
            'Jangada':['26225115', '-26.3666', '-51.25'],
            'Lapa':['25474946', '-25.7817', '-49.7598'],
            'Madeireira_Gavazzoni':['25485116', '-25.80682', '-51.22884'],
            'Nova_Prata_do_Iguacu':['25345331', '-25.5666', '-53.5166'],
            'Palmas':['26285158', '-26.4682', '-51.9762'],
            'Palmital_do_Meio':['26025109', '-26.02999', '-51.14149'],
            'Pato_Branco':['26075241', '-26.1229', '-52.6514'],
            'Pinhais':['25254905', '-25.3907', '-49.1299'],
            'Pinhao':['25385157', '-25.64944', '-51.9625'],
            'Ponta_Grossa':['25135001', '-25.0137', '-50.1524'],
            'Pontilhao':['25555031', '-25.9166', '-50.5166'],
            'Porto_Amazonas':['25334953', '-25.55', '-49.8833'],
            'Porto_Capanema':['25345435', '-25.6154', '-53.7923'],
            'Porto_Palmeirinha':['26015237', '-26.0291', '-52.6283'],
            'Porto_Santo_Antonio':['25235306', '-25.3833', '-53.1'],
            'Porto_Vitoria':['26105114', '-26.1666', '-51.2333'],
            'Reservatorio_Salto_Caxias':['25325329', '-25.5333', '-53.4833'],
            'Rio_Negro':['26064948', '-26.1097', '-49.80194'],
            'Salto_Cataratas':['25415426', '-25.6833', '-54.4333'],
            'Salto_Caxias_Hid':['25325330', '-25.5333', '-53.5'],
            'Salto_Caxias_Met':['25315329', '-25.52092', '-53.49412'],
            'Salto_Osorio':['25315301', '-25.52213', '-53.03087'],
            'Santa_Cruz_do_Timbo':['26125049', '-26.38392', '-50.87826'],
            'Sao_Bento':['25564947', '-25.9333', '-49.7833'],
            'Sao_Mateus_do_Sul':['25525023', '-25.87702', '-50.38755'],
            'Sao_Miguel_do_Iguacu':['25115408', '-25.3528', '-54.2546'],
            'Segredo':['25475206', '-25.7911', '-52.11895'],
            'Solais_Novo':['26055155', '-26.0833', '-51.9166'],
            'Uniao_da_Vitoria_Hid':['26145104', '-26.22772', '-51.08059'],
            'Uniao_da_Vitoria_Met':['26145103', '-26.22825', '-51.06827'],
            'Vossoroca':['25494905', '-25.8166', '-49.0833'],
            }


## COLETA DADOS PRECIPITACAO
for posto_nome, posto_informacoes in postos_precip.items():
    posto_codigo = posto_informacoes[0]
    posto_lat = posto_informacoes[1]
    posto_long = posto_informacoes[2]

    ########## SERIES 15 MIN ##########
    print('Coletando dados brutos',posto_nome)
    t_ini = dt.datetime(1997, 1, 1,  0,  0) #AAAA, M, D, H, Min
    t_fim = dt.datetime.now()

    #coleta dados de precipitacao
    dados = coletar_dados(t_ini,t_fim, posto_codigo, '(7)')
    dados.columns = ['h_mm', 'sensor_cota']
    dados = dados.drop('sensor_cota', 1)

    #converte indice para formato DATETIME ISO UTC
    dados.index = pd.to_datetime(dados.index, utc=True).rename('datahora_UTC')
    dados["h_mm"] = pd.to_numeric(dados["h_mm"], downcast = "float")

    ########## TRATA SERIES 15 MIN ##########

    #DADOS BRUTOS -> FLAG 0
    #DADO BRUTO BAIXADO SEM VALOR -> FLAG 1
    dados['flag'] = np.where(dados['h_mm'].isnull(), 1, 0)

    # cria DFs padrão de data, para serem preenchidas com os dados baixados
    t_ini = dados.index[0]
    t_fim = dados.index[-1]

    date_rng_15min = pd.date_range(start=t_ini, end=t_fim,freq='15min',tz="UTC")
    table_15min = pd.DataFrame(date_rng_15min, columns=['datahora'])
    table_15min['datahora_UTC']= pd.to_datetime(table_15min['datahora'])
    table_15min = table_15min.set_index('datahora_UTC')
    table_15min.drop(['datahora'], axis=1, inplace = True)
    df_15min = pd.merge(table_15min, dados, how='left',
                        left_index=True, right_index=True)
    df_15min = df_15min[~df_15min.index.duplicated(keep='first')]

    #DATA SEM REGISTRO NA SERIE DE DADOS BRUTOS -> FLAG 2
    df_15min['flag'] = np.where(df_15min['flag'].isnull(), 2, df_15min['flag'])

    #SINALIZA A OCORRENCIA DE VALORES NEGATIVOS -> FLAG 3
    #SINALIZA A OCORRENCIA DE VALORES SUPERIORES A 45 MM -> FLAG 3
    #REMOVE VALORES DE COTA NEGATIVOS
    df_15min['flag'] = np.where((df_15min['h_mm'] <0), 3, df_15min['flag'])
    df_15min['h_mm'] = np.where((df_15min['h_mm'] <0), np.nan, df_15min['h_mm'])
    df_15min['flag'] = np.where((df_15min['h_mm'] >45), 3, df_15min['flag'])
    df_15min['h_mm'] = np.where((df_15min['h_mm']>45), np.nan, df_15min['h_mm'])

    #SINALIZA PERSISTENCIA DE VALORES NAO NULOS -> FLAG 4
    # H <= 2MM <- 6 HORAS = 24 REGISTROS
    # H > 2MM <- 1 HORA = 4 REGISTROS
    dados2 = df_15min.groupby((df_15min['h_mm'].
                               shift()!=df_15min['h_mm']).cumsum()
                              ).filter(lambda x: len(x) >= 24)
    dados2 = dados2[dados2['h_mm']>0]
    dados2 = dados2[dados2['h_mm']<=2]
    dados3 = df_15min.groupby((df_15min['h_mm'].
                               shift()!=df_15min['h_mm']).cumsum()
                              ).filter(lambda x: len(x) >= 4)
    dados3 = dados3[dados3['h_mm']>0]
    dados3 = dados3[dados3['h_mm']>2]

    df_15min['flag'] = np.where(df_15min.index.isin(dados2.index),
                                4, df_15min['flag'])
    df_15min['flag'] = np.where(df_15min.index.isin(dados3.index),
                                4, df_15min['flag'])
    df_15min['h_mm'] = np.where(df_15min.index.isin(dados2.index),
                                np.nan, df_15min['h_mm'])
    df_15min['h_mm'] = np.where(df_15min.index.isin(dados3.index),
                                np.nan, df_15min['h_mm'])

    #COLUNA FLAG PARA INTEIRO
    df_15min['flag'] = df_15min['flag'].astype(int)

    # #exporta dados brutos para csv
    # with open('../dados/'+posto_nome+'.pds','w',newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow([posto_nome])
    #     writer.writerow([posto_lat, posto_long])
    # df_15min.to_csv('../dados/'+posto_nome+'.pds', mode = 'a', sep = ";",
    #                 date_format='%Y-%m-%dT%H:%M:%S+00:00', float_format='%.2f')


    ########## TRANSFORMA SERIE HORARIA ##########

    df_15min.drop(['flag'], axis=1, inplace = True)

    #cria DFs padrao horario para ser preenchido com os dados de 15 min
    t_ini = df_15min.index[0].round('1h')
    t_fim = df_15min.index[-1]
    date_rng_horario = pd.date_range(start=t_ini, end=t_fim, freq='H', tz="UTC")
    table_hor = pd.DataFrame(date_rng_horario, columns=['date'])
    table_hor['datahora_UTC']= pd.to_datetime(table_hor['date'])
    table_hor = table_hor.set_index('datahora_UTC')
    table_hor.drop(['date'], axis=1, inplace = True)

    # agrupa em dados horarios, com intervalo fechado à direita (acumulado/media da 0:01 a 1:00);
    # coluna count resulta a soma (contagem) dos "1", coluna valor resulta na media dos valores;
    # para os valores de cont < 4, substitui o dado em 'valor' por NaN:
    df_15min['count'] = np.where(df_15min['h_mm'].notnull(), 1, 0)
    df_horario = (df_15min.resample("H", closed='right', label='right').
                  agg({'count' : np.sum, 'h_mm' : np.sum}))
    #df_horario.loc[df_horario['count'] < 4, ['q_m3s']] = np.nan
    #df_horario.loc[df_horario['count'] < 4, ['m']] = np.nan

    # remove colunas 'count' dos dataframes e agrupa com data padrao
    df_horario.drop('count', axis=1, inplace=True)
    table_hor = pd.merge(table_hor, df_horario, left_index = True,
                         right_index = True, how = 'left')
    table_hor = table_hor[~table_hor.index.duplicated(keep='first')]

    #exporta dados horarios para csv
    with open('../dados/'+posto_nome+'.pd','w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([posto_nome])
        writer.writerow([posto_lat, posto_long])
    table_hor.to_csv('../dados/'+posto_nome+'.pd', mode = 'a', sep = ";",
                     date_format='%Y-%m-%dT%H:%M:%S+00:00', float_format='%.2f')

    print(posto_nome, ' acabou - ', list(postos_precip).index(posto_nome)+1,"/",
          len(postos_precip))
