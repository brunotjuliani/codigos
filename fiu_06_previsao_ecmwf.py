import pygrib
import numpy as np
import pandas as pd
import datetime as dt
import math
import csv

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


## COORDENADAS ÁREA DE ESTUDO
# Leitura Grade Bacia
print('Lendo grade de pontos')
area = 534
arquivo_grade = '../dados/Fiu/pontos_grade_fiu.csv'
#arquivo_grade = '/discolocal/bruno/Fiu/pontos_grade_fiu.csv'
grade = pd.read_csv(arquivo_grade, sep=',')
# Define coordenadas maximas e minimas para coleta (folga adotada p/ + 1 ponto)
minx = min(grade['x']) +360 - 0.15
maxx = max(grade['x']) +360 + 0.15
miny = min(grade['y']) - 0.15
maxy = max(grade['y']) + 0.15

## DIA DISPARO (MODIFICAR PARA DATETIME TODAY)
# hoje = dt.date.today()
# ano = hoje.year
# mes = hoje.month
# dia = hoje.day
ano = 2020
mes = 6
dia = 25
dispara = dt.datetime(ano, mes, dia,  00)

## Inicia dataframe e loop de ensemble
dados_peq = pd.DataFrame()
ens_n = 0
while ens_n <= 50:
    print('Iniciando membro ', ens_n+1)
    #INICIA DATAFRAME P/ DIFERENTES PONTOS
    df_previsao = pd.DataFrame()

    ## INSERIR LOOP PARA RANGE DE HORIZONTES (HORAS A FRENTE DE PREVISAO)
    #print('Coletando dados de previsão')
    horizonte = 1
    while horizonte <= 168:
        previsao = dispara + dt.timedelta(hours = (horizonte))
        prev_mes = previsao.month
        prev_dia = previsao.day
        prev_hora = previsao.hour
        df_previsao.loc[horizonte,'datahora'] = previsao.isoformat()

        ## LEITURA DO ARQUIVO GRIB - 1 HORIZONTE DE PREVISÃO - ENSEMBLE COM N DADOS
        grbfile = f"/simepar/modelos/ecmwf/ens/SCPRSPRJ/0p2/pos/{ano:02d}/{mes:02d}/{dia:02d}/00/D1X{mes:02d}{dia:02d}0000{prev_mes:02d}{prev_dia:02d}{prev_hora:02d}001.grib2"
        #grbfile = f"/discolocal/bruno/Fiu/00/D1X{mes:02d}{dia:02d}0000{prev_mes:02d}{prev_dia:02d}{prev_hora:02d}001.grib2"
        try:
            grbs = pygrib.open(grbfile)
        except:
            grbfile = f"/simepar/modelos/ecmwf/ens/SCPRSPRJ/0p2/pos/{ano:02d}/{mes:02d}/{dia:02d}/00/D1E{mes:02d}{dia:02d}0000{prev_mes:02d}{prev_dia:02d}{prev_hora:02d}001.grib2"
            #grbfile = f"/discolocal/bruno/Fiu/00/D1E{mes:02d}{dia:02d}0000{prev_mes:02d}{prev_dia:02d}{prev_hora:02d}001.grib2"
            try:
                grbs = pygrib.open(grbfile)
                pass
            except:
                horizonte +=1
                continue

        #seleciona membro do ensemble e le variaveis
        membro = grbs.select(perturbationNumber=ens_n)
        data, lats, lons = membro[0].data(lat1=miny, lat2=maxy, lon1=minx, lon2=maxx)
        data2 = np.hstack(data)

        #divide dataframe para os pontos estudados
        ponto = 0
        while ponto < len(data2):
            df_previsao.loc[horizonte,ponto] = data2[ponto]
            ponto += 1
        horizonte += 1
    #Datetime index
    df_previsao['datahora']= pd.to_datetime(df_previsao['datahora'])
    df_previsao = df_previsao.set_index('datahora')
    #Remove linhas sem previsao
    df_previsao = df_previsao.dropna(axis = 0, how = 'all')
    #Separa chuva por passo de tempo do acumulado - fillna para lidar com primeira linha
    df_discreto = df_previsao.diff().fillna(df_previsao.iloc[0])
    #Acumula para passo de tempo de 6 horas
    df_6hrs = df_discreto.resample("6H", closed='right', label = 'right').sum()

    ## Inicializa DataFrames de espacialização
    #print('Inciando espacialização para área da bacia')
    DF_postos = df_6hrs
    DF_grade = pd.DataFrame()
    DF_grade.index.name = 'datahora'
    DF_dists = pd.DataFrame()

    ## Capturar as coordenadas de cada ponto de previsao e comparar com grade da bacia
    lats2 = np.hstack(lats)
    lons2 = np.hstack(lons)
    ponto = 0
    while ponto < len(lats2):
        long_p  = lons2[ponto]
        lat_p = lats2[ponto]
        # Calcular a distancia (km) entre os pontos de previsao e grade da bacia
        for pi in grade.index:
            ponto_x = grade.loc[pi].x
            ponto_y = grade.loc[pi].y
            dist = haversine(long_p, lat_p, ponto_x, ponto_y)
            DF_dists.loc[pi,ponto] = dist
        ponto +=1

    ## Calcular a precipitacao interpolada para cada ponto de grade
    L = len(grade)
    no_postos = len(DF_postos.columns)
    for i,pi in enumerate(grade.index):
    #    print('Ponto {}/{} da grade.'.format(i+1,L))
        D = np.array([DF_dists.loc[pi,i] for i in DF_postos.columns]) # vetor de distancias
        W = np.array([1/(di**2) for di in D]) # vetor de pesos
        for t in DF_postos.index:
            P_t = DF_postos.loc[t].values # vetor precipitacoes
            W_t = np.array([0 if np.isnan(P_t[i]) else W[i] for i in range(no_postos)])
            prec = np.sum(W_t * np.nan_to_num(P_t))/np.sum(W_t)
            DF_grade.loc[t, pi] = np.around(prec, decimals=2)
    #Calcular a espacialização da previsao
    PME = DF_grade.mean(axis=1, skipna=True)
    pme_prev = pd.DataFrame(PME.rename('chuva_mm').round(2))
    pme_prev.index = pme_prev.index.tz_localize('UTC')

    ## LEITURA DO ARQUIVO COM SERIE HISTORICA ESPACIALIZADA
    #print('Lendo dados historicos observados')
    #Historico de chuva
    pme_hist = pd.read_csv('../dados/Fiu/pme_fiu.csv', index_col='datahora')
    #pme_hist = pd.read_csv('/discolocal/bruno/Fiu/pme_fiu.csv', index_col='datahora')
    pme_hist.index = pd.to_datetime(pme_hist.index, utc=True)
    pme_hist = pme_hist.resample("6H", closed='right', label = 'right').sum()
    #Recorta periodo de aquecimento - 2 anos
    chuva_recorte = pme_hist.loc[dispara-dt.timedelta(days=730):dispara]
    #Inclui previsao
    chuva_comb = pd.concat([chuva_recorte, pme_prev])
    chuva_comb = chuva_comb[~chuva_comb.index.duplicated(keep='last')]
    chuva_comb = chuva_comb.rename(columns={'chuva_mm':'pme'})

    #ENCERRANDO LOOP E CRIANDO DF
    dados_peq['pme_'+str(ens_n)] = chuva_comb['pme']
    ens_n += 1

