import docker
import os
import yaml

def CriaArquivoDockerCompose(zbx_hostname_composefile,zbx_server_composefile):
    diretorio_compose='/opt/globalcare/docker/docker-compose.yml'
    docker_compose = {
                    'version': '4.0',
                    'services': {
                        'zabbix-proxy-v4': {
                            'image': 'zabbix/zabbix-proxy-sqlite3:alpine-5.0',
                            'container_name': 'proxy',
                            'hostname': 'proxy',
                            'ports': ['10051:10051'],
                            'cap_add': ['NET_ADMIN'],
                            'environment': [
                                'ZBX_DEBUGLEVEL=3',
                                'ZBX_TIMEOUT=30',
                                'ZBX_PROXYLOCALBUFFER=1',
                                'ZBX_PROXYOFFLINEBUFFER=2',
                                'ZBX_CONFIGFREQUENCY=600',
                                'ZBX_STARTPOLLERS=15',
                                'ZBX_STARTPOLLERSUNREACHABLE=5',
                                'ZBX_STARTTRAPPERS=15',
                                'ZBX_STARTPINGERS=2',
                                'ZBX_CACHESIZE=16M',
                                'ZBX_HISTORYCACHESIZE=32M',
                                'ZBX_HISTORYINDEXCACHESIZE=8M',
                                'ZBX_STARTVMWARECOLLECTORS=1',
                                'ZBX_VMWAREFREQUENCY=60',
                                'ZBX_VMWAREPERFFREQUENCY=60',
                                'ZBX_VMWARECACHESIZE=8M',
                                'ZBX_VMWARETIMEOUT=10',
                                'TNS_ADMIN=/usr/lib/oracle/12.1/client64/network/admin',
                                'ZBX_ENABLEREMOTECOMMANDS=1',
                                'ZBX_TLSCONNECT=psk',
                                'ZBX_TLSPSKFILE=tls.psk'
                            ],
                            'volumes': [
                                '/opt/globalcare/scripts:/usr/lib/zabbix/externalscripts',
                                '/opt/globalcare/tls.psk:/var/lib/zabbix/enc/tls.psk',
                                '/etc/odbc.ini:/etc/odbc.ini',
                                '/etc/timezone:/etc/timezone:ro',
                                '/etc/localtime:/etc/localtime:ro',
                                '/etc/hosts:/etc/hosts'
                            ],
                            'restart': 'always',
                            'networks': {
                                'zbx-network': {
                                    'ipv4_address': '172.25.0.100'
                                }
                            }
                        }
                    },
                    'networks': {
                        'zbx-network': {
                            'ipam': {
                                'driver': 'default',
                                'config': [
                                    {'subnet': '172.25.0.0/24'}
                                ]
                            }
                            }
                    }
                }
    docker_compose['services']['zabbix-proxy-v4']['environment'].extend([
    f'ZBX_HOSTNAME={zbx_hostname_composefile}',
    f'ZBX_SERVER_HOST={zbx_server_composefile}',
    f'ZBX_TLSPSKIDENTITY={zbx_hostname_composefile}'
])            
    #docker_compose['services']['zabbix-proxy-v4']['environment'][0] = f'ZBX_HOSTNAME={zbx_hostname_composefile}'
    #docker_compose['services']['zabbix-proxy-v4']['environment'][1] = f'ZBX_SERVER_HOST={zbx_server_composefile}'
    #docker_compose['services']['zabbix-proxy-v4']['environment'][20] = f'ZBX_TLSPSKIDENTITY={zbx_hostname_composefile}'
    # Verifica se o arquivo /etc/odbc.ini existe
    if not os.path.exists('/etc/odbc.ini'):
        # Se não existe, cria um arquivo vazio
        open('/etc/odbc.ini', 'w').close()
    if not os.path.exists(str(diretorio_compose)):
        with open(diretorio_compose, mode="wt", encoding="utf-8") as file:
            yaml.dump(docker_compose, file)
            return diretorio_compose
    else:
        dockercreate=input(f'O arquivo já existe no diretorio {diretorio_compose}, deseja continuar? (Responda s ou n): ')
        while dockercreate != "s" and dockercreate != "n":
            dockercreate = input("Você quer continuar? (s/n): ")
            if dockercreate == "s":
                    with open({diretorio_compose}, mode="wt", encoding="utf-8") as file:
                        yaml.dump(docker_compose, file)
                    print("Arquivo sobrescrito")
                    return diretorio_compose
            elif dockercreate == "n":
                print("Saindo")
            else:
                print("Resposta inválida, tente novamente.")