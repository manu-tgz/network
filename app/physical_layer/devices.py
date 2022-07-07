from app.tools.null import null_list
from app.tools.collections import get_diferent_by_key_in_dict,get_diferents_by_index_in_list
 
class Log:
    all_data = [] 
    def __init__(self):
        self.data = []
    def log(self, time ,device , action ,data, status):
        s = " ".join([str(time),device,action,str(data), status])
        self.data.append(s)
        self.all_data.append(s)
    
    def __call__(self, time ,device , action ,data, status):
        self.log(time ,device , action ,data, status)

class Device:
    def __init__(self,name): 
        self.log = Log()
        self.name = name
        self.ports= None 
        
    def connect(self, ethernet, port):
        """Conecta un cable a un device. En un puerto de la computadora conecta el cable"""
        ethernet.connect(self, port)
        self.ports[port] = ethernet
        
    def disconnect(self, port):
        self.ports[port].disconnect(self.name)
        self.ports[port] = None 

class Ethernet:
    def __init__(self):
        self.devices = {}
        self.last_time = None

    def connect(self, device, port_index):
        if len(self.devices) >= 2:
            raise Exception("EL CABLE YA TIENE 2 DISPOSITIVOS CONECTADOS!")
        self.devices[device.name] = device, port_index

    def disconnect(self, device_name):
        self.devices.pop(device_name)
        
    def transfer(self, sender, data, devices,time,signal_time,is_the_last):
        pass
        
class EthernetHalfDuplex(Ethernet):
    
    def transfer(self, sender, data,time,signal_time, is_the_last):
        """obtiene el dispositivo que va a recibir y le pasa la informacion"""
        if len(self.devices) != 2: return data 
        
        out_device, out_port = get_diferent_by_key_in_dict(self.devices,sender)[0]
        
        if self.last_time != None and self.is_collision(time, signal_time):
            self.last_time = time
            out_device.recieve(data, out_port,time,signal_time,"error",is_the_last)
            return bi(int(data))
        
        self.last_time = time
        out_device.recieve(data, out_port,time,signal_time,"ok",is_the_last)
        return data
        
    def is_collision(self, time, signal_time):
        #  pregunta si hay colision y luego actualiza last_time
        # print("last_time={} time={}".format(self.last_time,time))
        return time - self.last_time < signal_time 
        
def bi(num):
    if num ==1: return 0
    else: return 1                  

class PC(Device):
    def __init__(self,name):
        super().__init__(name)
        self.ports = [None] 

    def connect(self, ethernet, port):
        if port != 0: raise Exception("Los host solo tienen el puerto 1.")
        super().connect(ethernet, port)

    def disconnect(self, port):
        if port != 0: raise Exception("Los host solo tienen 1 puerto.")
        super().disconnect(port)
        
    def send(self, data_to_send, time, signal_time, is_the_last):
        if self.ports[0] == None:
            raise Exception("Don't have "+self.name) 
                
        data_scanned =self.ports[0].transfer(self.name,data_to_send,time,signal_time,is_the_last)
        
        result = "ok" if data_scanned == data_to_send else "collision"  
        self.log(time,self.name+"_1", "send", data_to_send,result )
        return result
   
    def recieve(self, data, port,time,signal_time, status, is_the_last):
        mydata = bi(int(data))
        
        if status == "ok" :
            mydata = data
        self.log_data(mydata,port,time)
        
        return mydata
  
    def log_data(self, data,_, time):
        self.log(time,self.name+"_1","receive",data, "")

class Hub(Device):
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
        
    def log_data(self, data, port_index,time):
        for i in range(len(self.ports)):
            if self.ports[i] == None:
                continue

            if port_index == i:
                self.log(time,self.name+"_"+str(i),"receive",data, "")
            else:
                self.log(time,self.name+"_"+str(i),"send",data, "")

    def recieve(self, data, enter_port,time,signal_time,status, is_the_last):
        """Me llego algo busco quienes reciben y se los envio"""
        send_ports = get_diferents_by_index_in_list(self.ports,enter_port)
        
        self.log_data(data,enter_port,time)
        return self.send( data, send_ports, time,signal_time, is_the_last)
    
    def send(self, data, ports,  time, signal_time, is_the_last):
        """le envio el bit a los dispositivos"""
        data_scanned = None
        diferent_data = False
        for port in ports:
            temp =  port.transfer(self.name, data, time, signal_time, is_the_last)
            if temp != data : 
                diferent_data = True
                data_scanned = temp
        return data if not diferent_data else data_scanned