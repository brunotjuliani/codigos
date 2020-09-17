""" Verifica se há uma nova previsão do WRF. Se houver cria séries de chuva média prevista nas bacias do SAPH"""
#===============================================================================================================================
from datetime import datetime, timedelta
from pickle import load, dump
from os.path import exists
from os import getcwd, putenv
from sys import path, argv
import numpy
from netCDF4 import Dataset

path.append('/simepar/hidro/PARANA/SAPH/Bibliotecas')
from infoSAPH import selecione
from admin import raiz, dataExec, listaDatas
from chuvaGrade import geraMascaraWRF
#===============================================================================================================================

print("\n%s/%s\n" % (getcwd(), argv[0]))
gui = datetime.now()

# Lista de datas cujos arquivos NetCDF estão com problemas e não devem ser utilizados
naoUsar = [datetime(2017, 4, 16, 12, 0, 0), datetime(2017, 5, 26, 12, 0, 0), datetime(2017, 5, 27, 00, 0, 0),datetime(2017, 7, 19, 12, 0, 0)]



#print(naoUsar)

#-------------------------------------------------------------------------

problemas = ""                    #string onde serão gravados problemas da rodada
lista = selecione("bacias", "id") #lista de todas as bacias do sistema
d0, dref = dataExec(['data_inicio_banco', 'data_referencia'])



# PARTE 1: Verificando se há previsão nova disponível
#===============================================================================================================================
"""
    Dado o horário de referência, em UTC, vou retrocedendo no tempo de 1 em 1 hora até encontrar um arquivo netCDF da previsão
do ensemble do WRF. Quando encontro verifico se há um arquivo com a mesma data no diretório local. Se houve significa que esta
rodada já foi processada. Do contrário é preciso atualizar as séries de chuva prevista nas bacias.

    OBS: Este procedimento não realiza o processamento de previsões anteriores à mais recente. Use o programa
1-atualiza_historico.py para esta tarefa. 
"""
dUTC = dref + timedelta(hours = 3)
num_horas, falha = 0, False

'''#formato original
while True:
    
    if dUTC in naoUsar:
        dUTC -= timedelta(hours = 1)
        num_horas += 1
        
    nome_arq = str("/simepar/modelos/ensemble/%s/ensemble_%s.nc" % (dUTC.strftime("%Y/%m/%d"), dUTC.strftime("%Y-%m-%d_%H")))    
    
    if exists(nome_arq):
        break
    
    dUTC -= timedelta(hours = 1)
    num_horas += 1
    
    if num_horas > 119:
        problemas += str("%s: Não há arquivo de previsão do WRF nas últimas 120 horas!\n" % datetime.now())
        falha = True
        break
'''

#----------------formato novo------------
dwrf = dUTC 
encontrado = False
dwrf_bugs  = [datetime(2016,6,14,12,0,0), datetime(2016,10,10,0,0,0), datetime(2017,4,16,12,0,0),datetime(2017,7,19,12,0,0), datetime(2017,12,5,12,0,0) ]
             #datetime(2017,7,20,0,0,0),datetime(2017,7,20,12,0,0),datetime(2017,7,21,0,0,0),datetime(2017,7,21,12,0,0)] #bugs

#horas adicionais de bugs - para correcao - mas nao funfa :/
#dbug0 = datetime(2017,7,19,13,0,0)
#dbugs = [dbug0 + timedelta(hours = x) for x in range(0,24*1) ]
#dwrf_bugs.append(dbugs)
#print(type(dbugs),type(dwrf_bugs))
#print(dwrf_bugs)
#print("\n",dbugs)
#input()
            
