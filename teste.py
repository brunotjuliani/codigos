import pandas as pd
import numpy as np
from datetime import date, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import sys
sys.path.append('../modelos/')
from plotar_hidro import plotar_hidro

arq = open('../dados/peq/bacia_01.peq')
areainc = float(arq.readline())
area = areainc
df = pd.read_csv('../dados/peq/bacia_01.peq', skiprows=[0],
                 index_col = 'datahora_UTC', parse_dates = True)
df2 = df.loc['2019':'2020']

fig = plotar_hidro(idx=df2.index, PME=df2['pme'], ETP=df2['etp'],
                   Qobs=df2['qjus'], Qmon=None, Qsims=None)
