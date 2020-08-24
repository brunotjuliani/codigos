def preenche_falhas(sr_bruta):
    sr_bruta = sr_bruta.asfreq('D')
    sr_tratada = sr_bruta.interpolate(method='spline', order=3)
    return sr_tratada
