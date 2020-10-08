### Observacoes
# 1 - para rodar eh preciso ter o geopandas e o fiona; no caso, ativar o geo_env
# 2 - considera a base hidrografica ottocodificada do Parana, disponib. pelo IAT

# para rodar tem que ativar o gen_env
# Dados de entrada
#   coexutorio - codigo da ottobacia contendo a secao exutoria
#   achs - shape contendo as Areas de Contribuicao Hidrograficas (ottobacias)

# Procedimentos..
# 1 - Encontrar a posicao do ultimo digito PAR contido em coexutorio e capturar
# todos os digitos ate essa posicao em "coesquerda"
# 2 - Filtrar o GDF: todos os codigos das ottobacias de montante devem comecar
# com "coesqueda"
# 3 - Antes de mais nada, algumas definicoes
#   coexutorio_dir = parte do codigo do exutorio que eh diferente de coesquerda
#   cobacia_dir    = parte do codigo da ottobacia que eh diferente de coesquerda
# 4 - Encontrar o primeiro digito distinto entre cobacia_dir e
# coexutorio_dir. Obs: iterar ao longo de cobaciar_dir ate encontrar um
# digto diferente, pois nunca vai ter um cobacia_dir com comprimento maior
# do que coexutorio_dir ao longo de uma string com digitos iguais
# Iterar no cobacia_dir que pode ser menor, igual ou maior que o coexutorio
# dar o break antes de ultrapassar o tamanho!
# 1


import pandas as pd
import geopandas as gpd
import datetime


def ottobacias_montante(coexutorio, achs):
    if not coexutorio in achs['nunivotto6'].values:
        print('ERRO: coexutorio nao encontrado no shape de ACHs')
        return 0
    # 1
    pos = 0
    # Avanca a posicao (pos) ate o ultimo digito par da esquerda p/ direita
    for i, dig_str in enumerate(coexutorio):
        dig = int(dig_str)
        if ((dig%2)==0):
            pos = i
    # Avanca os 9s apos o ultimo digito par
    for dig in coexutorio[pos+1:]:
        if int(dig) == 9:
            pos+=1
        else:
            break
    # 2
    gdf = achs.loc[achs['nunivotto6'].str.startswith(coexutorio[:(pos+1)])]
    # 3
    total = len(gdf)
    count = 0
    for index, cobacia in gdf['nunivotto6'].items():
        count += 1
        print('Processamento {:.2f} %'.format(count/total*100))
        for i in range(pos, len(cobacia)):
            dig_bac = int(cobacia[i])
            dig_ext = int(coexutorio[i])
            if dig_bac != dig_ext:
                if dig_bac < dig_ext:
                    gdf = gdf.drop([index], axis=0)
                break
    return gdf

achs = gpd.read_file('/discolocal/bruno/Shapefiles/NIVEL6_A/GEOFT_BHO_REF_ACH_n6_A.shp', layer=0)
# tdrs = gpd.read_file('/Users/arlan/Projetos/hidrografia-pr/REDE_Hidrografica_OTTOCODIFICADA_PR.gdb', layer=1)
lista_ottos = {
    'Ponte_MT_242' : '444833',
    'Ponte_MT_222' : '444911',
    'UHE_Colider' : '444755',
    'UHE_Sinop' : '444779',
    'UHE_Teles_Pires' : '444517',
    'UHE_Sao_Manoel' : '444511',
    'Foz_Sao_Manoel' : '444111'
}

lista_cabeceiras = {
    'Ponte_MT_242' : '444833',
    'Ponte_MT_222' : '444911',
    }

lista_1_montante = {
    'UHE_Colider' : ['UHE_Sinop'],
    'UHE_Teles_Pires' : ['UHE_Colider'],
    'UHE_Sao_Manoel' : ['UHE_Teles_Pires'],
    'Foz_Sao_Manoel' : ['UHE_Sao_Manoel'],
}

lista_2_montantes = {
    'UHE_Sinop' : ['Ponte_MT_242', 'Ponte_MT_222'],
}


