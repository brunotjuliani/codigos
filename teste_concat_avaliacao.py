#IMPORTANDO BIBLIOTECAS

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import HydroErr as he
import time
#FUNCAO GLOBALS
gbl = globals()

#DEFINICAO DOS ENDEREÇOS

dir_dados = "/discolocal/bruno/Coleta_Dados"
dir_previsoes = "/discolocal/bruno/Coleta_Dados/Historico_Previsoes"
dir_observado = "/discolocal/bruno/Observado"
dir_horizontes = "/discolocal/bruno/Historico_Horizontes"
dir_usinas = "/discolocal/bruno/Coleta_Dados/Dados_Usinas"


#DEFINICAO DOS MODELOS / ESTACOES A SEREM AVALIADOS

calibracoes = {
#                '112':'Rio_Negro','114':'Rio_Negro',
#                '116':'Rio_Negro','117':'Rio_Negro',
#                '212':'Porto_Amazonas','214':'Porto_Amazonas',
#                '216':'Porto_Amazonas','217':'Porto_Amazonas',
#                '312':'Sao_Bento','314':'Sao_Bento',
#                '316':'Sao_Bento','317':'Sao_Bento',
#                '412':'Pontilhao','414':'Pontilhao',
#                '416':'Pontilhao', '417':'Pontilhao',
#                '512':'Santa_Cruz_Timbo','514':'Santa_Cruz_Timbo',
#                '516':'Santa_Cruz_Timbo','517':'Santa_Cruz_Timbo',
#                '612':'Sao_Mateus_Sul','614':'Sao_Mateus_Sul',
#                '616':'Sao_Mateus_Sul','617':'Sao_Mateus_Sul',
#                '712':'Divisa','714':'Divisa',
#                '716':'Divisa','717':'Divisa',
#                '812':'Fluviopolis','814':'Fluviopolis',
#                '816':'Fluviopolis','817':'Fluviopolis',
#                '912':'Uniao_da_Vitoria', '914':'Uniao_da_Vitoria',
#                '916':'Uniao_da_Vitoria', '917':'Uniao_da_Vitoria',
#                '1010':'Madereira_Gavazzoni', '1012':'Madereira_Gavazzoni',
#                '1014':'Madereira_Gavazzoni', '1015':'Madereira_Gavazzoni',
#                '1110':'Jangada', '1112':'Jangada',
#                '1114':'Jangada', '1115':'Jangada',
#                '1310':'Solais_Novo', '1312':'Solais_Novo',
#                '1314':'Solais_Novo', '1315':'Solais_Novo',
#                '1410':'Porto_Santo_Antonio', '1412':'Porto_Santo_Antonio',
#                '1414':'Porto_Santo_Antonio', '1415':'Porto_Santo_Antonio',
#                '1510':'Aguas_do_Vere', '1512':'Aguas_do_Vere',
#                '1514':'Aguas_do_Vere', '1515':'Aguas_do_Vere',
                '2010':'Porto_Capanema', '2012':'Porto_Capanema',
#                '2110':'Hotel_Cataratas', '2112':'Hotel_Cataratas',
#                '2114':'Hotel_Cataratas', '2115':'Hotel_Cataratas',
            }
calibracoes_usinas ={
#                '1210':'GBM', '1212':'GBM', '1214':'GBM', '1215':'GBM',
#                '1218':'GBM', '1219':'GBM',
#                '1610':'SGD', '1612':'SGD', '1614':'SGD', '1615':'SGD',
#                '1710':'FCH', '1712':'FCH', '1714':'FCH', '1715':'FCH',
#                '1810':'SCL', '1812':'SCL',
#                '1910':'SCX', '1910':'SCX',
}


#LISTA MODELOS E ESTACOES SELECIONADOS
for calibracao_cod, estacao_nome in calibracoes.items():
    print(calibracao_cod, estacao_nome)


#DEFINE PERIODO DE AVALIACAO

data_inicio = "2015-09-03" #YYYY-MM-DD
data_fim = "2020-09-09" #YYYY-MM-DD
periodo = pd.date_range(data_inicio, data_fim)
periodo = pd.DataFrame(periodo)
periodo.columns = ["Data"]
periodo["Ano"] = pd.DatetimeIndex(periodo["Data"]).year
periodo["Mes"] = pd.DatetimeIndex(periodo["Data"]).month.map("{:02}".format)
periodo["Dia"] = pd.DatetimeIndex(periodo["Data"]).day.map("{:02}".format)
#print(periodo)