while not encontrado:

    # Montando nome do arquivo NetCDF
    #formato anterior a 20/07/2016
    #nome_arq = str("/simepar/modelos/ensemble/%s/ensemble_%s.nc" % (dwrf.strftime("%Y/%m/%d"), dwrf.strftime("%Y-%m-%d_%H")))
    
    #modificado por Bruno em 17/09/2020
    #nome_arq = str("/simepar/modelos/simepar/wrf/SSE/5km/raw/%s/SSE5km.op05_wrfout_%s.nc" % (dwrf.strftime("%Y/%m/%d/%H"), dwrf.strftime("%Y-%m-%d_%H")))
    

    #formato em 20/07/2017?
    nome_arq = str("/simepar/modelos/simepar/wrf/SSE/9km/raw/%s/SSE9km.op02_wrfout_%s.nc" % (dwrf.strftime("%Y/%m/%d/%H"), dwrf.strftime("%Y-%m-%d_%H"))) 
    
    #formato em 24/06/2018
    #if dref>=datetime(2018,6,25):
    #    nome_arq = str("/simepar/modelos/simepar/wrf/SSE/8km/raw/%s/SSE8km.op02_wrfout_d01_%s.nc" % (dwrf.strftime("%Y/%m/%d/%H"), dwrf.strftime("%Y-%m-%d_%H"))) 
    
    # Alteracao para formato interpolado em 06/12/2017
    #nome_arq = str("/simepar/modelos/simepar/wrf/SSE/9km/raw/%s/SSE9km.op07_wrfout_%s-interpolado.nc" % (dwrf.strftime("%Y/%m/%d/%H"), dwrf.strftime("%Y-%m-%d_%H")))
    #nome_arq = str("/simepar/modelos/simepar/wrf/BR/9km/raw/%s/BR9km.op07_wrfout_%s.nc" % (dwrf.strftime("%Y/%m/%d/%H"), dwrf.strftime("%Y-%m-%d_%H")))  
    
    print('buscando:',nome_arq)
    # Existe o arquivo?
    if exists(nome_arq):
        
        encontrado = True
        print(nome_arq,encontrado,'existe')        
        if dwrf in dwrf_bugs:
            encontrado = False
            dwrf -= timedelta(hours = 1)
            print(nome_arq,encontrado,'bugado')
        else:
            print(nome_arq,encontrado,'ok')
            #tenta abrir 
            try:
                f=Dataset(nome_arq)
            except RuntimeError:
                encontrado = False 
                print(nome_arq,encontrado,'crash-open')            
            
    else:
        dwrf -= timedelta(hours = 1)
        #print(nome_arq,encontrado,'nope')
        if dwrf < dref-timedelta(days = 5):
            break

dUTC = dwrf #usa isso mais abaixo
if not encontrado:
    problemas += str("%s: Não há arquivo de previsão do WRF nas últimas 120 horas!\n" % datetime.now())
    falha = True

#----------fim------formato novo------------


aux = str("Historico/ensemble_media_%s.pickle" % dUTC.strftime("%Y-%m-%d_%H"))

if exists(aux):     
    print(" Rodada das %s já foi processada." % dUTC)
    
elif falha:
    print(" Não há arquivo de previsão do WRF nas últimas 120 horas.")
#===============================================================================================================================



