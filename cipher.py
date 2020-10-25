import re
import sys
import tkinter as tk
import math

# Objects for linear and differential
class Cryptanalysis:
    # the inputs that visualise() takes. Here to check what needs to be part of the object
    # inputString, numOfBits, numOfRounds, sBoxes, sBox, pBox, type, first, tr, pbs, p_fin, svalues
    sbox = []
    pbox = []
    num_rounds = 0
    trail = []
    probabilities = []
    type =""
    input_string = ""

    # Initialise the cryptanalysis class
    def __init__(self, type, sbox, pbox, num_rounds):
        self.sbox = sbox
        self.pbox = pbox
        self.num_rounds = num_rounds
        self.type = type
        print(type, " created")

  ######################
  # DIFFERENTIAL CLASS #
  ######################

class Differential(Cryptanalysis):
    """Class for differential cryptanalysis. This inherits from the cryptanalysis class."""

    # Own variables
    ddt = [] # Difference Distribution Table

    # Initialise the differential class
    def __init__(self, sbox, pbox, num_rounds):
        # Call the super class initialiser
        super().__init__("Differential", sbox, pbox, num_rounds)
        Differential.calculate_ddt(self)

    # Get the Difference Distribution Table
    def calculate_ddt(self):
        for i in range(len(self.sbox)):
            self.sbox[i] = int(self.sbox[i])

        ddt = [[0 for col in range(16)] for row in range(16)]
        for w in range(len(self.sbox)):
            for i in range(len(self.sbox)):
                j = i ^ w
                # Get the corresponding sbox values
                a = self.sbox[i]
                b = self.sbox[j]
                # Get the difference from the sbox values
                c = a ^ b
                ddt[w][c] = ddt[w][c] + 1
        self.ddt = ddt

    def diff_trail(sbox, data, ddt, pbox, rounds):
        # Populate the trail changes, calculate the most probable transformation.
        trail = []
        # Keep the probability of the round respect the previous one
        probabilities = []
        general_prob = 1
        r = 0
        svalues = []
        over_prob = False
        while not over_prob:
            # If it is the first round, do it from the input
            if r == 0:
                prob = 1
                # trail.append(getInts(data))
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
                # vals = []
                prob = 1
                # Same as before, but taking the previous ones as base
                vals, prob = doSbox(trail[r - 1], prob, ddt)
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
    def p_box_swaps(self):
        # print("************Entered PBOX*********")
        output = []
        # Get the binary values of the input difference
        for ch in self.input_string:
            output.extend(getBinary(ch))
        bin_output = [0] * len(self.pbox)
        # Do the swaps
        for n in range(int(len(self.pbox))):
            # print(len(pBox))
            # print(n)
            # print(pBox[n], "position of pbox")
            bin_output[self.pbox[n]] = output[n]
        new_diff = []
        # That division should be the number of bits of the thingy
        for r in range(len(self.input_string)):
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




  ################
  # LINEAR CLASS #
  ################

class Linear(Cryptanalysis):
    #Own variables
    linear_approx_table = []

    # Initialise the linear class
    def __init__(self, sbox, pbox, num_rounds):
        # Call the super class initialiser
        super().__init__("Linear", sbox, pbox, num_rounds)

    def parity(self, i):
        i = i - ((i >> 1) & 0x55555555)
        i = (i & 0x33333333) + ((i >> 2) & 0x33333333)
        i = (((i + (i >> 4)) & 0x0F0F0F0F) * 0x01010101) >> 24
        return int(i % 2)

    def correlation(self, lat, size):
        #  input mask
        for row in range(size):
            #  output mask
            for col in range(size):
                lat[row][col] = (2 * lat[row][col] / size) - 1

    def linApptable(self, sbox):
        size = len(sbox)
        for i in range(size):
            sbox[i] = int(sbox[i])
        lat = [[0 for col in range(size)] for row in range(size)]
        #  input mask
        for row in range(size):
            #  output mask
            for col in range(size):
                for x in range(size):

                    masked_input = self.parity(row & x)

                    masked_output = self.parity(col & sbox[x])

                    #  check if they produce the same result
                    if (masked_input == masked_output):
                        lat[row][col] += 1
        self.correlation(lat, size)
        return lat


    def linTrail(self, noOfSbox, maskString, lat):
        mask = [maskString[i:i + noOfSbox] for i in range(0, len(maskString), noOfSbox)]
        total_corr = 1
        signed_cor = 1
        newMask = []
        sBoxCorr = []
        for num in mask:
            n = int(num, 2)
            maxCorr = 0
            output = 16
            for x in range(noOfSbox * 4):
                if abs(lat[n][x]) > maxCorr:
                    maxCorr = abs(lat[n][x])
                    signed_cor = lat[n][x]
                    output = x
                elif abs(lat[n][x]) == maxCorr and x < output:
                    output = x
                    signed_cor = lat[n][x]
            sBoxCorr.append(math.log(maxCorr, 2.0))
            total_corr = total_corr * signed_cor
            # convert to log base 2
            total_corr_base_2 = math.log(abs(total_corr), 2.0)
            newMask.append(output)
        return total_corr_base_2, newMask, sBoxCorr
