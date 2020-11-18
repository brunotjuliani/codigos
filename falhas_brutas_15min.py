import json
import pandas as pd
import os

#detalha horario de erros grosseiros
#revisao ate 31/10/2020
#pd.date_range(start="2019-01-11 08:00:00",end="2019-01-15 11:00:00",freq='15min').format(formatter=lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
erros = {'Rio_Negro' : [
    pd.date_range(start="1997-10-24T03:15:00Z",end="1997-10-31T11:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '1998-01-27T20:00:00Z',
    pd.date_range(start="1998-06-04T23:15:00Z",end="1998-06-05T02:00:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    pd.date_range(start="1998-06-05T13:15:00Z",end="1998-06-05T16:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    pd.date_range(start="1998-06-10T04:00:00Z",end="1998-06-12T18:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '1998-07-03T02:30:00Z',
    '1998-07-03T15:15:00Z',
    pd.date_range(start="1998-09-14T18:30:00Z",end="1998-09-15T18:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '1998-12-31T02:45:00Z',
    pd.date_range(start="1999-06-01T17:00:00Z",end="1999-06-01T18:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '1999-09-03T20:00:00Z',
    pd.date_range(start="1999-10-09T12:15:00Z",end="1999-10-10T18:00:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '1999-10-13T16:15:00Z',
    '1999-10-13T17:15:00Z',
    '1999-12-06T17:15:00Z',
    '1999-12-06T17:30:00Z',
    pd.date_range(start="2000-06-05T17:15:00Z",end="2000-06-05T19:45:00Z",
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
    pd.date_range(start="2003-04-30T17:00:00Z",end="2003-05-07T10:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2003-05-10T01:30:00Z',
    '2003-07-03T08:00:00Z',
    '2003-07-24T03:30:00Z',
    '2003-07-25T01:15:00Z',
    '2003-08-05T04:30:00Z',
    '2003-09-13T22:45:00Z',
    '2003-10-07T14:00:00Z',
    '2004-07-31T10:30:00Z',
    '2004-08-24T19:15:00Z',
    '2004-10-01T14:30:00Z',
    '2005-01-10T10:45:00Z',
    '2005-03-24T06:30:00Z',
    '2005-06-17T18:15:00Z',
    '2005-06-27T13:00:00Z',
    '2005-06-29T14:45:00Z',
    '2005-07-01T14:00:00Z',
    '2005-07-14T06:30:00Z',
    '2005-08-07T22:15:00Z',
    '2005-08-29T17:45:00Z',
    '2005-09-03T11:30:00Z',
    '2005-09-07T03:30:00Z',
    '2005-09-08T22:30:00Z',
    pd.date_range(start="2005-11-11T15:00:00Z",end="2005-11-11T17:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    pd.date_range(start="2005-11-28T17:15:00Z",end="2005-11-28T18:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2006-04-22T21:45:00Z',
    '2006-04-26T04:45:00Z',
    pd.date_range(start="2006-06-23T13:30:00Z",end="2006-06-28T10:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2007-08-10T17:15:00Z',
    '2007-11-28T18:30:00Z',
    '2007-12-15T18:15:00Z',
    '2007-12-27T14:30:00Z',
    '2008-02-22T02:15:00Z',
    '2008-03-31T05:15:00Z',
    '2008-04-16T16:30:00Z',
    '2008-05-21T09:00:00Z',
    '2008-06-07T10:45:00Z',
    '2008-08-27T14:30:00Z',
    '2008-08-30T02:30:00Z',
    '2009-03-18T09:15:00Z',
    '2009-03-28T22:15:00Z',
    '2009-10-02T19:30:00Z',
    '2009-11-06T13:15:00Z',
    '2009-12-04T14:15:00Z',
    '2010-04-08T05:15:00Z',
    '2010-04-29T19:45:00Z',
    pd.date_range(start="2010-04-30T16:45:00Z",end="2010-04-30T17:15:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    pd.date_range(start="2010-05-05T05:30:00Z",end="2010-05-06T16:00:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2011-05-06T14:45:00Z',
    '2012-02-23T15:30:00Z',
    '2012-04-16T12:00:00Z',
    '2012-04-16T12:30:00Z',
    '2012-04-21T12:30:00Z',
    '2012-04-25T03:45:00Z',
    '2012-06-06T15:00:00Z',
    '2012-07-10T21:00:00Z',
    '2013-05-22T14:45:00Z',
    '2013-08-30T15:00:00Z',
    '2013-11-19T18:30:00Z',
    pd.date_range(start="2014-01-16T13:15:00Z",end="2014-01-17T16:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2014-06-11T20:30:00Z',
    pd.date_range(start="2017-05-14T03:15:00Z",end="2017-05-14T04:00:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2017-06-01T15:30:00Z',
    pd.date_range(start="2017-06-02T00:15:00Z",end="2017-06-02T15:15:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2020-09-22T18:30:00Z',
                        ],

         'Porto_Amazonas' : [
    '1997-11-20T19:30:00Z',
    pd.date_range(start="1998-02-13T16:00:00Z",end="1998-02-13T18:30:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    pd.date_range(start="1999-07-14T15:00:00Z",end="1999-07-15T16:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2000-01-22T02:15:00Z',
    pd.date_range(start="2001-03-02T15:45:00Z",end="2001-03-06T18:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2001-07-19T17:30:00Z',
    '2001-08-07T02:15:00Z',
    '2001-08-07T03:45:00Z',
    '2001-08-07T09:30:00Z',
    '2001-08-07T14:00:00Z',
    '2001-08-07T14:15:00Z',
    '2001-08-08T01:15:00Z',
    '2001-08-08T02:45:00Z',
    pd.date_range(start="2001-08-08T12:15:00Z",end="2001-08-08T12:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2001-08-08T14:15:00Z',
    '2001-08-08T17:00:00Z',
    pd.date_range(start="2001-08-09T13:00:00Z",end="2001-08-09T14:00:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2002-02-03T02:30:00Z',
    '2002-02-12T16:45:00Z',
    '2002-02-12T17:00:00Z',
    '2002-03-24T05:00:00Z',
    pd.date_range(start="2002-06-15T16:45:00Z",end="2002-06-15T18:30:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2003-06-11T17:30:00Z',
    pd.date_range(start="2003-09-04T15:15:00Z",end="2003-09-04T18:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2004-05-13T20:45:00Z',
    '2004-08-31T09:45:00Z',
    '2004-11-30T06:45:00Z',
    '2004-11-30T06:45:00Z',
    '2005-04-15T21:45:00Z',
    '2005-06-22T09:45:00Z',
    '2005-07-18T06:00:00Z',
    '2005-07-25T22:45:00Z',
    '2005-12-04T17:30:00Z',
    '2006-01-15T13:45:00Z',
    '2007-08-14T02:30:00Z',
    '2008-09-29T10:15:00Z',
    '2009-03-27T20:15:00Z',
    '2009-04-24T06:15:00Z',
    '2009-10-09T13:45:00Z',
    pd.date_range(start="2010-02-16T21:45:00Z",end="2010-02-25T17:15:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2010-05-13T17:45:00Z',
    '2010-06-26T21:15:00Z',
    '2010-06-27T02:15:00Z',
    '2010-06-29T11:15:00Z',
    '2010-07-02T18:00:00Z',
    '2010-08-02T03:30:00Z',
    '2010-08-05T08:00:00Z',
    '2010-08-16T07:15:00Z',
    pd.date_range(start="2010-09-03T14:30:00Z",end="2010-09-09T18:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2010-09-10T19:15:00Z',
    '2010-09-10T20:15:00Z',
    '2010-09-15T11:15:00Z',
    '2010-09-15T12:15:00Z',
    '2010-09-20T11:30:00Z',
    '2010-09-20T12:30:00Z',
    '2010-09-24T13:00:00Z',
    '2010-09-25T13:15:00Z',
    '2010-09-26T17:15:00Z',
    '2010-10-05T11:45:00Z',
    '2010-10-09T02:45:00Z',
    '2010-10-30T04:15:00Z',
    '2010-11-02T23:15:00Z',
    '2010-11-05T22:00:00Z',
    '2010-11-12T20:30:00Z',
    '2010-11-14T04:30:00Z',
    '2010-11-14T05:30:00Z',
    '2010-11-22T19:45:00Z',
    '2010-11-22T20:00:00Z',
    '2010-11-29T09:15:00Z',
    '2010-12-01T19:15:00Z',
    '2010-12-01T21:15:00Z',
    '2010-12-02T01:15:00Z',
    '2010-12-05T21:30:00Z',
    '2010-12-08T10:00:00Z',
    '2010-12-15T20:30:00Z',
    '2010-12-24T06:15:00Z',
    '2011-01-05T00:15:00Z',
    '2011-01-08T14:30:00Z',
    '2011-01-08T17:30:00Z',
    '2011-01-11T07:45:00Z',
    '2011-01-13T23:15:00Z',
    '2011-01-20T00:30:00Z',
    '2011-01-21T01:30:00Z',
    '2011-01-23T07:15:00Z',
    '2011-02-11T05:00:00Z',
    '2011-02-11T12:00:00Z',
    '2011-02-11T15:00:00Z',
    '2011-02-25T13:15:00Z',
    '2011-03-01T03:15:00Z',
    '2011-03-03T10:15:00Z',
    '2011-03-06T10:15:00Z',
    '2011-03-08T23:30:00Z',
    '2011-03-24T09:00:00Z',
    '2011-03-30T11:30:00Z',
    '2011-04-13T02:30:00Z',
    '2011-04-20T03:30:00Z',
    '2011-04-30T16:00:00Z',
    '2011-06-09T07:00:00Z',
    '2011-06-13T16:00:00Z',
    '2011-06-14T14:00:00Z',
    '2011-06-19T11:15:00Z',
    '2011-06-28T14:30:00Z',
    '2011-06-30T17:30:00Z',
    '2011-07-01T15:30:00Z',
    '2011-07-06T06:30:00Z',
    '2011-07-11T06:45:00Z',
    '2011-07-11T13:45:00Z',
    '2011-07-18T09:00:00Z',
    '2011-07-18T10:00:00Z',
    '2011-07-24T05:30:00Z',
    '2011-07-28T14:15:00Z',
    '2011-07-28T23:15:00Z',
    '2011-08-16T23:15:00Z',
    '2011-08-17T00:15:00Z',
    '2011-08-19T04:00:00Z',
    '2011-08-28T14:15:00Z',
    '2011-08-29T01:15:00Z',
    '2011-09-01T17:30:00Z',
    '2011-09-04T18:30:00Z',
    '2011-09-15T00:30:00Z',
    '2011-09-18T11:45:00Z',
    '2011-09-18T16:45:00Z',
    '2011-09-20T20:00:00Z',
    '2011-09-20T21:00:00Z',
    '2011-10-06T11:15:00Z',
    '2011-10-08T11:30:00Z',
    '2011-10-09T11:30:00Z',
    '2011-10-16T19:00:00Z',
    '2011-10-21T07:30:00Z',
    '2011-10-23T04:15:00Z',
    '2011-11-01T18:00:00Z',
    '2011-11-11T11:15:00Z',
    '2011-11-13T03:15:00Z',
    '2011-11-14T06:15:00Z',
    '2011-11-21T21:30:00Z',
    '2011-12-09T00:15:00Z',
    '2011-12-16T03:00:00Z',
    '2011-12-31T01:30:00Z',
    pd.date_range(start="2012-01-05T17:45:00Z",end="2012-01-06T01:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    pd.date_range(start="2012-01-11T13:45:00Z",end="2012-01-11T14:45:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2012-01-21T01:15:00Z',
    '2012-01-23T07:15:00Z',
    '2012-01-28T21:15:00Z',
    '2012-01-30T15:15:00Z',
    '2012-02-05T07:30:00Z',
    '2012-02-06T10:30:00Z',
    '2012-02-15T10:15:00Z',
    '2012-03-16T08:15:00Z',
    '2012-03-22T10:30:00Z',
    '2012-03-25T20:00:00Z',
    '2012-04-07T18:15:00Z',
    pd.date_range(start="2012-04-08T17:00:00Z",end="2012-04-09T17:30:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2012-10-23T20:15:00Z',
    pd.date_range(start="2014-11-01T19:30:00Z",end="2014-11-04T17:00:00Z",
                  freq='15min').format(formatter=lambda x: x.strftime(
                      '%Y-%m-%dT%H:%M:%SZ')),
    '2015-02-18T20:30:00Z',
    '2015-02-19T02:15:00Z',

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
