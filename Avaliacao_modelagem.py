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
data_fim = dt.datetime(2020, 8, 30,  23,  59)


#DEFINICAO MODELOS
modelos = ["212", "214", "216", "217"]
horas_resumo = [1, 6] + list(np.arange(12,169,12))
horizontes = range(168)



#IMPORTA MODELO A ANALIZAR

dir_aval = (dir_desempenho + '/aval_' + modelos[0][-3] + '_' +
            data_ini.strftime("%Y%m%d") + "_" + data_fim.strftime("%Y%m%d"))
try:
    os.mkdir(dir_aval)
except OSError as error:
    pass
nash_completo = pd.DataFrame()
nash_resumo = pd.DataFrame()
kge_completo = pd.DataFrame()
kge_resumo = pd.DataFrame()
for modelo in modelos:
    os.chdir(dir_horizontes)
    gbl["evolucao_horizontes_"+modelo] = pd.DataFrame()
    for horizonte in horizontes:
        os.chdir(dir_horizontes + "/" + modelo)
        gbl["avaliacao_"+modelo+"_"+str(horizonte)] = (
            pd.read_csv("Cod_"+modelo+"_Horizonte_"+str(horizonte)+".csv",
                        header = 0))
        gbl["avaliacao_"+modelo+"_"+str(horizonte)] = (
            gbl["avaliacao_"+modelo+"_"+str(horizonte)].loc[
                gbl["avaliacao_"+modelo+"_"+str(horizonte)]["Data"].between(
                    str(data_ini), str(data_fim))])
        gbl["Nash_"+modelo+"_"+str(horizonte)] = he.nse(
            gbl["avaliacao_"+modelo+"_"+str(horizonte)]["Vazao_prev"],
            gbl["avaliacao_"+modelo+"_"+str(horizonte)]["vazao_obs"])
        gbl["KGE_Mod_"+modelo+"_"+str(horizonte)] = he.kge_2012(
            gbl["avaliacao_"+modelo+"_"+str(horizonte)]["Vazao_prev"],
            gbl["avaliacao_"+modelo+"_"+str(horizonte)]["vazao_obs"])
        gbl["evolucao_horizontes_"+modelo].loc[horizonte,"Hora"] = horizonte + 1
        gbl["evolucao_horizontes_"+modelo].loc[horizonte,"Nash"] = gbl[
            "Nash_"+modelo+"_"+str(horizonte)]
        gbl["evolucao_horizontes_"+modelo].loc[horizonte, "KGE_Mod"] = gbl[
            "KGE_Mod_"+modelo+"_"+str(horizonte)]
    os.chdir(dir_aval)
    plt.figure()
    plt.plot(gbl["evolucao_horizontes_"+modelo].Hora,
             gbl["evolucao_horizontes_"+modelo].Nash, label = "Nash-Sutcliffe")
    plt.plot(gbl["evolucao_horizontes_"+modelo].Hora,
             gbl["evolucao_horizontes_"+modelo].KGE_Mod, label = "KGE-2012")
    plt.xticks(np.arange(0, max(gbl["evolucao_horizontes_"+modelo].Hora)+1, 24))
    plt.legend(loc='best')
    plt.title('Ajuste - Modelo '+modelo)
    plt.xlabel('Horizonte (h)')
    plt.ylabel('Coeficiente')
    plt.savefig(modelo+"_Avaliacao_"+data_ini.strftime("%Y%m%d")+"_"+
                data_fim.strftime("%Y%m%d")+".png")
    plt.close()
    nash_completo['Nash_'+modelo] = gbl["evolucao_horizontes_"+modelo]['Nash']
    nash_resumo['Nash_'+modelo] = gbl["evolucao_horizontes_"+modelo][
        'Nash'].loc[gbl["evolucao_horizontes_"+modelo]['Hora'].isin(
            horas_resumo)]
    kge_completo['KGE_'+modelo] = gbl["evolucao_horizontes_"+modelo]['KGE_Mod']
    kge_resumo['KGE_'+modelo] = gbl["evolucao_horizontes_"+modelo][
        'KGE_Mod'].loc[gbl["evolucao_horizontes_"+modelo]['Hora'].isin(
            horas_resumo)]
nash_completo.to_csv('Nash_'+modelos[0][-3]+'_'+data_ini.strftime("%Y%m%d") +
                     "_" + data_fim.strftime("%Y%m%d"))
nash_resumo.to_csv('Resumo_Nash_'+modelos[0][-3]+'_'+
                   data_ini.strftime("%Y%m%d")+"_"+data_fim.strftime("%Y%m%d"))
kge_completo.to_csv('KGE_' + modelos[0][-3] +'_'+ data_ini.strftime("%Y%m%d") +
                     "_" + data_fim.strftime("%Y%m%d"))
kge_resumo.to_csv('Resumo_KGE' + modelos[0][-3]+'_'+data_ini.strftime("%Y%m%d")+
                     "_" + data_fim.strftime("%Y%m%d"))
