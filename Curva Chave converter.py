import pandas as pd
import numpy as np
from datetime import datetime
from scipy.interpolate import interp1d
import os

dir_cota = "/discolocal/bruno/Dados_Cota"
os.chdir(dir_cota)


dados=pd.read_csv('balsa_nova_cota.csv')
dados['cota_cm'] = dados['cota_cm'] *100 #transforma m em cm
chave=pd.read_excel('relTabelaCotaVazao.xls',decimal=',', thousands='.')


periodos=chave['Unnamed: 0'].str.find('Período')
periodos=periodos[periodos>-1].index
periodos=chave['Unnamed: 0'][periodos]
periodos=periodos.reset_index(drop=True)

chave=chave[chave['Unnamed: 0'].astype(str).apply(lambda x: x.isnumeric())]
chave.columns=['Nivel','0','1','2','3','4','5','6','7','8','9']
chave.index=chave['Nivel']
chave=chave.drop('Nivel',axis=1)
chave=chave.stack()
chave.index.names=['cm','mm']
chave=chave.reset_index(level=[0,1])
chave[0]=chave[0].astype(float)
chave['diff']=chave[0].diff()

chave

i=0
def posicao(valor1):
    global i
    if valor1<0:
        i=i+1
    return periodos[i]

chave['validade']=np.vectorize(posicao)(chave['diff'])
chave['cm']=chave['cm'].astype(float)+chave['mm'].astype(float)
chave=chave.drop(['mm','diff'],axis=1)
chave.columns=['H','Q','validade']
dados['data']=pd.to_datetime(dados['data'])
i=0
chave
for periodo in periodos:
    if i==0:
        dinicial=datetime.strptime('01/01/1900', '%d/%m/%Y')
    else:
        #dinicial=datetime.strptime(periodo.split(' ')[1], '%d/%m/%Y')
        dinicial=dfinal
    if i==len(periodos)-1:
        dfinal=datetime.today()
    else:
        dfinal=datetime.strptime(periodo.split(' ')[3], '%d/%m/%Y')
    daux1=dados[(dados['data'] > dinicial) & (dados['data'] <= dfinal)]
    daux2=chave[chave['validade']==periodo]
    f = interp1d(daux2['H'], daux2['Q'],fill_value="extrapolate")
    if i==0:
        previsto=pd.DataFrame(f(daux1['cota_cm']))
    else:
        previsto=previsto.append(pd.DataFrame(f(daux1['cota_cm'])))
    i=i+1
#dados=pd.concat([dados,previsto],axis=1)
dados['vazao']=previsto[0]
dados.columns=['data','cota_cm','vazao']
dados.plot(x='data',y=['vazao'])
dados.to_csv('Tranformado.csv',index=False)
