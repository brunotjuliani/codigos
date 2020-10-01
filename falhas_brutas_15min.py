import json
import pandas as pd
import os

dir_observado = "/discolocal/bruno/Observado"
os.chdir(dir_observado)

#detalha horario de erros grosseiros a partir de 2000
#ultima atualizacao 31/08/2020
#pd.date_range(start="2019-01-11 08:00:00",end="2019-01-15 11:00:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
erros = {'Rio_Negro' : [
    pd.date_range(start="2000-05-10 18:45:00",end="2000-06-17 05:45:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
    pd.date_range(start="2000-08-14 12:00:00",end="2000-08-16 01:15:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
    pd.date_range(start="2000-11-10 17:15:00",end="2000-11-11 15:30:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
    pd.date_range(start="2000-12-27 16:30:00",end="2000-12-29 12:45:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
    pd.date_range(start="2003-04-30 14:15:00",end="2003-05-07 07:45:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
    pd.date_range(start="2003-10-03 13:30:00",end="2003-10-05 03:15:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
    '2005-03-24 03:30:00',
    pd.date_range(start="2005-11-11 13:00:00",end="2005-11-11 15:45:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
    pd.date_range(start="2006-06-23 10:45:00",end="2006-06-28 07:45:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
    pd.date_range(start="2007-07-30 18:15:00",end="2007-07-31 12:45:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
    '2008-03-31 02:15:00',
    '2008-04-18 19:30:00',
    '2008-08-29 23:30:00',
    '2009-03-18 06:15:00',
    '2009-03-28 19:15:00',
    pd.date_range(start="2010-04-27 22:15:00",end="2010-04-29 17:00:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
    pd.date_range(start="2010-05-05 02:15:00",end="2010-05-06 13:00:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
    '2012-02-23 13:30:00',
    '2012-04-16 09:00:00',
    '2012-04-16 09:30:00',
    '2012-04-16 14:15:00',
    '2012-04-25 00:45:00',
    '2012-06-06 12:00:00',
    '2012-07-10 18:00:00',
    pd.date_range(start="2014-01-14 17:15:00",end="2014-01-16 11:45:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
    pd.date_range(start="2014-06-10 16:45:00",end="2014-06-11 15:45:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
    '2014-09-02 16:00:00',
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

json.dump(erros, open('erros_grosseiros_15min.txt', 'w'))
