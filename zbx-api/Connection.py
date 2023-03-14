from zabbix_api import ZabbixAPI
import getpass


def LoginZabbix(zabbix_url,user,password):
    def VersaoZabbix():
        try:
            return zapi.api_version()
        except Exception as err:
            print(f'Falha ao conectar na API do zabbix, erro: {err}')
            zapi.logout()
        try:
            zapi = ZabbixAPI(zabbix_url, timeout=1800)
            zapi.login(user,password)
            print(f'Conectado ao Zabbix URL: {zabbix_url}, versão atual: {VersaoZabbix()}')
            return zapi
        except Exception as err:
            print(f'Problema na conexão erro {err}')
            zapi.logout()