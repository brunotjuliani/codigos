#BIBLIOTECAS
import os
import HydroErr as he
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
gbl = globals()

#DEFINICAO PERIODO ANALISE
data_ini = dt.datetime(2020, 1, 1,  0,  0) #YYYY, M, D, H, Min
data_fim = dt.datetime(2020, 8, 30,  23,  59)

dir_observado = "/home/bruno/Documentos/Observado"
dir_home = "/home/bruno"
os.chdir(dir_observado)

nome_bacia = 'Rio_Negro'

serie_observada = pd.read_csv('vazao_'+nome_bacia+'.csv', index_col=0)
serie_observada.index = pd.to_datetime(serie_observada.index)
serie_observada = serie_observada.loc[str(data_ini) : str(data_fim)]
serie_observada

serie_observada['q_m3s'].plot(linewidth=0.5)
