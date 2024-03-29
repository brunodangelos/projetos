from zabbix_api import ZabbixAPI
import csv
from Connection import LoginZabbix
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



arquivocsv='servicos.csv'

def BuscarHostCSV(hostname):
    #hostname = input("Insira o nome do host (Caso não coloque nenhum valor buscará todos): ")
    #print("\n")
    with open(arquivocsv,'r', newline='',encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                if (row['host'] in hostname):
                    host_search_params = {
                        'output': ['hostid','name','status'],
                        'filter': {
                            'status': '0'},
                        'search': {
                            'name': '*'+hostname+'*'
                        },
                        "searchWildcardsEnabled": 'true',
                        'sortfield': 'name'
                    }
                        # Make the host search request
                    host_search_result = zapi.host.get(host_search_params)
                    return host_search_result
            except Exception as err:
                print(f'Não foi possivel encontrar host: {err}')

def BuscarItemid(itemname,hostid):
# Initialize a list to store the results
    #itemname = input("Insira o nome item que deseja buscar (Aceita expressão regular): ")
    #print("\n")
    try:
        item_search_params = {
            'output': ['itemid','name'],
            'hostids': hostid,
            'search': {
                'name': itemname
            },
            "searchWildcardsEnabled": 'true',
            "searchByAny": 'true',
            'sortfield': 'name'
        }
        item_search_result = zapi.item.get(item_search_params)
        return item_search_result['0']['itemid']
    except Exception as e:
                print("Erro ao localizar itens: ", e)
                #pass

def BuscarTriggerid(nometrigger, hostid):
    try:
        trigger_search_params = {
            'output': ['triggerid','description'],
            'filter' : {
                    'hostid' : hostid
            },
            'search': {
                'description': '*'+nometrigger+'*'
            },
            'searchWildcardsEnabled': 'true',
            'searchByAny' : 'true'
        }
        trigger_search_result = zapi.trigger.get(trigger_search_params)
        return trigger_search_result[0]['triggerid']
    except Exception as e:
        print("Erro ao localizar trigger :",e)
        zapi.logout()

def AddService():
    # Abra o arquivo CSV e leia os dados
    with open(arquivocsv,'r', newline='',encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        # Use tqdm para exibir uma barra de progresso
        for row in reader:
                #hostname = row['host']
                svcname = row['nome_servico'] 
                # Obtenha os parâmetros do serviço do arquivo CSV
                host = BuscarHostCSV(row['host'])
                svchostname = host[0]['name']
                service_name = "BPBUNGE - APP PIMS - " + svcname + " - " + svchostname
                service_triggerid = BuscarTriggerid(svcname, host[0]['hostid'])
                #service_algorithm_type = row['tipo_algoritmo']
                #service_algorithm_expression = row['expressao_algoritmo']

                # Crie o serviço usando o método service.create
                service_create_params = {
                    'name': service_name,
                    'algorithm': 1,
                    'showsla': 1,
                    'goodsla': 99.00,
                    'sortorder': 1,
                    'triggerid': service_triggerid,
                    #'hostid': service_hostid
                }
                try:
                    service_result = zapi.service.create(service_create_params)

                    # Verifique se o serviço foi criado com sucesso
                    if 'serviceids' in service_result:
                        print(f"O serviço '{service_name}' foi criado com sucesso. ID do serviço: {service_result['serviceids'][0]}")
                    else:
                        print(f"Falha ao criar o serviço '{service_name}'. Erro: {service_result['error']['data']}")
                        zapi.logout()

                except Exception as e:
                    print(f"Ocorreu um erro durante o processo: {e}")
                    zapi.logout()
AddService()

"""trigger = BuscarTriggerid("Servidor: {HOST.NAME} foi reiniciado (uptime menor que {$UPTIME} )", 16631)
print(trigger)"""