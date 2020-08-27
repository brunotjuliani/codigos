#BLIBLIOTECAS
import HydroErr as he
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime as dt
gbl = globals()


#DEFINICAO ENDERECOS
dir_horizontes = "/home/bruno/Documentos/Historico_Horizontes"
dir_desempenho = "/home/bruno/Documentos/Historico_Horizontes/Desempenho"


#DEFINICAO PERIODO ANALISE
data_ini = dt.datetime(2015, 9, 3,  0,  0) #YYYY, M, D, H, Min
data_fim = dt.datetime(2020, 8, 20,  23,  59)


#DEFINICAO MODELOS
modelos = ["112", "114", "116", "117"]
horas_resumo = [1, 6] + list(np.arange(12,169,12))
horizontes = range(168)

#IMPORTA MODELO A ANALIZAR
for modelo in modelos:
    os.chdir(dir_horizontes)
    gbl["evolucao_horizontes_"+modelo] = pd.DataFrame()
    for horizonte in horizontes:
        os.chdir(dir_horizontes + "/" + modelo)
        gbl["avaliacao_"+modelo+"_"+str(horizonte)] = pd.read_csv("Cod_"+modelo+"_Horizonte_"+str(horizonte)+".csv", header = 0)
        gbl["avaliacao_"+modelo+"_"+str(horizonte)] = gbl["avaliacao_"+modelo+"_"+str(horizonte)].loc[gbl["avaliacao_"+modelo+"_"+str(horizonte)]["Data"].between(str(data_ini), str(data_fim))]
        gbl["Nash_"+modelo+"_"+str(horizonte)] = he.nse(gbl["avaliacao_"+modelo+"_"+str(horizonte)]["Vazao_prev"],gbl["avaliacao_"+modelo+"_"+str(horizonte)]["vazao_obs"])
        gbl["KGE_Mod_"+modelo+"_"+str(horizonte)] = he.kge_2012(gbl["avaliacao_"+modelo+"_"+str(horizonte)]["Vazao_prev"],gbl["avaliacao_"+modelo+"_"+str(horizonte)]["vazao_obs"])
        gbl["evolucao_horizontes_"+modelo].loc[horizonte, "Hora"] = horizonte + 1
        gbl["evolucao_horizontes_"+modelo].loc[horizonte, "Nash"] = gbl["Nash_"+modelo+"_"+str(horizonte)]
        gbl["evolucao_horizontes_"+modelo].loc[horizonte, "KGE_Mod"] = gbl["KGE_Mod_"+modelo+"_"+str(horizonte)]
    os.chdir(dir_desempenho)
    plt.figure()
    plt.plot(gbl["evolucao_horizontes_"+modelo].Hora, gbl["evolucao_horizontes_"+modelo].Nash, label = "Nash-Sutcliffe")
    plt.plot(gbl["evolucao_horizontes_"+modelo].Hora, gbl["evolucao_horizontes_"+modelo].KGE_Mod, label = "KGE-2012")
    plt.xticks(np.arange(0, max(gbl["evolucao_horizontes_"+modelo].Hora)+1, 24))
    plt.legend(loc='best')
    plt.title('Ajuste - Modelo '+modelo)
    plt.xlabel('Horizonte (h)')
    plt.ylabel('Coeficiente')
    plt.savefig(modelo+"_Avaliacao_"+data_ini.strftime("%Y%m%d")+"_"+data_fim.strftime("%Y%m%d")+".png")
    plt.close()
    gbl["evolucao_horizontes_"+modelo].to_csv(modelo+"_Avaliacao_"+data_ini.strftime("%Y%m%d")+"_"+data_fim.strftime("%Y%m%d")+".csv")
    gbl["evolucao_horizontes_"+modelo].loc[gbl["evolucao_horizontes_"+modelo]['Hora'].isin(horas_resumo)].to_csv(modelo+"_Resumo_"+data_ini.strftime("%Y%m%d")+"_"+data_fim.strftime("%Y%m%d")+".csv")
