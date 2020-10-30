
import sys
sys.path.append('/home/bruno/github/modelos/')
import spot_setup
import pandas as pd
import spotpy
import numpy as np
import gr4j
import matplotlib.pyplot as plt
from matplotlib import gridspec
from spotpy.analyser import *
from spotpy.algorithms import sceua
from plotar_hidro import plotar_hidro

# Leitura das forcantes
arq = open('/discolocal/bruno/Observado/Teste/reservatorio_fiu.peq')
area = float(arq.readline())
df = pd.read_csv('/discolocal/bruno/Observado/Teste/reservatorio_fiu.peq',
                 skiprows=[0], index_col = 'data', parse_dates = True)
PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()
idx = df.index.to_numpy()

#df = df.loc['2020']

# def plotHH(t,sP,sQ):
#     fig = plt.figure()
#     gs = gridspec.GridSpec(2, 1, height_ratios=[1, 2])
#
#     # HYDROGRAM CHART
#     ax = plt.subplot(gs[1])
#     ax.plot(t,sQ)
#     ax.set_ylabel(u'Q(m³/s)', color='b')
#     ax.set_xlabel('Time (min.)')
#     ax.tick_params(axis='y', colors='b')
#     ax.xaxis.grid(b=True, which='major', color='.7', linestyle='-')
#     ax.yaxis.grid(b=True, which='major', color='.7', linestyle='-')
#     ax.set_xlim(min(t), max(t))
#     ax.set_ylim(0, max(sQ)*1.2)
#
#     # PRECIPITATION/HYETOGRAPH CHART
#     ax2 = plt.subplot(gs[0])
#     ax2.bar(t, sP, 1, color='red')
#     ax2.xaxis.grid(b=True, which='major', color='.7', linestyle='-')
#     ax2.yaxis.grid(b=True, which='major', color='0.7', linestyle='-')
#     ax2.set_ylabel('P(mm)')
#     ax2.set_xlim(min(t), max(t))
#     plt.setp(ax2.get_xticklabels(), visible=False)
#
#     plt.tight_layout()
#     ax2.invert_yaxis()
#     plt.gcf().subplots_adjust(bottom=0.15)
#     plt.show()
#     #plt.savefig(filename,format='pdf')
#     plt.close(fig)
#
# plotHH(df.index, df['pme'], df['qjus'])

### CALIBRAR
spot_setup = spot_setup.setup_gr4j_nash(area, PME, ETP, Qjus, h_aq=365, fobj='KGE')
sampler = sceua(spot_setup)
sampler.sample(5000, ngs=10, kstop=3, peps=0.1, pcento=0.1)
results = sampler.getdata()
params = get_best_parameterset(results,maximize=False)
bestindex, bestobjf = get_minlikeindex(results)
simulation_fields = get_simulation_fields(results)
Qsim = {}
Qsim['best_NSE'] = list(results[simulation_fields][bestindex][0])

# Plotagem
fig = plotar_hidro(idx=df.index, PME=PME, ETP=ETP, Qobs=Qjus, Qmon=None, Qsim=Qsim['best_NSE'])
