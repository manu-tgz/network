# class Hub(Device):
#     def __init__(self,name,amount_ports):
#         super().__init__(name)
#         self.amount_ports = int(amount_ports) 
#         self.ports = null_list(amount_ports)
#         self.transmision_actual = None
#         self.transmision_recibida = None

#     def connect(self, ethernet, port):
#         if not self.ports[port] is None: raise Exception("The port {} is not avaible.")
#         super().connect(ethernet, port)    

#     def get_transmision_dato(self, dato, puerto):
#         self.transmision_recibida = dato
#         self.enviar_datos(dato,puerto) #no reenvia a enviar por el puerto que recibe

#     def enviar_datos(self,dato,puerto_negado):
#         for puerto in self.puertos:
#             if puerto != puerto_negado and puerto.desconectado == False:
#                 puerto.enviar_dato(dato)

# class PC(Device):
#     def __init__(self,name):
#         super().__init__(name)
#         self.ports = [None] 
#         self.transmision_actual = None
#         self.transmision_recibida = None

#     def connect(self, ethernet, port):
#         if port != 0: raise Exception("Los host solo tienen el puerto 1.")
#         super().connect(ethernet, port)

#     def desconectar(self):
#         self.puerto.ethernet.desconectar(self.puerto)

#     def get_transmision_dato(self, dato, puerto):
#         self.transmision_recibida = dato

#     def enviar_dato(self,dato):
#         self.puertos[0].enviar_dato(dato)

#     def desconectar(self):
#         self.puertos.ethernet.desconectar()