from zabbix_api import ZabbixAPI

# Set the Zabbix API URL
zabbix_url = 'http://<zbxurl>/api_jsonrpc.php'

# Set the authentication parameters
user = "<user>"
password = "<pass>"

def VersaoZabbix():
    try:
        #print(f'versao atual {zapi.api_version()}')
        return zapi.api_version()
    except Exception as err:
        print(f'Falha ao conectar na API do zabbix, erro: {err}')
        zapi.logout()
try:
    zapi = ZabbixAPI(zabbix_url, timeout=1800)
    zapi.login(user,password)
    print(f'Conectado ao Zabbix URL: {zabbix_url}, versão atual: {VersaoZabbix()}')
except Exception as err:
    print(f'Problema na conexão erro {err}')
    zapi.logout()