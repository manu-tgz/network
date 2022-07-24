from app.link_layer.devices import LinkLog, LinkHub, LinkPC, Switch
from app.tools.ip import convert_bits_line_to_ip
from .address import IpAddress

"""Devices de la capa NET
"""
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
  
"""PC de la capa NET"""
class NetPC( LinkPC, NetDevice):
    def __init__(self, name):
        LinkPC.__init__(self, name)
        NetDevice.__init__(self)
        
        self.interfaces = [
            {"mac":None, "ip":None, "buffer":"", "cable": None} 
        ]        
 

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
        

# class Router(NetLayerComputer):
#     def __init__(self, name, total_ports):
#         NetLayerComputer.__init__(self, name) 
#         self.interfaces = [ { "buffer":"" } for _ in range(total_ports) ]
    
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

#     def recieve_data(self, data, enter_port, devices):

#         devices.append((self,enter_port+1))

#         if self.current_transmision == None or Env.current_env.global_time - self.last_transmision_time > Env.current_env.signal_time :
#             return data

#         return int(data) ^ int(self.current_transmision)

