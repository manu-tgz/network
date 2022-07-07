from app.physical_layer.devices import EthernetHalfDuplex
from app.interface_layer.process_interface import Process

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
        self.ethernet = EthernetHalfDuplex
          
    def execute(self, network):
        #print(network.devices)
        if not network.devices.__contains__(self.dev1) or not network.devices.__contains__(self.dev2):
            raise Exception("No existe el dispositivo.")

        d1=network.devices[self.dev1]
        d2=network.devices[self.dev2]

        ethernet = self.ethernet()
        d1.connect(ethernet,self.port1)
        d2.connect(ethernet,self.port2)

class SendData(Process):
    def __init__(self, time, host, data, index=0,collision=False ):
        super().__init__(time)
        self.host = host
        self.data= data
        self.index = index
        self.collision = collision

    # Make async/await
    def execute(self, network):
        """Envia un bit y si todo ok crea otro evento para que se envie lo que falte
        si hubo collision lo reenvia en 10 o 20 segundos"""
        if not network.devices.__contains__(self.host):
            raise Exception("Dont't exist {} dispositive".format(self.host))
        is_the_last = self.index == len(self.data)-1
        result = network.devices[self.host].send(self.data[self.index],self.time,network.signal_time,is_the_last)
        time = self.time+ network.signal_time
        
        # print("send time:{} host:{} data:{} result:{}".format(self.time, self.host,self.data[self.index],result))
        return self.create_event(time, result)
        
    def create_event(self,time, result):
        """crea otro evento para que se envie el proximo bit o reenviar el de collision"""
        if result == "ok" and self.index+1 < len(self.data):
            return [(time, SendData(time, self.host,self.data,self.index+1))]
        elif result == "collision":
            if self.collision is True: time+=10
            return [(time, SendData(time, self.host,self.data, self.index, True ))]         
        
class Disconnect(Process):
    def __init__(self, time, host, port):
        super().__init__(time)
        self.host = host
        self.port = port

    def execute(self,network):
        network.devices[self.host].disconnect(self.port)  