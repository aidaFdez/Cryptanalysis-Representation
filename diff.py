#Pattern matching library
import re

#Compute the Differential Distribution Table
def diffDistTable(sbox):
    #print("Primero")
    #print(sbox)
    for i in range(len(sbox)):
        sbox[i] = int(sbox[i])
    #print("segundo")
    #print(sbox)
    ddt = [[0 for col in range(16)] for row in range(16)]
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

def diffTrail(sbox, data):
    #Get the data in numbers
    str = getInts(data)
    #Transform based on s-box
    transformed = []
    for c in str:
        transformed.append(sbox[c])
    #Populate the trail changes, calculate the most probable transformation
    trail = []
    return trail


def getInts(str):
    pattern = re.compile("([abcdefABCDEF][0-9])*")
    nums = []
    if pattern.match(str):
        for c in str:
            print(c)
            if (c == '0'): nums.append(0)
            if (c == '1'): nums.append(1)
            if (c == '2'): nums.append(2)
            if (c == '3'): nums.append(3)
            if (c == '4'): nums.append(4)
            if (c == '5'): nums.append(5)
            if (c == '6'): nums.append(6)
            if (c == '7'): nums.append(7)
            if (c == '8'): nums.append(8)
            if (c == '9'): nums.append(9)
            if (c == 'a' or c == 'A'): nums.append(10)
            if (c == 'b' or c == 'B'): nums.append(11)
            if (c == 'c' or c == 'C'): nums.append(12)
            if (c == 'd' or c == 'D'): nums.append(13)
            if (c == 'e' or c == 'E'): nums.append(14)
            if (c == 'f' or c == 'F'): nums.append(15)
    else: nums.append(9999)
    return nums

#TODO Divide the input, so it has the correct sizes. How do we pad the ones that are not long enough?

#TODO Each arrow can show the difference probability when clicked? Show as a table with what difference before and difference afterwards

#TODO Understand how to use the outut in more than one round
