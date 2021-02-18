import pandas as pd, numpy as np
import psycopg2, psycopg2.extras
import datetime as dt

hist = pd.read_csv('../dados/vazoesfluviometricas_passauna.txt', header = None, sep=' ')
hist

hist = hist.drop([8, 9, 10], axis=1)
hist = hist.replace('-', np.nan)
hist['data'] = pd.to_datetime(hist[[1,2,3]], errors='coerce')
serie = pd.DataFrame()
serie['data'] = pd.to_datetime(hist[[1,2,3]])


previsao_7d["Data"] = pd.to_datetime(previsao_7d[["Year", "Month", "Day"]])
