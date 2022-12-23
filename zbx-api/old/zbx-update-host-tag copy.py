from pyzabbix import ZabbixAPI
import pandas
import csv

#with open('D:\/hostbp_.csv') as f:
#    output = [str(s) for line in f.readlines() for s in line[:-1].split(',')]
#f = csv.reader(open('D:\/hostbp_.csv'), delimiter=',',dialect='excel')
#f  = {  'host' : ''  }
zapi = ZabbixAPI("http://localhost")
zapi.login(user="zbx", password="zbx")

def GetHostid():
    excel_data_df = pandas.read_excel('file', sheet_name='Geral',usecols=['HOSTNAME','ENDERECO IP'])
    f= {  'host' : excel_data_df['HOSTNAME'].tolist()  } 
    hosts = zapi.host.get(filter=f, output=['hostids', 'host'] );
    for host in hosts:
        print ("ID: {} - Host: {}".format(host['hostid'], host['host']))
    print (len(hosts))
    #return hosts

GetHostid()