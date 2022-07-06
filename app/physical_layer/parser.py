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
    def __init__(self):
        self.parsers = {"create": CreateParser(),
                        "connect":ConnectParser,
                        "send":SendParser,
                        "disconnect":DisconnectParser
        }
    
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

        for key in self.parsers:
            if intruccion.function == key:
                return self.parsers[key].execute(intruccion)
        
class CreateParser():
    def __init__(self):
        self.device_parser = {"hub": CreateParser.hub,
                              "host": CreateParser.host 
        }
        
    def execute(self, intruccion):
        device = intruccion.args.pop(0)
        values = None
        for key in self.device_parser:
            if device == key:
                values = self.device_parser[key](intruccion)
                break
        if not values is None:        
            return (values[0],CreateDevice(*values)) 
        else:
            raise Exception("Dispositivo no encontrado") 
       
    def hub(intruccion):
        return [intruccion.time, Hub, [intruccion.args[0], intruccion.args[1]]]  
    
    def host(intruccion):
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