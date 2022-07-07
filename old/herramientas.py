def buscar_mac(mac,macs):
    for puerto in range(len(macs)):
        for direccion in range (len(macs[puerto])):
            if mac == macs[puerto][direccion]:
                return True, puerto
    return False, None  

def send_frame(host, MAC, data):
    '''Envia la data de un host al que se desea o a todos en caso de que no este definida la MAC 
    a la cual se desea enviar la info, crea la trama con la informacion dada y la envia bit a bit.
    Una vez termina de enviar la trama limpia los buffers de los dispositivos.
    Esta funcion ejecuta la instruccion: <time> send_frame <host> <mac destino> <data> '''
    pass
    # bites = frame(host, MAC, data)
    # time = Env.current_env.time
    # for i in range(len(bites)):
    #     Env.current_env.add_action(time,link_layer_send_event(time,host.name,bites[i], is_last_bit=False if i!=len(bites)-1 else True))  
    #     time+=Env.current_env.signal_time

def frame(host, MAC, data):
    # aqui hay que crear la trama, es algo trivial, hay que escribir bastante pero es una talla sencilla jeje...
    #en el pdf se explica bien como esta conformada una trama(frame)...
    pass