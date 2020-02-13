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

def diffTrail(sbox, data, ddt):
    #Get the data in numbers
    str = getInts(data)
    """#Transform based on s-box
    transformed = []
    for c in str:
        transformed.append(sbox[c])"""
    #Populate the trail changes, calculate the most probable transformation
    trail = []
    for val in str:
        print(val, " has match ", highProb(val, ddt))
        trail.append(highProb(val, ddt))
    return trail

#Do the swaps according to the pBox
def pBoxSwaps(pBox, input):
    output = ""
    for ch in input:
        output += getBinary(ch)
    print("Output is ", output)
    for n in range(len(pBox)):
        return
    return output

def getBinary(inp):
    if (c == '0'): return "0000"
    if (c == '1'): return "1000"
    if (c == '2'): return "0100"
    if (c == '3'): return "1100"
    if (c == '4'): return "0010"
    if (c == '5'): return "1010"
    if (c == '6'): return "0110"
    if (c == '7'): return "1110"
    if (c == '8'): return "0001"
    if (c == '9'): return "1001"
    if (c == 'a' or c == 'A'): return "0101"
    if (c == 'b' or c == 'B'): return "1101"
    if (c == 'c' or c == 'C'): return "0011"
    if (c == 'd' or c == 'D'): return "1011"
    if (c == 'e' or c == 'E'): return "0111"
    if (c == 'f' or c == 'F'): return "1111"

#Get the highest probability of a value
def highProb(input, ddt):
    #Probability of the highest found until now
    prob = 0
    #Value of the highest probability
    num = 0
    #Counter to keep track of the iteration we are in
    numCount = 0
    for value in ddt[input]:
        if (value > prob):
            #If the value is bigger than the one before, then keep that one in mind
            prob = value
            num = numCount
        #Keep track of the iteration we are in
        numCount = numCount+1
    #Return the index of the most probable, ie: the one it gets substituted for
    return num

#Get the integer related to the input
def getInts(str):
    #Pattern of the input
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
