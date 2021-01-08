from datetime import datetime, timedelta
import pandas as pd
import sys
sys.path.append('../modelos/')
from plotar_hidro import plotar_hidro
import HydroErr as he


def Fracionamento(datas, Qobs, Qalta, Qmedia, Qbaixa, Qbaixa2, Qmin, Qalta2):

    # Amplitudes
    AQbax = Qbaixa2 - Qmin
    AQmed = Qalta2 - Qbaixa2
    AQalt = Qalta2 + AQbax

    ND = len(datas)    # Quantidade de dados no período de simulação

    # Computando nova série de vazão modelada
    Qmod = {}
    for i in range(ND):
        dt = datas[i]

        # Vazão consistente mais próxima, se a atual não for consistente
        if Qobs[dt] == None:

            # Vazão consistente anterior (sempre está uma hora atrás, pois se ela era None já está preenchida)
            if i == 0:
                Q1 = None
            else:
                j1 = i-1
                Q1 = Qobs[datas[j1]]

            # Vazão consistente posterior (agora sim busca um valor consistente até chegar ao fim da série) ...
            if i == ND-1:    #... a menos que seja o último!
                Q2 = None
            else:
                for j2 in range(i+1,ND):
                    if Qobs[datas[j2]] != None: break
                Q2 = Qobs[datas[j2]]

            # Sem dados!
            if Q1 == None and Q2 == None:
                erro = str('\n     Não há dado de vazão observada em %s, entre %s e %s,' % (nome, datas[0], datas[-1]))
                erro += 'para aplicar método de fracionamento do hidrograma.\n'
                raise ValueError(erro)

            # Reconstituindo ...
            if Q1 == None:
                Qobs[dt] = Q2
            elif Q2 == None:
                Qobs[dt] = Q1
            else:
                Qobs[dt] = (Q2-Q1)*(i-j1)/(j2-j1) + Q1

        # Seguindo com o método do fracionamento
        if Qobs[dt] <= Qbaixa2:    # Faixa de vazões baixas
            peso_media = ( ((Qobs[dt]-Qmin)/AQbax)**2 ) * 0.5
            peso_baixa = 1.0 - peso_media
            peso_alta  = 0.0

        elif Qobs[dt] > Qbaixa2 and Qobs[dt] <= Qalta2:    # Faixa de vazões médias
            peso_alta  = ( ((Qobs[dt]-Qbaixa2)/(AQmed))**2.5 ) * 0.5
            peso_baixa = ( ((Qalta2-Qobs[dt])/(AQmed))**2.5 ) * 0.5
            peso_media = 1.0 - (peso_alta + peso_baixa)

        elif Qobs[dt] > Qalta2 and Qobs[dt] <= AQalt:    # Faixa de vazões média-altas
            peso_media = ( ((AQalt-Qobs[dt])/AQbax)**2 ) * 0.5
            peso_alta  = 1.0 - peso_media
            peso_baixa = 0.0

        else:    # (Qobs > AQalt) Vazões muito altas
            peso_alta, peso_media, peso_baixa = 1.0, 0.0, 0.0

        # Vazão modelada
        Qmod[dt] = peso_alta*Qalta[dt] + peso_media*Qmedia[dt] + peso_baixa*Qbaixa[dt]

    return Qmod


