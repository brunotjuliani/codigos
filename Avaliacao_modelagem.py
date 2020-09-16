#BIBLIOTECAS
import os
import HydroErr as he
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
gbl = globals()


#DEFINICAO ENDERECOS
dir_horizontes = "/discolocal/bruno/Historico_Horizontes"
dir_desempenho = "/discolocal/bruno/Historico_Horizontes/Desempenho"
dir_observado = "/discolocal/bruno/Observado"
dir_usinas = "/discolocal/bruno/Coleta_Dados/Dados_Usinas"

#DEFINICAO PERIODO ANALISE
data_ini = dt.datetime(2015, 9, 3,  0,  0) #YYYY, M, D, H, Min
data_fim = dt.datetime(2020, 9, 10,  23,  59)
data_texto = ('Data inicial: ' + str(data_ini.strftime("%Y-%m-%d")) + '\n' +
              'Data final: ' + str(data_fim.strftime("%Y-%m-%d")))

#DEFINICAO MODELOS ESTACOES
calibracoes = {
#                'Rio_Negro' : ['112', '114', '116', '117'],
#                'Porto_Amazonas' : ['212', '214', '216', '217'],
#                'Sao_Bento' : ['312', '314', '316', '317'],
#                'Pontilhao' : ['412', '414', '416', '417'],
#                'Santa_Cruz_Timbo' : ['512', '514', '516', '517'],
#                'Sao_Mateus_Sul' : ['612', '614', '616', '617'],
                'Divisa' : ['712', '714', '716', '717'],
#                'Fluviopolis' : ['812', '814', '816', '817'],
#                'Uniao_da_Vitoria' : ['912', '914', '916', '917'],
#                'Madereira_Gavazzoni' : ['1010', '1012', '1014', '1015'],
#                'Jangada' : ['1110', '1112', '1114', '1115'],
#                'Solais_Novo' : ['1310', '1312', '1314', '1315'],
#                'Porto_Santo_Antonio' : ['1410', '1412', '1414', '1415'],
#                'Aguas_do_Vere' : ['1510', '1512', '1514', '1515'],
#                'Porto_Capanema' : ['2010', '2012'],
#                'Hotel_Cataratas' : ['2110', '2112', '2114', '2115'],
            }
calibracoes_usinas ={
                'GBM' : ['1210', '1212', '1214', '1215', '1218', '1219'],
                'SGD' : ['1610', '1612', '1614', '1615'],
                'FCH' : ['1710', '1712', '1714', '1715'],
                'SCL' : ['1810', '1812'],
                'SCX' : ['1910', '1912'],
}

horas_resumo = [1, 6] + list(np.arange(12,169,12))
horizontes = range(168)

#IMPORTA MODELO A ANALIZAR PARA ESTACOES
for nome_bacia, modelos in calibracoes.items():
    #codigo da bacia
    bacia = modelos[0][:-2]

    #imprime horario de início
    print("Inicia Bacia ",bacia)
    print(dt.datetime.now())

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
    serie_observada = serie_observada[data_ini : data_fim]

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
                            header = 0, index_col = 0))
            #junta com vazao observada
            gbl["avaliacao_"+modelo+str(horizonte)] = gbl[
                "avaliacao_"+modelo+str(horizonte)].merge(serie_observada[
                    'q_m3s'],how='left',left_index=True,right_index=True)
            #remove linhas sem Valor observado
            gbl["avaliacao_"+modelo+"_"+str(horizonte)] = gbl[
                "avaliacao_"+modelo+"_"+str(horizonte)].dropna()
            #recorta horizonte para periodo analisado
            gbl["avaliacao_"+modelo+"_"+str(horizonte)] = (gbl[
                "avaliacao_"+modelo+"_"+str(horizonte)][data_ini : data_fim])
            #aplica Nash para cada horizonte
            gbl["Nash_"+modelo+"_"+str(horizonte)] = he.nse(
                gbl["avaliacao_"+modelo+"_"+str(horizonte)]["Vazao_prev"],
                gbl["avaliacao_"+modelo+"_"+str(horizonte)]["q_m3s"])
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
    plt.title('Ajuste Nash - Modelo '+bacia, loc = 'left')
    plt.xlabel('Horizonte (h)')
    plt.ylabel('Coeficiente Nash')
    plt.annotate(data_texto, xy=(1,1), xytext=(-4,26), fontsize=10,
                 xycoords='axes fraction', textcoords='offset points',
                 bbox=dict(facecolor='white', alpha=0.8),
                 horizontalalignment='right', verticalalignment='top')
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
    plt.title('Serie ' + nome_bacia, loc = 'left')
    plt.xlabel('Data')
    plt.ylabel('Q [m3s-1]')
    plt.annotate(data_texto, xy=(1,1), xytext=(-4,26), fontsize=10,
                 xycoords='axes fraction', textcoords='offset points',
                 bbox=dict(facecolor='white', alpha=0.8),
                 horizontalalignment='right', verticalalignment='top')
    plt.savefig(bacia+'_observado_'+data_ini.strftime("%Y%m%d")+"_"+
                          data_fim.strftime("%Y%m%d")+'.png', dpi = 300)
    plt.close()

    #finaliza cada bacia e imprime horario de finalizacao
    print("Concluido Bacia ",bacia)
    print(dt.datetime.now())


