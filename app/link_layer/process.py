from app.interface_layer.process_interface import Process
from .devices import PCMac, FrameSerializer
from app.physical_layer.process import SendData

class ProcessMAC(Process):
    def __init__(self, time, host, mac):
        super().__init__(time)
        self.mac = mac
        self.host = host

class SetMAC(ProcessMAC):

    def execute(self, network):
        device = network.devices[self.host]
        if type(device) is PCMac:
            device.set_MAC(self.mac)
        else:
            Exception('This is not a PC with MAC') 
            
class SendFrame(SendData):  
    def __init__(self, time, host, mac, data):
        super().__init__(time, host, data)
        self.mac = mac
        self.frame = None
        
    def execute(self, network):
        if self.frame == None: 
            host_MAC =network.devices[self.host].MAC
            self.data = self.frame = FrameSerializer.serializer_frame(host_MAC, self.mac, self.data)
            print(FrameSerializer.deserializer_frame(self.data))
        return super().execute(network)
