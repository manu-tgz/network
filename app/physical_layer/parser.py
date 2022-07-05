from .devices import Hub, PC
from .process import CreateDevice, ConnectDevices,SendData,Disconnect
from .devices import Log
from app.tools.file import  save, get_line_txt

class Intruction:
    """25 create host c1
      time: 25 , function:create, args: [host, c1]
    """
    def __init__(self, time:int, function, args): 
        self.time=time
        self.function = function
        self.args = args
    
class PhysicalParser:
    def get_commands_from_txt(self,file_name):
        lines = get_line_txt(file_name)
        return self.parser(lines) 
        
    def parser(self,lines):
        """Parsear las lines
        Args:
            lines (list): line from txt file
        """
        result=[]
        for line in lines:
            result.append(self.intrucciones(line.split(" ")))                  
        return result
    
    def save_data(self,file_name, devices):
        print("Saving data...") 
        for d in devices:
            save(d+".txt","output/solution_"+file_name,devices[d].log.data)
        save("all.txt","output/solution_"+file_name,Log.all_data)
        print("Done!")
    
    def intrucciones(self,words):
        intruccion = Intruction(int(words[0]), words[1], words[2:])
        
        if intruccion.function == "create":
            return CreateParser.execute(intruccion)
        elif intruccion.function == "connect":
            return ConnectParser.execute(intruccion)
        elif intruccion.function == "send":
            return SendParser.execute(intruccion )
        elif intruccion.function == "disconnect":
            return DisconnectParser(intruccion )
        # else:
        #     raise Exception("Comando no encontrado pruebe  'create', 'connect', 'send', 'disconnect'.")

class CreateParser():
    def execute(intruccion):
        device = intruccion.args.pop(0)

        if device == "hub":
            values= CreateParser.hub_parser(intruccion) 
        elif device == "host":
            values= CreateParser.host_parser(intruccion) 
        else:
            raise Exception("Dispositivo no encontrado pruebe 'hub','host'.") 
        
        return (values[0],CreateDevice(*values)) 
       
    def hub_parser(intruccion):
        return [intruccion.time, Hub, [intruccion.args[0], intruccion.args[1]]]  
    
    def host_parser(intruccion):
        return [intruccion.time, PC, [intruccion.args[0]]]        

class ConnectParser():
    def execute(intruccion):
        dev1, port1=intruccion.args.pop(0).split("_")
        dev2, port2=intruccion.args.pop(0).split("_")
        return (intruccion.time,ConnectDevices(intruccion.time,dev1, int(port1)-1,dev2, int(port2)-1 ))

class SendParser():
    def execute(intruccion):
        host = intruccion.args.pop(0)
        data = intruccion.args.pop(0)
        return (intruccion.time,SendData(intruccion.time,host, data))

class DisconnectParser:
    def execute(intruccion):
        dev1, port1=intruccion.args.pop(0).split("_")
        return (intruccion.time, Disconnect(intruccion.time,dev1, int(port1)-1))
    

