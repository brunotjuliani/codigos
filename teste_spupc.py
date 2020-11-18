from datetime import date, timedelta


def PeriodoConsulta(arqdata = '/discolocal/bruno/SPAupc/data.txt'):
    """ Retorna em formato da classe 'date' a data lida na segunda linha do arquivo fornecido é função, e a data no
    décimo dia anterior a esta. """
    from datetime import date, timedelta

    f = open(arqdata,'r')
    l = f.readlines()
    f.close()
    dn = date(int(l[1][0:4]), int(l[1][5:7]), int(l[1][8:10]))   #l[1] é a segunda linha
    d0 = dn - timedelta(days = 10)
    print ('\n                                                  Janela de dados: %s a %s\n' % (d0,dn))
    return d0, dn



d0, dref = PeriodoConsulta()
d0 = dref + timedelta(days = 1)    # Estou aproveitando a variável 'd0' para identificar o dia posterior à data de referência, ou seja, hoje!
print(d0)
Bac=1

# Obtendo valor de chuva média observada em d0 (hoje)
arq1   = open(str('/discolocal/bruno/SPAupc/ECVs/ecv%1i.txt' % Bac), 'r')
ctd    = arq1.readlines()
status = False    # Aqui 'status' será True quando for lido a linha do arquivo 'arq1' cuja data é 'd0'
iL     = -1

len(ctd[iL])

while not status:    # Irei ler o arquivo de baixo para cima
    if len(ctd[iL]) < 4:
        iL -= 1
        continue

    lin = ctd[iL].split()
    dt  = date(int(lin[0]), int(lin[1]), int(lin[2]))

    if dt == d0:
        cmb_obs = float(lin[4])
        status  = True

    else:
        iL -= 1

arq1.close()

# Regravando arquivo de previsão de chuva incluindo os dados de hoje
arq2   = open(str('prevcmb_%1i.txt' % Bac), 'r')
ctd    = arq2.readlines()
arq2.close()

arq2   = open(str('prevcmb_%1i.txt' % Bac), 'w')
status = False    # Aqui 'status' será True quando o dado em 'd0' tiver sido gravado no arquivo 'arq2'

for lin in ctd:
    if len(lin) < 4: continue

    dt = date( int(lin[0:4]), int(lin[5:7]), int(lin[8:10]) )

    if dt == d0:
        arq2.write('%s %9.2f\n' % (dt.strftime('%Y %m %d'), cmb_obs))
        status = True

    else:
        arq2.write('%s' % lin)

if not status:
    arq2.write('%s %9.2f\n' % (d0.strftime('%Y %m %d'), cmb_obs))

arq2.close()
