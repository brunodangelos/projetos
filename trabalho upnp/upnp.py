import miniupnpc

upnp = miniupnpc.UPnP()
upnp.discoverdelay = 10
upnp.discover()
upnp.selectigd()
port = 3389

upnp.addportmapping( port, 'TCP', upnp.lanaddr,port, 'Isso nao e legal')