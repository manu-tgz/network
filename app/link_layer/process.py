from app.interface_layer.process_interface import Process
from .devices import PCMac

class ProcessMAC(Process):
    def __init__(self, time, host, mac):
        super().__init__(time)
        self.mac = mac
        self.host = host

class SetMAC(ProcessMAC):

    def execute(self, network):
        device = network.devices[self.host]
        if device is PCMac:
            device.set_mac(self.mac)
        else:
            Exception('This is not a PC with MAC') 
            
class SendFrame(ProcessMAC):  
    def __init__(self, time, host, mac, data):
        super().__init__(time, host, mac)
        self.data = data
        
    def execute(self, network):
        pass