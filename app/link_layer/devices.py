from app.physical_layer.devices import *
from app.tools.null import null_lists

class Link_log(Log):
    all_link_data = []
    link_data = []

    def log_link(self, string):
        self.link_data.append(string)
        self.all_link_data.append(string)
        
class PCMac(PC):
    def __init__(self,name):
        super().__init__(name)
        self.MAC = None
        self.MAC_in_bit=None
        self.log = Link_log()
    
    def set_MAC(self, MAC):
        self.MAC = MAC
        self.MAC_in_bit = bin(int(MAC,16))[2:]
        
class LinkHub(Hub):
    def __init__(self, name, amount_ports):
        super().__init__(name, amount_ports)
        self.log = Link_log()

    def reset_buffer(self):
        pass      
        
class Switch(LinkHub):
    def __init__(self, name, amount_ports):
        super().__init__(name, amount_ports)
        self.mac = null_lists(amount_ports)
        
    def reset_buffer(self):
        pass
        
class Frame:
    def __init__(self,host, MAC, data):
        self.host = host
        self.MAC = MAC
        self.data = data
        self.frame = self.generate_frame()
        
    def generate_frame(self):
        return 
        
        