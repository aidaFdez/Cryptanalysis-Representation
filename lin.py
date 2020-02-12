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
        #  output mask
        for col in range(size):
            lat[row][col] = (2*lat[row][col]/size)-1

def linTrail(noOfSbox, maskString, lat):
    mask = [maskString[i:i+noOfSbox] for i in range (0, len(maskString), noOfSbox)]
    total_corr = 1
    newMask = []
    for num in mask:
        n = int(num,2)
        maxCorr = 0
        output = 16
        for x in range(noOfSbox*4):
            if abs(lat[n][x]) > maxCorr:
                #print(num,x,output, maxCorr)
                maxCorr = abs(lat[n][x])
                output = x
            elif abs(lat[n][x]) == maxCorr and x < output:
                #print(num,x,output)
                output = x
        total_corr = total_corr*maxCorr
        
        newMask.append(output)
    return total_corr, newMask
    
        #implement for multiple rounds 
            
        #print relevant things and format

        #stop prop





