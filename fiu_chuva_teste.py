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

for tempo in periodo:
    print(tempo)
    try:
        hora=tempo.hour
        ano=tempo.year
        mes=tempo.month
        dia=tempo.day
        arquivo =f'/simepar/product/siprec/simepar/L4/nc/hourly/{ano}/{mes:02d}/{dia:02d}/siprec_v2_{ano}_{mes:02d}_{dia:02d}_{hora:02d}.nc'
        da=xr.open_dataset(arquivo)
        da.close()
    except Exception as e:
        print(e)
