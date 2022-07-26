from app.physical_layer.parser import PhysicalParser, CreateParser,ConnectParser
from app.tools.file import  save
from .devices import *
from app.interface_layer.parser_interface import ABCParser
from .process import SetMAC, SendFrame

class LinkParser(ABCParser):
    def __init__(self):
        super().__init__()
        self.parsers = {"connect":LinkConnectParser(),
                        "send_frame":FrameParser,
                        "create": CreateParserLink(),
                        "mac":MacParser
        }
        self.parser_class = PhysicalParser

    def save_data(self, file_name, devices):
        for d in devices:
            save(d+".txt","output/solution_"+file_name,devices[d].log.data)
            save(d+"_data.txt","output/solution_"+file_name,devices[d].log.link_data)
    
        save("all.txt","output/solution_"+file_name, LinkLog.all_data)
        save("all_data.txt","output/solution_"+file_name, LinkLog.all_link_data)
        print("OK")        
        
class MacParser:
    def execute(instruction):
        return (instruction.time, SetMAC(instruction.time, *instruction.args))

class FrameParser:
    def execute(instruction):
        return (instruction.time, SendFrame(instruction.time, *instruction.args))
    
class CreateParserLink(CreateParser):
    def __init__(self):
        super().__init__()
        self.device_parser.update({"switch":self.switch
        })

        self.device_class.update({"hub": LinkHub,
                                  "host":LinkPC,
                                  "switch":Switch
        })

    
    def switch(self,instruction):
        return [instruction.time, self.device_class['switch'], [instruction.args[0], instruction.args[1]]]  
    
class LinkConnectParser(ConnectParser):
    def execute(self,instruction):
        tuple =  super().execute(instruction)
        tuple[1].ethernet= DuplexEthernet
        return tuple