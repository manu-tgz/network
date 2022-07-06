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

    def connect(self, device, port_index):
        if len(self.devices) >= 2:
            raise Exception("EL CABLE YA TIENE 2 DISPOSITIVOS CONECTADOS!")
        self.devices[device.name] = device, port_index

    def disconnect(self, device_name):
        self.devices.pop(device_name)
    
    def transfer(self, sender, data, devices,global_time,signal_time):
        if len(self.devices) != 2: return data 
        reciever_device, reciever_port = get_diferent_by_key_in_dict(self.devices,sender)[0]

        return reciever_device.recieve(data, reciever_port,devices,global_time,signal_time) 

class PC(Device):
    def __init__(self,name):
        super().__init__(name)
        self.ports = [None] 
        self.current_transmision = None
        self.last_transmision_time = None 

    def connect(self, ethernet, port):
        if port != 0: raise Exception("Los host solo tienen el puerto 1.")
        super().connect(ethernet, port)

    def disconnect(self, port):
        if port != 0: raise Exception("Los host solo tienen 1 puerto.")
        super().disconnect(port)
        
    def send(self, data_to_send, global_time, signal_time):
        if self.ports[0] == None:
            raise Exception("Don't have "+self.name) # AQUI!!!!!!!!!!!!!!!!!!
                
        self.last_transmision_time = global_time 
        self.current_transmision = data_to_send 
        devices = []
        data_scanned =self.ports[0].transfer(self.name,data_to_send, devices,global_time,signal_time)

        for d,p in devices:
            #d.log(global_time,d.name+"_"+str(p),"recieve",data_scanned,"")
            d.log_data(data_scanned,p,global_time)
            
        self.log(global_time,self.name+"_1", "send", data_to_send, "ok" if data_scanned == data_to_send else "collision")
   
    def recieve(self, data, port, devices,global_time,signal_time):
        devices.append((self,1))

        if self.current_transmision == None or global_time - self.last_transmision_time > signal_time :
            return data

        return int(data) ^ int(self.current_transmision)
  
    def log_data(self, data,_, global_time):
        self.log(global_time,self.name+"_1","receive",data, "")

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
        
    def log_data(self, data, port_index,global_time):
        for i in range(len(self.ports)):
            if self.ports[i] == None:
                continue

            if port_index == i:
                self.log(global_time,self.name+"_"+str(i),"receive",data, "")
            else:
                self.log(global_time,self.name+"_"+str(i),"send",data, "")

    def recieve(self, data, enter_port, devices,global_time,signal_time):
        devices.append((self,enter_port))
        send_ports = get_diferents_by_index_in_list(self.ports,enter_port)
        return self.send( data, send_ports, devices, global_time,signal_time)
    
    def send(self, data, ports, devices, global_time, signal_time):
        data_scanned = None
        diferent_data = False
        for port in ports:
            temp =  port.transfer(self.name, data, devices, global_time, signal_time)
            if temp != data : 
                diferent_data = True
                data_scanned = temp
        return data if not diferent_data else data_scanned