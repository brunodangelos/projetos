import sys
import datetime
from zabbix_api import ZabbixAPI
import csv
from progressbar import ProgressBar, Percentage, ETA, ReverseBar, RotatingMarker, Timer
import threading
from Connection import LoginZabbix

LoginZabbix()

def BuscarHost():
    hostname = input("Insira o nome do host (Caso não coloque nenhum valor buscará todos): ")
    print("\n")
    host_search_params = {
        'output': ['hostid','name','status'],
        'filter': {
            'status': '0'},
        'search': {
            'name': hostname
        },
        "searchWildcardsEnabled": 'true',
        'sortfield': 'name'
    }
    try:
        # Make the host search request
        host_search_result = zapi.host.get(host_search_params)
        #print(host_search_result)
        return host_search_result
    except Exception as err:
        print(f'Não foi possivel encontrar host: {err}')

def BuscarItems():
# Initialize a list to store the results
    host_search_result = BuscarHost()
    itemname = input("Insira o nome item que deseja buscar (Aceita expressão regular): ")
    print("\n")
    try:
        results = []
        i=0
        linhas = sum(1 for linha in host_search_result)
        bar = ProgressBar(maxval=linhas,widgets=[Percentage(), ReverseBar(), ETA(), RotatingMarker(), Timer()]).start()
        for host in host_search_result:        
            #Set the item search parameters for the current host
            item_search_params = {
                'output': ['lastvalue','name','state','units'],
                'hostids': host['hostid'],
                'search': {
                    'name': itemname
                },
                "searchWildcardsEnabled": 'true',
                "searchByAny": 'true',
                'sortfield': 'name'
            }
            # Make the item search request for the current host
            item_search_result = zapi.item.get(item_search_params)
            for items in item_search_result:
                # Extract the item value, name, and host name from the search result
                if (items['lastvalue'].isnumeric() == False and items['lastvalue'].replace('.','',1).isdigit() == True) or (items['lastvalue'].isnumeric()):
                    if (items['lastvalue'].isnumeric() == False and items['lastvalue'].replace('.','',1).isdigit() == True):
                        item_value = '{:.2f}'.format(float(items['lastvalue']))
                    else :
                        item_value = items['lastvalue']             
                else:
                    item_value = items['lastvalue']
                item_name = items['name']
                item_state = "Enabled" if items['state']=="0" else "Disabled"
                item_unit = items['units']
                host_name = host['name']
                # Append the result to the results list
                results.append({'item_value': item_value, 'item_name': item_name, 'host_name': host_name, 'item_state': item_state, 'item_unit': item_unit})
            i +=1
            bar.update(i)
    except Exception as e:
                print("Erro ao localizar itens: ", e)
                #pass
    finally:
        bar.finish()
        return results



def CriarArquivoCSV():
    results = BuscarItems()
    try:
        with open('D:\output.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            fieldnames = ['hostname', 'item', 'value','itemunit','itemstate']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
        # Print the results
            for result in results:
                #print(f"Host name: {result['host_name']} - Item name: {result['item_name']} - Item value: {result['item_value']} ")
                writer.writerow({'hostname': result['host_name'],'item' : result['item_name'], 'value' : result['item_value'], 'itemunit' : result['item_unit'] ,'itemstate' : result['item_state'] })
        print ("\nArquivo escrito com sucesso")
    except Exception as e:
        print("Erro ao criar csv: ",e)     


CriarArquivoCSV() 
zapi.logout() 
#BuscarHost()

