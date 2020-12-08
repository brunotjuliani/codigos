'''
Arquivo de exemplo para executar a espacializacao da precipitacao
'''

# 1 - Importar as bibliotecas necessarias, principalmente geopandas
import geopandas as gpd
import pandas as pd
import glob
import numpy as np

# 4 - Coletar as entradas

grade = gpd.read_file('../dados/grade/g_01.gpkg')
grade
path_pd = '../dados/p_diario/'
EPSG = 31982

# 5 - Executar IDWx

# 1 - Converter os pontos da geometria para o SRC projetado
grade = grade.to_crs('EPSG:{}'.format(EPSG))

# 2 - Inicializar os DataFrames
DF_postos = pd.DataFrame()
DF_grade = pd.DataFrame()
DF_grade.index.name = 'datahora_UTC'
DF_dists = pd.DataFrame()

# 3 - Abrir os arquivos .pd individualmente
arquivos_pd = glob.glob(path_pd+'*.pd')
for arquivo_pd in arquivos_pd:

    # 4 - Capturar as coordenadas do posto no arquivo .pd
    nome_posto = arquivo_pd.split('/')[-1].split('.pd')[0]
    lat_long = pd.read_csv(arquivo_pd, skiprows=1, nrows=1, header=None,
                           sep = ';').iloc[0]
    lat  = lat_long[0]
    long = lat_long[1]

    # 5 - Converter a coordenada de WGS84 (padrao) para o SRC projetado
    df_temp = pd.DataFrame({'posto':[nome_posto],
                            'Lat':[lat],
                            'Long':[long]})
    geometry = gpd.points_from_xy(x=df_temp.Long, y=df_temp.Lat)
    gdf_temp = gpd.GeoDataFrame(df_temp, geometry=geometry)
    gdf_temp.set_crs('EPSG:4326', inplace=True)
    gdf_temp = gdf_temp.to_crs('EPSG:{}'.format(EPSG))
    posto_x = gdf_temp.loc[0].geometry.x
    posto_y = gdf_temp.loc[0].geometry.y

    # 6 - Calcular a distancia (km) entre o posto e todos os pontos da grade
    for pi in grade.index:
        ponto_x = grade.loc[pi].geometry.x
        ponto_y = grade.loc[pi].geometry.y
        dist = ((posto_x-ponto_x)**2+(posto_y-ponto_y)**2)**(1/2)
        DF_dists.loc[pi,nome_posto] = dist/1000

    # 7 - Coletar a serie de dados do posto e conceatenar em DF_postos
    sr_posto = pd.read_csv(arquivo_pd, skiprows=2, parse_dates=True,
                           index_col='datahora_UTC', sep=';')['h_mm']
    sr_posto = sr_posto.rename(nome_posto)
    DF_postos = DF_postos.join(sr_posto, how='outer')

# 8 - Calcular a precipitacao interpolada para cada ponto de grade
L = len(grade)
no_postos = len(DF_postos.columns)
for i,pi in enumerate(grade.index):
    D = np.array([DF_dists.loc[pi,i] for i in DF_postos.columns]) # vetor de distancias
    W = np.array([1/(di**2) for di in D]) # vetor de pesos
    for t in DF_postos.index:
        print('Calculando precipitacao no ponto {}/{} da grade - {}'.format(i+1,L, t))
        P_t = DF_postos.loc[t].values # vetor precipitacoes
        W_t = np.array([0 if np.isnan(P_t[i]) else W[i] for i in range(no_postos)])
        prec = np.sum(W_t * np.nan_to_num(P_t))/np.sum(W_t)
        DF_grade.loc[t, pi] = np.around(prec, decimals=2)

# 9 - Calcular a PME na grade
PME = DF_grade.mean(axis=1, skipna=True)
#return DF_grade, PME

# 6 - Exportar a PME no padrao preconizado nas diretrizes da Hidrologia - Simepar
PME.rename('h_mm').round(2).to_csv('../dados/pme_bacia_01.pd', index_label='data')
# Obs: falta salvar o lat,long no arquivo .pd, o ideal seria o centroide da grade
