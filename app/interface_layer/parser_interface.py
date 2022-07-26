from app.tools.file import   get_line_txt

class Instruction:
    """25 create host c1
      time: 25 , function:create, args: [host, c1]
    """
    def __init__(self, time:int, function, args): 
        self.time=time
        self.function = function
        self.args = args
    
class ABCParser:
    parsers = {}
    parser_class = None
    
    def get_commands_from_txt(self,file_name):
        lines = get_line_txt(file_name)
        return self.parser(lines) 
        
    def parser(self,lines):
        """Parsear las lines
        Args:
            lines (list): line from txt file
        Returns:
            list: Process list
        """

        result=[]
        for line in lines:
            result.append(self.get_intructions(line.split(" ")))                  
        return result
    
    def save_data(self,file_name, devices):
        pass

    def get_intructions(self,words):
        """
        Args:
            words (strings): son las palabras entradas en la linea del comando

        Returns:
            Process: el proceso a ejecutar
        """
        result = self.instructions(words)
        if result is None and not self.parser_class is None:
            return self.parser_class().get_intructions(words)
        return result
    
    def instructions(self,words):
        instruction = Instruction(int(words[0]), words[1], words[2:])

        for key in self.parsers:
            if instruction.function == key:
                return self.parsers[key].execute(instruction)    

class InstructionParser:
    def execute(instruction):
        pass