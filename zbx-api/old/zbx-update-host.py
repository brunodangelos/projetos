from pyzabbix import ZabbixAPI
import csv
from progressbar import ProgressBar, Percentage, ETA, ReverseBar, RotatingMarker, Timer

zapi = ZabbixAPI("localhost")
zapi.login(user="zbx", password="zbx")

arq = csv.reader(open('file'))

linhas = sum(1 for linha in arq)

f = csv.reader(open('file'), delimiter=';')
bar = ProgressBar(maxval=linhas,widgets=[Percentage(), ReverseBar(), ETA(), RotatingMarker(), Timer()]).start()
i = 0

for [hostname,ip] in f:
    hostcriado = zapi.host.update(
        host= hostname,
        status= 0,
        interfaces=[{
            "type": 1,
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
            "templateid": 10001
        }]
    )


    i += 1
    bar.update(i)

bar.finish