## Historico de vazao - APENAS PARA COMPARACAO
vazao = pd.read_excel('../dados/Fiu/dados_horarios_fiu.xlsx')
#vazao = pd.read_excel('/discolocal/bruno/Fiu/dados_horarios_fiu.xlsx')
vazao.index = (pd.to_datetime(vazao.Data) + pd.to_timedelta(vazao.Hora, unit = 'h'))
vazao.index = vazao.index.tz_localize('UTC')
vazao['qjus'] = np.where((vazao['Afluente'] == 'S/L'), np.nan, vazao['Afluente'])
vazao = vazao[['qjus']]
vazao['qjus'] = pd.to_numeric(vazao['qjus'])
vazao['qjus'] = np.where((vazao['qjus'] < 0), np.nan, vazao['qjus'])
vazao = vazao.resample("6H", closed='right', label = 'right').mean()

dados_peq = pd.merge(dados_peq, vazao, how = 'left',
                 left_index = True, right_index = True)

## Carrega Evapotranspiracao padrao
etp = pd.read_csv('../dados/Fiu/etp_londrina_padrao.csv', sep = ',')
#etp = pd.read_csv('/discolocal/bruno/Fiu/etp_londrina_padrao.csv', sep = ',')
etp.index = (etp['Mes'].map('{:02}'.format) + '-' +
             etp['Dia'].map('{:02}'.format) + '-' +
             etp['Hora'].map('{:02}'.format))
#cria DFs padrao horario para ser preenchido com ETP horarios
t_ini = dados_peq.index[0].round('1d')
t_fim = dados_peq.index[-1]
date_rng_horario = pd.date_range(start=t_ini, end=t_fim, freq='H', tz = "UTC")
etp_hor = pd.DataFrame(date_rng_horario, columns=['date'])
etp_hor.index = etp_hor['date']
etp_hor['datahora'] = etp_hor.index.strftime('%m-%d-%H')
etp_hor['etp'] = etp_hor['datahora'].map(etp['etp'])
etp_hor = etp_hor.drop(['date', 'datahora'], axis=1)
etp = etp_hor.resample("6H", closed='right', label = 'right').sum()
#Combina no PEQ
dados_peq = pd.merge(dados_peq, etp, how = 'left',
                 left_index = True, right_index = True)

with open('../dados/Fiu/peq_previsao0625_Fiu.csv', 'w', newline = '') as file:
    writer = csv.writer(file)
    writer.writerow([area])
dados_peq.to_csv('../dados/Fiu/peq_previsao0625_Fiu.csv', mode = 'a',
                 index_label='datahora_UTC', float_format='%.3f')
