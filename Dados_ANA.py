import hydrobr
import pandas as pd


PR = hydrobr.get_data.ANA.list_prec_stations(state='Paraná', source='ANA')


print(PR)


estacoes_60anos = pd.DataFrame()
for i in PR.index:
    linha_estacao = pd.DataFrame()
    codigo = {PR.loc[i,"Code"]}
    serie = hydrobr.get_data.ANA.prec_data(codigo, only_consisted=False)
    tamanho = len(serie) / 365
    falhas = serie.isna().sum()
    falha_percent = (falhas / len(serie))*100
    if tamanho >= 60:
        linha_estacao = PR.iloc[[i,]]
        linha_estacao["N_Anos"] = tamanho
        linha_estacao["Falhas_porcent"] = falha_percent
        concatenar = [estacoes_60anos, linha_estacao]
        estacoes_60anos = pd.concat(concatenar)
