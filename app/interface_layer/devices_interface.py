from app.tools.null import null_list

class Device:
    def __init__(self,name): 
        self.name = name
        self.log = None
        self.ports= None 
        
    def connect(self, ethernet, port):
        """Conecta un cable a un device. En un puerto de la computadora conecta el cable"""
        ethernet.connect(self, port)
        self.ports[port] = ethernet
        
    def disconnect(self, port):
        self.ports[port].disconnect(self.name)
        self.ports[port] = None 
    
    def recieve(self, data, enter_port,time,signal_time,status, is_the_last):
        pass
    
    def send(self, data, time, signal_time, is_the_last):
        pass
        
class ManyPortsDevice(Device):
    def __init__(self,name,amount_ports):
        super().__init__(name)
        self.amount_ports = int(amount_ports) 
        self.ports = null_list(self.amount_ports)

    def connect(self, ethernet, port):
        if not self.ports[port] is None: raise Exception("The port {} is not avaible.")
        super().connect(ethernet, port) 
 
    def disconnect(self, port):
        if 0 < port or port >=len(self.ports):
            raise Exception("Numero incorrecto de puerto!")
        super().disconnect(port)
