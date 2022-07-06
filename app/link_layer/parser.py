from app.physical_layer.parser import PhysicalParser, CreateParser
from app.tools.file import  save
from .devices import *

class LinkParser(PhysicalParser):
    def __init__(self):
        super().__init__()
        self.parsers["mac"]= MacParser
        self.parsers["send_frame"]= FrameParser 

    def save_data(file_name, devices):
        print("Saving data...") 
        for d in devices:
            save(d+".txt","output/solution_"+file_name,devices[d].log.data)
            save(d+"_data.txt","output/solution_"+file_name,devices[d].log.link_data)
    
        save("all.txt","output/solution_"+file_name,Link_log.all_data)
        save("data_all.txt","output/solution_"+file_name,Link_log.all_link_data)
        print("OK")
        
class MacParser:
    def __init__(self):
        pass
    def execute(intruccion):
        pass  

class FrameParser:
    def __init__(self):
        pass
    def execute(intruccion):
        pass
    
class CreateParserLink(CreateParser):
    def __init__(self):
        super().__init__()
        self.device_parser["switch"] = CreateParserLink.switch
    
    def hub(intruccion):
        return [intruccion.time, LinkHub, [intruccion.args[0], intruccion.args[1]]]  
    
    def host(intruccion):
        return [intruccion.time, PCMac, [intruccion.args[0]]]
    
    def switch(intruccion):
        return 
