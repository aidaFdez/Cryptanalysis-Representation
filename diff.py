# Pattern matching library
import re
import sys
import tkinter as tk


# Compute the Differential Distribution Table
def diffDistTable(sbox):
    for i in range(len(sbox)):
        sbox[i] = int(sbox[i])
    # print("segundo")
    # print(sbox)
    ddt = [[0 for col in range(16)] for row in range(16)]
    for w in range(len(sbox)):
        for i in range(len(sbox)):
            j = i ^ w
            # Get the corresponding sbox values
            a = sbox[i]
            b = sbox[j]
            # Get the difference from the sbox values
            c = a ^ b
            ddt[w][c] = ddt[w][c] + 1
    return ddt


def diffTrail(sbox, data, ddt, pbox, rounds):
    # print("The data is ", data)
    # Get the data in numbers
    # str = getInts(data)
    # Populate the trail changes, calculate the most probable transformation.
    trail = []
    # Keep the probability of the round respect the previous one
    probabilities = []
    general_prob = 1
    r = 0
    svalues = []
    over_prob = False
    # general_prob >= 2**(-16)
    #trail.append(getInts(data))
    while (not over_prob):

        # for r in range(rounds):
        # print("In round ", r)
        # If it is the first round, do it from the input
        if r == 0:
            prob = 1
            #trail.append(getInts(data))
            vals, prob = doSbox(getInts(data), prob, ddt)

            # add the vals to the svalues, so to have the values of each s box
            svalues.append(vals)
            # Need to apply the permutation to the values:
            swapped = pBoxSwaps(pbox, vals)
            # print(swapped, " Values after swapping")
            trail.append(swapped)
            # Save the probability of this round
            probabilities.append(prob)
            general_prob = general_prob * prob
        # If it is not the first round, do it from what was left before
        else:
            #vals = []
            prob = 1
            # Same as before, but taking the previous ones as base
            vals, prob = doSbox(trail[r-1], prob, ddt)
            # add the vals to the svalues, so to have the values of each s box
            svalues.append(vals)
            swapped = pBoxSwaps(pbox, vals)
            # print("values are ", vals)
            # Save the probability of this round
            probabilities.append(prob)
            if (general_prob * prob <= 2 ** (-16)):
                over_prob = True
            else:
                general_prob = general_prob * prob
                trail.append(swapped)
        r = r + 1
    return trail, probabilities, general_prob, svalues


# Do the swaps according to the pBox
def pBoxSwaps(pBox, input):
    # print("************Entered PBOX*********")
    output = []
    # Get the binary values of the input difference
    for ch in input:
        output.extend(getBinary(ch))
    bin_output = [0] * len(pBox)
    # Do the swaps
    for n in range(int(len(pBox))):
        # print(len(pBox))
        # print(n)
        # print(pBox[n], "position of pbox")
        bin_output[pBox[n]] = output[n]
    new_diff = []
    # That division should be the number of bits of the thingy
    for r in range(len(input)):
        num = []
        num.append(bin_output[r * 4])
        num.append(bin_output[r * 4 + 1])
        num.append(bin_output[r * 4 + 2])
        num.append(bin_output[(r * 4) + 3])
        # print("num is ", num)
        new_diff.extend(fromBinary(num))
    # print("************Exiting PBOX*********")

    # print(new_diff, " extended -------------------------------")
    return new_diff




# Get the highest probability of a value
def highProb(input, ddt):
    # Probability of the highest found until now
    prob = 0
    # Value of the highest probability
    num = 0
    bin_input = getBinary(input)
    # Counter to keep track of the iteration we are in
    numCount = 0
    for value in ddt[input]:
        # Hamming heuristic
        if (value == prob):
            # Add all the numbers, the shortest one has less 0s
            valCounter =getBinary(value)
            numCounter = getBinary(num)
            valequal = 0
            numequal = 0
            # count how many are different
            for i in range(len(bin_input)):
                if not (valCounter[i] == bin_input[i]):
                    valequal += 1
                if not (numCounter[i] == bin_input[i]):
                    numequal += 1
            # If the value is smaller, then get that
            if (valCounter < numCounter):
                prob = value
                num = numCount
            # print("After ", num, " ", prob)

        if (value > prob):
            # If the value is bigger than the one before, then keep that one in mind
            prob = value
            num = numCount
        # Keep track of the iteration we are in
        numCount = numCount + 1
    # print("***** Changed ", input, " to ", num)
    # Return the index of the most probable, ie: the one it gets substituted for
    return num, prob

