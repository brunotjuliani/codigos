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
from tqdm import tqdm


def ottobacias_montante(coexutorio, achs):
    if not coexutorio in achs['cobacia'].values:
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
    gdf = achs.loc[achs['cobacia'].str.startswith(coexutorio[:(pos+1)])]
    # 3
    total = len(gdf)
    count = 0
    for index, cobacia in tqdm(gdf['cobacia'].items(),
                               total = len(gdf['cobacia'])):
        count += 1
        #print('Processamento {:.2f} %'.format(count/total*100))
        for i in range(pos, len(cobacia)):
            dig_bac = int(cobacia[i])
            dig_ext = int(coexutorio[i])
            if dig_bac != dig_ext:
                if dig_bac < dig_ext:
                    gdf = gdf.drop([index], axis=0)
                break
    return gdf

achs = gpd.read_file('/discolocal/bruno/Shapefiles/REDE_Hidrografica_OTTOCODIFICADA_PR.gdb', layer=0)
# tdrs = gpd.read_file('/Users/arlan/Projetos/hidrografia-pr/REDE_Hidrografica_OTTOCODIFICADA_PR.gdb', layer=1)
lista_ottos = {
#    'B01_Rio_Negro' : '8629755',
#    'B02_Porto_Amazonas' : '86285193',
#    'B03_Sao_Bento' : '86296319',
#    'B04_Pontilhao' : '86278191',
#    'B05_Santa_Cruz_do_Timbo' : '86261713',
#    'B06_Sao_Mateus_do_Sul' : '8628139',
#    'B07_Divisa' : '86293533',
#    'B08_Fluviopolis' : '8627739',
#    'B09_Uniao_da_Vitoria' : '8625971',
#    'B10_Madeireira_Gavazoni' : '86256571',
#    'B10_Madeireira_Gavazoni_2' : '86256573',
#    'B10_Madeireira_Gavazoni_3' : '86256572',
#    'B11_Jangada' : '8625837331',
#    'B12_Foz_do_Areia' : '86255935',
#    'B13_Solais_Novo' : '862543393',
#    'B14_Porto_Santo_Antonio' : '862181913',
#    'B15_Aguas_do_Vere' : '8622173513',
#    'B16_Segredo' : '8625119',
#    'B17_Foz_do_Chopim' : '862211193',
#    'B18_Santa_Clara' : '86243353',
#    'B19_Salto_Caxias' : '862173153',
#    'B20_Porto_Capanema' : '86213193',
#    'B21_Hotel_Cataratas' : '8621115193'
#    'B21_Hotel_CAtaratas_2' : '862111531',
#    'B21_Hotel_CAtaratas_3' : '862111521',
#    'Piraquara_II' : '8628981991',
#    'Irai' : '8628993151',
#    'Passauna' : '862858355',
#    'Reservatorio_Fiu' : '8642354135',
    'apucaraninha_montante' : '8642354393',
}
for noexutorio, coexutorio in lista_ottos.items():
    print("Iniciando Bacia ",noexutorio)
    print(datetime.datetime.now())
    k = str(input('Incluir ottobacia de exutoria para ponto ' + noexutorio +
                  '? (S ou N)'))
    while k not in ('S', 'N'):
        k = str(input('Falha. Incluir ottobacia de exutoria para ponto ' +
                      noexutorio + '? (S ou N)'))
    gdf = ottobacias_montante(coexutorio, achs)
    if k == 'N':
        gdf = gpd.overlay(gdf, gdf.loc[gdf['cobacia'] == coexutorio],
                          how = 'difference')
    gdf.to_file('/discolocal/bruno/Shapefiles/Otto_Sispshi2/Ottos_Completo/ottos_'+noexutorio+'.shp')
    gdf['Dissolve'] = 0
    gdf = gdf.dissolve(by = 'Dissolve')
    gdf.to_file('/discolocal/bruno/Shapefiles/Otto_Sispshi2/Areas_Dissolve/areas_'+noexutorio+'.shp')
    print("Exporta arquivo ", noexutorio)
    print(datetime.datetime.now())
