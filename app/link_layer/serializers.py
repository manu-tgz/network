from math import ceil
from app.tools.bits import format_8bit, sum_bytes

class FrameSerializer:
    """
                                  TRAMA
    |   16 bits  |  16 bits    |  8 bits   |  8 bits    |      |            |
    |------------|-------------|-----------|------------|------|------------|
    | MAC_source | MAC_receive | data_size | check_size | data | check_data |
    """
    def serializer_frame(host_MAC, MAC, data):

        MAC_source = bin(int(host_MAC,16))[2:]
        MAC_receive = bin(int(MAC,16))[2:]  
        
        num = ceil((len(data)/2))
        data_size = format_8bit(bin(num)[2:],1)
        
        check = bin(sum_bytes(data))[2:]
        check_num = ceil(len(check)/8)
        check_size = format_8bit(bin(check_num)[2:],1)
        
        data_bin = bin(int(data,16))[2:]
        data =format_8bit(data_bin,num)
        
        check_data= format_8bit(check,check_num)
        
        return MAC_receive + MAC_source + data_size + check_size + data + check_data
    
    def deserializer_frame(frame):
        result = {}
        result["MAC_receive"] = hex(int(frame[0:16] ,2))[2:].upper()
        result["MAC_source"] = hex(int(frame[16:32] ,2))[2:].upper()
        
        result["data_size"] = data_size =  8 * int(frame[32:40],2) 
        result["check_size"] = check_size =8 * int(frame[40:48],2)
        result["data"] = hex(int(frame[48:48+data_size] ,2))[2:].upper()   
        result["check_data"]= frame[48+data_size:48+data_size+check_size]
        
        return result
        
    def firts_var(frame):
        """Reeturn MAC that receives"""
        return hex(int(frame[0:16] ,2))[2:].upper()
    
    def frame_error(check_data, data):
        return check_data != format_8bit(bin(sum_bytes(data))[2:],2)