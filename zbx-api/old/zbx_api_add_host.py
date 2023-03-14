from zabbix_api import ZabbixAPI
import csv 
import time

URL='localhost'
USERNAME='zbx'
PASSWORD='zbx'

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

groupids = ['1178']
groups = [{"groupid": groupid} for groupid in groupids]

info_interfaces= {
    "1": {"type": "SNMP", "id": "2", "port": "161"},
    "2": {"type":  "SNMP", "id": "2", "port": "161"}
}

def Create_Host(unidade,host,description,tag_name,tag_value,ip):
    try:
        create_host = zapi.host.create ({
            "groups" : groups,
            "host": host,
            "description": description,
            "inventory_mode": 0,
            "inventory": {
                "contact": "a@a.com",
                "site_city": unidade
            },
            "interfaces" : {
                "type": info_interfaces['1']['id'],
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": info_interfaces['1']['port'],
                "details": {
                    "version": 2,
                    "bulk": 1,
                    "community": "{$SNMP_COMMUNITY}"
                }       
            },
            "tags" : {
                "tag": tag_name,
                "value": tag_value
            }
        })
        print(f'Host {host}, cadastrado com sucesso!')
    except Exception as err:
        print(f'Falha ao cadastrar o host: erro {err}')

start_time = time.time()
with open('file') as file:
    file_csv = csv.reader(file, delimiter=';')
    for [uni,hostname,desc,tagname,tagvalue,ip] in file_csv:
        Create_Host(unidade=uni,host=hostname,description=desc,tag_name=tagname,tag_value=tagvalue,ip=ip)
end_time=time.time()
total_time = (end_time-start_time)*1000
print(f'Total time = {total_time:.2f} ms')
