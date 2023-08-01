from pyzabbix import ZabbixAPI
import csv 
import time

URL = 'http://localhost/api_jsonrpc.php'
USERNAME = 'Admin'
PASSWORD = 'zabbix'

try:
    zapi = ZabbixAPI(URL, timeout=15)
    zapi.login(USERNAME, PASSWORD)
    print(f'Conectado a: {URL}, versão atual: {zapi.api_version()}')
except Exception as err:
    print(f'Problema na conexão erro {err}')

info_interfaces= {
    "1": {"type": "Agent", "id": "1", "port": "10050"},
    "2": {"type":  "SNMP", "id": "2", "port": "161"}
}

def Get_or_Create_HostGroup(name):
    try:
        existing_groups = zapi.hostgroup.get(filter={'name': name})
        if existing_groups:
            print(f'Hostgroup "{name}" já existe (ID: {existing_groups[0]["groupid"]})')
            return existing_groups[0]["groupid"]
        
        create_group = zapi.hostgroup.create(name=name)
        #print(f'Hostgroup "{name}" criado com sucesso (ID: {create_group["groupids"][0]})')
        return create_group['groupids'][0]
    except Exception as err:
        print(f'Falha ao criar/verificar o hostgroup: erro {err}')
        return None

def Create_Host(host, ip, group_id, location, latitude, longitude, host_type):
    try:
        existing_hosts = zapi.host.get(filter={'host': host})
        if existing_hosts:
            print(f'Host "{host}" já existe (ID: {existing_hosts[0]["hostid"]})')
            return

        interface = {
            "main": 1,
            "useip": 1,  # 1 - Monitora por IP
            "ip": ip,
            "dns": ""
        }
        if host_type == 'zabbix_agent':
            interface["type"] = info_interfaces['1']['id']  # 1 - Agente Zabbix
            interface["port"] = info_interfaces['1']['port']
        elif host_type == 'snmp':
            interface["type"] = info_interfaces['2']['id']  # 2 - SNMP
            interface["port"] = info_interfaces['2']['port']
            interface["details"] = {
                "version": 2,
                "community": "${SNMP_COMMUNITY}"  # Substitua pela macro correta se necessário
            }

        create_host = zapi.host.create({
            "host": host,
            "status": 1,
            "interfaces": [interface],
            "groups": [{"groupid": group_id}],
            "templates": [
                {
                    "templateid": "10207"
                }
            ],
            "inventory": {
                "location": location,
                "location_lat": latitude,
                "location_lon": longitude
            }
        })
        print(f'Host "{host}" cadastrado com sucesso no Hostgroup ID: {group_id}')
    except Exception as err:
        print(f'Falha ao cadastrar o host: erro {err}')

start_time = time.time()
with open('host.csv') as file:
    file_csv = csv.reader(file, delimiter=';')
    next(file_csv)  # Pular a primeira linha (cabeçalho)
    current_group_id = None

    for [hostgroup, hostname, ip, location, latitude, longitude, host_type] in file_csv:
        # Verificar se o hostgroup já foi criado, se não, criar.
        if not current_group_id or hostgroup != current_group_name:
            current_group_id = Get_or_Create_HostGroup(hostgroup)
            current_group_name = hostgroup

        Create_Host(host=hostname, ip=ip, group_id=current_group_id, location=location, latitude=latitude, longitude=longitude, host_type=host_type)

end_time = time.time()
total_time = (end_time - start_time) * 1000
print(f'Total time = {total_time:.2f} ms')
