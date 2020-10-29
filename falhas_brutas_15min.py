import json
import pandas as pd
import os

#detalha horario de erros grosseiros
#ultima atualizacao 31/08/2020
#pd.date_range(start="2019-01-11 08:00:00",end="2019-01-15 11:00:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
erros = {'Rio_Negro' : [
    pd.date_range(start="1997-10-24T03:15:00Z",end="1997-10-31T11:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    pd.date_range(start="1998-06-04T23:15:00Z",end="1998-06-05T02:00:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    pd.date_range(start="1998-06-05T13:15:00Z",end="1998-06-05T16:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    pd.date_range(start="1998-06-10T04:00:00Z",end="1998-06-13T09:15:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    pd.date_range(start="1998-09-14T18:30:00Z",end="1998-09-15T18:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '1999-09-03T20:00:00Z',
    pd.date_range(start="1999-10-09T12:15:00Z",end="1999-10-13T17:15:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
                        ],

         'Porto_Amazonas' : [
                             ],

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

json.dump(erros, open('/discolocal/bruno/Observado/Pre_Consistencia/erros_grosseiros_bruto.txt',
                       'w'),indent = 2)
