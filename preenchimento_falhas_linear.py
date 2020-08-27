import pandas as pd
import numpy as np
import os
import datetime as dt

dir_seca = '/home/bruno/Documentos/Seca_Iguacu/Dados_Estacoes'
os.chdir(dir_seca)

estacoes = {
            'Porto_Amazonas',
            'Rio_Negro',
            'Sao_Mateus_Sul',
            'Uniao_da_Vitoria'
             }

for estacao in estacoes:
    serie_original = pd.read_csv(estacao+'_comparacao.csv', sep = ',', decimal='.')
    nome_estacao = estacao
    serie_original.columns = ['data', 'convencional', 'telemetrica', 'preenchimento']
    serie_tratada = serie_original[['data', 'preenchimento']]
    serie_tratada['q_m3s'] = serie_tratada['preenchimento'].interpolate(
        method = 'spline', order = 3, limit_direction ='forward')
    serie_tratada = serie_tratada.drop('preenchimento',1).dropna()
    serie_tratada.to_csv(estacao+'_final.csv', index = False)
    #serie_tratada.to_csv(nome_estacao+'_vazao_tratada.csv', index = False)
