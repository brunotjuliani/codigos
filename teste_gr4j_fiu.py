
import sys
sys.path.append('/home/bruno/github/modelos/')
import gr4j
import spot_setup
import funcoes_objetivo
import pandas as pd
import spotpy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec


# Leitura das forcantes
arq = open('/discolocal/bruno/Observado/Teste/reservatorio_fiu.peq')
area = float(arq.readline())
df = pd.read_csv('/discolocal/bruno/Observado/Teste/reservatorio_fiu.peq',
                 skiprows=1)
df = df.dropna()
idx = df['data']
PME = df['pme'].to_numpy()
ETP = df['etp'].to_numpy()
Qjus = df['qjus'].to_numpy()

df['datetime'] = pd.to_datetime(df['data'])
df = df.set_index('datetime')

def plotHH(t,sP,sQ):
    fig = plt.figure()
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 2])

    # HYDROGRAM CHART
    ax = plt.subplot(gs[1])
    ax.plot(t,sQ)
    ax.set_ylabel(u'Q(m³/s)', color='b')
    ax.set_xlabel('Time (min.)')
    ax.tick_params(axis='y', colors='b')
    ax.xaxis.grid(b=True, which='major', color='.7', linestyle='-')
    ax.yaxis.grid(b=True, which='major', color='.7', linestyle='-')
    ax.set_xlim(min(t), max(t))
    ax.set_ylim(0, max(sQ)*1.2)

    # PRECIPITATION/HYETOGRAPH CHART
    ax2 = plt.subplot(gs[0])
    ax2.bar(t, sP, 1, color='red')
    ax2.xaxis.grid(b=True, which='major', color='.7', linestyle='-')
    ax2.yaxis.grid(b=True, which='major', color='0.7', linestyle='-')
    ax2.set_ylabel('P(mm)')
    ax2.set_xlim(min(t), max(t))
    plt.setp(ax2.get_xticklabels(), visible=False)

    plt.tight_layout()
    ax2.invert_yaxis()
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.show()
    #plt.savefig(filename,format='pdf')
    plt.close(fig)

plotHH(df.index, df['pme'], df['qjus'])

# Teste de verificacao da implementacao do calibrador

import matplotlib.pyplot as plt

def calibra_e_plota(fobj):
    setup = spot_setup.gr4j_muskingum(area, PME, ETP, Qjus, h_aq=365, fobj=fobj)
    sampler = spotpy.algorithms.sceua(setup, dbname='SCEUA_gr4j_20out2020', dbformat='csv')
    sampler.sample(5000, ngs=6, kstop=3, peps=0.1, pcento=0.1)
    results = sampler.getdata()
    params = spotpy.analyser.get_best_parameterset(results,maximize=False)
    x1, x2, x3, x4 = params[0][0], params[0][1], params[0][2], params[0][3]
    k, x = params[0][4], params[0][5]
    Qsim = gr4j.sim_muskingum(area, PME, ETP, x1, x2, x3, x4, k, x)
    return Qsim

fobj = 'NSE'
Qsim = calibra_e_plota(fobj)
plt.plot(idx, Qsim, label=fobj)

plt.plot(idx, Qjus, label='Qobs')

plt.legend()
plt.show()
