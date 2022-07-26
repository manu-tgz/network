from app.tools.ip import *

class IpAddress:
    def __init__(self, string : str, format="ip"):
        if format == "ip":
            self.ip_num = string
        elif format == "bin": 
            self.ip_num = convert_bits_line_to_ip(string)
        else : raise Exception("Formato de ip indistinguible.")

    @property
    def get_bits(self):
        return convert_ip_to_bits_line(self.ip_num)
    
    def __str__(self):
        return self.ip_num
    def __repr__(self):
        return "IPADDRESS:(" + self.ip_num+")"
     
    
    def __eq__(self, o):
        return self.ip_num == o.ip_num

    def get_subnet(self, subnet_mask):
        return IpAddress(self.get_subnet_bits(subnet_mask), "bin" )
    
    def get_broadcast(self, subnet_mask):
        return convert_bits_line_to_ip(self.get_broadcast_bits(subnet_mask)) 

    def get_broadcast_bits(self, subnet_mask):
        line=self.get_subnet_bits(subnet_mask) 
        sol = list(line) 
        i = 1
        while sol[-i] == "0":
            sol[-i] = "1"
            i+=1
        return "".join(sol) 

    def get_subnet_bits(self,subnet_mask):
        return bits_and_bits(self.get_bits, subnet_mask.get_bits)