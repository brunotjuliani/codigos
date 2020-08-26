import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

dir_seca = '/home/bruno/Documentos/Seca_Iguacu/Dados_Estacoes'
os.chdir(dir_seca)

estacoes = {
            'Pontilhao',
            'Porto_Amazonas',
            'Rio_Negro',
            'Santa_Cruz_Timbo',
            'Sao_Bento',
            'Sao_Mateus_Sul',
            'Uniao_da_Vitoria'
             }


for estacao in estacoes:
    date_rng_diario = pd.date_range(start='1930-05-01', end='2020-08-26', freq='D')
    table_dia = pd.DataFrame(date_rng_diario, columns=['date'])
    table_dia['data']= pd.to_datetime(table_dia['date'])
    table_dia = table_dia.set_index('data')
    table_dia.drop(['date'], axis=1, inplace = True)

    convencional = pd.read_csv(estacao+'_convencional.csv', sep = ',', index_col = 0)
    convencional[convencional['convencional'] < 0] = np.nan
    telemetrica = pd.read_csv(estacao+'_telemetrica.csv', sep = ',', index_col = 0)
    telemetrica.columns = ['telemetrica']
    telemetrica[telemetrica['telemetrica'] < 0] = np.nan

    comparacao = table_dia.merge(convencional, how='left', left_index=True, right_index=True)
    comparacao = comparacao.merge(telemetrica, how = 'left', left_index=True, right_index=True)
    comparacao['preenchimento'] = comparacao['convencional']
    comparacao['preenchimento'] = comparacao['preenchimento'].fillna(comparacao['telemetrica'])

    comparacao.to_csv(estacao+'_comparacao.csv')

    plt.figure()
    plt.plot(comparacao['convencional'], label = "Convencional", linewidth = 0.8)
    plt.plot(comparacao['telemetrica'], label = "Telemetrica", linewidth = 0.5)
    plt.legend(loc='best')
    plt.title('Comparacao Medicoes')
    plt.xlabel('Data')
    plt.ylabel('Q - m3s-1')
    plt.savefig(estacao+'_comparacao.png', dpi = 300)
    plt.close()
