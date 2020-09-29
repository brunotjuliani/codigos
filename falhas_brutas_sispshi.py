import json
import pandas as pd
import os

dir_observado = "/discolocal/bruno/Observado"
os.chdir(dir_observado)

#detalha horario de erros grosseiros a partir de 2015
#ultima atualizacao 31/08/2020
#pd.date_range(start="2019-01-11 08:00:00",end="2019-01-15 11:00:00",freq='H').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
erros = {'Rio_Negro' : [pd.date_range(start="2000-05-09 08:00:00",
                                      end="2000-06-17 22:00:00",
                                      freq='H').format(
                                          formatter=lambda x: x.strftime(
                                              '%Y-%m-%d %H:%M:%S')),
                        pd.date_range(start="2000-08-14 13:00:00",end="2000-08-16 01:00:00",freq='H').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
                        pd.date_range(start="2000-11-10 18:00:00",end="2000-11-11 14:00:00",freq='H').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
                        pd.date_range(start="2000-12-27 17:00:00",end="2000-12-29 12:00:00",freq='H').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
                        pd.date_range(start="2001-05-03 19:00:00",end="2001-05-04 15:00:00",freq='H').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S')),
                        '2001-05-14 15:00:00', '2001-05-14 16:00:00', '2002-04-01 17:00:00', '2002-04-01 18:00:00'


                        ],

         'Porto_Amazonas' : ['2017-11-17 00:00:00', '2017-11-17 01:00:00',
                             '2017-12-27 01:00:00', '2017-12-27 02:00:00',
                             '2019-03-22 10:00:00', '2019-09-09 21:00:00',
                             '2019-09-10 15:00:00', '2020-05-06 12:00:00',
                             ],

         'Sao_Bento' : ['2017-06-22 14:00:00', '2017-06-22 15:00:00',
                        pd.date_range(start="2019-01-11 10:00:00",
                                      end="2019-01-15 13:00:00",
                                      freq='H').format(
                                          formatter=lambda x: x.strftime(
                                              '%Y-%m-%d %H:%M:%S')),
                        '2019-03-15 12:00:00', '2019-03-18 18:00:00',
                        '2019-03-18 19:00:00', '2019-03-18 20:00:00',
                        pd.date_range(start="2019-03-19 16:00:00",
                                      end="2019-03-19 21:00:00",
                                      freq='H').format(
                                          formatter=lambda x: x.strftime(
                                              '%Y-%m-%d %H:%M:%S')),
                        '2019-06-01 14:00:00' , '2019-06-01 15:00:00',
                        '2019-06-01 16:00:00'
                        ],

         'Pontilhao' : [
                        ],

         'Santa_Cruz_Timbo' : [
                               ],

         'Sao_Mateus_Sul' : ['2020-02-11 12:00:00',
                             ],

         'Divisa' : ['2016-11-05 01:00:00',
                     pd.date_range(start="2017-03-25 12:00:00",
                                   end="2017-03-25 19:00:00",freq='H').format(
                                       formatter=lambda x: x.strftime(
                                           '%Y-%m-%d %H:%M:%S')),
                    '2017-03-26 15:00:00', '2017-06-04 23:00:00',
                    '2017-06-05 03:00:00',
                    pd.date_range(start="2017-08-13 14:00:00",
                                  end="2017-08-18 17:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    '2018-01-25 13:00:00',
                     pd.date_range(start="2018-01-26 13:00:00",
                                   end="2018-01-26 20:00:00",freq='H').format(
                                       formatter=lambda x: x.strftime(
                                           '%Y-%m-%d %H:%M:%S')),
                    '2018-01-31 18:00:00',
                    pd.date_range(start="2018-02-12 13:00:00",
                                  end="2018-02-16 19:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    '2018-02-20 13:00:00', '2018-02-20 14:00:00',
                    pd.date_range(start="2018-03-03 09:00:00",
                                  end="2018-03-04 15:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    pd.date_range(start="2019-04-28 16:00:00",
                                  end="2019-04-30 10:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    pd.date_range(start="2019-05-02 09:00:00",
                                  end="2019-05-02 13:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    pd.date_range(start="2019-05-04 12:00:00",
                                  end="2019-05-04 20:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    pd.date_range(start="2019-05-05 18:00:00",
                                  end="2019-05-06 14:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    '2019-05-30 05:00:00',
                    pd.date_range(start="2019-05-30 20:00:00",
                                  end="2019-05-31 13:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    '2020-07-13 12:00:00', '2020-07-20 14:00:00',
                    '2020-07-20 15:00:00', '2020-07-22 15:00:00'
                     ],

         'Fluviopolis' : ['2018-03-07 13:00:00',
                          ],

         'Uniao_da_Vitoria' : [
                               ],

         'Madereira_Gavazzoni' : [],

         'Jangada' : [
                      ],

         'Solais_Novo' : ['2019-08-30 17:00:00', '2020-02-24 16:00:00',
                        '2020-02-24 17:00:00',
                          ],

         'Porto_Santo_Antonio' : [],

         'Aguas_do_Vere' : [
                            ],

         'Porto_Capanema' : [pd.date_range(start="2015-05-06 01:00:00",
                                           end="2015-05-07 18:00:00",
                                           freq='H').format(
                                               formatter=lambda x: x.strftime(
                                                   '%Y-%m-%d %H:%M:%S')),

                             ],

         'Hotel_Cataratas' : ['2020-04-28 02:00:00',
                              pd.date_range(start="2020-04-28 20:00:00",
                                            end="2020-04-29 17:00:00",freq='H').format(
                                                formatter=lambda x: x.strftime(
                                                    '%Y-%m-%d %H:%M:%S')),
                              ]

                  }

json.dump(erros, open('erros_grosseiros.txt', 'w'))
