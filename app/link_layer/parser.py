from app.physical_layer.parser import PhysicalParser, CreateParser,ConnectParser
from app.tools.file import  save
from .devices import *
from app.interface_layer.parser_interface import ABCParser
from .process import SetMAC, SendFrame

class LinkParser(ABCParser):
    def __init__(self):
        super().__init__()
        self.parsers = {"create": CreateParserLink(),
                        "mac":MacParser,
                        "send_frame":FrameParser,
                        "connect":LinkConnectParser()
        }
        self.parser_class = PhysicalParser

    def save_data(self, file_name, devices):
        for d in devices:
            save(d+".txt","output/solution_"+file_name,devices[d].log.data)
            save(d+"_data.txt","output/solution_"+file_name,devices[d].log.link_data)
    
        save("all.txt","output/solution_"+file_name, Link_log.all_data)
        save("all_data.txt","output/solution_"+file_name, Link_log.all_link_data)
        print("OK")        
        
class MacParser:
    def execute(intruccion):
        return (intruccion.time, SetMAC(intruccion.time, *intruccion.args))

class FrameParser:
    def execute(intruccion):
        return (intruccion.time, SendFrame(intruccion.time, *intruccion.args))
    
class CreateParserLink(CreateParser):
    def __init__(self):
        super().__init__()
        self.device_parser = {"switch":CreateParserLink.switch,
                              "hub": CreateParserLink.hub,
                              "host": CreateParserLink.host 
        }
    
    def hub(intruccion):
        return [intruccion.time, LinkHub, [intruccion.args[0], intruccion.args[1]]]  
    
    def host(intruccion):
        return [intruccion.time, PCMac, [intruccion.args[0]]]
    
    def switch(intruccion):
        return [intruccion.time, Switch, [intruccion.args[0], intruccion.args[1]]]  
    
class LinkConnectParser(ConnectParser):
    def execute(self,intruccion):
        tuple =  super().execute(intruccion)
        tuple[1].ethernet= DuplexEthernet