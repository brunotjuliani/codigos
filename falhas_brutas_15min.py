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
             '2000-01-22 00:15:00',
             '2000-11-18 14:45:00',
             pd.date_range(start="2001-02-18 00:00:00",end="2001-02-19 20:45:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
             pd.date_range(start="2001-02-27 23:45:00",end="2001-03-09 23:45:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
             pd.date_range(start="2001-03-27 11:30:00",end="2001-03-28 11:45:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
             pd.date_range(start="2001-08-09 10:15:00",end="2001-08-09 16:15:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
             '2001-11-05 23:30:00',
             pd.date_range(start="2002-06-12 14:30:00",end="2002-06-12 19:00:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
             '2002-10-29 10:15:00',
             '2004-08-31 06:45:00',
             '2005-04-15 18:45:00',
             '2005-06-22 06:45:00',
             '2005-07-18 03:00:00',
             '2005-07-25 19:45:00',
             '2005-12-04 15:30:00',
             '2009-03-27 17:15:00',
             pd.date_range(start="2010-02-18 15:15:00",end="2010-02-25 14:00:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
             pd.date_range(start="2010-07-15 08:00:00",end="2010-07-15 11:15:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
             pd.date_range(start="2010-09-03 11:45:00",end="2010-09-09 15:45:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
             pd.date_range(start="2012-01-05 15:45:00",end="2012-01-05 23:30:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
             pd.date_range(start="2012-01-11 11:45:00",end="2012-01-11 12:45:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
             '2012-10-23 18:15:00',
             pd.date_range(start="2014-11-01 17:30:00",end="2014-11-04 15:00:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
             '2015-02-18 18:30:00',
             '2016-04-18 14:45:00',
             pd.date_range(start="2017-11-16 23:15:00",end="2017-11-17 00:15:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
             pd.date_range(start="2017-12-27 00:30:00",end="2017-12-27 01:45:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
             '2019-03-22 10:15:00',
             '2019-09-10 14:45:00',
             '2020-05-06 11:15:00',
             '2020-05-06 11:30:00',
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

json.dump(erros, open('erros_grosseiros_15min.txt', 'w'),indent = 2)