def ExecutaSACSIMPLES(param, datas, evap, cmb, qmont, area, condinic, retorna_estados=False):
    param[10] = int(param[10])    # NRC deve ser um inteiro daqui pra frente

    # Condição inicial do solo da bacia
    Rsolo = [condinic[0], condinic[1]]
    if Rsolo[0] > param[0] or Rsolo[0] < 0:
        erro = '\n     Volume de água na camada superior é inconsistente!'
        erro += str('\n     Condição inicial = %f mm; Máximo comportado = %f mm.\n' % (Rsolo[0], param[0]))
        raise ValueError(erro)
    if Rsolo[1] > param[1] or Rsolo[1] < 0:
        erro = '\n     Volume de água na camada inferior é inconsistente!'
        erro += str('\n     Condição inicial = %f mm; Máximo comportado = %f mm.\n' % (Rsolo[1], param[1]))
        raise ValueError(erro)

    # Condição inicial dos reservatórios de propagação
    Rprop = condinic[2:]
    if len(Rprop) != param[10]:
        erro = '\n     Número de reservatórios na condição inicial é diferente do parâmetro do modelo.'
        erro += str('\n     Valores na C.I. = %i;    NRC = %i.\n' % (len(Rprop), param[10]))
        raise ValueError(erro)
    for i in range(param[10]):
        if Rprop[i] < 0:
            erro = str('\n     Cond. inicial do reservatório %i de propação é nula!\n' % (i+1))
            raise ValueError(erro)

    # Inicializando dicionários de dados simulados
    Qmod, Stados = {}, {}

    # Ciclo temporal da simulação
    for dt in datas:
        Rsolo, VolBac = SAC_Simples(param,Rsolo,evap[dt],cmb[dt])
        VolBac  = VolBac * area * 1000    #Convertendo volume da bacia de mm para m³
        try:
            VolMont = max(qmont[dt] * 3600, 0.0) #Volume proveniente de montante em 1 hora.
        except TypeError:
            print('\n\n    Vazao de montante é None.\n', dt, '\n')
            raise
        Rprop, VolMod = CRCL(param, Rprop, VolBac, VolMont)

        # Estados do modelo ao final do passo de integração
        Stados[dt] = [Rsolo[0], Rsolo[1]].extend(Rprop)    # Não fazer Rsolo.extend(Rprop). Pode vincular Stados a Rsolo.

        # Vazão modelada, m³/s
        Qmod[dt] = VolMod / 3600.0

    # Retornando dados modelados
    if retorna_estados:
        return Qmod, Stados
    else:
        del Stados
        return Qmod

