import numpy as np
import pandas as pd

posto_nome = 'Rio_Negro'
posto_codigo = '26064948'

########## SERIES 15 MIN ##########
print('Tratando ',posto_nome)
dados = pd.read_csv('/discolocal/bruno/Observado/Cota_Bruto/' +
                          posto_codigo + 'FB.csv', index_col = 0, sep = ';')
dados.index = pd.to_datetime(dados.index)

#DADOS BRUTOS -> FLAG 0
#DADO BRUTO BAIXADO SEM VALOR -> FLAG 1
dados['flag'] = np.where(dados['h_m'].isnull(), 1, 0)

dados["q_m3s"] = pd.to_numeric(dados["q_m3s"], downcast="float")
dados["h_m"] = pd.to_numeric(dados["h_m"], downcast = "float")

# cria DFs padrão de data, para serem preenchidas com os dados baixados
t_ini = dados.index[0]
t_fim = dados.index[-1]

date_rng_15min = pd.date_range(start=t_ini, end=t_fim, freq='15min')
table_15min = pd.DataFrame(date_rng_15min, columns=['datahora'])
table_15min['datahora_UTC']= pd.to_datetime(table_15min['datahora'])
table_15min = table_15min.set_index('datahora_UTC')
table_15min.drop(['datahora'], axis=1, inplace = True)
df_15min = pd.merge(table_15min, dados, how='left',
                    left_index=True, right_index=True)
df_15min = df_15min[~df_15min.index.duplicated(keep='first')]

#DATA SEM REGISTRO NA SERIE DE DADOS BRUTOS -> FLAG 2
df_15min['flag'] = np.where(df_15min['flag'].isnull(), 2, df_15min['flag'])

#SINALIZA A OCORRENCIA DE VALORES NEGATIVOS -> FLAG 3
#REMOVE VALORES DE COTA NEGATIVOS
df_15min['flag'] = np.where((df_15min['h_m'] < 0), 3, df_15min['flag'])
df_15min['h_m'] = np.where((df_15min['h_m'] < 0), np.nan, df_15min['h_m'])

#SINALIZA COTAS CONSTANTES DE 6 HORAS -> FLAG 4
#REMOVE COTAS CONSTANTES - AQUI APLICADO PARA 24 OBS DE 15 MIN - 6 HORAS
dados2 = df_15min.groupby((df_15min['h_m'].shift()!=df_15min['h_m']).cumsum()
                       ).filter(lambda x: len(x) >= 24)
df_15min['flag'] = np.where(df_15min.index.isin(dados2.index),
                            4, df_15min['flag'])
df_15min['h_m'] = np.where(df_15min.index.isin(dados2.index),
                           np.nan, df_15min['h_m'])

#REMOVE VALORES DE VAZAO DO PONTO EM QUE COTA TENHA SIDO RETIRADA
df_15min['q_m3s'] = np.where(df_15min['h_m'].isnull(),
                             np.nan, df_15min['q_m3s'])

#COLUNA FLAG PARA INTEIRO
df_15min['flag'] = df_15min['flag'].astype(int)

#exporta observado para csv
df_15min.to_csv('/discolocal/bruno/Observado/Cota_Bruto/'+posto_codigo+'FC.csv',
                date_format='%Y-%m-%dT%H:%M:%SZ', sep = ";",
                float_format = '%.3f')

print(posto_nome, 'acabou)
