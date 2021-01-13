from netCDF4 import Dataset
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
import glob
from time import time
import xarray as xr
import geopandas as gpd

inicio='2013-01-01 00:00:00'
fim='2020-12-31 23:59:59'
periodo=pd.date_range(start=inicio,end=fim,freq='1h',closed=None)
df_resumo = pd.DataFrame(index=periodo)

grade = gpd.read_file('../dados/grade/grade_fiu_2.gpkg')
df_grade = pd.DataFrame(columns = ['Long', 'Lat'])
df_grade['Long'] = grade.geometry.x
df_grade['Lat'] = grade.geometry.y
for i in df_grade.index:
    df_resumo[i] = np.nan
for tempo in periodo:
    if tempo.hour == 0:
        print(tempo)
    try:
        hora=tempo.hour
        ano=tempo.year
        mes=tempo.month
        dia=tempo.day
        arquivo =f'/simepar/product/siprec/simepar/L4/nc/hourly/{ano}/{mes:02d}/{dia:02d}/siprec_v2_{ano}_{mes:02d}_{dia:02d}_{hora:02d}.nc'
        da=xr.open_dataset(arquivo)
        for i in df_grade.index:
            lon = df_grade.loc[i,'Long']
            lat = df_grade.loc[i,'Lat']
            try:
                chuva_ponto=da['SIPREC'].sel(latitudes=lat,longitudes=lon,method='nearest',drop=True)[0].values
            except:
                chuva_ponto=da['SIPREC'].sel(lat_sat=lat,lon_sat=lon,method='nearest',drop=True).values
            df_resumo.loc[tempo,i] = chuva_ponto
        da.close()
    except Exception as e:
        print(e)
df_resumo['Media'] = df_resumo.mean(axis=1)
df_resumo.to_csv('../dados/pme/fiu_siprec.csv', sep = ',',
                 date_format='%Y-%m-%dT%H:%M:%S+00:00', float_format='%.2f')
