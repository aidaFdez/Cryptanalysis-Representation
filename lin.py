import math

#  Compute the Linear Approximation table
def linApptable(sbox):
    size = len(sbox)
    for i in range(size):
        sbox[i] = int(sbox[i])
    lat = [[0 for col in range(size)] for row in range(size)]
    #  input mask
    for row in range(size):
        #  output mask
        for col in range(size):
            for x in range(size):

                masked_input = parity(row & x)
            
                masked_output = parity(col & sbox[x])

                #  check if they produce the same result
                if (masked_input == masked_output):
                    lat[row][col] += 1
    correlation(lat, size)
    return lat

# Hamming weight
def parity(i):
    i = i - ((i >> 1) & 0x55555555)
    i = (i & 0x33333333) + ((i >> 2) & 0x33333333)
    i = (((i + (i >> 4)) & 0x0F0F0F0F) * 0x01010101) >> 24
    return int(i % 2)

def correlation(lat,size):
    #  input mask
    for row in range(size):
        #  output mask
        for col in range(size):
            lat[row][col] = (2*lat[row][col]/size)-1

def linTrail(noOfSbox, maskString, lat):
    mask = [maskString[i:i+noOfSbox] for i in range (0, len(maskString), noOfSbox)]
    total_corr = 1
    signed_cor = 1
    newMask = []
    sBoxCorr = []
    for num in mask:
        n = int(num,2)
        maxCorr = 0
        output = 16
        for x in range(noOfSbox*4):
            if abs(lat[n][x]) > maxCorr:
                maxCorr = abs(lat[n][x])
                signed_cor = lat[n][x]
                output = x
            elif abs(lat[n][x]) == maxCorr and x < output:
                output = x
                signed_cor = lat[n][x]
        sBoxCorr.append(math.log(maxCorr, 2.0))
        total_corr = total_corr*signed_cor
        #convert to log base 2
        total_corr_base_2 = math.log(abs(total_corr), 2.0)
        newMask.append(output)
    return total_corr_base_2, newMask, sBoxCorr
    






