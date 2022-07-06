from app.physical_layer.parser import PhysicalParser, CreateParser
from app.tools.file import  save
from .devices import *
from app.interface_layer.parser_interface import ABCParser
from .process import SetMAC, SendFrame


class LinkParser(ABCParser):
    def __init__(self):
        super().__init__()
        self.parsers = {"create": CreateParserLink(),
                        "mac":MacParser,
                        "send_frame":FrameParser
        }
        self.parser_class = PhysicalParser
        

    def save_data(file_name, devices):
        print("Saving data...") 
        for d in devices:
            save(d+".txt","output/solution_"+file_name,devices[d].log.data)
            save(d+"_data.txt","output/solution_"+file_name,devices[d].log.link_data)
    
        save("all.txt","output/solution_"+file_name, Link_log.all_data)
        save("data_all.txt","output/solution_"+file_name, Link_log.all_link_data)
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
        self.device_parser["switch"] = CreateParserLink.switch
    
    def hub(intruccion):
        return [intruccion.time, LinkHub, [intruccion.args[0], intruccion.args[1]]]  
    
    def host(intruccion):
        return [intruccion.time, PCMac, [intruccion.args[0]]]
    
    def switch(intruccion):
        return [intruccion.time, Switch, [intruccion.args[0], intruccion.args[1]]]  