#DEFINICAO HORARIOS DAS RODADAS
hora_rodadas = ['04', '07', '10', '13', '16', '19', '22']


#CONCATENACAO PREVISOES ESTACOES FLUVIOMETRICAS

for calibracao_cod, estacao_nome in calibracoes.items():
    print("Iniciando Bacia ",estacao_nome,", calibracao ", calibracao_cod)
    print(datetime.datetime.now())
    #cria pasta respectivo a calibracao para resultado
    dir_cod = dir_horizontes + "/" + str(calibracao_cod)
    try:
        os.mkdir(dir_cod)
    except OSError as error:
        pass
    for rodada in hora_rodadas:
        #leitura e interpretacao dos diferentes arquivos de previsao
        for i in periodo.index:
            ano = periodo.loc[i,"Ano"]
            mes = periodo.loc[i, "Mes"]
            dia = periodo.loc[i, "Dia"]
            os.chdir(dir_previsoes)
            try:
                try:
                    previsao_7d = pd.read_csv(str(ano)+"/"+str(mes)+"/"+
                                              str(ano)+str(mes)+str(dia)+rodada+
                                              ".txt", header = None)
                except pd.errors.EmptyDataError:
                    #print("Falha em ", periodo.iloc[i]["Data"])
                    continue
            except OSError:
                #print("Falha em ", periodo.iloc[i]["Data"])
                continue
            previsao_7d["Codigo"] = previsao_7d[0].str.slice(0, 4).astype(
                str).astype(int)
            previsao_7d["Year"] = previsao_7d[0].str.slice(5,9)
            previsao_7d["Month"] = previsao_7d[0].str.slice(10,12)
            previsao_7d["Day"] = previsao_7d[0].str.slice(13,15)
            previsao_7d["Hora"] = previsao_7d[0].str.slice(16,18).astype(
                str).astype(int)
            previsao_7d["Precip_prev"] = pd.to_numeric(previsao_7d[0].str.slice(
                19,26), downcast = "float")
            previsao_7d["Vazao_prev"] = pd.to_numeric(previsao_7d[0].str.slice(
                27,35), downcast = "float")
            previsao_7d["Data"] = pd.to_datetime(previsao_7d[[
                "Year", "Month", "Day"]]) + pd.to_timedelta(
                    previsao_7d["Hora"], unit = "h")
            previsao_7d = previsao_7d.drop([
                0, 'Year', 'Month', 'Day', 'Hora'], 1)
            #limita a análise para a calibracao desejada - 168 passos de tempo
            previsao_7d = previsao_7d.loc[(previsao_7d["Codigo"] == int(
                calibracao_cod))].iloc[1:169,].reset_index(drop=True)
            previsao_7d = previsao_7d.set_index('Data')
            #armazena serie para cada horizonte horario
            for horizonte in range(len(previsao_7d)):
                if i == 0:
                    gbl['c'+str(calibracao_cod)+'_horizonte_'+str(horizonte)+
                        '_'+str(rodada)] = previsao_7d.iloc[[horizonte,]]
                else:
                    try:
                        gbl['c'+str(calibracao_cod)+'_horizonte_'+
                            str(horizonte)+'_'+str(rodada)]
                    except KeyError:
                        gbl['c'+str(calibracao_cod)+'_horizonte_'+
                            str(horizonte)+'_'+str(rodada)] = pd.DataFrame()
                    gbl['c'+str(calibracao_cod)+'_linha_'+str(horizonte)+'_'+
                        str(rodada)] = previsao_7d.iloc[[horizonte,]]
                    gbl['c'+str(calibracao_cod)+'_concatenar_'+str(horizonte)+
                        '_'+str(rodada)] = [gbl['c'+str(calibracao_cod)+
                                                '_horizonte_'+str(horizonte)+
                                                '_'+str(rodada)],
                                            gbl['c'+str(calibracao_cod)+
                                                '_linha_'+str(horizonte)+'_'+
                                                str(rodada)]]
                    gbl['c'+str(calibracao_cod)+'_horizonte_'+
                        str(horizonte)+'_'+str(rodada)] = pd.concat(
                            gbl['c'+str(calibracao_cod)+'_concatenar_'+
                                str(horizonte)+'_'+str(rodada)])

    #exporta series historicas para cada horizonte
    os.chdir(dir_cod)
    for horizonte in range(len(previsao_7d)):
        for rodada in hora_rodadas:
            if rodada == hora_rodadas[0]:
                gbl["Cod_"+str(calibracao_cod)+'_Horizonte_'+
                    str(horizonte)] =(gbl['c'+str(calibracao_cod)+'_horizonte_'+
                                          str(horizonte)+'_'+str(rodada)])
            else:
                gbl["Cod_"+str(calibracao_cod)+'_Horizonte_'+str(horizonte)] = (
                    pd.concat([gbl["Cod_" + str(calibracao_cod)+'_Horizonte_'+
                                   str(horizonte)],
                               gbl['c'+str(calibracao_cod)+'_horizonte_'+
                                   str(horizonte)+'_'+str(rodada)]]))
        gbl["Cod_"+str(calibracao_cod)+'_Horizonte_'+str(horizonte)] = (
            gbl["Cod_"+str(calibracao_cod)+'_Horizonte_'+str(horizonte)].loc[(
                gbl["Cod_" + str(calibracao_cod)+'_Horizonte_'+
                    str(horizonte)]['Codigo']==int(calibracao_cod))].sort_index(
                    ).dropna())
        #remove linhas sem Observações
        gbl["Cod_"+str(calibracao_cod)+'_Horizonte_'+str(horizonte)] = gbl[
            "Cod_"+str(calibracao_cod)+'_Horizonte_'+str(horizonte)].dropna()
        #exporta serie final
        os.chdir(dir_cod)
        gbl["Cod_"+str(calibracao_cod)+'_Horizonte_'+str(horizonte)].to_csv(
            "Cod_"+str(calibracao_cod)+'_Horizonte_'+str(horizonte)+".csv")

    print("Concluido Bacia ",estacao_nome,", calibracao ", calibracao_cod)
    print(datetime.datetime.now())




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

