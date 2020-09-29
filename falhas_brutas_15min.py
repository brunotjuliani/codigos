import json
import pandas as pd
import os

dir_observado = "/discolocal/bruno/Observado"
os.chdir(dir_observado)

#detalha horario de erros grosseiros a partir de 2000
#ultima atualizacao 31/08/2020
#pd.date_range(start="2019-01-11 08:00:00",end="2019-01-15 11:00:00",freq='H').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
erros = {'Rio_Negro' : [
    pd.date_range(start="2000-05-10 18:45:00",end="2000-06-17 05:45:00",freq='H').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
    pd.date_range(start="2000-08-14 12:00:00",end="2000-08-16 01:15:00",freq='H').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
    pd.date_range(start="2000-11-10 17:15:00",end="2000-11-11 15:30:00",freq='H').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
    pd.date_range(start="2000-12-27 16:30:00",end="2000-12-29 12:45:00",freq='H').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
    pd.date_range(start="2003-04-30 14:15:00",end="2003-05-07 07:45:00",freq='H').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
    pd.date_range(start="2003-10-03 13:30:00",end="2003-10-05 03:15:00",freq='H').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
                        ],

         'Porto_Amazonas' : [

         'Sao_Bento' : [
                        ],

         'Pontilhao' : [
                        ],

         'Santa_Cruz_Timbo' : [
                               ],

         'Sao_Mateus_Sul' : [
                             ],

         'Divisa' : [
                     ],

         'Fluviopolis' : [
                          ],

         'Uniao_da_Vitoria' : [
                               ],

         'Madereira_Gavazzoni' : [],

         'Jangada' : [
                      ],

         'Solais_Novo' : [
                          ],

         'Porto_Santo_Antonio' : [],

         'Aguas_do_Vere' : [
                            ],

         'Porto_Capanema' : [
                             ],

         'Hotel_Cataratas' : [
                              ]

                  }

json.dump(erros, open('erros_grosseiros_15min.txt', 'w'))
