import hydrobr
import pandas as pd
import os

dir_seca = '/discolocal/bruno/Dados_Cota'
os.chdir(dir_seca)

estacoes = {#'Rio_Negro':'65100000',
            #'Porto_Amazonas':'65035000',
            #'Sao_Bento':'65155000',
            #'Pontilhao':'65200000',
            #'Santa_Cruz_Timbo':'65295000',
            #'Sao_Mateus_Sul':'65060000',
            #'Uniao_da_Vitoria':'65310000',
            'Balsa_Nova':'65028000',
            }

for estacao_nome,estacao_cod in estacoes.items():
    serie = hydrobr.get_data.ANA.flow_data({estacao_cod}, only_consisted=False)
    serie.index.name = 'data'
    if estacao_cod.endswith('00'):
        tipo = 'convencional'
    if estacao_cod.endswith('01'):
        tipo = 'telemetrica'
    serie.columns = [tipo]
    serie.to_csv(estacao_nome+'_'+tipo+'.csv')
