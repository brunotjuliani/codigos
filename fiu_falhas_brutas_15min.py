import json
import pandas as pd
import os

#detalha horario de erros grosseiros
#revisao ate 30/11/2020
#pd.date_range(start="2019-01-11 08:00:00",end="2019-01-15 11:00:00",
#              freq='15min').format(formatter=lambda x: x.strftime(
#                   '%Y-%m-%d %H:%M:%S'))
erros = {
         'Apucaraninha_montante' : [],
                  }

# json.dump(erros, open(
#     '/discolocal/bruno/Observado/Pre_Consistencia/erros_grosseiros_bruto.txt',
#     'w'),indent = 2)
json.dump(erros, open(
    '../dados/fiu/erros_grosseiros_fiu.txt',
    'w'),indent = 2)