def SAC_Simples(Param,Ssolo,PET,PREC):

    #Calculando a perda por evapotranspiração, na zona superior, no intervalo
    E1 = PET * (Ssolo[0]/Param[0])    #E1  = Evapotranspiração ocorrida na zona superior (mm)

    #Descontando a evapotranspiração da zona superior do solo, porém não pode ser perdida mais água
    #do que há nesta camada.
    if E1 > Ssolo[0]:
        E1 = Ssolo[0]
        Ssolo[0] = 0.0
    else:
        Ssolo[0] = Ssolo[0] - E1
    RED = PET - E1    #RED = Resíduo da evapotranspiração para ser descontada na camada inferior do solo

    #Calculando a perda por evapotranspiração, na zona inferior, no intervalo
    # E2  = Evapotranspiração ocorrida na zona inferior (mm)
    E2 = RED * ((Ssolo[1]/Param[1]) ** Param[7])

    #Descontando a evapotranspiração da zona inferior do solo, porém não pode ser perdida mais água
    #do que há nesta camada.
    if E2 > Ssolo[1]:
        E2 = Ssolo[1]
        Ssolo[1] = 0.0
    else:
        Ssolo[1] = Ssolo[1] - E2

    #Calculando os escoamentos de percolação e superficial.
    # TWX   = Umidade em excesso na zona superior, no intervalo (mm)
    # ROIMP = Escoamento superficial da área impermeável
    try:
        ROIMP = PREC * ((Ssolo[0]/Param[0]) ** Param[5])
        PREC = PREC - ROIMP
    except TypeError:
        print('PREC recebeu valor None!')
        ROIMP, PREC = 0.0, 0.0

    if (PREC + Ssolo[0]) > Param[0]:
        TWX = PREC + Ssolo[0] - Param[0]
        Ssolo[0] = Param[0]
    else:
        TWX = 0.0
        Ssolo[0] = Ssolo[0] + PREC

    #Inicializando acumuladores do intervalo DT
    SBF   = 0.0                #Escoamento de base
    SSUR  = 0.0                #Escoamento superficial
    SIF   = 0.0                #Escoamento interno (subsuperficial)
    SPERC = 0.0                #Percolação

    #Determinando os incrementos computacionais de tempo para o intervalo básico de tempo.
    #Nenhum incremento irá exceder 5.0 milimetros de Ssolo[0]+TWX.
    # NINC = Número de incrementos de tempo em que o intervalo de tempo será dividido para posterior
    #        contabilidade da umidade do solo.
    # DINC = Comprimento de cada incremento em dias
    # PINC = Quantidade de umidade disponível para cada incremento
    NINC = int( round(1.0 + 0.20*(Ssolo[0]+TWX), 0) )
    DINC = (1.0/NINC) / 24.0    # "/ 24" = "* (1/24)". "1/24" é o DT [dias], ou seja, dados horários.
    PINC = TWX/NINC

    #Calculando frações de deplecionamento da água para o tempo de incremento, sendo que as taxas de
    #depleção são para um dia.
    # DUZ  = Depleção de água da zona superior, por incremento
    # DLZ  = Depleção de água da zona inferior, por incremento
    DUZ  = 1.0 - ( (1.0-Param[2])**DINC )
    DLZ  = 1.0 - ( (1.0-Param[3])**DINC )


    # INICIANDO CICLO DE INTEGRAÇÃO PARA CADA INCREMENTO, PARA O INTERVALO DE TEMPO
    for I in range(NINC):

        #Calculando o escoamento de base da zona inferior e o acumulado do intervalo de tempo
        # BF = Escoamento de base
        BF   = Ssolo[1] * DLZ
        SBF  = SBF + BF
        Ssolo[1] = Ssolo[1] - BF

        #Calculando o volume percolado
        # UZRAT = Umidade da camada superior do solo
        # LZRAT = Umidade da camada inferior do solo
        # PERC = Volume percolado no incremento de tempo
        UZRAT = Ssolo[0] / Param[0]
        LZRAT = Ssolo[1] / Param[1]
        PERC  = DLZ * Param[1] * (1.0 + Param[4] * ((1.0-LZRAT)**Param[6])) * UZRAT

        #Verificando se o volume percolado está realmente disponível na camada superior
        if PERC > Ssolo[0]:
            PERC = Ssolo[0]

        #Verificando se a camada inferior comporta o volume percolado
        if (PERC+Ssolo[1]) > Param[1]:
            PERC = Param[1] - Ssolo[1]

        #Transferindo água percolada
        Ssolo[0] = Ssolo[0] - PERC
        Ssolo[1] = Ssolo[1] + PERC
        SPERC = SPERC + PERC

        #Calculando o escoamento interno e o acumulado
        # DEL = Escoamento interno
        #OBS: A quantidade PINC ainda não foi adicionada
        DEL  = Ssolo[0] * DUZ
        SIF  = SIF + DEL
        Ssolo[0] = Ssolo[0] - DEL

        #Distribuir PINC entre a zona superior e o escoamento superficial
        SUR = 0.0
        if PINC > 0.0:
            #Se houver excesso, vira escoamento superficial
            if (PINC+Ssolo[0]) > Param[0]:
                SUR = PINC + Ssolo[0] - Param[0]
                Ssolo[0] = Param[0]
            #Do contrário, adiciona tudo na camada superior
            else:
                Ssolo[0] = Ssolo[0] + PINC
            SSUR = SSUR + SUR

    # FIM DO CICLO DE INTEGRAÇÃO PARA CADA INCREMENTO, PARA O INTERVALO DE TEMPO

    #Descontando volume do escoamento de base que vai para o aquífero
    # BFCC = componente do escoamento de base que vai para o canal
    BFCC = SBF * Param[8]

    #Calculando escoamento afluente da bacia para o canal no intervalo de tempo
    # TCI  = Escoamento afluente total
    # GRND = Escoamento subterrâneo
    # SURF = Escoamento superficial
    TCI = ROIMP + SSUR + SIF + BFCC

    return Ssolo, TCI

# Propagação por Cascata de Reservatórios
def CRCL(Param,Sprop,VOLbac,VOLmont):
    Vprop = [[0.0, 0.0, 0.0] for i in range(Param[10])]

    #Calculando fluxos no início do passo de tempo e adicionando volumes de entrada
    for i in range(Param[10]):
        Vprop[i][0] = Param[9] * Sprop[i]
        Sprop[i] += VOLbac/Param[10]    #Volume produzido pela bacia incremental
    Sprop[0] += VOLmont    #Volume contribuinte de montante

    #Balanço de massa no primeiro reservatório
    Vprop[0][1] = Param[9] * Sprop[0]
    Vprop[0][2] = 0.50 * (Vprop[0][0] + Vprop[0][1])
    Sprop[0]   -= Vprop[0][2]

    #Propagando água entre reservatórios
    for i in range(1,Param[10]):
        Sprop[i]   += Vprop[i-1][2]
        Vprop[i][1] = Param[9] * Sprop[i]
        Vprop[i][2] = 0.50 * (Vprop[i][0] + Vprop[i][1])
        Sprop[i]   -= Vprop[i][2]

    return Sprop, Vprop[Param[10]-1][2]
