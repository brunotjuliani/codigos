'''
Arquivo de exemplo para executar a espacializacao da precipitacao
'''

# 1 - Importar as bibliotecas necessarias, principalmente geopandas
import geopandas as gpd

# 2 - Adicionar o path do repositorio "modelos"
import sys
sys.path.append('/home/bruno/github/modelos/')

# 3 - Importar a funcao de interpolacao desejada do modulo de espacializacao
from espacializacao import idw

# 4 - Coletar as entradas
# grade = gpd.read_file('/home/bruno/github/modelos/exemplos/espacializacao/grade.gpkg')
# grade
# path_pd = '/home/bruno/github/modelos/exemplos/espacializacao/dados/'
# EPSG = 31983

grade = gpd.read_file('../dados/grade/g_01.pgkg')
grade
path_pd = '../dados/p_diario/'
EPSG = 31982

# 5 - Executar IDWx
DF_grade, PME = idw(grade, path_pd, EPSG)
grade
# 6 - Exportar a PME no padrao preconizado nas diretrizes da Hidrologia - Simepar
PME.rename('p').round(2).to_csv('../dados/pme_bacia_01.pd', index_label='data')
# Obs: falta salvar o lat,long no arquivo .pd, o ideal seria o centroide da grade
