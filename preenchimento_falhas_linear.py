import pandas as pd
import numpy as np
import os
import datetime as dt

#INPUTS
dir_secas = "/home/bruno/Documentos/Seca_Iguacu/Dados_Estacoes"
os.chdir(dir_secas)

#LISTA ESTACOES
estacoes = ['65035000_Porto_Amazonas',
            '65060000_Sao_Mateus_do_Sul',
            '65100000_Rio_Negro',
            '65155000_Sao_Bento',
            '65208001_Pontilhao']

for estacao in estacoes:
    serie_original = pd.read_csv(estacao+'.csv', sep = ',', decimal='.')
    nome_estacao = estacao

    serie_original.columns = ['data', 'q_m3s_orig']
    serie_tratada = serie_original
    serie_tratada['q_m3s_corr'] = serie_tratada.q_m3s_orig.interpolate(
        method = 'linear', limit_direction ='forward')
    serie_tratada.to_csv(nome_estacao+'_vazao_tratada.csv', index = False)