for noexutorio, coexutorio in lista_ottos.items():
    print("Iniciando Bacia ",noexutorio)
    print(datetime.datetime.now())
    gdf = ottobacias_montante(coexutorio, achs)
    gdf.to_file('/discolocal/bruno/Teles_Pires/Ottos_Completo/ottos_'+noexutorio+'.shp')
    gdf['Dissolve'] = 0
    gdf = gdf.dissolve(by = 'Dissolve')
    gdf.to_file('/discolocal/bruno/Teles_Pires/Areas_Dissolve/areas_'+noexutorio+'.shp')
    print("Exporta arquivo ", noexutorio)
    print(datetime.datetime.now())

for baciaprincipal, codigo in lista_cabeceiras.items():
    print("Iniciando Divisao Bacia ",baciaprincipal)
    areabaciaprincipal = gpd.read_file(
        '/discolocal/bruno/Teles_Pires/Ottos_Completo/ottos_'+
        baciaprincipal+'.shp' , layer=0)
    areabaciaprincipal.to_file(
        '/discolocal/bruno/Teles_Pires/Areas_Isoladas/Otto/'+
        baciaprincipal+'_otto.shp')
    areabaciaprincipal['Dissolve'] = 0
    areabaciaprincipal = areabaciaprincipal.dissolve(by = 'Dissolve')
    areabaciaprincipal.to_file(
        '/discolocal/bruno/Teles_Pires/Areas_Isoladas/Limite/'+
        baciaprincipal+'_limites.shp')


for baciaprincipal, montantes in lista_1_montante.items():
    print("Iniciando Divisao Bacia ",baciaprincipal)
    baciamontante1 = montantes[0]
    areabaciaprincipal = gpd.read_file(
        '/discolocal/bruno/Teles_Pires/Ottos_Completo/ottos_'+
        baciaprincipal+'.shp' , layer=0)
    areabaciamontante1 = gpd.read_file(
        '/discolocal/bruno/Teles_Pires/Ottos_Completo/ottos_'+
        baciamontante1+'.shp' , layer=0)
    areamontante = areabaciamontante1
    areadiferenca = gpd.overlay(areabaciaprincipal, areamontante,
                                how = 'difference')
    areadiferenca.to_file(
        '/discolocal/bruno/Teles_Pires/Areas_Isoladas/Otto/'+
        baciaprincipal+'_otto.shp')
    areadiferenca['Dissolve'] = 0
    areadiferenca = areadiferenca.dissolve(by = 'Dissolve')
    areadiferenca.to_file(
        '/discolocal/bruno/Teles_Pires/Areas_Isoladas/Limite/'+
        baciaprincipal+'_limites.shp')

for baciaprincipal, montantes in lista_2_montantes.items():
    print("Iniciando Divisao Bacia ",baciaprincipal)
    baciamontante1 = montantes[0]
    baciamontante2 = montantes[1]
    areabaciaprincipal = gpd.read_file(
        '/discolocal/bruno/Teles_Pires/Ottos_Completo/ottos_'+
        baciaprincipal+'.shp' , layer=0)
    areabaciamontante1 = gpd.read_file(
        '/discolocal/bruno/Teles_Pires/Ottos_Completo/ottos_'+
        baciamontante1+'.shp' , layer=0)
    areabaciamontante2 = gpd.read_file(
        '/discolocal/bruno/Teles_Pires/Ottos_Completo/ottos_'+
        baciamontante2+'.shp' , layer=0)
    areamontante = gpd.overlay(areabaciamontante1, areabaciamontante2,
                                how = 'union')
    areadiferenca = gpd.overlay(areabaciaprincipal, areamontante,
                                how = 'difference')
    areadiferenca.to_file(
        '/discolocal/bruno/Teles_Pires/Areas_Isoladas/Otto/'+
        baciaprincipal+'_otto.shp')
    areadiferenca['Dissolve'] = 0
    areadiferenca = areadiferenca.dissolve(by = 'Dissolve')
    areadiferenca.to_file(
        '/discolocal/bruno/Teles_Pires/Areas_Isoladas/Limite/'+
        baciaprincipal+'_limites.shp')
