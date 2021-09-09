from datetime import datetime
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np

def harvesine(lon1, lat1, lon2, lat2):
    '''
    Calcula a distancia de circulo maximo dois pontos na superficie da Terra
    '''
    # Converte graus em radianos pela funcao 'radians' do math
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # Formula de haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Raio da Terra em km. Usar 3956 para milhas
    return c * r

D = pd.DataFrame()
grade_def = pd.read_csv('./grade_def.csv', index_col='idGrade')
postos_def = pd.read_csv('./dados_selecao_maxmin.csv', index_col='estcodigo')

min(postos_def['v_vento_medio'])
max(postos_def['v_vento_medio'])
min(postos_def['t_med_medio'])
max(postos_def['t_med_medio'])
min(postos_def['t_max_med'])
max(postos_def['t_max_med'])
min(postos_def['t_min_med'])
max(postos_def['t_min_med'])
min(postos_def['v_rajada_max'])
max(postos_def['v_rajada_max'])


for idGrade in grade_def.index:
    lon1, lat1 = grade_def.loc[idGrade, ['x','y']]
    for idPosto in postos_def.index:
        lon2, lat2 = postos_def.loc[idPosto, ['estlongitude','estlatitude']]
        D.loc[idGrade, idPosto] = harvesine(lon1, lat1, lon2, lat2)
D.index.names = ['idGrade']
D.to_csv('./matriz_distancias.csv', index_label='idGrade', float_format='%.2f')

dmax = 800

#Organiza para espacializacao
dados_postos = postos_def[['t_med_medio', 't_max_med', 't_min_med',
                           'v_vento_medio', 'v_rajada_max']]
dados_postos = dados_postos.transpose()

# Metodo Matricial
dados_postos = dados_postos[D.columns.tolist()] # Tem que ordenar
dados_grade = pd.DataFrame(columns=grade_def.index) # Tem que ordenar
n = len(grade_def)

for row in dados_postos.itertuples():
    t = row[0]
    dados_postos_t = np.asarray(row[1:])

    # Calcula a matriz de pesos W no tempo t com base nas premissas de distancia e disponibilidade
    dados_postos_t = np.tile(dados_postos_t, (n, 1))
    mascara_t = np.logical_or(D.values > dmax, np.isnan(dados_postos_t))
    W_t = np.ma.array(1/D.values**2, mask = mascara_t)

    # Interpola
    dados_grade_t = np.sum(W_t * dados_postos_t, axis=1) / np.sum(W_t, axis=1)
    dados_grade.loc[t,:] = dados_grade_t.filled(np.nan)
dados_grade = dados_grade.applymap(lambda x: np.round(x, 3))

dados_grade.transpose()

grade_info = grade_def.copy()
grade_info['t_med_medio'] = dados_grade.transpose()['t_med_medio']
grade_info['t_max_med'] = dados_grade.transpose()['t_max_med']
grade_info['t_min_med'] = dados_grade.transpose()['t_min_med']
grade_info['v_vento_medio'] = dados_grade.transpose()['v_vento_medio']
grade_info['v_rajada_max'] = dados_grade.transpose()['v_rajada_max']

grade_info.to_csv('grade_info_maxmin.csv')

grade_info['v_rajada_max'].min()
