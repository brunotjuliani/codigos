## PARA DADOS EM NÍVEL DE SUPERFÍCIE
#imports
import pandas as pd
from datetime import datetime, timedelta
from ecmwfapi import ECMWFService
#fazendo um range para se colocar às datas selecionadas
date_range = pd.date_range(start='20210801',end='20210801', freq="D").strftime('%Y%m%d').to_list()
for dates in date_range:
    server = ECMWFService( "mars", url = "https://api.ecmwf.int/v1",
                           key = "66dc9750b0f18814d51fa8658c52d73f", email = "rafael.toshio@simepar.br")
    server.execute(
        {
            "class" :"od",
            "date" : dates, #pode remover esse range e usar dada como 20160101/to/20160102
            "expver" : "1",
            "levtype" : "sfc",
            "number" : "0/1/2/3/4/5/6/7/8/9/10/11/12/13/14",
            "param" : "228.128", #Buscar parâmetro da variável no catálogo
            "grid" : "0.2/0.2", #tamanho da grade
            "step" : "all", #step de horas
            "area" : "-25.0/-54.4/-26.8/-49.0", #lat/lon
            "stream" : "mmsf",
            "time" : "00",#rodada
            "type" : "fc",
            "target" : "data.grib2"
        },
        "../Dados/ECMWF_Grib/teste_ECMWF_anual.grib2")
