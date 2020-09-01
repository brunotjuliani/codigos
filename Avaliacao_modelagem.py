#BIBLIOTECAS
import os
import HydroErr as he
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
gbl = globals()


#DEFINICAO ENDERECOS
dir_horizontes = "/home/bruno/Documentos/Historico_Horizontes"
dir_desempenho = "/home/bruno/Documentos/Historico_Horizontes/Desempenho"
dir_observado = "/home/bruno/Documentos/Observado"

#DEFINICAO PERIODO ANALISE
data_ini = dt.datetime(2015, 9, 3,  0,  0) #YYYY, M, D, H, Min
data_fim = dt.datetime(2020, 8, 30,  23,  59)



#DEFINICAO MODELOS
calibracoes = {
                'Rio_Negro' : ['112', '114', '116', '117'],
                'Porto_Amazonas' : ['212', '214', '216', '217'],
                'Sao_Bento' : ['312', '314', '316', '317'],
                'Pontilhao' : ['412', '414', '416', '417'],
                'Santa_Cruz_Timbo' : ['512', '514', '516', '517'],
                'Sao_Mateus_Sul' : ['612', '614', '616', '617'],
                'Divisa' : ['712', '714', '716', '717'],
                'Fluviopolis' : ['812', '814', '816', '817'],
                'Uniao_da_Vitoria' : ['912', '914', '916', '917'],
                'Madereira_Gavazzoni' : ['1010', '1012', '1014', '1015'],
                'Jangada' : ['1110', '1112', '1114', '1115'],
                'Solais_Novo' : ['1310', '1312', '1314', '1315'],
                'Porto_Santo_Antonio' : ['1410', '1412', '1414', '1415'],
                'Aguas_do_Vere' : ['1510', '1512', '1514', '1515'],
                'Porto_Capanema' : ['2010', '2012'],
                'Hotel_Cataratas' : ['2110', '2112', '2114', '2115'],
            }


horas_resumo = [1, 6] + list(np.arange(12,169,12))
horizontes = range(168)

#IMPORTA MODELO A ANALIZAR
for nome_bacia, modelos in calibracoes.items():
    #codigo da bacia
    bacia = modelos[0][:-2]

    #cria pasta para bacia e periodo analisado
    dir_aval = (dir_desempenho + '/aval_' + bacia + '_' +
                data_ini.strftime("%Y%m%d") + "_" + data_fim.strftime("%Y%m%d"))
    try:
        os.mkdir(dir_aval)
    except OSError as error:
        pass

    #importa vazao observada para periodo analisado
    os.chdir(dir_observado)
    serie_observada = pd.read_csv('vazao_' + nome_bacia + '.csv', index_col = 0)
    serie_observada.index = pd.to_datetime(serie_observada.index)
    serie_observada = serie_observada.loc[str(data_ini) : str(data_fim)]

    #cria dataframes vazios
    nash_completo = pd.DataFrame()
    nash_resumo = pd.DataFrame()

    #loop para diferentes calibracoes de uma mesma bacia
    #inicia figura
    plt.figure()
    for modelo in modelos:
        os.chdir(dir_horizontes)
        gbl["evolucao_horizontes_"+modelo] = pd.DataFrame()

        #loop para diferentes horizontes
        for horizonte in horizontes:
            #le arquivo de cada horizonte
            os.chdir(dir_horizontes + "/" + modelo)
            gbl["avaliacao_"+modelo+"_"+str(horizonte)] = (
                pd.read_csv("Cod_"+modelo+"_Horizonte_"+str(horizonte)+".csv",
                            header = 0))
            #recorta horizonte para periodo analisado
            gbl["avaliacao_"+modelo+"_"+str(horizonte)] = (
                gbl["avaliacao_"+modelo+"_"+str(horizonte)].loc[
                    gbl["avaliacao_"+modelo+"_"+str(horizonte)]["Data"].between(
                        str(data_ini), str(data_fim))])
            #aplica Nash para cada horizonte
            gbl["Nash_"+modelo+"_"+str(horizonte)] = he.nse(
                gbl["avaliacao_"+modelo+"_"+str(horizonte)]["Vazao_prev"],
                gbl["avaliacao_"+modelo+"_"+str(horizonte)]["vazao_obs"])
            #armazena no df geral com todos horizontes
            gbl["evolucao_horizontes_"+modelo].loc[horizonte,"Hora"]=horizonte+1
            gbl["evolucao_horizontes_"+modelo].loc[horizonte,"Nash"] = gbl[
                "Nash_"+modelo+"_"+str(horizonte)]

        #salva os resultados de cada calibracao em uma coluna para mesma bacia
        os.chdir(dir_aval)
        #arquivo completo com todos horizontes
        nash_completo['Nash_'+modelo]=gbl["evolucao_horizontes_"+modelo]['Nash']
        #arquivo resumo com passos de 12 horas
        nash_resumo['Nash_'+modelo] = gbl["evolucao_horizontes_"+modelo][
            'Nash'].loc[gbl["evolucao_horizontes_"+modelo]['Hora'].isin(
                horas_resumo)]
        #armazena linha de cada calibracao na figura
        plt.plot(gbl["evolucao_horizontes_"+modelo].Hora,
                 gbl["evolucao_horizontes_"+modelo].Nash,
                 label = "Calibracao "+modelo)
    #continua figura e exporta para cada bacia
    plt.ylim(0,1)
    plt.yticks(np.arange(0.0, 1.0, 0.1))
    plt.xlim(0, 168)
    plt.xticks(np.arange(0, max(gbl["evolucao_horizontes_"+modelo].Hora)+1, 24))
    plt.grid()
    plt.legend(loc='best')
    plt.title('Ajuste Nash - Modelo '+bacia)
    plt.xlabel('Horizonte (h)')
    plt.ylabel('Coeficiente Nash')
    plt.savefig(bacia+"_Nash_"+data_ini.strftime("%Y%m%d")+"_"+
                data_fim.strftime("%Y%m%d")+".png", dpi = 300)
    plt.close()

    #exporta dados de resultado em tabela
    nash_completo.to_csv('Nash_'+bacia+'_'+data_ini.strftime("%Y%m%d") + "_" +
                         data_fim.strftime("%Y%m%d") + '.csv')
    nash_resumo.to_csv('Resumo_Nash_' + bacia +'_'+ data_ini.strftime("%Y%m%d")+
                       "_" + data_fim.strftime("%Y%m%d")+ '.csv')

    #exporta figura com serie historica observada para periodo analisado
    plt.figure()
    plt.plot(serie_observada['q_m3s'], label = "Observado", linewidth = 0.5)
    plt.title('Serie ' + nome_bacia)
    plt.xlabel('Data')
    plt.ylabel('Q [m3s-1]')
    plt.savefig(bacia+'_observado_'+data_ini.strftime("%Y%m%d")+"_"+
                          data_fim.strftime("%Y%m%d")+'.png', dpi = 300)
    plt.close()

    #finaliza cada bacia e imprime horario de finalizacao
    print("Concluido Bacia ",bacia)
    print(dt.datetime.now())
