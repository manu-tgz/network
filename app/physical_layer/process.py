from app.physical_layer.devices import Ethernet

class Process:
    def __init__(self, time ):
        self.time = time
    def execute(self, network):
        pass
    def __lt__(self, other):
        return True

class CreateDevice(Process):
    def __init__(self, time, device, args ):
        super().__init__(time)
        self.device = device
        self.args= args
        
    def execute(self, network):
        device = self.device(*self.args)
        network.add_device(device)
    
class ConnectDevices(Process):
    """conecta 2 puertos de 2 dispositivo 
    """
    def __init__(self, time, dev1, port1, dev2, port2):
        super().__init__(time)
        self.dev1 = dev1
        self.port1 = port1
        self.dev2 = dev2
        self.port2 = port2
          
    def execute(self, network):
        #print(network.devices)
        if not network.devices.__contains__(self.dev1) or not network.devices.__contains__(self.dev2):
            raise Exception("No existe el dispositivo.")

        d1=network.devices[self.dev1]
        d2=network.devices[self.dev2]

        ethernet = Ethernet()
        d1.connect(ethernet,self.port1)
        d2.connect(ethernet,self.port2)

class SendData(Process):
    def __init__(self, time, host, data ):
        super().__init__(time)
        self.host = host
        self.data= data
        
    def execute(self, network):
        if not network.devices.__contains__(self.host):
            raise Exception("No existe el dispositivo.")
        time = self.time
        send_events = []
        for byte in self.data:
            send_events.append((time, Send(time, self.host,int(byte))))
            time+=network.signal_time
        return send_events
            
class Send(SendData):
    def execute(self, network):
        network.devices[self.host].send(self.data,self.time,network.signal_time)
        
class Disconnect(Process):
    def __init__(self, time, host, port):
        super().__init__(time)
        self.host = host
        self.port = port

    def execute(self,network):
        network.devices[self.host].disconnect(self.port)  