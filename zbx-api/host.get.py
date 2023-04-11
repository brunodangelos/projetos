import sys
import datetime
from zabbix_api import ZabbixAPI
import csv
from progressbar import ProgressBar, Percentage, ETA, ReverseBar, RotatingMarker, Timer
import threading
import getpass

def VersaoZabbix():
    try:
        return zapi.api_version()
    except Exception as err:
        print(f'Falha ao conectar na API do zabbix, erro: {err}')
        zapi.logout()


zabbix_url = 'https://'+input('Insira a url do zabbix: ') +'/api_jsonrpc.php'     # Set the Zabbix API URL
user = input("Insira o usuário: ") # Set the authentication user
password = getpass.getpass("Insira sua senha: ") # Set the authentication password
try:
    zapi = ZabbixAPI(zabbix_url, timeout=1800)
    zapi.login(user,password)
    print(f'Conectado ao Zabbix URL: {zabbix_url}, versão atual: {VersaoZabbix()}')
except Exception as err:
    print(f'Problema na conexão erro {err}')
    zapi.logout()


def BuscarHost():
    VersaoZabbix()
    hostname = input("Insira o nome do host (Caso não coloque nenhum valor buscará todos): ")
    print("\n")
    host_search_params = {
        'output': ['hostid','name','status','description'],
        'filter': {
            'status': '1'},
        'search': {
            'name': hostname
        },
        "searchWildcardsEnabled": 'true',
        'sortfield': 'name'
    }
    try:
        # Make the host search request
        host_search_result = zapi.host.get(host_search_params)
        print(host_search_result)
        #return host_search_result
    except Exception as err:
        print(f'Não foi possivel encontrar host: {err}')
BuscarHost()