from .devices import Hub, PC
from .process import CreateDevice, ConnectDevices,SendData,Disconnect
from .devices import Log
from app.interface_layer.parser_interface import ABCParser
from app.tools.file import  save


class PhysicalParser(ABCParser):
    def __init__(self):
        self.parsers = {"send":SendParser,
                        "disconnect":DisconnectParser,
                        "create": CreateParser(),
                        "connect":ConnectParser()
        }
    
    def save_data(self,file_name, devices):
        for d in devices:
            save(d+".txt","output/solution_"+file_name,devices[d].log.data)
        save("all.txt","output/solution_"+file_name,Log.all_data)
        print("Ok!")
    
class CreateParser():
    def __init__(self):
        self.device_parser = {"hub": self.hub,
                              "host": self.host 
        }
        self.device_class = {"hub": Hub,
                              "host":PC 
        }
        
    def execute(self, instruction):
        device = instruction.args.pop(0)
        values = None
        for key in self.device_parser:
            if device == key:
                values = self.device_parser[key](instruction)
                break
        if not values is None:        
            return (values[0],CreateDevice(*values))  
       
    def hub(self,instruction):
        return [instruction.time, self.device_class['hub'], [instruction.args[0], int(instruction.args[1])]]  
    
    def host(self, instruction):
        return [instruction.time, self.device_class['host'], [instruction.args[0]]]
     
class ConnectParser():
    def execute(self,instruction):
        dev1, port1=instruction.args.pop(0).split("_")
        dev2, port2=instruction.args.pop(0).split("_")
        return (instruction.time,ConnectDevices(instruction.time,dev1, int(port1)-1,dev2, int(port2)-1 ))

class SendParser():
    def execute(instruction):
        host = instruction.args.pop(0)
        data = instruction.args.pop(0)
        return (instruction.time,SendData(instruction.time,host, data))

class DisconnectParser:
    def execute(instruction):
        dev1, port1=instruction.args.pop(0).split("_")
        return (instruction.time, Disconnect(instruction.time,dev1, int(port1)-1))