from pyzabbix import ZabbixAPI
import csv
import pandas
from progressbar import ProgressBar, Percentage, ETA, ReverseBar, RotatingMarker, Timer

zapi = ZabbixAPI("localhost")
zapi.login(user="zbx", password="zbx")

def GetHostid():
    excel_data_df = pandas.read_excel('file', sheet_name='Geral',usecols=['HOSTNAME','ENDERECO IP'])
    f= {  'host' : excel_data_df['HOSTNAME'].tolist()  } 
    hosts = zapi.host.get(filter=f, output=['hostids']);
    return hosts


#arq = csv.reader(open('D:\/hostbp.csv'))
#linhas = sum(1 for linha in arq)
#linhas= len(pandas.read_excel('D:\/Host_BP_Criticidade.xlsx', sheet_name='Geral',usecols=['HOSTNAME']))

#f = csv.reader(open('D:\/hostbp.csv'), delimiter=';')
excel_data_df=pandas.read_excel('file', sheet_name='Geral',usecols=['HOSTNAME','SEVERIDADE','PRIORIDADE'])
host_list= {  'host' : GetHostid()  } 
tag_list= { 'tags' : [{'tag' : excel_data_df['SEVERIDADE'].tolist(),'value' : excel_data_df['PRIORIDADE'].tolist()}]}

#bar = ProgressBar(maxval=linhas,widgets=[Percentage(), ReverseBar(), ETA(), RotatingMarker(), Timer()]).start()
#i = 0

#for [f['HOSTNAME'],f['PRIORIDADE NEGÓCIO']] in len(f['HOSTNAME']):
hostcriado = zapi.host.massupdate(
    hosts=host_list,
#    tags=tag_list
    )
  #  i += 1
   # bar.update(i)

#bar.finish