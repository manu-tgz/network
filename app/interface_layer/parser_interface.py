from app.tools.file import   get_line_txt

class Intruction:
    """25 create host c1
      time: 25 , function:create, args: [host, c1]
    """
    def __init__(self, time:int, function, args): 
        self.time=time
        self.function = function
        self.args = args
    
class Parser:
    parsers = {}
    parser_class = None
    
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
            result.append(self.get_intructions(line.split(" ")))                  
        return result
    
    def save_data(self,file_name, devices):
        pass

    def get_intructions(self,words):
        result = self.intrucciones(words)
        if result is None and not self.parser_class is None:
            return self.parser_class().get_intructions(words)
        return result
    
    def intrucciones(self,words):
        intruccion = Intruction(int(words[0]), words[1], words[2:])

        for key in self.parsers:
            if intruccion.function == key:
                return self.parsers[key].execute(intruccion)