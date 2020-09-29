#file to try to get numbers in binary, hexadecimal and decimal

#From decimal to binary
def to_bin(n):
   bin = format(n, 'b')
   print(bin)
   return bin

def to_hex(n):
    hex = format(n, 'X')
    print(hex)
    return hex

def bin_to_dec(n):
    dec = format(int(n, 2), 'd')
    print(dec)
    return dec

def hex_to_dec(n):
    dec = int(n, 16)
    print(dec)
    return dec


