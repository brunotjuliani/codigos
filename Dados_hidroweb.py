import pandas as pd
import requests
url = 'http://www.snirh.gov.br/hidroweb/rest/api/documento/convencionais?tipo=2&documentos='

import os

diretorio = '/discolocal/bruno/Observado/Hidroweb'
os.chdir(diretorio)

estacoes = {
            'Balsa_Nova':'65028000'
            #'Sao_Jose':'2351027',
            #'Marilandia_do_Sul' : '2351063',
            #'Lerroville' : '2351039',
            #'Fabrica_de_Papelao' : '2351040',
            #'Bairro_Tres_Vendas' : '2351041'
            #'Porto_Amazonas':'65035000',
            #'Sao_Bento':'65155000',
            #'Pontilhao':'65200000',
            #'Santa_Cruz_Timbo':'65295000',
            #'Sao_Mateus_Sul':'65060000',
            #'Uniao_da_Vitoria':'65310000',
            #'Balsa_Nova':'65028000',
            }

for nome, codigo in estacoes.items():
    try:
        novo_url=url+str(codigo)
        novo_local='{}.zip'.format(str(nome))
        arquivo=requests.get(novo_url)
        open(novo_local,'wb').write(arquivo.content)
        #wget.download(novo_url, novo_local)
        print('{} baixado'.format(nome))
    except:
        print('{} não funcionou'.format(nome))
