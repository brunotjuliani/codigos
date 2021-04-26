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

# FORMATO DE CONSULTA: 'CODIGO_SIMEPAR':[Nome_Estacao, Altitude, Lat, Long]
postos_met = {
    '23855385':['Altonia',368,-23.85808,-53.85237],
    # '25134848':['Antonina',60,-25.24341,-48.75248],
    # '25444869':['APPA_Antonina',2,-25.44716,-48.69434],
    # '23515154':['Apucarana',746,-23.5175,-51.5302],
    # '24235332':['Assis_Chateaubriand',450,-24.3886,-53.5411],
    # '25505367':['Baixo_Iguaçu',274,-25.50895,-53.67738],
    # '23005002':['Cambara',450,-23.0025,-50.0362],
    # '24075240':['Campo_Mourao',601,-24.07305,-52.40387],
    # '24035222':['Campo_Mourao_antiga',601.2,-24.08543,-52.38654],
    # '24535333':['Cascavel',719.3,-24.8845,-53.5547],
    # '24494915':['Cerro_Azul',366,-24.8267,-49.2604],
    # '23395232':['Cianorte',451,-23.6522,-52.5476],
    # '23695263':['Cianorte_Cocamar',534,-23.69372,-52.63736],
    # '23605062':['Cornelio_Procopio',647,-23.20645,-50.62793],
    # '25264916':['Curitiba',935,-25.44817,-49.23033],
    # '24385115':['Candido_de_Abreu',645,-24.6321,-51.2452],
    # '25335129':['Entre_Rios',1095,-25.5459,-51.4884],
    # '25275035':['Fernandes_Pinheiro',893,-25.4532,-50.5839],
    # '26055139':['Foz_do_Areia',780,-26.0037,-51.6679],
    # '25245437':['Foz_do_Iguaçu',232,-25.4059,-54.6167],
    # '25435458':['Foz_do_Iguaçu_Itaipu',168,-25.4361,-54.58286],
    # '26055305':['Francisco_Beltrao',652,-26.0593,-53.06548],
    # '24045415':['Guaira',227.9,-24.07487,-54.26151],
    # '25215130':['Guarapuava',1070,-25.3845,-51.4935],
    # '25324831':['Guaratuba',0,-25.84536,-48.58049],
    # '24134940':['Jaguariaiva',900,-24.2269,-49.677],
    # '25474946':['Lapa',909.8,-25.7817,-49.7598],
    # '25425241':['Laranjeiras_do_Sul',838,-25.42767,-52.41211],
    # '22915315':['Loanda',491,-22.91718,-53.15146],
    # '23185109':['Londrina',585,-23.3595,-51.1647],
    # '23275159':['Maringa',570,-23.4483,-51.9881],
    # '25345331':['N_Prata_do_Iguaçu',546.3,-25.5666,-53.5166],
    # '26285158':['Palmas',1100,-26.4682,-51.9762],
    # '26585152':['Palmas_Horizonte',1344,-26.5829,-51.52019],
    # '24535213':['Palmital',783,-24.8644,-52.2186],
    # '24185355':['Palotina',303,-24.3129,-53.9008],
    # '25534852':['Paranagua',19,-25.5378,-48.5296],
    # '23055226':['Paranavai',480,-23.0916,-52.4438],
    # '26075241':['Pato_Branco',721.8,-26.1229,-52.6514],
    # '25254905':['Pinhais',930,-25.3907,-49.1299],
    # '25385157':['Pinhao',910,-25.64944,-51.9625],
    # '25135001':['Ponta_Grossa',888.25,-25.0137,-50.1524],
    # '22434707':['Replan',608.28,-22.73,-47.1],
    # '25174828':['Reserva_Natural_Salto_Morato',32,-25.1779,-48.2881],
    # '25315329':['Salto_Caxias',440,-25.52092,-53.49412],
    # '25315301':['Salto_Osorio',514,-25.52213,-53.03087],
    # '24505420':['Santa_Helena',271,-24.9168,-54.3103],
    # '23255010':['Santo_Antonio_da_Platina',661,-23.2558,-50.10379],
    # '25115408':['Sao_Miguel_do_Iguaçu',298,-25.3528,-54.2546],
    # '25554836':['Techint',30,-25.55347,-48.36707],
    # '24205037':['Telemaco_Borba',768,-24.339,-50.6106],
    # '24475343':['Toledo',516.4,-24.7834,-53.7196],
    # '24555296':['Ubirata',529,-24.5545,-52.96648],
    # '23445317':['Umuarama',480,-23.75066,-53.30766],
    # '26145103':['Uniao_da_Vitoria',756.53,-26.22825,-51.06827]
           }

## COLETA DADOS VENTO

for posto_codigo,posto_info in postos_met.items():
    posto_nome = posto_info[0]
    posto_alt = posto_info[1]
    posto_lat = posto_info[2]
    posto_long = posto_info[3]

    ########## SERIES 15 MIN ##########
    print('Coletando dados brutos',posto_nome)
    t_ini = dt.datetime(1997, 1, 1,  0,  0) #AAAA, M, D, H, Min
    t_fim = dt.datetime.now()

    #coleta dados de vento
    vel_vento = coletar_dados(t_ini,t_fim, posto_codigo, '(8)')
    vel_vento.columns = ['ms-1', 'sensor']
    dir_vento = coletar_dados(t_ini,t_fim, posto_codigo,'(10)')
    dir_vento.columns = ['g', 'sensor']
    dados_vento = pd.merge(vel_vento['ms-1'],dir_vento['g'],how='outer',
                     left_index=True,right_index=True)

    #converte indice para formato DATETIME ISO UTC
    dados_vento.index = pd.to_datetime(dados_vento.index).rename('datahora')
    dados_vento['ms-1'] = pd.to_numeric(dados_vento['ms-1'], downcast="float")

    # #exporta observado para csv
    # dados.to_csv(posto_nome+'_vento.csv',
    #                 date_format='%Y-%m-%dT%H:%M:%SZ', sep = ',',
    #                 float_format = '%.2f')
    print(posto_nome, 'acabou - ')
