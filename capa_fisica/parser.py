from .devices import Hub, PC
from .physical import CreateDevice

class Intruccion:
    """25 create host c1
      time: 25 , function:create, args: [host, c1]
    """
    def __init__(self, time:int, function, args): 
        self.time=time
        self.function = function
        self.args = args
        
def parser(lines):
    """Parsear las lines

    Args:
        lines (list): line from txt file
    """
    result=[]
    for line in lines:
        result.append(intrucciones(line.split(" ")))                  
    return result
    
def intrucciones(words):
    
    intruccion = Intruccion(int(words[0]), words[1], words[2:])
    
    if intruccion.function == "create":
        return Create_Parser.execute(intruccion)
    # elif intruccion.function == "connect":
    #     return parse_connect(intruccion)
    # elif intruccion.function == "send":
    #     return parse_send(intruccion )
    # elif intruccion.function == "disconnect":
    #     return parse_disconnect(intruccion )
    else:
        raise Exception("Comando no encontrado pruebe  'create', 'connect', 'send', 'disconnect'.")

class Create_Parser():
    
    def execute(intruccion):
        device = intruccion.args.pop(0)

        if device == "hub":
            values= Create_Parser.hub_parser(intruccion) 
        elif device == "host":
            values= Create_Parser.host_parser(intruccion) 
        else:
            raise Exception("Dispositivo no encontrado pruebe 'hub','host'.") 
        
        return CreateDevice(*values)
       
    def hub_parser(intruccion):
        return [intruccion.time, Hub, [intruccion.args[0], intruccion.args[1]]]  
    
    def host_parser(intruccion):
        return [intruccion.time, PC, [intruccion.args[0]]]        
  