import math

#  Compute the Linear Approximation table
def linApptable(sbox):
    size = len(sbox)
    for i in range(size):
        sbox[i] = int(sbox[i])
    lat = [[0 for col in range(size)] for row in range(size)]
    #  input mask
    for row in range(size):
        #if((row != 1)):
            #assert(1==0)
        #    continue
        #  output mask
        for col in range(size):
            #if((col != 1)):
            #    continue
            # for all inputs i
            #assert(row == 1)
            #assert(col == 1)
            for x in range(size):

                masked_input = parity(row & x)
            
                masked_output = parity(col & sbox[x])

                #  check if they produce the same result
                if (masked_input == masked_output):
                    lat[row][col] += 1
    corrolation(lat,size)
    return lat

def parity(i):
    i = i - ((i >> 1) & 0x55555555)
    i = (i & 0x33333333) + ((i >> 2) & 0x33333333)
    i = (((i + (i >> 4)) & 0x0F0F0F0F) * 0x01010101) >> 24
    return int(i % 2)

def corrolation(lat,size):
    #  input mask
    for row in range(size):
        #if((row != 1)):
            #assert(1==0)
        #    continue
        #  output mask
        for col in range(size):
            lat[row][col] = (2*lat[row][col]/size)-1