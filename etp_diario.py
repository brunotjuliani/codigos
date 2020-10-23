import pandas as pd
import numpy as np
import pyet
import math

meteo = pd.read_csv('/discolocal/bruno/Observado/Teste/Londrina_dados_etp.csv',
                    index_col = 0, sep = ';')

tmax = meteo.loc[:,"Tmax"]
tmin = meteo.loc[:,"Tmin"]
rh = meteo.loc[:,"Rh"]
wind = meteo.loc[:,"Vento"]
solar = meteo.loc[:,"Rad_Solar"]
elevation = 585
latitude = math.radians(-23.3595)

fao56 = et.pm_fao56(wind = wind, elevation = elevation, latitude = latitude,
                    solar = solar, tmax = tmax, tmin = tmin, rh = rh)
fao56.to_csv('/discolocal/bruno/Observado/Teste/'+posto_nome+
                 '_etp.csv',date_format='%Y-%m-%dT%H:%M:%SZ',
                 sep = ";",float_format = '%.3f')
