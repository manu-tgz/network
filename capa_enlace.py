from shutil import ExecError
from herramientas import buscar_mac

class ControladorRed:
    pass


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


class PC:
    def __init__(self,nombre):
        self.nombre = nombre 
        self.mac = ''
        self.buffer = ''
        self.puertos = [] 
        self.transmision_actual = None
        self.transmision_recibida = None
        self.add_puerto(Puerto(self))    

    def set_mac(self, mac):
        self.mac = mac

    def add_puerto(self, puerto:Puerto):
        if len(self.puertos) == 1:
            Exception("La PC tiene un solo puerto")        
            return
        self.puerto.append(puerto)
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
        self.buffer += str(dato)
        self.transmision_recibida = dato

    def enviar_dato(self,dato):
        self.puertos[0].enviar_dato(dato)

    def desconectar(self):
        self.puertos.cable.desconectar()
    
    def reset_buffer(self):
        self.buffer = ''
        self.comprobar_mac(self)
    
    def comprobar_mac(self):
        # aqui hay que analizar que paso con la mac y el hash que llega.... 
        # este metodo se pide una vez se termine de enviar una trama, se pide en realidad reset_buffer
        # el cual llama a este metodo... En este metodo se detecta si hubo o no una colision, debes decidir que hacer
        # con ello... Pero si el hash da mal pues hubo colision, puedes decir que hay colision y error en ese caso
        pass

class Hub:
    def __init__(self,nombre,cantidad_puertos):
        self.cantidad_puertos = cantidad_puertos 
        self.nombre = nombre 
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

class Switch:
    def __init__(self,nombre,cantidad_puertos):
        self.cantidad_puertos = cantidad_puertos 
        self.nombre = nombre 
        self.puertos = [] 
        self.transmision_actual = None
        self.transmision_recibida = None
        self.mac = [ [] for _ in range(cantidad_puertos) ] #new
        self.add_todos_los_puertos()
        self.buffer = None

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
    
    def posicion_puerto(self, puerto):
        for i in range(len(self.puertos)):
            if puerto== self.puertos[i] : return i
        return -1    

    def get_transmision_dato(self, dato, puerto):
        self.transmision_recibida = dato
        
        # Este buffer se va llenando segun le llegan datos, segun el resultado de su buffer segun lo que envia
        #la trama bit a bit, cuando el buffer llega a 32 guarda la mac del dispositivo que envia(16:32), y cu
        if len(self.buffer) < 32:
            self.buffer += str(dato)
        
        if len(self.buffer) == 32:
            self.mac[self.posicion_puerto(puerto)].append(self.buffer[16:32])

        if len(self.buffer)>=16 :    
            mac_buscada = buscar_mac(self.buffer[0:16],self.macs)
        else:
            self.enviar_datos(dato,puerto)
            return
        # Si la mac a la que se debe enviar existe en los registros del switch, solo envia a la misma,
        #de lo contrario envia a todas mientras tanto, ergo los 1ros 16 bits los envia a todos los 
        #dispositivos conectados.
        if(mac_buscada[0]):
            self.puertos[mac_buscada[1]].enviar_dato(dato)
        else:    
            self.enviar_datos(dato,puerto)
        
    def enviar_datos(self,dato,puerto_negado):
        for puerto in self.puertos:
            if puerto != puerto_negado and puerto.desconectado == False:
                puerto.enviar_dato(dato)


