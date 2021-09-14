# file to try to get numbers in binary, hexadecimal and decimal

# From decimal to binary
def to_bin(n):
   bin = format(n, 'b')
   print(bin)
   return bin


def to_hex(n):
    hexdec = format(n, 'X')
    print(hexdec)
    return hexdec


def bin_to_dec(n):
    dec = format(int(n, 2), 'd')
    print(dec)
    return dec


def hex_to_dec(n):
    dec = int(n, 16)
    print(dec)
    return dec


def sbox_values(b):
    first = str(b[0])+str(b[5])
    second = str(b[1])+str(b[2])+str(b[3])+str(b[4])
    first = bin_to_dec(first)
    second = bin_to_dec(second)
    return first, second


