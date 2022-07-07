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