from capa_fisica.physical import Log

class Device:
    def __init__(self,name): 
        self.log = Log()
        self.name = name 

class Cable:
    def __init__(self,puerto1,puerto2):
        self.puerto1 = puerto1
        self.puerto2 = puerto2
        puerto1.cable = self
        puerto2.cable = self
    
    def enviar_informacion(self,dato,puerto_enviando):
        if puerto_enviando == self.puerto1:
            self.puerto2.recibir_dato(dato)
        else:
            self.puerto1.recibir_dato(dato)

    def desconectar(self):
        self.puerto1.cable = None
        self.puerto2.cable = None


class Puerto:
    def __init__(self,dispositivo):
        self.dispositivo = dispositivo
        self.cable = None
    
    def conectar(self,puerto):
        Cable(self,puerto)
    
    def recibir_dato(self, dato):
        self.dispositivo.get_transmision_dato(dato,self)

    def enviar_dato(self, dato):
        self.cable.enviar_dato(dato,self)
    
    def desconectado(self):
        return self.cable == None


class PC(Device):
    def __init__(self,name):
        super().__init__(name)
        self.puertos = [] 
        self.transmision_actual = None
        self.transmision_recibida = None
        self.add_puerto(Puerto(self))    

    def add_puerto(self, puerto:Puerto):
        if len(self.puertos) == 1:
            Exception("La PC tiene un solo puerto")        
            return
        self.puertos.append(puerto)
        puerto.dispositivo = self

    def conectar(self, dispositivo):
        for puerto in dispositivo.puertos:
            if puerto.desconectado():
                self.puerto.conectar(puerto)
                return
        Exception("El dispositivo a conectarse no tiene puertos disponibles")        

    def desconectar(self):
        self.puerto.cable.desconectar(self.puerto)

    def get_transmision_dato(self, dato, puerto):
        self.transmision_recibida = dato

    def enviar_dato(self,dato):
        self.puertos[0].enviar_dato(dato)

    def desconectar(self):
        self.puertos.cable.desconectar()

class Hub(Device):
    def __init__(self,name,cantidad_puertos):
        super().__init__(name)
        self.cantidad_puertos = int(cantidad_puertos) 
        self.puertos = [] 
        self.transmision_actual = None
        self.transmision_recibida = None
        self.add_todos_los_puertos()

    def add_puerto(self, puerto:Puerto):
        if len(self.puertos) >= self.cantidad_puertos:
            Exception("Se alcanzo el limite de puertos en el Hub")        
            return
        self.puertos.append(puerto)
        puerto.dispositivo = self
    
    def add_todos_los_puertos(self):
        for i in range (self.cantidad_puertos):
            self.add_puerto(Puerto(self))

    def conectar(self, dispositivo):
        for puerto in dispositivo.puertos:
            if puerto.desconectado():
                self.puerto.conectar(puerto)
                return
        Exception("El dispositivo a conectarse no tiene puertos disponibles")        

    def get_transmision_dato(self, dato, puerto):
        self.transmision_recibida = dato
        self.enviar_datos(dato,puerto) #no reenvia a enviar por el puerto que recibe

    def enviar_datos(self,dato,puerto_negado):
        for puerto in self.puertos:
            if puerto != puerto_negado and puerto.desconectado == False:
                puerto.enviar_dato(dato)
