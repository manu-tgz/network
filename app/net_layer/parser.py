from app.physical_layer.parser import CreateParser
from .devices import NetPC
class CreateParserNet(CreateParser):
    def __init__(self):
        super().__init__()
        self.device_parser = {"switch":CreateParserNet.switch,
                              "hub": CreateParserNet.hub,
                              "host": CreateParserNet.host 
        }
    
    def hub(intruccion):
        return [intruccion.time, LinkHub, [intruccion.args[0], intruccion.args[1]]]  
    
    def host(intruccion):
        return [intruccion.time, NetPC, [intruccion.args[0]]]
    
    def switch(intruccion):
        return [intruccion.time, Switch, [intruccion.args[0], intruccion.args[1]]] 