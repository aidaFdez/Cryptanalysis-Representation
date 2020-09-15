
import time
from sage.crypto.sbox import SBox
#Compute the Differential Distribution Table
def diffDistTable(sbox):
    #print("Primero")
    #print(sbox)
    for i in range(len(sbox)):
        sbox[i] = int(sbox[i])
    #print("segundo")
    #print(sbox)
    ddt = [[0 for col in range(len(sbox))] for row in range(len(sbox))]
    for w in range(len(sbox)):
        for i in range(len(sbox)):
            j = i^w
            #Get the corresponding sbox values
            a = sbox[i]
            b = sbox[j]
            #Get the difference from the sbox values
            c = a^b
            ddt[w][c] = ddt[w][c]+1
    return ddt

def test():
    wrong = 0
    timesMine = []
    timesSage = []
    #Do this 1000 times
    for counter in range(100000):
        #Get a random permutation of
        perm =  Permutations(16).random_element()
        #perm is in range [1,16] and we need it in [0,15]
        sBox = [x-1 for x in perm]

        startMine = time.time()
        ddtMine = diffDistTable(sBox)
        endMine = time.time()
        timeMine = endMine - startMine
        timesMine.append(timeMine)

        sb = SBox(sBox)
        startSage = time.time()
        ddtSage = sb.difference_distribution_table()
        endSage = time.time()
        timeSage = endSage - startSage
        timesSage.append(timeSage)

        bool = True
        for i in range(16):
            for j in range(16):
                #print(ddtMine[i][j], " vs ",  ddtSage[i][j])
                if not (ddtMine[i][j] == ddtSage[i][j]):
                    bool = False
        #If there was one wrong, record the mistake
        if(bool == False):
            wrong = wrong +1
    avgMine = sum(timesMine)/len(timesMine)
    avgSage = sum(timesSage)/len(timesSage)
    varMine = sum((i - avgMine) ** 2 for i in timesMine) / len(timesMine)
    varSage = sum((i - avgSage) ** 2 for i in timesSage) / len(timesSage)
    #print(sum(timesMine[:10])/10)
    #print(sum(timesSage[:10])/10)
    return wrong, avgMine, avgSage, varMine, varSage


if __name__ == '__main__':
    num, avgMine, avgSage, varMine, varSage = test()
    print(num, " were wrong")
    print(avgMine, " is the average time for my algorithm")
    print(avgSage, " is the average time for Sage's algorithm")
    print(varMine, " is the variance for my algorithm")
    print(varSage, " is the variance for Sage's algorithm")
    print(avgMine-avgSage, " is the difference of averages")
