

import pandas as pd
import geopandas as gpd
import datetime

lista_cabeceiras = {
    'B01_Rio_Negro' : '8629755',
#    'B02_Porto_Amazonas' : '86285193',
#    'B03_Sao_Bento' : '86296319',
#    'B04_Pontilhao' : '86278191',
#    'B05_Santa_Cruz_do_Timbo' : '86261713',
#    'B10_Madeireira_Gavazoni' : '86256571',
#    'B11_Jangada' : '8625837331',
#    'B13_Solais_Novo' : '862543393',
#    'B14_Porto_Santo_Antonio' : '862181913',
#    'B15_Aguas_do_Vere' : '8622173513',
#    'B18_Santa_Clara' : '86243353',
    }

lista_1_montante = {
    'B06_Sao_Mateus_do_Sul' : ['B02_Porto_Amazonas'],
    'B17_Foz_do_Chopim' : ['B15_Aguas_do_Vere'],
    'B20_Porto_Capanema' : ['B19_Salto_Caxias'],
    'B21_Hotel_Cataratas' : ['B20_Porto_Capanema'],
}

lista_2_montantes = {
    'B07_Divisa' : ['B01_Rio_Negro', 'B03_Sao_Bento'],
    'B09_Uniao_da_Vitoria' : ['B08_Fluviopolis', 'B05_Santa_Cruz_do_Timbo'],
    'B16_Segredo' : ['B12_Foz_do_Areia', 'B13_Solais_Novo'],
}

lista_3_montantes = {
    'B08_Fluviopolis' : ['B04_Pontilhao', 'B06_Sao_Mateus_do_Sul',
                         'B07_Divisa'],
    'B12_Foz_do_Areia' : ['B09_Uniao_da_Vitoria', 'B10_Madeireira_Gavazoni',
                          'B11_Jangada'],

}

lista_4_montantes = {
        'B19_Salto_Caxias' : ['B16_Segredo', 'B18_Santa_Clara',
                              'B17_Foz_do_Chopim', 'B14_Porto_Santo_Antonio']
}


for baciaprincipal, codigo in lista_cabeceiras.items():
    areabaciaprincipal = gpd.read_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Ottos_Completo/ottos_'+
        baciaprincipal+'.shp' , layer=0)
    areabaciaprincipal.to_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Areas_Isoladas/Otto/'+
        baciaprincipal+'_otto.shp')
    areabaciaprincipal['Dissolve'] = 0
    areabaciaprincipal = areabaciaprincipal.dissolve(by = 'Dissolve')
    areabaciaprincipal.to_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Areas_Isoladas/Limite/'+
        baciaprincipal+'_limites.shp')


'''
for baciaprincipal, montantes in lista_1_montante.items():
    baciamontante1 = montantes[0]
    areabaciaprincipal = gpd.read_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Ottos_Completo/ottos_'+
        baciaprincipal+'.shp' , layer=0)
    areabaciamontante1 = gpd.read_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Ottos_Completo/ottos_'+
        baciamontante1+'.shp' , layer=0)
    areamontante = areabaciamontante1
    areadiferenca = gpd.overlay(areabaciaprincipal, areamontante,
                                how = 'difference')
    areadiferenca.to_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Areas_Isoladas/Otto/'+
        baciaprincipal+'_otto.shp')
    areadiferenca['Dissolve'] = 0
    areadiferenca = areadiferenca.dissolve(by = 'Dissolve')
    areadiferenca.to_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Areas_Isoladas/Limite/'+
        baciaprincipal+'_limites.shp')
'''

