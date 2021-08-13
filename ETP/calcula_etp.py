import pandas as pd
import numpy as np
import math
import datetime as dt

def calcular_EVP3(temp,latitude,dia_ano):#Fórmula de Oudim
        lat=math.radians(latitude)
        j=dia_ano
        dr=1+0.033*math.cos(2*math.pi*j/365)
        d=0.409*math.sin(2*math.pi*dia_ano/365-1.39)
        X=(1-(math.tan(lat)**2)*(math.tan(d)**2))
        if X<0:
            X=0.00001
        ws=math.pi/2-math.atan(-math.tan(lat)*math.tan(d)/(X**0.5))
        Ra=118.08/math.pi*dr*(ws*math.sin(lat)*math.sin(d)+math.cos(lat)*math.cos(d)*math.sin(ws))
        ET=Ra*(temp+5)/226
        if ET<0:
            ET=0
        return ET

nome = 'inmet_braganca_paulista'
latitude = -22.95

#datetime em BRT
serie_hor = pd.read_csv(f'{nome}.csv', parse_dates=True, index_col=0)

serie_hor['T_med'] = (serie_hor['TEM_MAX'] + serie_hor['TEM_MIN'])/2
serie_d = (serie_hor.resample("D", closed='left').agg({np.mean}))
serie_d['d_j'] = serie_d.index.dayofyear
serie_d['ETP'] = serie_d.apply(lambda x : calcular_EVP3(x['T_med'].values[0],latitude, x['d_j'].values[0]), axis = 1)
serie_d = serie_d.loc['2018':]
serie_d = serie_d[['T_med', 'ETP']]
serie_d.columns = ['t_med', 'etp']
serie_d.to_csv('etp_d_braganca_paulista.csv', float_format='%.3f')

## APLICA PARABOLA HORARIA E TRANSFORMA EM UTC
## COMO ETP NAO É INFLUENCIADA NO PERIODO DA NOITE, A DIVISAO DOS DIAS P/ ETP DIARIA NAO IMPORTA
## BRT SE INICIA AS 7 HORAS, UTC AS 10

ETPH=[]
tempos=[]
for data,E in zip(serie_d.index,serie_d['etp']):
    A=-6*E/2197
    B=150/2197*E
    C=-684/2197*E
    for hora in range(0,24):
        ETP=A*hora**2+B*hora+C
        if ETP<0:
            ETP=0
        ETPH.append(ETP)
        tempos.append(str(data)+f' {hora}:00')

dados_horarios=pd.DataFrame({'datahora':tempos,'ETPH':ETPH})
dados_horarios['datahora']=pd.to_datetime(dados_horarios['datahora'])
dados_horarios.index = dados_horarios['datahora']
dados_horarios = dados_horarios[['ETPH']]
dados_horarios['ETPH']=dados_horarios['ETPH'].round(decimals=3)
#Localiza dados em BRT(-03:00) e converte para UTC, no formato padrao
dados_horarios.index = (pd.to_datetime(dados_horarios.index) + dt.timedelta(hours=3)).tz_localize('utc')
dados_horarios.to_csv('etp_h_braganca_paulista.csv', float_format='%.3f')

##DADOS 6 HRS
dados_6hrs = dados_horarios.resample("6H", closed='right', label='right').agg({'ETPH' : np.sum})
