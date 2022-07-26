from app.interface_layer.devices_interface import ManyPortsDevice
from app.link_layer.devices import LinkLog, LinkHub, LinkPC, Switch
from app.tools.ip import convert_bits_line_to_ip
from .address import IpAddress

"""Devices de la capa NET"""
class NetLog(LinkLog) :
    all_net_data = []
    def __init__(self):
        LinkLog.__init__(self)
        self.net_data = []

    def _log_net(self, string):
        self.net_data.append(string)
        self.all_net_data.append(string)
    def log_net(self,time,ip_origin_bits,payload, extra=""):
        self._log_net(f"{time} {convert_bits_line_to_ip(ip_origin_bits)} {payload} {(' ('+extra+')') if  extra !='' else '' }")

class NetDevice ():
    def __init__(self):
        self.log = NetLog()
        self.interfaces = None
        self.ip_address = None
        self.buffer = None
        self._route_table = [] 
    
    def connect(self, cable, port):
        self.interfaces[port]["cable"] = cable
        cable.connect(self,port)
        
    def set_ip_and_mask(self,ip,mask, interface):
        self.set_ip(ip,interface)
        self.set_subnet_mask(mask,interface)

    def set_ip(self, ip,interface):
        self.interfaces[interface-1]["ip"] = ip

    def set_subnet_mask(self, ip,interface=1):
        self.interfaces[interface-1]["mask"] = ip

    def refresh_interface(self, interface):
        self.ip_address = self.interfaces[interface-1]["ip"]
        self.MAC = self.interfaces[interface-1]["mac"]
        self.buffer = self.interfaces[interface-1]["buffer"]
        self.ports=[self.interfaces[interface-1]["cable"]]
    
    def add_route(self,destination,mask,gateway,interface):
        # ordenar por cantidad de unos (1) en la mascara !!
        self._route_table.append({
            "destination": destination ,"mask" : mask , 
            "gateway" : gateway , "interface": interface 
        }) 

    def clear_routes(self):
        self._route_table.clear()

    def delete_route(self,destination,mask,gateway,interface):
        i = 0
        for r in self._route_table:
            if r["destination"] == destination and r["mask"] == mask and r["gateway"] == gateway and r["interface"]==interface:
                self._route_table.pop(i)
            i+=1

"""PC de la capa NET"""
class NetPC( LinkPC, NetDevice):
    def __init__(self, name):
        LinkPC.__init__(self, name)
        NetDevice.__init__(self)
        
        self.interfaces = [
            {"mac":None, "ip":None, "buffer":"", "cable": None} 
        ]
        
    def set_MAC(self, MAC, interface):
        self.interfaces[interface-1]["mac"]= MAC
        super().set_MAC(MAC)
                
    def send(self, data_to_send, time, signal_time, is_the_last):
        return super().send(data_to_send, time, signal_time, is_the_last)

class NetHub(LinkHub):
    def __init__(self, name, amount_ports):
        super().__init__(self, name, amount_ports)
        self.log = NetLog()
        
    def net_reset_buffer(self,interface):
        self.reset_buffer()

class NetSwitch (Switch):
    def __init__(self, name, amount_ports):
        Switch.__init__(self, name, amount_ports)
        self.log = NetLog()
    def net_reset_buffer(self, interface):
        self.reset_buffer()
        
class Router(ManyPortsDevice, NetDevice):
    def __init__(self, name, amount_ports):
        ManyPortsDevice.__init__(self,name,amount_ports)
        NetDevice.__init__(self) 
        self.interfaces = [ { "buffer":"" } for _ in range(amount_ports) ]
    
    def set_MAC(self, MAC, interface):
        self.interfaces[interface-1]["mac"]= MAC
        self.MAC = MAC
         
#     def net_reset_buffer(self, interface):
#        #self.ip_addrs = self.interfaces[interface-1]["ip"]
#        #self.MAC = self.interfaces[interface-1]["mac"]
#        #self.buffer = self.interfaces[interface-1]["buffer"]
#        #self.port=self.interfaces[interface-1]["cable"] 
#         self.refresh_interface(interface)

#         is_not_other = False 
#         #self._process_icmp()
#         is_not_other|= self._process_arpq(interface)

#         if not is_not_other: 
#             try:
#                 mac_recive,data=resolve_frame(self.buffer) 
                
#                 ip_destiny,ip_origin,ttl,protocol,payload=resolve_net_package(data)
#                 route = search_route_in_routes(ip_destiny, self._route_table)

#                 if route == None:
#                     # no existe una ruta
#                     send_ip_package_or_resolve_mac(self, ip_origin, None,dec_to_bits(TTL_DEFAULT), dec_to_bits(1), dec_to_bits(3), mac=mac_recive ,interface=interface ) 

#                     self.refresh_interface(interface)
#                     LinkLayerComputer.reset_buffer(self)
#                     self.clean_buffer(interface)  
#                     return

#                 send_ip_package_or_resolve_mac(self, route["destination"],ip_origin, ttl, protocol, payload,interface=route["interface"])
#             except:
#                 pass

#         self.refresh_interface(interface)
#         LinkLayerComputer.reset_buffer(self)
#         self.clean_buffer(interface)  