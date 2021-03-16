import numpy as np
import pandas as pd
import json

#postos_vazao = {
#                'Rio_Negro':'26064948',
#                'Porto_Amazonas':'25334953',
#                'Sao_Bento':'25564947',
#                'Pontilhao':'25555031',
#                'Santa_Cruz_Timbo':'26125049',
#                'Sao_Mateus_Sul':'25525023',
#                'Divisa':'26055019',
#                'Fluviopolis':'26025035',
#                'Uniao_da_Vitoria':'26145104',
#                'Madereira_Gavazzoni':'25485116',
#                'Jangada':'26225115',
#                'Solais_Novo':'26055155',
#                'Porto_Santo_Antonio':'25235306',
#                'Aguas_do_Vere':'25465256',
#                'Porto_Capanema':'25345435',
#                'Hotel_Cataratas':'25685442'
#            }

posto_nome = 'Aguas_do_Vere'
posto_codigo = '25465256'

########## SERIES 15 MIN ##########
print('Tratando ',posto_nome)
# dados = pd.read_csv('/discolocal/bruno/Observado/Pre_Consistencia/' +
#                           posto_nome + 'FB.csv', index_col = 0, sep = ';')
dados = pd.read_csv('../dados/' + posto_nome + 'FB.csv',
                    index_col = 0, sep = ';')
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
df_15min['flag'] = np.where((df_15min['h_m'] <= 0), 3, df_15min['flag'])
df_15min['flag'] = np.where((df_15min['q_m3s'] <= 0), 3, df_15min['flag'])
df_15min['h_m'] = np.where((df_15min['h_m'] <= 0), np.nan, df_15min['h_m'])
df_15min['h_m'] = np.where((df_15min['q_m3s'] <= 0), np.nan, df_15min['h_m'])

#SINALIZA COTAS CONSTANTES DE 12 HORAS -> FLAG 4
#REMOVE COTAS CONSTANTES - AQUI APLICADO PARA 48 OBS DE 15 MIN - 12 HORAS
dados2 = df_15min.groupby((df_15min['h_m'].shift()!=df_15min['h_m']).cumsum()
                       ).filter(lambda x: len(x) >= 48)
df_15min['flag'] = np.where(df_15min.index.isin(dados2.index),
                            4, df_15min['flag'])
df_15min['h_m'] = np.where(df_15min.index.isin(dados2.index),
                           np.nan, df_15min['h_m'])

## SINALIZA SPIKES -> FLAG 5
## REMOVE SPIKES
# #SPIKES COMO OUTLIER CENTRAL DE JANELA MOVEL DE 96 OBSERVACOES - 24 HORAS
# #CONSIDERADO OUTLIER MEDIA +- 3 VEZES DESVIO PADRAO DA JANELA MOVEL
# df_15min['media_movel'] = df_15min['h_m'].rolling(window = 24, center = True,
#                                                   min_periods = 1).mean()
# df_15min['sd_movel'] = df_15min['h_m'].rolling(window = 24, center = True,
#                                                min_periods = 1).std()
# df_15min['flag'] = np.where((df_15min['h_m'] < (df_15min['media_movel'] -
#                                                 3*(df_15min['sd_movel']))),
#                             5, df_15min['flag'])
# df_15min['h_m'] = np.where((df_15min['h_m'] < (df_15min['media_movel'] -
#                                                3*(df_15min['sd_movel']))),
#                            np.nan, df_15min['h_m'])
# df_15min['flag'] = np.where((df_15min['h_m'] > (df_15min['media_movel'] +
#                                                 3*(df_15min['sd_movel']))),
#                             5, df_15min['flag'])
# df_15min['h_m'] = np.where((df_15min['h_m'] > (df_15min['media_movel'] +
#                                                3*(df_15min['sd_movel']))),
#                            np.nan, df_15min['h_m'])
# df_15min.drop(['media_movel', 'sd_movel'], axis=1, inplace = True)

# SINALIZA ERROS VISUAIS -> FLAG 5
# REMOVE SPIKES COM BASE EM DICIONARIO DE ERROS GROSSEIROS
#importa dicionario de erros grosseiros e escolhe estacao
#dicionario_erros = json.load(open('/discolocal/bruno/Observado/Pre_Consistencia/erros_grosseiros_bruto.txt'))
dicionario_erros = json.load(open('../dados/erros_grosseiros_bruto.txt'))
erros_estacao = dicionario_erros[posto_nome]
#trata a matriz de erros
try:
    erros_estacao = np.hstack(erros_estacao)
except ValueError:
    pass
#remove spikes da serie observada
df_15min.loc[pd.to_datetime(erros_estacao), 'h_m'] = np.nan
df_15min['flag'] = np.where(df_15min.index.isin(pd.to_datetime(erros_estacao)),
                            np.where((df_15min['flag'] != 0), df_15min['flag'],
                                     5), df_15min['flag'])

#REMOVE VALORES DE VAZAO DO PONTO EM QUE COTA TENHA SIDO RETIRADA
df_15min['q_m3s'] = np.where(df_15min['h_m'].isnull(),
                             np.nan, df_15min['q_m3s'])

#COLUNA FLAG PARA INTEIRO
df_15min['flag'] = df_15min['flag'].astype(int)

#exporta observado para csv
# df_15min.to_csv('/discolocal/bruno/Observado/Pre_Consistencia/'+posto_nome+'FC.csv',
#                 date_format='%Y-%m-%dT%H:%M:%SZ', sep = ";",
#                 float_format = '%.3f')
df_15min.to_csv('../dados/'+posto_nome+'FC.csv',
                date_format='%Y-%m-%dT%H:%M:%SZ', sep = ";",
                float_format = '%.3f')

print(posto_nome, ' acabou')
