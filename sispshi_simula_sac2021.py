import pandas as pd
import sacsma2021
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Leitura
PEQ = pd.read_csv('sispshi_01_Rio_Negro_peq.csv', skiprows=1, index_col='datahora')
area = pd.read_csv('sispshi_01_Rio_Negro_peq.csv', nrows=1, header=None).values[0][0]
dt = 0.25
PME = PEQ['pme']
ETP = PEQ['etp']
Qjus = PEQ['qjus']
fconv = area/(dt*86.4) # mm -> m3/s

params = pd.read_csv('sispshi_par_sacsma2021_01.csv', index_col='parNome').to_dict('dict')['parValor']
params2 = pd.read_csv('sispshi_par_sacsma2021_01.csv', index_col='parNome').to_dict('dict')['par2']

Qsim, Qbfp, Qbfs, Qtci, Qtco = sacsma2021.simulacao(area, dt, PME, ETP, params, Qmon=None, estados=None)
Qsim2, Qbfp2, Qbfs2, Qtci2, Qtco2 = sacsma2021.simulacao(area, dt, PME, ETP, params2, Qmon=None, estados=None)


# Plotagem
fig = make_subplots(rows=3, cols=1, shared_xaxes=True, specs=[[{'rowspan': 1, 'colspan': 1}],[{'rowspan': 2, 'colspan': 1}],[{'rowspan': 0, 'colspan': 0}]])
fig.add_trace(go.Scatter(x=PEQ.index, y=PME, name="PME (mm)"), row=1, col=1)
fig['layout']['yaxis']['autorange'] = "reversed"
fig.add_trace(go.Scatter(x=PEQ.index, y=ETP, name="ETP (mm)"), row=1, col=1)
fig.add_trace(go.Scatter(x=PEQ.index, y=Qjus, name="Qobs (m3/s)", marker_color='black'), row=2, col=1)
fig['data'][2]['line']['color']="black"
fig.add_trace(go.Scatter(x=PEQ.index, y=Qsim, name='Qsim - 1', marker_color='green'), row=2, col=1)
fig.add_trace(go.Scatter(x=PEQ.index, y=Qsim2, name='Qsim - 2', marker_color='red'), row=2, col=1)
fig.update_yaxes(title_text='Chuva [mm]', row=1, col=1)
fig.update_yaxes(title_text='Vazão [m3s-1]', row=2, col=1)
fig.update_layout(legend_title_text='Comparação Modelo Sacramento')
fig.update_layout(autosize=False,width=800,height=450,margin=dict(l=30,r=30,b=10,t=10))
fig.show()
