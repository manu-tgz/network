from app.physical_layer.devices import *
from app.tools.null import null_lists
from math import ceil
from app.tools.bits import format_8bit, sum_bytes

class Link_log(Log):
    all_link_data = []
    link_data = []

    def log_link(self, time, frame,error):
        string = str(time) +" "+ frame["MAC_source"] +" "+ frame["data"] +" "+ error
        self.link_data.append(string)
        self.all_link_data.append(string)
      
class DuplexEthernet(Ethernet):
    def transfer(self, sender, data, devices,time,signal_time):
        """obtiene el dispositivo que va a recibir y le pasa la informacion"""
        if len(self.devices) != 2: return data 
        
        out_device, out_port = get_diferent_by_key_in_dict(self.devices,sender)[0]
        
        self.last_time = time
        out_device.recieve(data, out_port,devices,time,signal_time,"ok")
        return data     
        
class PCMac(PC):
    def __init__(self,name):
        super().__init__(name)
        self.MAC = None
        self.log = Link_log()
        self.last_frame = ''
    
    def set_MAC(self, MAC):
        self.MAC = MAC
        
    def recieve(self, data, port, time, signal_time, status,is_the_last):
        data_scan = super().recieve(data, port, time, signal_time, status,is_the_last)
        self.last_frame += str(data_scan)
        
        if is_the_last: 
            self.save_frame(time)
            self.last_frame = ""
        
        return data_scan

    def save_frame(self, time):
 
        MAC = str(FrameSerializer.firts_var(self.last_frame))
        if MAC == self.MAC or MAC == "1"*16:
            frame = FrameSerializer.deserializer_frame(self.last_frame)
            error = '' 
            if FrameSerializer.frame_error(frame['check_data'], frame['data']):
                error = "error"
            
            self.log.log_link(time,frame,error)   
  
       
class LinkHub(Hub):
    def __init__(self, name, amount_ports):
        super().__init__(name, amount_ports)
        self.log = Link_log()

    def reset_buffer(self):
        pass      
        
class Switch(LinkHub):
    def __init__(self, name, amount_ports):
        super().__init__(name, amount_ports)
        self.mac = null_lists(int(amount_ports))
        self.full_buffers = False
        self.buffer_recive = ''
        self.buffer_send = ''

    def reset_buffer(self):
        self.buffer_recive = ''
        self.buffer_send = ''

    def recieve(self, data, enter_port,time,signal_time,status,is_the_last):
        """Me llego algo busco quienes reciben y se los envio"""
        self.log_data(data,enter_port,time)
        
        if(len(self.buffer_recive) < 16):
            self.buffer_recive += str(data) 
        else:
            if len(self.buffer_send) <16 :
                self.buffer_send += str(data)
            if(len(self.buffer_send) == 16 and self.full_buffers == False):
                self.mac[enter_port].append(self.buffer_send)
                self.full_buffers = True

        port_mac = find_mac(self.buffer_recive,self.mac) 
        
        if(port_mac != None): 
            return self.send(data, [self.ports[port_mac]] , time,signal_time,is_the_last)
        else:
            send_ports = get_diferents_by_index_in_list(self.ports,enter_port)
            return self.send( data, send_ports, time,signal_time,is_the_last)
    
    def send(self, data, ports,  time, signal_time,is_the_last):
        """le envio el bit a los dispositivos"""
        data_scanned = None
        diferent_data = False
        for port in ports:
            temp =  port.transfer(self.name, data, time, signal_time,is_the_last)
            if temp != data : 
                diferent_data = True
                data_scanned = temp
        return data if not diferent_data else data_scanned 

def find_mac(mac,macs):
    for port in range(len(macs)):
        for address in range (len(macs[port])):
            if mac == macs[port][address]:
                return port 

class FrameSerializer:
    """
                                  TRAMA
    |   16 bits  |  16 bits    |  8 bits   |  8 bits    |      |            |
    |------------|-------------|-----------|------------|------|------------|
    | MAC_source | MAC_receive | data_size | check_size | data | check_data |
    """
    def serializer_frame(host_MAC, MAC, data):

        MAC_source = bin(int(host_MAC,16))[2:]
        MAC_receive = bin(int(MAC,16))[2:]  
        
        num = ceil((len(data)/2))
        data_size = format_8bit(bin(num)[2:],1)
        
        check = bin(sum_bytes(data))[2:]
        check_num = ceil(len(check)/8)
        check_size = format_8bit(bin(check_num)[2:],1)
        
        data_bin = bin(int(data,16))[2:]
        data =format_8bit(data_bin,num)
        
        check_data= format_8bit(check,check_num)
        
        return MAC_receive + MAC_source + data_size + check_size + data + check_data
    
    def deserializer_frame(frame):
        result = {}
        result["MAC_receive"] = hex(int(frame[0:16] ,2))[2:].upper()
        result["MAC_source"] = hex(int(frame[16:32] ,2))[2:].upper()
        
        result["data_size"] = data_size =  8 * int(frame[32:40],2) 
        result["check_size"] = check_size =8 * int(frame[40:48],2)
        result["data"] = hex(int(frame[48:48+data_size] ,2))[2:].upper()   
        result["check_data"]= frame[48+data_size:48+data_size+check_size]
        
        return result
        
    def firts_var(frame):
        """Reeturn MAC that receives"""
        return hex(int(frame[0:16] ,2))[2:].upper()
    
    def frame_error(check_data, data):
        return check_data != format_8bit(bin(sum_bytes(data))[2:],2)     