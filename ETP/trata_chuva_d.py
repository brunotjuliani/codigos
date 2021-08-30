import pandas as pd
import numpy as np

serie = pd.read_csv('25435458_simepar.csv', skiprows=2, index_col='datahora', parse_dates=True)

serie_dia = (serie.resample("D", closed='right').agg({'chuva_mm':np.sum}))

serie_dia = serie_dia.loc['2019':]
serie_dia.index = serie_dia.index.strftime('%Y-%m-%d')
serie_dia.to_csv(f'./simepar_25435458.csv', float_format='%.2f')
