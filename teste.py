import pandas as pd
import numpy as np
from datetime import date, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import sys
sys.path.append('../modelos/')
from plotar_hidro import plotar_hidro
from json import loads

bac = 12
dirSite = 'abc/'

pc = (dirSite + str('vaz%2.2i.json' % bac))
pc

arq = '../vaz12.json'
with open(arq) as f:
    file_data = f.read()
file_data
file_data = file_data.replace('nan', 'null')
xy = loads(file_data)
del file_data
file_data

json_file = 'my_file.json'


with open(json_file) as f:
    file_data = f.read()

file_data = file_data.replace('REPLACE_ME', 'new string')
<...>

with open(json_file, 'w') as f:
    f.write(file_data)

xy = loads(arq.read())
arq = open('../vaz12.json' % bac), 'r')
    xy = loads(arq.read())
    for i in range(len(xy)):
        dt = datetime.strptime(xy[i][0], '%Y-%m-%d %H:%M:%S')
        try:
            dados[dt][1] = xy[i][1]
        except KeyError:
            dados[dt] = ref[:]
            dados[dt][1] = xy[i][1]
    arq.close()
