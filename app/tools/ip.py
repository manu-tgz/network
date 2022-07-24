def convert_bits_line_to_ip(bits : str):
    if len(bits) != 32 : raise Exception("Wrong ip length, must have 32 bits.")

    sol = [] 
    for i in range(4):
        sol.append( str(int( bits[i*8:(i+1)*8], 2)) )     
    
    return ".".join(sol)