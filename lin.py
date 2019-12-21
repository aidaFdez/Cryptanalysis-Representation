#  Compute the Linear Approximation table
def linApptable(sbox):
    size = len(sbox)
    for i in range(size):
        sbox[i] = int(sbox[i])
    lat = [[0 for col in range(size)] for row in range(size)]
    #  input mask
    for x in range(size):
        #  output mask
        for y in range(size):
            total = 0
            # for all inputs i
            for i in range(size):


                masked_input = i * x
                masked_output = sbox[i] * y

                #  check if they produce the same result
                if (masked_input == masked_output):
                    lat[x][y] += 1
    return lat
