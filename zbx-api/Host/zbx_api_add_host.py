from zabbix_api import ZabbixAPI
import csv 
import time

URL=''
USERNAME='Admin'
PASSWORD='zabbix'

def VersaoZabbix():
    try:
        #print(f'versao atual {zapi.api_version()}')
        return zapi.api_version()
    except Exception as err:
        print(f'Falha ao conectar na API do zabbix, erro: {err}')

try:
    zapi = ZabbixAPI(URL, timeout=15)
    zapi.login(USERNAME,PASSWORD)
    print(f'Conectado a: {URL}, versão atual: {VersaoZabbix()}')
except Exception as err:
    print(f'Problema na conexão erro {err}')

groupids = ['22']
groups = [{"groupid": groupid} for groupid in groupids]

info_interfaces= {
    "1": {"type": "Agent", "id": "1", "port": "10050"},
    "2": {"type":  "SNMP", "id": "2", "port": "161"}
}

def Create_Host(host,ip):
    try:
        create_host = zapi.host.create ({
            "groups" : groups,
            "host": host,
            "interfaces" : {
                "type": info_interfaces['1']['id'],
                "main": 1,
                "useip": 0, # --- 0 - Monitora por DNS e 1 - Monitora por IP
                "ip": "",
                "dns": ip,
                "port": info_interfaces['1']['port'],      
            }
        })
        print(f'Host {host}, cadastrado com sucesso!')
    except Exception as err:
        print(f'Falha ao cadastrar o host: erro {err}')

start_time = time.time()
with open('C:/data/website.csv') as file:
    file_csv = csv.reader(file, delimiter=';')
    for [hostname,ip] in file_csv:
        Create_Host(host=hostname,ip=ip)
end_time=time.time()
total_time = (end_time-start_time)*1000
print(f'Total time = {total_time:.2f} ms')
