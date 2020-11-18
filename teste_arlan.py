# Arlan Scortegagna - fevereiro/2020
# Instalei o psycopg2 no ambiente "uhepc" atraves do comando: "conda install -n uhepc psycopg2"
# Esse arquivo tem por objetivo gerar os arquivos de previsão de chuva "prevcmb_id.txt"

from datetime import date, timedelta
import pandas as pd
import psycopg2
from psycopg2 import extras

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


d0, hoje = PeriodoConsulta()
dprev0 = hoje + timedelta(days=1)
dprevN = hoje + timedelta(days=14)
dprevN

Bacias = {
          '1' : ['295','Gavião II'],
          '2' : ['296','Riachão do Jacuípe'],
          '3' : ['297','Ponte Rio Branco'],
          '4' : ['298','Ponte Paratigi'],
          '5' : ['299','Itaetê'],
          '6' : ['300','Iaçu'],
          '7' : ['301','Fazenda Santa Fé'],
          '8' : ['302','Ponte Paraguaçu'],
          '9' : ['303','UHE Pedra do Cavalo']
          }

print('===================================================================\n')
print(' !!!!!!!!!!!!!!   INTERVENÇÃO ARLAN (fev/2020)  !!!!!!!!!!!!!!!     ')
print('\n===================================================================')

for id in Bacias.keys():
  id_vmhidro = id
  id_banco = Bacias[id_vmhidro][0]
  print(id_banco)
  nome = Bacias[id_vmhidro][1]
  print('Gerando arquivo de previsão de chuva para bacia {}'.format(nome))
  texto_psql = str('''
                    select daidate, daivalue
                    from daily, customerlocationexp
                    where dailocationid = {} and customid = 6 and daisourceid = 3
                    and dairuntime = '{}'
                    order by dailocationid, daidate
                   '''.format(id_banco, dprev0.isoformat() ))
  conn = psycopg2.connect(dbname='forecastdev', user='reader', password='r&ead3r', host='vmpostgres-master', port='5432')
  consulta = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
  consulta.execute( texto_psql )
  fout = open( '/discolocal/bruno/SPAupc/prevcmb_{}.txt'.format(id_vmhidro) , 'w')
  datas_sql = []
  for row in consulta.fetchall():
    nova_data = row[0]
    novo_valor = row[1]['precIntensity']
    if (nova_data in datas_sql) or (nova_data > dprevN):
      continue
    else:
      print(nova_data)
      datas_sql.append(nova_data)
      fout.write('%4i %2.2i %2.2i  %8.2f\n' % (nova_data.year, nova_data.month, nova_data.day, novo_valor))
  fout.close()

print('===================================================================\n')
print(' !!!!!!!!!!!!!!!!!!!!   FIM DA INTERVENÇÃO   !!!!!!!!!!!!!!!!!!!!     ')
print('\n===================================================================')

print('===================================================================\n')
print(' !!!!!!!!!!!!!!   ALTERAÇÃO BRUNO (nov/2020)  !!!!!!!!!!!!!!!     ')
print('\n===================================================================')
dates = pd.date_range(dprev0,dprevN)
CMB_prev = []
CMB_datas = []
#Solicita entrada de previsoes para 14 dias
for data in range(len(dates)):
    data_prev = dates[data]
    chuva_prev = None
    while chuva_prev is None:
        try:
            chuva_prev = float(
                input("Entre com a Chuva Média na Bacia (mm/d) para o dia " +
                      str(data_prev.date()) + ":" +" [Exemplo: 5.7]"))
        except ValueError:
            print("Valor não reconhecido.")
    CMB_prev.append(chuva_prev)
previsao_cmb = {'Data':dates, 'CMB_prev':CMB_prev}
df_previsao = pd.DataFrame(previsao_cmb)
df_previsao['Data']
df_previsao = df_previsao.set_index('Data')