'''
for baciaprincipal, montantes in lista_2_montantes.items():
    baciamontante1 = montantes[0]
    baciamontante2 = montantes[1]
    areabaciaprincipal = gpd.read_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Ottos_Completo/ottos_'+
        baciaprincipal+'.shp' , layer=0)
    areabaciamontante1 = gpd.read_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Ottos_Completo/ottos_'+
        baciamontante1+'.shp' , layer=0)
    areabaciamontante2 = gpd.read_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Ottos_Completo/ottos_'+
        baciamontante2+'.shp' , layer=0)
    areamontante = gpd.overlay(areabaciamontante1, areabaciamontante2,
                                how = 'union')
    areadiferenca = gpd.overlay(areabaciaprincipal, areamontante,
                                how = 'difference')
    areadiferenca.to_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Areas_Isoladas/Otto/'+
        baciaprincipal+'_otto.shp')
    areadiferenca['Dissolve'] = 0
    areadiferenca = areadiferenca.dissolve(by = 'Dissolve')
    areadiferenca.to_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Areas_Isoladas/Limite/'+
        baciaprincipal+'_limites.shp')
'''

'''
for baciaprincipal, montantes in lista_3_montantes.items():
    baciamontante1 = montantes[0]
    baciamontante2 = montantes[1]
    baciamontante3 = montantes[2]
    areabaciaprincipal = gpd.read_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Ottos_Completo/ottos_'+
        baciaprincipal+'.shp' , layer=0)
    areabaciamontante1 = gpd.read_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Ottos_Completo/ottos_'+
        baciamontante1+'.shp' , layer=0)
    areabaciamontante2 = gpd.read_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Ottos_Completo/ottos_'+
        baciamontante2+'.shp' , layer=0)
    areabaciamontante3 = gpd.read_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Ottos_Completo/ottos_'+
        baciamontante3+'.shp' , layer=0)
    areamontante = gpd.overlay(areabaciamontante1, areabaciamontante2,
                                how = 'union')
    areamontante = gpd.overlay(areamontante, areabaciamontante3, how = 'union')
    areadiferenca = gpd.overlay(areabaciaprincipal, areamontante,
                                how = 'difference')
    areadiferenca.to_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Areas_Isoladas/Otto/'+
        baciaprincipal+'_otto.shp')
    areadiferenca['Dissolve'] = 0
    areadiferenca = areadiferenca.dissolve(by = 'Dissolve')
    areadiferenca.to_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Areas_Isoladas/Limite/'+
        baciaprincipal+'_limites.shp')
'''
'''
for baciaprincipal, montantes in lista_4_montantes.items():
    baciamontante1 = montantes[0]
    baciamontante2 = montantes[1]
    baciamontante3 = montantes[2]
    baciamontante4 = montantes[3]
    areabaciaprincipal = gpd.read_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Ottos_Completo/ottos_'+
        baciaprincipal+'.shp' , layer=0)
    areabaciamontante1 = gpd.read_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Ottos_Completo/ottos_'+
        baciamontante1+'.shp' , layer=0)
    areabaciamontante2 = gpd.read_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Ottos_Completo/ottos_'+
        baciamontante2+'.shp' , layer=0)
    areabaciamontante3 = gpd.read_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Ottos_Completo/ottos_'+
        baciamontante3+'.shp' , layer=0)
    areabaciamontante4 = gpd.read_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Ottos_Completo/ottos_'+
        baciamontante4+'.shp' , layer=0)
    areamontante1 = gpd.overlay(areabaciamontante1, areabaciamontante2,
                                how = 'union')
    areamontante2 = gpd.overlay(areabaciamontante3, areabaciamontante4,
                                how = 'union')
    areamontante = gpd.overlay(areamontante1, areamontante2, how = 'union')
    areadiferenca = gpd.overlay(areabaciaprincipal, areamontante,
                                how = 'difference')
    areadiferenca.to_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Areas_Isoladas/Otto/'+
        baciaprincipal+'_otto.shp')
    areadiferenca['Dissolve'] = 0
    areadiferenca = areadiferenca.dissolve(by = 'Dissolve')
    areadiferenca.to_file(
        '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Areas_Isoladas/Limite/'+
        baciaprincipal+'_limites.shp')
'''