def doSbox(strg, prob, ddt):
    vals = []
    if( (type(strg) is str)):
        strg = getInts(strg)
    if(type(strg) == int):
        value, probability = highProb(strg, ddt)
        # Save the trail value
        vals.append(value)
        # Update the probability of that specific trail
        prob = prob * (probability / 16)
    else:
        for val in range(len(strg)):
            # print(type(val))
            value, probability = highProb(strg[val], ddt)
            # Save the trail value
            vals.append(value)
            # Update the probability of that specific trail
            prob = prob * (probability / 16)
    return vals, prob

# Get the integer related to the input
def getInts(str):
    # Pattern of the input
    pattern = re.compile("([abcdefABCDEF][0-9])*")
    nums = []
    if pattern.match(str):
        for c in str:
            # print(c)
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
    else:
        nums.append(9999)
    return nums
def getBinary(c):
    #print(c, " is the received")
    if (c == 0): return [0, 0, 0, 0]
    if (c == 1): return [1, 0, 0, 0]
    if (c == 2): return [0, 1, 0, 0]
    if (c == 3): return [1, 1, 0, 0]
    if (c == 4): return [0, 0, 1, 0]
    if (c == 5): return [1, 0, 1, 0]
    if (c == 6): return [0, 1, 1, 0]
    if (c == 7): return [1, 1, 1, 0]
    if (c == 8): return [0, 0, 0, 1]
    if (c == 9): return [1, 0, 0, 1]
    if (c == 10 or c == 'A'): return [0, 1, 0, 1]
    if (c == 11 or c == 'B'): return [1, 1, 0, 1]
    if (c == 12 or c == 'C'): return [0, 0, 1, 1]
    if (c == 13 or c == 'D'): return [1, 0, 1, 1]
    if (c == 14 or c == 'E'): return [0, 1, 1, 1]
    if (c == 15 or c == 'F'): return [1, 1, 1, 1]
    else:
        try:
            sys.exit(0)
        except SystemExit:
            print("The numbers were not correct, so no match could be found")


def fromBinary(c):
    # print(c)
    if (c == [0, 0, 0, 0]): return [0]
    if (c == [1, 0, 0, 0]): return [1]
    if (c == [0, 1, 0, 0]): return [2]
    if (c == [1, 1, 0, 0]): return [3]
    if (c == [0, 0, 1, 0]): return [4]
    if (c == [1, 0, 1, 0]): return [5]
    if (c == [0, 1, 1, 0]): return [6]
    if (c == [1, 1, 1, 0]): return [7]
    if (c == [0, 0, 0, 1]): return [8]
    if (c == [1, 0, 0, 1]): return [9]
    if (c == [0, 1, 0, 1]): return [10]
    if (c == [1, 1, 0, 1]): return [11]
    if (c == [0, 0, 1, 1]): return [12]
    if (c == [1, 0, 1, 1]): return [13]
    if (c == [0, 1, 1, 1]): return [14]
    if (c == [1, 1, 1, 1]): return [15]


def vals_string(vals):
    # print("********************************")
    # print(vals)
    stn = "["
    sep = ""
    for val in vals:
        # print(val)
        stn = stn + sep
        sep = ","
        stn = stn + str(val)
    stn = stn + "]"
    return stn


def popup(title, msg):
    popup = tk.Tk()
    popup.wm_title(title)
    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    # B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    # B1.pack()
    var = tk.IntVar()
    button = tk.Button(popup, text="Click Me", command=lambda: var.set(1))
    button.pack()

    # print("waiting...")
    button.wait_variable(var)
    # print("done waiting.")
# ("You chose " + str(numOfRounds) + " but it is efficient to calculate up to " + str(len(trail)) + ", so this was used")

# TODO boton de cambiar, cambios simples,
# Hecho mirar las flechas,Log 2, complejidad (opuesto probabilidad) seria nº textos elegidos necesarios, total probabilidad acumulada
