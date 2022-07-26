from app.interface_layer.parser_interface import ABCParser, InstructionParser
from app.link_layer.parser import CreateParserLink, LinkParser
from app.tools.file import save
from .process import SetMACNET, IpProcess,RouteAdd,RouteDelete, RouteReset
from .devices import NetPC, NetHub, NetSwitch, NetLog, Router

class NetParser(ABCParser):
    def __init__(self):
        super().__init__()
        self.parsers = {"create": NetCreateParser(),
                        "mac":NetMacParser,
                        "ip":IpParser,
                        "send_packet":SendPacket,
                        "route":RouteParser()
                        
                        # "send_frame":FrameParser,
                        # "connect":LinkConnectParser()
        }
        self.parser_class = LinkParser

    def save_data(self, file_name, devices):
        for d in devices:
            save(d+".txt","output/solution_"+file_name,devices[d].log.data)
            save(d+"_data.txt","output/solution_"+file_name,devices[d].log.link_data)
            save(d+"_payload.txt","output/solution_"+file_name,devices[d].log.net_data)
            print(d,":")
            for l in devices[d].log.net_data:
                print(" ",l)
        # guardamos all.txt con el registro de todos los dispositivos.
        save("all.txt","output/solution_"+file_name,NetLog.all_data)
        save("data_all.txt","output/solution_"+file_name,NetLog.all_link_data)
        save("payload_all.txt","output/solution_"+file_name,NetLog.all_net_data)

class NetCreateParser(CreateParserLink):
    def __init__(self):
        super().__init__()
        self.device_class.update({"hub": NetHub,
                                  "host":NetPC,
                                  "switch":NetSwitch,
                                  "router":Router
        })
        self.device_parser.update({"router":self.router
        })       
    
    def router(self,instruction):
        return [instruction.time, self.device_class['router'], [instruction.args[0], int(instruction.args[1])]]  
        
class InterfaceParser:
    """Son los parser para las lineas de comando que traen interfaces"""
    def split_and_update(instruction):
        splited_name = instruction.args[0].split(":")
        instruction.args[0] = splited_name[0] 
        interface = splited_name[1] if len(splited_name)==2 else 1
        instruction.args.append(interface)
        
class NetMacParser:
    def execute(instruction):
        InterfaceParser.split_and_update(instruction)
        return (instruction.time, SetMACNET(instruction.time, *instruction.args))
    
class IpParser:
    def execute(instruction):
        InterfaceParser.split_and_update(instruction)
        return (instruction.time, IpProcess(instruction.time, *instruction.args))

class SendPacket(InstructionParser):
    def execute(instruction):
        pass

class RouteParser(InstructionParser):
    def __init__(self):
        self.function_parser = {"reset": self.reset,
                                "add": self.add,
                                "delete":self.delete
        }
           
    def execute(self, instruction):
        function = instruction.args.pop(0)
        event = None
        for key in self.function_parser:
            if function == key:
                event = self.function_parser[key](instruction)
                break
        if not event is None:        
            return (instruction.time, event)
        
    def reset(self,instruction):
        return RouteReset(instruction.time, *instruction.args)
    
    def add(self, instruction):
        if len(instruction.args)!=5:
            raise Exception("Faltan argumentos")
        return RouteAdd(instruction.time, *instruction.args)
    
    def delete(self, instruction):
        if len(instruction.args)!=5:
            raise Exception("Faltan argumentos")        
        return RouteDelete(instruction.time, *instruction.args)