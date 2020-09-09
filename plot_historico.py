#BIBLIOTECAS
import pandas as pd
import numpy as np
import os
import datetime as dt
import matplotlib.pyplot as plt
import scipy.stats as stats

dir_secas = "/discolocal/bruno/Seca_Iguacu"
os.chdir(dir_secas)
serie_original = pd.read_csv('Pontilhao_vazao.csv', sep = ',', decimal='.')
serie_tratada = pd.read_csv('dados_estacoes/pontilhao_tratada.csv', sep = ',', decimal='.')

serie_original

serie_tratada

plt.plot(serie_original['data'],serie_original['Q_m3'], label = "Original")
plt.plot(serie_tratada['data'],serie_tratada['q_m3s'], label = "Tratada")
plt.savefig('Plot_preenchimento.png', dpi = 300)
