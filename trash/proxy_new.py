import docker
import os
import yaml
from pyzabbix import ZabbixAPI
import getpass
import secrets

def CriaPSK():
    psk_file = 'tls.psk'
    #Cria arquivo psk
    if not (os.path.exists(str(psk_file))):
        # Cria o arquivo de chave PSK
        psk = secrets.token_hex(32)+'\n'
        with open('/opt/globalcare/'+str(psk_file), 'wb') as f:
            f.write(psk.encode('utf-8'))
    else:
        psk = open('/opt/globalcare/'+str(psk_file), 'r') 
    return psk

def VerificaContainer():
    # Conexão com o daemon do Docker
    client = docker.from_env()
    # Verifica se o container existe
    try:
        container = client.containers.get(container_name)
    except docker.errors.NotFound:
        container = None
    finally:
        return container

def CriaArquivoDockerCompose(zbx_hostname_composefile,zbx_server_composefile):
    docker_compose = {
                    'version': '4.0',
                    'services': {
                        'zabbix-proxy-v4': {
                            'image': 'dockerglobalcare/globalcare:5.3',
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
    # Adicionar o hostname e o servidor na lista de ambiente
    docker_compose['services']['zabbix-proxy-v4']['environment'].extend([
    f'ZBX_HOSTNAME={zbx_hostname_composefile}',
    f'ZBX_SERVER_HOST={zbx_server_composefile}',
    f'ZBX_TLSPSKIDENTITY={zbx_hostname_composefile}'
    ])            
    # Verifica se o arquivo /etc/odbc.ini existe
    if not os.path.exists('/etc/odbc.ini'):
        # Se não existe, cria um arquivo vazio
        open('/etc/odbc.ini', 'w').close()
    return docker_compose

def CadastraProxy():
    def VersaoZabbix():
        try:
            return zapi.api_version()
        except Exception as err:
            print(f'Falha ao conectar na API do zabbix, erro: {err}')
            zapi.logout()
    user = input("Insira o usuário zabbix: ") # Set the authentication user
    password = getpass.getpass("Insira sua senha zabbix: ") # Set the authentication password
    try:
        zabbix_url = 'https://'+zbx_server_composefile
        zapi = ZabbixAPI(zabbix_url, timeout=1800)
        zapi.login(user,password)
        print(f'Conectado ao Zabbix URL: {zabbix_url}, versão atual: {VersaoZabbix()}')
        try :
            # Verifica se o Zabbix proxy já existe
            proxy = zapi.proxy.get(filter={'host': zbx_hostname_composefile})
            if not proxy:
                # Cria o Zabbix proxy
                zapi.proxy.create(host=zbx_hostname_composefile, status=5, tls_connect=2, tls_accept=2, tls_psk_identity=zbx_hostname_composefile, tls_psk=chave_psk)
                print("Proxy cadastrado com sucesso!\nChave psk:",chave_psk)
                VerificaDockerCompose()
            else:
                print("Erro: Zabbix Proxy já cadastrado")
        finally:
            pass
            #print("Processo finalizado!")
    except Exception as err:
        print(f'Erro na conexão com o zabbix: {err}')

def VerificaDockerCompose():
    # Verifica se o arquivo docker-compose.yml já existe    
    if os.path.exists(str(diretorio_compose)):
        # Se existe, pergunta se o usuário deseja sobrescrever o arquivo
        dockercreate = input(f'O arquivo já existe no diretorio {diretorio_compose}, deseja sobrescrever? (Responda s ou n): ')
        if dockercreate == "s":
            docker_compose = CriaArquivoDockerCompose(zbx_hostname_composefile,zbx_server_composefile)
            print("Arquivo sobrescrito, reinciando container")
            with open(diretorio_compose, mode="wt", encoding="utf-8") as file:
                yaml.dump(docker_compose, file)
            container = VerificaContainer()
            if container == None:
                compose_cmd = f'docker compose -f {os.path.join(compose_dir, "docker-compose.yml")} up -d'
            else:
                compose_cmd = f'docker stop {container_name} && docker rm {container_name} && docker compose -f {os.path.join(compose_dir, "docker-compose.yml")} up -d'
            os.system(compose_cmd)
           #CadastraProxy()
        elif dockercreate == "n":
            print("Saindo")
    else:
        # Se não existe, cria o arquivo
        docker_compose = CriaArquivoDockerCompose(zbx_hostname_composefile,zbx_server_composefile)
        with open(diretorio_compose, mode="wt", encoding="utf-8") as file:
            yaml.dump(docker_compose, file)
            container = VerificaContainer()
            if container == None:
                compose_cmd = f'docker compose -f {os.path.join(compose_dir, "docker-compose.yml")} up -d'
            else:
                compose_cmd = f'docker stop {container_name} && docker rm {container_name} && docker compose -f {os.path.join(compose_dir, "docker-compose.yml")} up -d'
            os.system(compose_cmd)
            #CadastraProxy()

chave_psk=CriaPSK()
diretorio_compose='/opt/globalcare/docker/docker-compose.yml'
compose_dir = '/opt/globalcare/docker'
container_name = 'proxy'
zbx_hostname_composefile = input("Insira o nome do host que será utilizado no zabbix: ")+".docker.prx.globalcare"
zbx_server_composefile = input("Insira o endereço do servidor zabbix: ")
CadastraProxy()
