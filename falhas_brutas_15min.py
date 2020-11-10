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
    '1999-12-06T17:15:00Z',
    '1999-12-06T17:30:00Z',
    pd.date_range(start="2000-06-05T17:15:00Z",end="2000-06-05T18:30:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    pd.date_range(start="2001-05-03T23:45:00Z",end="2001-05-04T19:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2001-05-09T14:45:00Z',
    pd.date_range(start="2001-05-14T17:30:00Z",end="2001-05-14T18:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2002-10-31T17:45:00Z',
    pd.date_range(start="2003-04-30T17:00:00Z",end="2003-04-30T18:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2003-05-10T01:30:00Z',
    '2003-07-03T08:00:00Z',
    '2003-07-24T03:30:00Z',
    '2003-08-05T04:30:00Z',
    '2003-09-13T22:45:00Z',
    '2003-10-07T14:00:00Z',
    '2004-07-31T10:30:00Z',
    '2004-08-24T19:15:00Z',
    '2004-10-01T14:30:00Z',
    '2005-01-10T10:45:00Z',
    '2005-03-24T06:30:00Z',
    '2005-06-17T18:15:00Z',
    '2005-06-29T14:45:00Z',
    '2005-07-01T14:00:00Z',
    '2005-07-14T06:30:00Z',
    '2005-08-07T22:15:00Z',
    '2005-08-29T17:45:00Z',
    pd.date_range(start="2005-11-28T17:15:00Z",end="2005-11-28T18:45:00Z",
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