#IMPORTA MODELO A ANALIZAR PARA USINAS
for nome_bacia, modelos in calibracoes_usinas.items():
    #codigo da bacia
    bacia = modelos[0][:-2]

    #imprime horario de início
    print("Inicia Bacia ",bacia)
    print(dt.datetime.now())

    #cria pasta para bacia e periodo analisado
    dir_aval = (dir_desempenho + '/aval_' + bacia + '_' +
                data_ini.strftime("%Y%m%d") + "_" + data_fim.strftime("%Y%m%d"))
    try:
        os.mkdir(dir_aval)
    except OSError as error:
        pass

    #importa vazao observada para periodo analisado
    os.chdir(dir_usinas)
    serie_observada = pd.read_csv(nome_bacia+".txt", header = None, skiprows = 1)
    serie_observada['Year'] = serie_observada[0].str.slice(0,4)
    serie_observada['Month'] = serie_observada[0].str.slice(5,7)
    serie_observada['Day'] = serie_observada[0].str.slice(8,10)
    serie_observada['Hora'] = serie_observada[0].str.slice(11,13).astype(str).astype(int)
    serie_observada['q_m3s'] = pd.to_numeric(serie_observada[0].str.slice(14,22), errors = 'coerce')
    serie_observada['Data'] = pd.to_datetime(serie_observada[['Year', 'Month', 'Day']]) + pd.to_timedelta(serie_observada['Hora'], unit = 'h')
    serie_observada = serie_observada.set_index('Data')
    serie_observada = serie_observada.drop([0, 'Year', 'Month', 'Day', 'Hora'], 1)
    serie_observada = serie_observada[serie_observada['q_m3s'] >= 0]
    serie_observada = serie_observada[data_ini : data_fim]

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
                            header = 0, index_col = 0))
            #junta com vazao observada
            gbl["avaliacao_"+modelo+str(horizonte)] = gbl[
                "avaliacao_"+modelo+str(horizonte)].merge(serie_observada[
                    'q_m3s'],how='left',left_index=True,right_index=True)
            #remove linhas sem Valor observado
            gbl["avaliacao_"+modelo+"_"+str(horizonte)] = gbl[
                "avaliacao_"+modelo+"_"+str(horizonte)].dropna()
            #recorta horizonte para periodo analisado
            gbl["avaliacao_"+modelo+"_"+str(horizonte)] = (gbl[
                "avaliacao_"+modelo+"_"+str(horizonte)][data_ini : data_fim])
            #aplica Nash para cada horizonte
            gbl["Nash_"+modelo+"_"+str(horizonte)] = he.nse(
                gbl["avaliacao_"+modelo+"_"+str(horizonte)]["Vazao_prev"],
                gbl["avaliacao_"+modelo+"_"+str(horizonte)]["q_m3s"])
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
    plt.title('Ajuste Nash - Modelo '+bacia, loc = 'left')
    plt.xlabel('Horizonte (h)')
    plt.ylabel('Coeficiente Nash')
    plt.annotate(data_texto, xy=(1,1), xytext=(-4,26), fontsize=10,
                 xycoords='axes fraction', textcoords='offset points',
                 bbox=dict(facecolor='white', alpha=0.8),
                 horizontalalignment='right', verticalalignment='top')
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
    plt.title('Serie ' + nome_bacia, loc = 'left')
    plt.xlabel('Data')
    plt.ylabel('Q [m3s-1]')
    plt.annotate(data_texto, xy=(1,1), xytext=(-4,26), fontsize=10,
                 xycoords='axes fraction', textcoords='offset points',
                 bbox=dict(facecolor='white', alpha=0.8),
                 horizontalalignment='right', verticalalignment='top')
    plt.savefig(bacia+'_observado_'+data_ini.strftime("%Y%m%d")+"_"+
                          data_fim.strftime("%Y%m%d")+'.png', dpi = 300)
    plt.close()

    #finaliza cada bacia e imprime horario de finalizacao
    print("Concluido Bacia ",bacia)
    print(dt.datetime.now())
