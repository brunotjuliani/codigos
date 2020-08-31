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

dir_dados = "/home/bruno/Documentos/Coleta_Dados"
dir_home = "/home/bruno"
dir_previsoes = "/home/bruno/Documentos/Coleta_Dados/Historico_Previsoes"
dir_observado = "/home/bruno/Documentos/Observado"
dir_horizontes = "/home/bruno/Documentos/Historico_Horizontes"



#DEFINICAO DOS MODELOS / ESTACOES A SEREM AVALIADOS

calibracoes = {
                '112':'Rio_Negro','114':'Rio_Negro',
                '116':'Rio_Negro','117':'Rio_Negro',
                '212':'Porto_Amazonas','214':'Porto_Amazonas',
                '216':'Porto_Amazonas','217':'Porto_Amazonas',
                #'312':'Sao_Bento','314':'Sao_Bento',
                #'316':'Sao_Bento','317':'Sao_Bento',
                #'412':'Pontilhao','414':'Pontilhao',
                #'416':'Pontilhao', '417':'Pontilhao',
                #'512':'Santa_Cruz_Timbo','514':'Santa_Cruz_Timbo',
                #'516':'Santa_Cruz_Timbo','517':'Santa_Cruz_Timbo',
                #'612':'Sao_Mateus_Sul','614':'Sao_Mateus_Sul',
                #'616':'Sao_Mateus_Sul','617':'Sao_Mateus_Sul',
                #'712':'Divisa','714':'Divisa',
                #'716':'Divisa','717':'Divisa',
                #'812':'Fluviopolis','814':'Fluviopolis',
                #'816':'Fluviopolis','817':'Fluviopolis',
                #'912':'Uniao_da_Vitoria', '914':'Uniao_da_Vitoria',
                #'916':'Uniao_da_Vitoria', '917':'Uniao_da_Vitoria',
                #'1010':'Madereira_Gavazzoni', '1012':'Madereira_Gavazzoni',
                #'1014':'Madereira_Gavazzoni', '1015':'Madereira_Gavazzoni',
                #'1110':'Jangada', '1112':'Jangada',
                #'1114':'Jangada', '1115':'Jangada',
                #'1310':'Solais_Novo', '1312':'Solais_Novo',
                #'1314':'Solais_Novo', '1315':'Solais_Novo',
                #'1410':'Porto_Santo_Antonio', '1412':'Porto_Santo_Antonio',
                #'1414':'Porto_Santo_Antonio', '1415':'Porto_Santo_Antonio',
                #'1510':'Aguas_do_Vere', '1512':'Aguas_do_Vere',
                #'1514':'Aguas_do_Vere', '1515':'Aguas_do_Vere',
                #'2010':'Porto_Capanema', '2012':'Porto_Capanema',
                #'2110':'Hotel_Cataratas', '2112':'Hotel_Cataratas',
                #'2114':'Hotel_Cataratas', '2115':'Hotel_Cataratas',
                #'1212':'Foz_do_Areia',
                #'1612':'Segredo',
                #'1712':'Foz_do_Chopim',
                #'1812':'Santa_Clara',
                #'1912':'Salto_Caxias',
            }


#LISTA MODELOS SELECIONADOS
for calibracao_cod, estacao_nome in calibracoes.items():
    print(calibracao_cod, estacao_nome)


#DEFINE PERIODO DE AVALIACAO

data_inicio = "2015-09-03" #YYYY-MM-DD
data_fim = "2020-08-30" #YYYY-MM-DD
periodo = pd.date_range(data_inicio, data_fim)
periodo = pd.DataFrame(periodo)
periodo.columns = ["Data"]
periodo["Ano"] = pd.DatetimeIndex(periodo["Data"]).year
periodo["Mes"] = pd.DatetimeIndex(periodo["Data"]).month.map("{:02}".format)
periodo["Dia"] = pd.DatetimeIndex(periodo["Data"]).day.map("{:02}".format)
#print(periodo)


#DEFINICAO HORARIOS DAS RODADAS
hora_rodadas = ['04', '07', '10', '13', '16', '19', '22']


#CONCATENACAO PREVISOES

for calibracao_cod, estacao_nome in calibracoes.items():
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
            os.chdir(dir_observado)
            #importa vazao observada
            vazao_observado = pd.read_csv("vazao_"+estacao_nome+".csv",
                                          index_col = 0).rename(
                                              columns = {'q_m3s':'vazao_obs'})
            #junta observado e previsao
            previsao_7d = previsao_7d.merge(vazao_observado['vazao_obs'],
                                            how='left', left_index=True,
                                            right_index=True)
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

    os.chdir(dir_cod)
    #exporta series historicas para cada horizonte
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
        #le arquivo antigo
        #gbl["Antigo_"+str(calibracao_cod)+"_h_"+str(horizonte)] = pd.read_csv(
        #    "Cod_"+str(calibracao_cod)+'_Horizonte_'+str(horizonte)+".csv",
        #    index_col = "Data")
        #juncao com novas datas
        #gbl["Cod_"+str(calibracao_cod)+'_Horizonte_'+str(horizonte)] =pd.concat(
        #    [gbl["Antigo_"+str(calibracao_cod)+"_h_"+str(horizonte)],
        #     gbl["Cod_" + str(calibracao_cod)+'_Horizonte_'+str(horizonte)]])
        #gbl["Cod_"+str(calibracao_cod)+'_Horizonte_'+str(horizonte)] = gbl[
        #    "Cod_"+str(calibracao_cod)+'_Horizonte_'+str(horizonte)][~gbl[
        #        "Cod_"+str(calibracao_cod)+'_Horizonte_'+
        #        str(horizonte)].index.duplicated(keep='first')]
        #remove linhas sem valor Observado
        gbl["Cod_"+str(calibracao_cod)+'_Horizonte_'+str(horizonte)] = gbl[
            "Cod_"+str(calibracao_cod)+'_Horizonte_'+str(horizonte)].dropna()
        #exporta serie final
        gbl["Cod_"+str(calibracao_cod)+'_Horizonte_'+str(horizonte)].to_csv(
            "Cod_"+str(calibracao_cod)+'_Horizonte_'+str(horizonte)+".csv")

    print("Concluido Bacia ",estacao_nome,", calibracao ", calibracao_cod)
    print(datetime.datetime.now())