#DEFINICAO PERIODO ANALISE
data_ini = dt.datetime(2015, 9, 3,  0,  0) #YYYY, M, D, H, Min
data_fim = dt.datetime(2020, 9, 9,  23,  59)
data_texto = ('Data inicial: ' + str(data_ini.strftime("%Y-%m-%d")) + '\n' +
              'Data final: ' + str(data_fim.strftime("%Y-%m-%d")))

#DEFINICAO MODELOS
calibracoes = {
#                'Rio_Negro' : ['112', '114', '116', '117'],
#                'Porto_Amazonas' : ['212', '214', '216', '217'],
#                'Sao_Bento' : ['312', '314', '316', '317'],
#                'Pontilhao' : ['412', '414', '416', '417'],
#                'Santa_Cruz_Timbo' : ['512', '514', '516', '517'],
#                'Sao_Mateus_Sul' : ['612', '614', '616', '617'],
#                'Divisa' : ['712', '714', '716', '717'],
#                'Fluviopolis' : ['812', '814', '816', '817'],
#                'Uniao_da_Vitoria' : ['912', '914', '916', '917'],
#                'Madereira_Gavazzoni' : ['1010', '1012', '1014', '1015'],
#                'Jangada' : ['1110', '1112', '1114', '1115'],
#                'Solais_Novo' : ['1310', '1312', '1314', '1315'],
#                'Porto_Santo_Antonio' : ['1410', '1412', '1414', '1415'],
#                'Aguas_do_Vere' : ['1510', '1512', '1514', '1515'],
                'Porto_Capanema' : ['2010', '2012'],
#                'Hotel_Cataratas' : ['2110', '2112', '2114', '2115'],
            }

horas_resumo = [1, 6] + list(np.arange(12,169,12))
horizontes = range(168)

#IMPORTA MODELO A ANALIZAR
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
            #junta com vazao observada
            gbl["avaliacao_"+modelo+"_"+str(horizonte)] = gbl[
                "avaliacao_"+modelo+"_"+str(horizonte)].merge(serie_observada[
                    'q_m3s'],how='left', left_index=True, right_index=True)
            #remove linhas sem Valor Observado
            gbl["avaliacao_"+modelo+"_"+str(horizonte)] = gbl[
                "avaliacao_"+modelo+"_"+str(horizonte)].dropna()
            #recorta horizonte para periodo analisado
            gbl["avaliacao_"+modelo+"_"+str(horizonte)] = (
                gbl["avaliacao_"+modelo+"_"+str(horizonte)].loc[
                    gbl["avaliacao_"+modelo+"_"+str(horizonte)]["Data"].between(
                        str(data_ini), str(data_fim))])
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