#PARTE 2: Processando dados do arquivo da previsão de chuva
#===============================================================================================================================
else:
    """
    Procedimento do programa.
    1 - Ler contornos simplificados das bacias. São listas de pares (long., lat.)
    2 - Ler matrizes das coordenadas e da previsão de chuva (média dos membros)
    3 - Para cada bacia do SAPH:
        4 - Identificar os pontos da malha do WRF que estão dentro do contorno da bacia para construir a
            máscara a ser aplicada sobre os dados de chuva;
        5 - Calcular a chuva média na bacia para cada hora no horizonte de previsão presente no arquivo do WRF e armazenar
        6 - Sobre-escrever arquivo no diretório local de chuva prevista para a bacia em processamento
    7 - Criar arquivo no diretório de histórico com as séries previstas de todas as bacias.
    """
    bCodes = [bac["id"] for bac in lista]
    NB = len(bCodes)

    # Lendo dados dos contornos
    poligs = {}
    for bacID in bCodes:
        
        aux = load( open(raiz + str("SIG/contorno_simples_%s.pickle" % bacID), "rb") )
        poligs[bacID] = [ numpy.array([xy[0] for xy in aux]), numpy.array([xy[1] for xy in aux]) ]



    # Recuperando dados do arquivo netCDF da previsão mais recente
    print(" Arquivo em processamento:", nome_arq)
    dados = Dataset(nome_arq)

    #Matrizes da latitude e da longitude dos pontos de grade
    WRFlat = dados.variables["XLAT"][0]
    WRFlon = dados.variables["XLONG"][0]

    #Lista de horários em UTC
    horasPrev = dados.variables["Times"][:]
    datas = []
    for i in range(len(horasPrev)):
        x = "".join(v.decode('UTF-8') for v in horasPrev[i])
        dt = datetime(int(x[0:4]), int(x[5:7]), int(x[8:10]), int(x[11:13]), 0, 0)
        datas.append(dt)
    NT = len(datas)

    #timedelta de conversão do horário UTC para horário local
    delta_t = timedelta(hours = -3)

    #Dados de chuva prevista nos pontos de grade ao longo do horizonte de previsão
    #precPrev = dados.variables["PREC_ENS"]
    precPrev1 = dados.variables["RAINC"]
    precPrev2 = dados.variables["RAINNC"]

    #Dicionário onde serão armazenados os dados de CMB acumulada em todas as bacias 
    prevCMB = {}


    for bacID in bCodes:
        
        #Máscara para cálculo de CMB
        """ Como a chuva prevista é dada em uma matriz de pontos, cria-se uma máscara com a mesma dimensão das matrizes de lat/long
        onde pontos fora ou longe do contorno da bacia recebem o valor 0 e pontos dentro ou próximos da bacia recebem o valor 1.
        Assim a operação matricial entre a máscara e a matriz de dados cria uma matriz de mesma dimensão com valores não nulos nos
        pontos onde que devem ser usados no cálculo da CMB.
            Os dados processados são armazenados em dois dicionários. Um que muda a cada bacia e serve para atualizar o arquivo de
        chuva prevista em acumulados horários (a que é utilizada pelos modelos hidrológicos nas previsões). O segundo é um dicio-
        -nario com as séries acumuladas de todas as bacias. Este é armazenado no histórico para usos futuros, tal como refazer as
        previsões ao longo de um determinado período.
            Duas observações importantes:
            (1) As data/horas no arquivo do WRF estão em UTC;
            (2) Os dados de precipitação estão acumulados desde a hora inicial da previsão do WRF.
        """
        
        mask = geraMascaraWRF(WRFlon, WRFlat, poligs[bacID][0], poligs[bacID][1], 0.08) #Aceita pontos até 0.08˚ fora do contorno
        numPts = numpy.sum(mask)
        prevCMB[bacID] = {}
        prevAtual = {}
        prevAcum = {}
        '''# unica variavel de precipitacao
        for i in range(NT):              
            prevCMB[bacID][datas[i]] = numpy.sum(precPrev[i] * mask) / numPts
            
            if i == 0:
                prevAtual[datas[i] + delta_t] = float(prevCMB[bacID][datas[i]])
                
            else:
                prevAtual[datas[i] + delta_t] = float(prevCMB[bacID][datas[i]] - prevCMB[bacID][datas[i-1]])
        '''
        
        # soma de variaveis de precipitacao
        for i in range(NT):              
            aux = precPrev1[i]+precPrev2[i]
            prevCMB[bacID][datas[i]] = numpy.sum(aux * mask) / numPts
            
            prevAcum[datas[i]+delta_t] = float(prevCMB[bacID][datas[i]])
            
            if i == 0:
                prevAtual[datas[i] + delta_t] = float(prevCMB[bacID][datas[i]])
                
            else:
                prevAtual[datas[i] + delta_t] = float(prevCMB[bacID][datas[i]] - prevCMB[bacID][datas[i-1]])        
        
        #Atualizando arquivo de previsão atual
        arq = open("ensemble_media_%s.pickle" % bacID, "wb")
        dump(prevAtual, arq)
        arq.close()
        
        #Salvando chuva acumulada tbm
        #arq = open("acum-ensemble_media_%s.pickle" % bacID, "wb")
        #dump(prevAcum, arq)
        #arq.close()        
        
    #Gerando novo arquivo no histórico com as previsões de todas as bacias
    arq = open("Historico/ensemble_media_%s.pickle" % dUTC.strftime("%Y-%m-%d_%H"), "wb")
    dump(prevCMB, arq)
    arq.close()

    print(" Dados de previsão entre %s e %s." % (datas[0], datas[-1]))
#===============================================================================================================================



#Gravando texto de problemas na rodada, se existir
if problemas != "":
    
    arq = open("log_previsao_chuva.txt", "a")
    arq.write("%s" % problemas)
    arq.close()

print("%s -> Concluido!\n" % datetime.now())
tempo = (datetime.now() - gui).total_seconds()
m = int(tempo) // 60
print(m, " minutos e", int(tempo) - m*60, " segundos")
