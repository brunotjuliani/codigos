import pandas as pd
import numpy as np
import os
import datetime as dt

#INPUTS
dir_secas = "/home/bruno/Documentos/Seca_Iguacu/Dados_Estacoes"
os.chdir(dir_secas)
serie_original = pd.read_csv('vazao_rio_negro.csv', sep = ',', decimal='.')
nome_estacao = 'Rio_Negro'

serie_original.columns = ['data', 'q_m3s_orig']
serie_tratada = serie_original
serie_tratada['q_m3s_corr'] = serie_tratada.q_m3s_orig.interpolate(
    method = 'linear', limit_direction ='forward')
serie_tratada

serie_tratada.to_csv
