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
            total = 0
            # for all inputs i
            for x in range(size):


                masked_input = row ^ x
                masked_output = col ^ int(sbox[x])
                print(masked_input)
                print(masked_output)

                #  check if they produce the same result
                if (masked_input == masked_output):
                    lat[row][col] += 1
    return lat
