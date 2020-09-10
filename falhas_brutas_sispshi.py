import json
import pandas as pd
import os

dir_observado = "/discolocal/bruno/Observado"
os.chdir(dir_observado)

#detalha horario de erros grosseiros a partir de 2015
#ultima atualizacao 31/08/2020

erros = {'Rio_Negro' : ['2017-05-14 00:00:00', '2017-06-01 12:00:00',
                        '2017-06-02 08:00:00', '2017-06-02 11:00:00',
                        '2017-06-02 12:00:00',
                        ],

         'Porto_Amazonas' : ['2017-12-26 23:00:00', '2017-12-27 00:00:00',
                             '2019-03-22 09:00:00', '2019-03-22 10:00:00',
                             '2019-09-09 20:00:00', '2019-09-09 21:00:00',
                             '2019-09-10 14:00:00', '2019-09-10 15:00:00',
                             '2019-09-11 02:00:00', '2019-09-11 09:00:00',
                             '2020-05-06 11:00:00',
                             ],

         'Sao_Bento' : ['2017-06-22 13:00:00', '2017-06-22 14:00:00',
                        pd.date_range(start="2019-01-11 08:00:00",
                                      end="2019-01-15 11:00:00",
                                      freq='H').format(
                                          formatter=lambda x: x.strftime(
                                              '%Y-%m-%d %H:%M:%S')),
                        '2019-03-15 11:00:00','2019-03-18 17:00:00',
                        '2019-03-18 18:00:00', '2019-03-18 19:00:00',
                        pd.date_range(start="2019-03-19 15:00:00",
                                      end="2019-03-19 20:00:00",
                                      freq='H').format(
                                          formatter=lambda x: x.strftime(
                                              '%Y-%m-%d %H:%M:%S')),
                        '2019-05-25 22:00:00', '2019-05-26 14:00:00',
                        '2019-05-26 22:00:00', '2019-05-27 15:00:00',
                        '2019-05-27 16:00:00',
                        pd.date_range(start="2019-06-01 12:00:00",
                                      end="2019-06-01 16:00:00",
                                      freq='H').format(
                                          formatter=lambda x: x.strftime(
                                              '%Y-%m-%d %H:%M:%S')),
                        pd.date_range(start="2019-06-03 15:00:00",
                                      end="2019-06-04 16:00:00",
                                      freq='H').format(
                                          formatter=lambda x: x.strftime(
                                              '%Y-%m-%d %H:%M:%S')),
                        ],

         'Pontilhao' : ['2017-12-13 14:00:00', '2017-12-13 15:00:00',
                        ],

         'Santa_Cruz_Timbo' : ['2019-01-29 14:00:00', '2019-02-26 21:00:00',
                               '2019-03-06 21:00:00',
                               ],

         'Sao_Mateus_Sul' : ['2017-02-08 13:00:00', '2017-09-02 10:00:00',
                             '2017-09-28 21:00:00',
                             ],

         'Divisa' : [pd.date_range(start="2016-11-04 23:00:00",
                                   end="2016-11-07 13:00:00",freq='H').format(
                                       formatter=lambda x: x.strftime(
                                           '%Y-%m-%d %H:%M:%S')),
                    pd.date_range(start="2017-03-24 15:00:00",
                                  end="2017-03-24 18:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    pd.date_range(start="2017-03-25 11:00:00",
                                  end="2017-03-25 18:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    pd.date_range(start="2017-03-26 14:00:00",
                                  end="2017-03-28 14:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    pd.date_range(start="2017-06-04 22:00:00",
                                  end="2017-06-05 15:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    pd.date_range(start="2017-08-13 13:00:00",
                                  end="2017-08-18 16:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    pd.date_range(start="2017-08-20 10:00:00",
                                  end="2017-08-21 08:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    pd.date_range(start="2017-08-30 07:00:00",
                                  end="2017-08-31 13:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    pd.date_range(start="2017-10-09 14:00:00",
                                  end="2017-10-10 13:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    '2018-01-25 08:00:00', '2018-01-25 11:00:00',
                    pd.date_range(start="2018-01-26 11:00:00",
                                  end="2018-01-26 18:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    '2018-01-29 10:00:00','2018-01-29 11:00:00',
                    '2018-01-31 16:00:00', '2018-02-08 12:00:00',
                    '2018-02-08 13:00:00',
                    pd.date_range(start="2018-02-12 01:00:00",
                                  end="2018-02-16 17:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    '2018-02-20 11:00:00', '2018-02-20 12:00:00',
                    '2018-02-20 13:00:00',
                    pd.date_range(start="2018-02-23 15:00:00",
                                  end="2018-02-24 17:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    '2018-02-26 09:00:00', '2018-02-26 10:00:00',
                    pd.date_range(start="2018-02-28 12:00:00",
                                  end="2018-02-28 19:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    pd.date_range(start="2018-03-02 12:00:00",
                                  end="2018-03-02 18:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    pd.date_range(start="2018-03-03 08:00:00",
                                  end="2018-03-05 12:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    pd.date_range(start="2019-05-02 08:00:00",
                                  end="2019-05-02 13:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    pd.date_range(start="2019-05-04 13:00:00",
                                  end="2019-05-04 19:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    pd.date_range(start="2019-05-05 18:00:00",
                                  end="2019-05-06 13:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    pd.date_range(start="2019-05-30 04:00:00",
                                  end="2019-05-31 08:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    '2020-07-20 12:00:00', '2020-07-20 13:00:00',
                    '2020-07-20 14:00:00', '2020-07-22 14:00:00',
                    '2020-07-22 15:00:00', '2020-07-22 21:00:00',
                    '2020-07-22 22:00:00',
                    pd.date_range(start="2020-07-23 13:00:00",
                                  end="2020-08-20 11:00:00",freq='H').format(
                                      formatter=lambda x: x.strftime(
                                          '%Y-%m-%d %H:%M:%S')),
                    ],

         'Fluviopolis' : [pd.date_range(start="2017-09-14 07:00:00",
                                        end="2017-09-22 13:00:00",
                                        freq='H').format(
                                            formatter=lambda x: x.strftime(
                                                '%Y-%m-%d %H:%M:%S')),
                          ],

         'Uniao_da_Vitoria' : ['2016-07-08 21:00:00',
                               pd.date_range(start="2017-05-18 08:00:00",
                                             end="2017-05-19 08:00:00",
                                             freq='H').format(
                                                 formatter=lambda x: x.strftime(
                                                     '%Y-%m-%d %H:%M:%S')),
                               '2017-05-19 17:00:00', '2017-05-19 18:00:00',
                               '2017-05-19 19:00:00', '2017-07-07 10:00:00',
                               '2017-07-07 11:00:00', '2019-09-18 13:00:00',
                               '2019-09-18 14:00:00',
                               ],

         'Madereira_Gavazzoni' : [],

         'Jangada' : ['2020-08-23 08:00:00',
                      ],

         'Solais_Novo' : ['2019-08-30 16:00:00', '2020-02-24 15:00:00',
                          '2020-02-24 16:00:00',
                          ],

         'Porto_Santo_Antonio' : [],

         'Aguas_do_Vere' : ['2016-03-17 06:00:00', '2016-03-17 17:00:00',
                            ],

         'Porto_Capanema' : [pd.date_range(start="2015-05-06 00:00:00",
                                           end="2015-05-07 14:00:00",
                                           freq='H').format(
                                               formatter=lambda x: x.strftime(
                                                   '%Y-%m-%d %H:%M:%S')),
                             ],

         'Hotel_Cataratas' : []

                  }

json.dump(erros, open('erros_grosseiros.txt', 'w'))
