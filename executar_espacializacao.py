'''
Arquivo de exemplo para executar a espacializacao da precipitacao
'''

# 1 - Importar as bibliotecas necessarias, principalmente geopandas
import geopandas as gpd
import pandas as pd
import glob
import numpy as np

# 4 - Coletar as entradas
bacia = input('Entre com o código da bacia (2 digitos): ')
lista_bacias = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                '21']
while bacia not in lista_bacias:
    bacia = input('Bacia nao reconhecida.\n'
                  'Entre com o código da bacia (2 digitos): ')

grade = gpd.read_file('../dados/grade/g_'+bacia+'.gpkg')
grade
path_pd = '../dados/precip/'
EPSG = 31982

# 5 - Executar IDWx

# 1 - Converter os pontos da geometria para o SRC projetado
grade = grade.to_crs('EPSG:{}'.format(EPSG))

# 2 - Inicializar os DataFrames
DF_postos = pd.DataFrame()
DF_grade = pd.DataFrame()
DF_grade.index.name = 'datahora'
DF_dists = pd.DataFrame()

# 3 - Abrir os arquivos .pd individualmente
arquivos_pd = glob.glob(path_pd+'*.csv')
for arquivo_pd in arquivos_pd:

    # 4 - Capturar as coordenadas do posto no arquivo .pd
    nome_posto = arquivo_pd.split('/')[-1].split('.csv')[0]
    lat_long = pd.read_csv(arquivo_pd, skiprows=2, nrows=1, header=None,
                           sep = ',').iloc[0]
    long = lat_long[0]
    lat  = lat_long[1]
    alt = lat_long[2]


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
    sr_posto = pd.read_csv(arquivo_pd, skiprows=3, parse_dates=True,
                           index_col='datahora', sep=',')['chuva_mm']
    sr_posto = sr_posto.rename(nome_posto)
    DF_postos = DF_postos.join(sr_posto, how='outer')

# 8 - Calcular a precipitacao interpolada para cada ponto de grade
L = len(grade)
no_postos = len(DF_postos.columns)
for i,pi in enumerate(grade.index):
    print('Iniciando ponto {}/{} da grade da bacia {}'.format(i+1,L,bacia))
    D = np.array([DF_dists.loc[pi,i] for i in DF_postos.columns]) # vetor de distancias
    W = np.array([1/(di**2) for di in D]) # vetor de pesos
    for t in DF_postos.index:
        #print('Calculando precipitacao no ponto {}/{} da grade - {}'.format(i+1,L, t))
        P_t = DF_postos.loc[t].values # vetor precipitacoes
        W_t = np.array([0 if np.isnan(P_t[i]) else W[i] for i in range(no_postos)])
        prec = np.sum(W_t * np.nan_to_num(P_t))/np.sum(W_t)
        DF_grade.loc[t, pi] = np.around(prec, decimals=2)
    print('Finalizado ponto {}/{} da grade'.format(i+1,L))

# 9 - Calcular a PME na grade
PME = DF_grade.mean(axis=1, skipna=True)
#return DF_grade, PME

# 6 - Exportar a PME no padrao preconizado nas diretrizes da Hidrologia - Simepar
PME.rename('chuva_mm').round(2).to_csv('../dados/pme/pme_bacia_'+bacia+'.csv',
                                       index_label='datahora')
