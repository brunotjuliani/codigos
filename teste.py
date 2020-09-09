#BIBLIOTECAS
import os
import HydroErr as he
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import pytz
gbl = globals()

#DEFINICAO PERIODO ANALISE
data_ini = dt.datetime(2015, 1, 1,  0,  0) #YYYY, M, D, H, Min
data_fim = dt.datetime(2020, 8, 31,  23,  59)

dir_observado = "/discolocal/bruno/Observado"
os.chdir(dir_observado)

nome_bacia = 'Hotel_Cataratas'

erros = []
try:
    erros = np.hstack(erros)
except ValueError:
    pass

serie_observada = pd.read_csv('vazao_'+nome_bacia+'.csv', index_col=0)
serie_observada.index = pd.to_datetime(serie_observada.index)
serie_observada.loc[pd.to_datetime(erros), 'q_m3s'] = np.nan
serie_observada = serie_observada.loc[str(data_ini) : str(data_fim)]
serie_observada

serie_observada['q_m3s'].plot(linewidth=0.5)
