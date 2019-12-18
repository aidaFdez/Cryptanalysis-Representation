#Compute the Differential Distribution Table
def diffDistTable(sbox):
    #print("Primero")
    #print(sbox)
    for i in range(len(sbox)):
        sbox[i] = int(sbox[i])
    #print("segundo")
    #print(sbox)
    ddt = [[0 for col in range(16)] for row in range(16)]
    for w in range(16):
        for i in range(16):
            j = i^w
            #Get the corresponding sbox values
            a = sbox[i]
            b = sbox[j]
            #Get the difference from the sbox values
            c = a^b
            ddt[w][c] = ddt[w][c]+1
    return ddt
