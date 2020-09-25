

import pandas as pd
import geopandas as gpd
import datetime

lista_cabeceiras = {
    'B01_Rio_Negro' : '8629755',
    'B02_Porto_Amazonas' : '86285193',
    'B03_Sao_Bento' : '86296319',
    'B04_Pontilhao' : '86278191',
    'B05_Santa_Cruz_do_Timbo' : '86261713',
    'B10_Madeireira_Gavazoni' : '86256571',
    'B11_Jangada' : '8625837331',
    'B13_Solais_Novo' : '862543393',
    'B14_Porto_Santo_Antonio' : '862181913',
    'B15_Aguas_do_Vere' : '8622173513',
    'B18_Santa_Clara' : '86243353',
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

baciaprincipal = 'B06_Sao_Mateus_do_Sul'
baciamontante1 = 'B02_Porto_Amazonas'

areabaciaprincipal = gpd.read_file(
    '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Ottos_Completo/ottos_'+
    baciaprincipal+'.shp' , layer=0)
areabaciamontante1 = gpd.read_file(
    '/discolocal/bruno/Shapefiles/Otto_Sispshi2/Ottos_Completo/ottos_'+
    baciamontante1+'.shp' , layer=0)
areadiferenca = gpd.overlay(areabaciaprincipal, areabaciamontante1, how = 'difference')
areadiferenca.to_file('/discolocal/bruno/Shapefiles/Otto_Sispshi2/Areas_Isoladas/'+baciaprincipal+'.shp')
