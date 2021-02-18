import pygrib
import numpy as np
import pandas as pd
import datetime as dt
#import geopandas as gpd

## COORDENADAS ÁREA DE ESTUDO

# area = gpd.read_file('../Teste/Fiu_area.gpkg')
# minx = area.bounds.minx
# maxx = area.bounds.maxx
# miny = area.bounds.miny
# maxy = area.bounds.maxy

minx = -51.266685
maxx = -50.933458
miny = -23.925056
maxy = -23.69154

## INICIALIZA DATA FRAME VAZIO
df = pd.DataFrame(columns = [1])
df.index.name = 'Horizonte'

## DIA DISPARO (MODIFICAR PARA DATETIME TODAY)
# hoje = dt.date.today()
# ano = hoje.year
# mes = hoje.month
# dia = hoje.day

ano = 2021
mes = 1
dia = 1
dispara = dt.datetime(ano, mes, dia,  00)

## INSERIR LOOP PARA RANGE DE HORIZONTES (HORAS A FRENTE DE PREVISAO)
horizonte = 1
previsao = dispara + dt.timedelta(hours = horizonte)
mesprev = previsao.month
diaprev = previsao.day
horaprev = previsao.hour

## LEITURA DO ARQUIVO GRIB - 1 HORIZONTE DE PREVISÃO - ENSEMBLE COM N DADOS
#endereco no servidor do Simepar
#grbfile = f"/simepar/modelos/ecmwf/ens/{ano:04d}/{mes:02d}/{dia:02d}/00/D1X{mes:02d}{dia:02d}0000{mesprev:02d}{diaprev:02d}{horaprev:02d}001"
grbfile = f"../dados/D1X{mes:02d}{dia:02d}0000{mesprev:02d}{diaprev:02d}{horaprev:02d}001"
grbs = pygrib.open(grbfile)

# grbs[1].data(lat1=miny, lat2=maxy, lon1=minx, lon2=maxx)

## CORTE DO ARQUIVO PELA ÁREA E MÉDIA DO VALOR PARA CADA PREVISÃO DO ENSEMBLE
for N in range(0, 51):
    membro = grbs.select(perturbationNumber=N)
    for i in [0,1]:
        data, lats, lons = membro[i].data(lat1=miny, lat2=maxy, lon1=minx, lon2=maxx)
        if data.size == 0:
            continue
        p = np.mean(data) #media da precipitacao entre os pontos
    df.loc[horizonte,N] = p

df
