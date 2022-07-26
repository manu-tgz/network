from app.interface_layer.process_interface import Process
from .devices import LinkPC, FrameSerializer
from app.physical_layer.process import SendData

class ProcessMAC(Process):
    def __init__(self, time, host, mac):
        super().__init__(time)
        self.mac = mac
        self.host = host
        self.device_class = []

class SetMAC(ProcessMAC):
    """Asignar la MAC a dispositivos permitidos (computadoras)

    Args:
        time: tiempo del proceso
        host: computadora de asigancion de Mac
        mac: MAC a asignar
    """
    def __init__(self, time, host, mac):
        super().__init__(time, host, mac)
        self.device_class = [LinkPC]

    def execute(self, network):
        device = network.devices[self.host]
        if type(device) in self.device_class:
            self.set_mac(device)
        else:
            Exception('This is not a device with MAC')
    
    def set_mac(self, device):
        device.set_MAC(self.mac)
    
class SendFrame(SendData):  
    def __init__(self, time, host, mac, data):
        super().__init__(time, host, data)
        self.mac = mac
        self.frame = None
        
    def execute(self, network):
        """Se crea la trama y se envia bit a bit"""
        if self.frame == None: 
            self.create_frame(network.devices[self.host].MAC)
        
        return super().execute(network)
    
    def create_frame(self, host_MAC):
        """Crear la trama que se quiere enviar"""
        self.data = self.frame = FrameSerializer.serializer_frame(host_MAC, self.mac, self.data)
        print(FrameSerializer.deserializer_frame(self.data))
