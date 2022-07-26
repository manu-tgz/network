import math

def format_8bit(bin_num, size):
    for i in range(8*size-len(bin_num)): bin_num = '0'+bin_num
    return bin_num

def sum_bytes(num):
    '''Convierte un h hexagesimal en sumatoria de sus respectivos bytes''' 
    if len(num)%2 !=0: num = '0'+ num
    result = 0 
    for b  in range(0,len(num),2):
        result+=int(num[b:b+2],16)
    return result

#region net
def hex_to_bin(h):
    return bin(int(h,16))[2:]

def bin_to_hex(b):
    return hex(int(b,2))[2:]

def dec_to_bits(number :int):
    b = bin(number)[2:]
    return "0"*(8 - len(b)) + b

def convert_chars_to_bits(string :str):
    return "".join( [ dec_to_bits(ord(c)) for c in string ] )
#endregion