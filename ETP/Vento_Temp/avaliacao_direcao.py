import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pinhais = pd.read_csv('./Direcao_Vento/Simepar_25254905.csv', index_col='datahora', parse_dates=True)
pinhais['direcao'] = np.nan
pinhais['direcao'] = np.where((pinhais['dir_vento'] <= 22.5), 'N', pinhais['direcao'])
pinhais['direcao'] = np.where((pinhais['dir_vento'] >= 337.5), 'N', pinhais['direcao'])
pinhais['direcao'] = np.where((pinhais['dir_vento'] > 22.5) & (pinhais['dir_vento'] < 67.5), 'NE', pinhais['direcao'])
pinhais['direcao'] = np.where((pinhais['dir_vento'] >= 67.5) & (pinhais['dir_vento'] <= 112.5), 'E', pinhais['direcao'])
pinhais['direcao'] = np.where((pinhais['dir_vento'] > 112.5) & (pinhais['dir_vento'] < 157.5), 'SE', pinhais['direcao'])
pinhais['direcao'] = np.where((pinhais['dir_vento'] >= 157.5) & (pinhais['dir_vento'] <= 202.5), 'S', pinhais['direcao'])
pinhais['direcao'] = np.where((pinhais['dir_vento'] > 202.5) & (pinhais['dir_vento'] < 247.5), 'SW', pinhais['direcao'])
pinhais['direcao'] = np.where((pinhais['dir_vento'] >= 247.5) & (pinhais['dir_vento'] <= 292.5), 'W', pinhais['direcao'])
pinhais['direcao'] = np.where((pinhais['dir_vento'] > 292.5) & (pinhais['dir_vento'] < 337.5), 'NW', pinhais['direcao'])

ocorrencias_pinhais = pd.DataFrame(pinhais.groupby(['direcao']).size())
ocorrencias_pinhais = ocorrencias_pinhais.drop(['nan'],0)
ocorrencias_pinhais['porcentagem'] = ocorrencias_pinhais[0]/ocorrencias_pinhais[0].sum()*100
ocorrencias_pinhais = ocorrencias_pinhais.reindex(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])
direcoes = ocorrencias_pinhais.index

ocorrencias_pinhais


plt.bar(np.arange(len(direcoes)), ocorrencias_pinhais['porcentagem'], color='gray')
plt.title('Pinhais')
plt.xlabel('Direção')
plt.ylabel('% de ocorrências')
plt.xticks(np.arange(len(direcoes)), direcoes)
plt.savefig('./Direcao_Vento/pinhais.png', bbox_inches='tight', transparent=False, facecolor='white')
