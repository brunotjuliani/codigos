#from netCDF4 import Dataset
import numpy as np
import pandas as pd
#from pathlib import Path
#from datetime import datetime
#import glob
#from time import time
import xarray as xr
import os

arquivo ='siprec_v2_2021_07_05_00.nc'
da=xr.open_dataset(arquivo, engine = 'netcdf4')
lat_list = np.clip(da.latitudes.values, -28, -22)
lat_list
lon_list = np.clip(da.longitudes.values, -56, -47)
lon_list
df = pd.DataFrame()
for i in lon_list:
    for j in lat_list:
        df['lon'] = i
        df['lat'] = j

# df = pd.DataFrame()
# df['lat'] = da.latitudes
# df['lon'] = da.longitudes
# da.close()
#
# df.to_csv('pontos_siprec.csv', index=False)
