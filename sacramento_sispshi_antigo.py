from datetime import datetime, timedelta
import pandas as pd
import sys
sys.path.append('../modelos/')
from plotar_hidro import plotar_hidro


def Fracionamento(datas, Qobs, Qalta, Qmedia, Qbaixa):

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

codigo = 26064948
nome = 'Rio Negro'
Hmed = 1.84
Hdp = 1.46
Hmax = 13.10
Hmin = 0.15
DH15M = 0.27
DH60M = 0.34
NDAC = 25
Qmed = 76.1
Qdp = 70.9
Qmax = 712.0
Qalta2 = 106.9
Qbaixa2 = 32.2
Qmin = 11.2
DQ15M = 10.0
DQ60M = 15.2


# Ordem obrigatória dos parâmetros:
# param[0] =  UZWM: capacidade máxima de armazenamento da camada superior do solo (mm);
# param[1] =  LZWM: capacidade máxima de armazenamento da camada inferior do solo (mm);
# param[2] =   UZK: taxa de transferência lateral da camada superior do solo (%/dia);
# param[3] =   LZK: taxa de transferência lateral da camada inferior do solo (%/dia);
# param[4] = ZPERC: coeficiente da equação de percolação (adim.);
# param[5] =  IMPX: expoente da equação de escoamento direto proveniente da área impermeável (adim.);
# param[6] =  REXP: expoente da equação de percolação (adim.);
# param[7] =  TRNX: expoente da equação para cálculo da transpiração (adim.)
# param[8] =  SIDE: fração do escoamento subterrâneo que chega ao canal (%);
# param[9] =  beta: fração do volume do reservatório de canal que escoa por passo de tempo (%);
# param[10]=   NRC: número de reservatórios conceituais (inteiro).

PARAM1 = { 1:
             {'MEDIA':
                      { 1: [ 206.540,  189.260, 0.18190, 0.01160, 297.000, 5.99990, 1.00010, 4.22680, 1.00000, 0.03831,  4],
                        2: [ 458.980,  817.550, 0.10000, 0.00280, 794.140, 0.55370, 1.02500, 0.91850, 0.81350, 0.04260, 15],
                        3: [ 423.990,  718.830, 0.10000, 0.00650, 620.500, 5.88330, 1.00070, 1.27730, 0.35840, 0.11435, 15],
                        4: [ 157.210,  204.720, 0.21170, 0.00770, 899.140, 5.99910, 2.67440, 1.04060, 1.00000, 0.02650,  3],
                        5: [ 237.480,  264.290, 0.15020, 0.00460, 893.100, 5.99940, 1.00000, 5.98900, 0.00010, 0.04628,  4],
                        6: [ 348.050,   94.550, 0.10730, 0.03300, 772.090, 1.71650, 4.57060, 0.14750, 0.78960, 0.22610, 15],
                        7: [ 118.740,   39.300, 0.18880, 0.19970, 801.070, 5.81300, 1.00030, 0.91950, 0.11880, 0.21294, 15],
                        8: [ 189.890,  178.510, 0.14480, 0.00790, 899.700, 5.99750, 1.11680, 3.66210, 0.99990, 0.04945,  4],
                        9: [ 100.930,  698.510, 0.26160, 0.00120, 819.900, 2.12060, 4.34020, 0.70760, 1.00000, 0.00730,  1],
                       10: [ 164.040,  197.660, 0.22130, 0.00910, 899.860, 5.98870, 3.06970, 1.07110, 1.00000, 0.03302,  4]
                      }}}

# Tríade de conjuntos de parâmetros para cada classe de vazão
aux = [ PARAM1[1]['MEDIA'][5],
        PARAM1[1]['MEDIA'][6],
        PARAM1[1]['MEDIA'][7]]
parametros = aux[:]

#Leitura das forçantes do modelo
arq = open('../dados/peq/bacia_01.peq')
areainc = float(arq.readline())
df = pd.read_csv('../dados/peq/bacia_01.peq', skiprows=[0],
                 index_col = 'datahora_UTC', parse_dates = True)
df = df.loc['2010':'2020']
df['qmon'] = 0
cmb = df['pme']
etp = df['etp']
qmont = df['qmon']
qobs = df['qjus']
Q0 = qobs[0]

# Lista das variáveis datahora do período de modelagem
t = df.index[0]
tN = df.index[-1]
datas = []
while t <= tN:
    datas.append(t)
    t += timedelta(hours = 1)

# Simulação com parâmetros para vazão alta
estados = [parametros[0][0]*0.5, parametros[0][1]*0.5]
aux = Q0 * 3600 / parametros[0][9]
for i in range(parametros[0][10]):
    estados.append(aux)
Qalta = ExecutaSACSIMPLES(parametros[0], datas, etp, cmb, qmont, areainc,
                          estados)

# Simulação com parâmetros para vazão média
estados = [parametros[1][0]*0.5, parametros[1][1]*0.5]
aux = Q0 * 3600 / parametros[1][9]
for i in range(parametros[1][10]):
    estados.append(aux)
Qmedia = ExecutaSACSIMPLES(parametros[1], datas, etp, cmb, qmont, areainc,
                           estados)


# Simulação com parâmetros para vazão baixa
estados = [parametros[2][0]*0.5, parametros[2][1]*0.5]
aux = Q0 * 3600 / parametros[2][9]
for i in range(parametros[2][10]):
    estados.append(aux)
Qbaixa = ExecutaSACSIMPLES(parametros[2], datas, etp, cmb, qmont, areainc,
                           estados)

# Vazão modelada com ponderação pela classe da vazão
Qmod = Fracionamento(datas, qobs, Qalta, Qmedia, Qbaixa)
Qmod
del Qalta, Qmedia, Qbaixa, estados
df['qsim'] = pd.DataFrame.from_dict(Qmod, orient = 'index')
Qsimulado = df[['qsim']]

# Plotagem
fig = plotar_hidro(idx=df.index, PME=df['pme'], ETP=df['etp'], Qobs=df['qjus'],
                   Qmon=None, Qsims=Qsimulado)
fig.savefig('../dados/peq/bacia_01_antigo.png', dpi = 300,
            bbox_inches = 'tight')
