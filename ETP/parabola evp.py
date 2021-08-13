import pandas as pd

dados=pd.read_csv("evp_londrina_inmet.csv",index_col='data')
ETPH=[]
tempos=[]

for data,E in zip(dados.index,dados['evp']):
    A=-6*E/2197
    B=150/2197*E
    C=-684/2197*E
    for hora in range(0,24):
        ETP=A*hora**2+B*hora+C
        if ETP<0:
            ETP=0
        ETPH.append(ETP)
        tempos.append(str(data)+f' {hora}:00')
        
dados_horarios=pd.DataFrame({'data_hora':tempos,'ETPH':ETPH})
dados_horarios['data_hora']=pd.to_datetime(dados_horarios['data_hora'])
dados_horarios['ETPH']=dados_horarios['ETPH'].round(decimals=2)
dados_horarios.to_csv('evp_londrina_horario_parabola.csv',index=False,float_format='%.2f')