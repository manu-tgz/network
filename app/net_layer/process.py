from app.link_layer.process import SetMAC
from app.interface_layer.process_interface import Process
from app.tools.bits import *
from .devices import NetPC, Router
from .address import IpAddress

class SetMACNET(SetMAC):
    def __init__(self, time, host, mac, interface):
        super().__init__(time,host, mac)
        self.device_class = [NetPC, Router]
        self.interface = int(interface)

    def set_mac(self, device):
        device.set_MAC(self.mac, self.interface)

class IpProcess(Process):
    def __init__(self, time, host, ip_address, mask, interface):
        super().__init__(time)
        self.host=host
        self.ip_address = IpAddress( ip_address )
        self.interface = int(interface)
        self.mask = IpAddress(mask)

    def execute(self, network):
        device = network.devices[self.host]
        device.set_ip_and_mask(self.ip_address, self.mask, self.interface)

class RouteProcess(Process):
    def __init__(self, time,host,destination,mask,gateway,interface):
        super().__init__(time)
        self.host =  host
        self.destination= IpAddress(destination)
        self.mask=IpAddress(mask)
        self.gateway=IpAddress(gateway)
        self.interface=int(interface)    

class RouteAdd(RouteProcess):
    def execute(self, network):
        device = network.devices[self.host]
        device.add_route(self.destination,self.mask,self.gateway, self.interface)

class RouteDelete(RouteProcess):
    def execute(self, network):
        device = network.devices[self.host]
        device.delete_route(self.destination,self.mask,self.gateway, self.interface)

class RouteReset(Process):
    def __init__(self, time,host):
        super().__init__(time)
        self.host =  host

    def execute(self,network):
        device = network.devices[self.host]
        device.clear_routes()

class SendPacket(Process):
    def __init__(self, time, host, ip_address, mask, interface):
        super().__init__(time)

    def execute(self, network):
        pass

#region net
def search_route_in_routes(ip_destiny,routes):
    for r in routes:
        if ip_destiny.get_subnet(r["mask"]) == r["destination"] :
            return r
    #raise Exception("No existe una ruta por defecto.")
    return None
    
#endregion