for id in Bacias.keys():
    id_vmhidro = id
    id_banco = Bacias[id_vmhidro][0]
    nome = Bacias[id_vmhidro][1]

    #Le previsao do banco de dados
    previsao_banco = pd.read_csv('/discolocal/bruno/SPAupc/prevcmb_{}.txt'.format(id_vmhidro), header = None)
    pd.read_csv('/simepar/hidro/SPAupc/Operacao/14d_Prev_CMB/prevcmb_{}.txt'.format(id_vmhidro), header = None, delim_whitespace = True)
    previsao_banco['year'] = previsao_banco[0].str.slice(0,4)
    previsao_banco['month'] = previsao_banco[0].str.slice(5,7)
    previsao_banco['day'] = previsao_banco[0].str.slice(8,10)
    previsao_banco['CMB_prev'] = pd.to_numeric(previsao_banco[0].str.slice(11,21),
                                              downcast = "float", errors = 'coerce')
    previsao_banco["Data"] = pd.to_datetime(previsao_banco[["year", "month", "day"]])
    previsao_banco = previsao_banco.set_index('Data')
    previsao_banco = previsao_banco.drop([0, 'year', 'month', 'day'], 1)

    #Atualiza previsao 14 dias com previsao mais recente do banco
    previsao_concat = df_previsao
    previsao_concat.update(previsao_banco['CMB_prev'])
    exporta = open( '/discolocal/bruno/SPAupc/prevcmb_{}.txt'.format(id_vmhidro) , 'w')
    exporta.close()
    exporta2 = open( '/discolocal/bruno/SPAupc/prevcmb_{}.txt'.format(id_vmhidro) , 'a')
    for i in range(len(previsao_concat)):
        exporta2.write('%4i %2.2i %2.2i  %8.2f\n' %
                      (previsao_concat.index.year[i],previsao_concat.index.month[i],
                       previsao_concat.index.day[i], previsao_concat['CMB_prev'][i]))
    exporta2.close()
    print('\nBacia {} atualizada!'.format(nome))
print('===================================================================\n')
print(' !!!!!!!!!!!!!!   FIM ALTERACAO BRUNO (nov/2020)  !!!!!!!!!!!!!!!     ')
print('\n===================================================================')


for id in Bacias.keys():
  id_vmhidro = id
  id_banco = Bacias[id_vmhidro][0]
  print('\n' + id_banco)
  nome = Bacias[id_vmhidro][1]
  print('Gerando arquivo de previsão de chuva para bacia {}'.format(nome))
  texto_psql = str('''
                    select daidate, daivalue
                    from daily, customerlocationexp
                    where dailocationid = {} and customid = 6 and daisourceid = 3
                    and dairuntime = '{}'
                    order by dailocationid, daidate
                   '''.format(id_banco, dprev0.isoformat() ))
  conn = psycopg2.connect(dbname='forecastdev', user='reader', password='r&ead3r', host='vmpostgres-master', port='5432')
  consulta = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
  consulta.execute( texto_psql )
  fout = open( '/simepar/hidro/SPAupc/Operacao/14d_Prev_CMB/prevcmb_{}.txt'.format(id_vmhidro) , 'w')
  datas_sql = []
  for row in consulta.fetchall():
    nova_data = row[0]
    novo_valor = row[1]['precIntensity']
    if (nova_data in datas_sql) or (nova_data > dprevN):
      continue
    else:
      print(nova_data)
      datas_sql.append(nova_data)
      fout.write('%4i %2.2i %2.2i  %8.2f\n' % (nova_data.year, nova_data.month, nova_data.day, novo_valor))
print('\nPRONTO!')
print('AGORA É REZAR PRA NÃO DAR CONFLITO...\n')
print('===================================================================\n')
print(' !!!!!!!!!!!!!!!!!!!!   FIM DA INTERVENÇÃO   !!!!!!!!!!!!!!!!!!!!     ')
print('\n===================================================================')
