from pyzabbix import ZabbixAPI
import csv
from progressbar import ProgressBar, Percentage, ETA, ReverseBar, RotatingMarker, Timer

zapi = ZabbixAPI("http://1.1.1.1/")
zapi.login(user="", password="")

arq = csv.reader(open('$DIRETORIO'))

linhas = sum(1 for linha in arq)

f = csv.reader(open('$DIRETORIO'), delimiter=';')
bar = ProgressBar(maxval=linhas,widgets=[Percentage(), ReverseBar(), ETA(), RotatingMarker(), Timer()]).start()
i = 0

for [hostname,ip] in f:
    hostcriado = zapi.host.create(
        host= hostname,
        status= 0,
        interfaces=[{
            "type": 0,
            "main": "1",
            "useip": 1,
            "ip": ip,
            "dns": "",
            "port": 10050
        }],
        groups=[{
            "groupid": 2
        }],
        templates=[{
            "templateid": 10186
        }]
    )


    i += 1
    bar.update(i)

bar.finish