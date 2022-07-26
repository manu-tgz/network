def convert_ip_to_bits_line(ip : str):
    return "".join(convert_ip_to_bits(ip)) 

def dec_to_bits(number :int):
    b = bin(number)[2:]
    return "0"*(8 - len(b)) + b

def convert_ip_to_bits(ip :str):
    return [ dec_to_bits(int(n)) for n in ip.split(".") ] 

def convert_bits_line_to_ip(bits : str):
    if len(bits) != 32 : raise Exception("Wrong ip length, must have 32 bits.")

    sol = [] 
    for i in range(4):
        sol.append( str(int( bits[i*8:(i+1)*8], 2)) )     
    
    return ".".join(sol)

def bits_and_bits(bits1 : str, bits2 :str):
    sol = ""
    for i in range(4):
        n1 = int(bits1[i*8:(i+1)*8],2)
        n2 = int(bits2[i*8:(i+1)*8],2)
        sol += dec_to_bits(n1 & n2) 
    return sol