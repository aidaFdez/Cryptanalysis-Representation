import re
import sys
import math
import experiment as ex
import diff
import itertools
import trails


# Objects for linear and differential
class Cryptanalysis:
    # the inputs that visualise() takes. Here to check what needs to be part of the object
    # inputString, numOfBits, numOfRounds, sBoxes, sBox, pBox, type, first, tr, pbs, p_fin, svalues
    sbox = []
    pbox = []
    num_rounds = 0
    trail = []
    probabilities = []
    tpe = ""
    input_string = ""

    # Initialise the cryptanalysis class
    def __init__(self, tpe, sbox, pbox, num_rounds, input_string):
        self.sbox = sbox
        self.pbox = pbox
        self.num_rounds = num_rounds
        self.tpe = tpe
        self.input_string = input_string
        # print(type, " created")

    # Getter methods
    def get_sbox(self):
        return self.sbox

    def get_numrounds(self):
        return self.num_rounds

    def get_type(self):
        return self.tpe

    ######################
    # DIFFERENTIAL CLASS #
    ######################


class Differential(Cryptanalysis):
    """Class for differential cryptanalysis. This inherits from the cryptanalysis class."""

    # Own variables
    ddt = []  # Difference Distribution Table
    type2 = ""  # Second type of differential, referred to the crypto algorithm (present, gift, DES)

    # Initialise the differential class
    def __init__(self, type2, sbox, pbox, num_rounds, input_string):
        # Call the super class initialiser
        super().__init__("Differential", sbox, pbox, num_rounds, input_string)
        # Differential.calculate_ddt(self)
        # print(self.ddt)
        if type2 == "present" or type2 == "gift":
            self.ddt = Differential.calculate_ddt(self)
        if type2 == "des":
            all_ddt = []
            for sb in sbox:
                all_ddt.append(Differential.calculate_ddt(self, sb))
            self.ddt = all_ddt

    def get_ddt(self):
        return self.ddt

    # Get the Difference Distribution Table
    @staticmethod
    def calculate_ddt(self, sbox=None):
        if sbox is None:
            sbox = self.sbox
        for i in range(len(sbox)):
            sbox[i] = int(sbox[i])

        ddt = [[0 for col in range(16)] for row in range(len(sbox))]
        for w in range(len(sbox)):  # Up to 16 because we are using hexadecimal
            for i in range(len(sbox)):
                #print("calculating", w, ", ", i)
                j = i ^ w
                # Get the corresponding sbox values
                a = sbox[i]
                b = sbox[j]
                # Get the difference from the sbox values
                c = a ^ b
                ddt[w][c] = ddt[w][c] + 1
        # self.ddt = ddt
        return ddt

    def p_box_swaps(self, input_string, pbox=None):
        """ Does the swaps of the values according to the permutation box defined"""
        if pbox is None:
            pbox = self.pbox
        output = []
        # Get the binary values of the input difference
        for ch in input_string:
            output.extend(getBinary(ch))
        bin_output = [0] * len(pbox)
        # Do the swaps
        for n in range(int(len(pbox))):
            bin_output[pbox[n]] = output[n]
        new_diff = []
        # That division should be the number of bits of the thingy
        for r in range(len(input_string)):
            num = []
            num.append(bin_output[r * 4])
            num.append(bin_output[r * 4 + 1])
            num.append(bin_output[r * 4 + 2])
            num.append(bin_output[(r * 4) + 3])
            # print(num)
            new_diff.extend(fromBinary(num))
        return new_diff

    # Get the highest probability of a value
    def high_prob(self, input_val, ddt=None):
        if ddt is None:
            ddt = self.ddt
        # Probability of the highest found until now
        prob = 0
        # Value of the highest probability
        num = 0
        bin_input = getBinary(input_val)
        # Counter to keep track of the iteration we are in
        numCount = 0
        # print(len(self.ddt))
        for value in ddt[input_val]:
            # Hamming heuristic
            if (value == prob):
                # Add all the numbers, the shortest one has less 0s
                valCounter = getBinary(value)
                numCounter = getBinary(num)
                valequal = 0
                numequal = 0
                # count how many are different
                # print(bin_input)

                if not len(valCounter) ==len(bin_input):
                    valCounter.insert(0, 0)
                    valCounter.insert(0, 0)
                if not len(numCounter) ==len(bin_input):
                    numCounter.insert(0, 0)
                    numCounter.insert(0, 0)
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

    def do_sbox(self, strg, prob, sbox=None):
        if sbox is None:
            sbox = self.sbox
        vals = []
        if ((type(strg) is str)):
            strg = getInts(strg)
        if (type(strg) == int):
            value, probability = self.high_prob(strg)
            # Save the trail value
            vals.append(value)
            # Update the probability of that specific trail
            prob = prob * (probability / 16)
        else:
            for val in range(len(strg)):
                # print(type(val))
                value, probability = self.high_prob(strg[val])
                # Save the trail value
                vals.append(value)
                # Update the probability of that specific trail
                prob = prob * (probability / 16)
        return vals, prob

    def diff_trail(self, data):
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
                vals, prob = self.do_sbox(getInts(data), prob)

                # add the vals to the svalues, so to have the values of each s box
                svalues.append(vals)
                # Need to apply the permutation to the values:
                swapped = self.p_box_swaps(vals, self.pbox)
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
                vals, prob = self.do_sbox(trail[r - 1], prob)
                # add the vals to the svalues, so to have the values of each s box
                svalues.append(vals)
                swapped = self.p_box_swaps(vals, self.pbox)
                # Save the probability of this round
                probabilities.append(prob)
                if (general_prob * prob <= 2 ** (-(len(self.pbox)))):
                    over_prob = True
                else:
                    general_prob = general_prob * prob
                    trail.append(swapped)
            r = r + 1
        self.trail = trail
        self.probabilities = probabilities
        return trail, probabilities, general_prob, svalues


class DESDifferential(Differential):

    def __init__(self, input_string=None, num_rounds=None, trail=None):
        sbox1 = [14, 0, 4, 15, 13, 7, 1, 4,
                 2, 14, 15, 2, 11, 13, 8, 1,
                 3, 10, 10, 6, 6, 12, 12, 11,
                 5, 9, 9, 5, 0, 3, 7, 8,
                 4, 15, 1, 12, 14, 8, 8, 2,
                 13, 4, 6, 9, 2, 1, 11, 7,
                 15, 5, 12, 11, 9, 3, 7, 14,
                 3, 10, 10, 0, 5, 6, 0, 13]
        sbox2 = [15, 3, 1, 13, 8, 4, 14, 7,
                 6, 15, 11, 2, 3, 8, 4, 14,
                 9, 12, 7, 0, 2, 1, 13, 10,
                 12, 6, 0, 9, 5, 11, 10, 5,
                 0, 13, 14, 8, 7, 10, 11, 1,
                 10, 3, 4, 15, 13, 4, 1, 2,
                 5, 11, 8, 6, 12, 7, 6, 12,
                 9, 0, 3, 5, 2, 14, 15, 9]
        sbox3 = [10, 13, 0, 7, 9, 0, 14, 9,
                 6, 3, 3, 4, 15, 6, 5, 10,
                 1, 2, 13, 8, 12, 5, 7, 14,
                 11, 12, 4, 11, 2, 15, 8, 1,
                 13, 1, 6, 10, 4, 13, 9, 0,
                 8, 6, 15, 9, 3, 8, 0, 7,
                 11, 4, 1, 15, 2, 14, 12, 3,
                 5, 11, 10, 5, 14, 2, 7, 12]
        sbox4 = [7, 13, 13, 8, 14, 11, 3, 5,
                 0, 6, 6, 15, 9, 0, 10, 3,
                 1, 4, 2, 7, 8, 2, 5, 12,
                 11, 1, 12, 10, 4, 14, 15, 9,
                 10, 3, 6, 15, 9, 0, 0, 6,
                 12, 10, 11, 1, 7, 13, 13, 8,
                 15, 9, 1, 4, 3, 5, 14, 11,
                 5, 12, 2, 7, 8, 2, 4, 14]
        sbox5 = [2, 14, 12, 11, 4, 2, 1, 12,
                 7, 4, 10, 7, 11, 13, 6, 1,
                 8, 5, 5, 0, 3, 15, 15, 10,
                 13, 3, 0, 9, 14, 8, 9, 6,
                 4, 11, 2, 8, 1, 12, 11, 7,
                 10, 1, 13, 14, 7, 2, 8, 13,
                 15, 6, 9, 15, 12, 0, 5, 9,
                 6, 10, 3, 4, 0, 5, 14, 3]
        sbox6 = [12, 10, 1, 15, 10, 4, 15, 2,
                 9, 7, 2, 12, 6, 9, 8, 5,
                 0, 6, 13, 1, 3, 13, 4, 14,
                 14, 0, 7, 11, 5, 3, 11, 8,
                 9, 4, 14, 3, 15, 2, 5, 12,
                 2, 9, 8, 5, 12, 15, 3, 10,
                 7, 11, 0, 14, 4, 1, 10, 7,
                 1, 6, 13, 0, 11, 8, 6, 13]
        sbox7 = [4, 13, 11, 0, 2, 11, 14, 7,
                 15, 4, 0, 9, 8, 1, 13, 10,
                 3, 14, 12, 3, 9, 5, 7, 12,
                 5, 2, 10, 15, 6, 8, 1, 6,
                 1, 6, 4, 11, 11, 13, 13, 8,
                 12, 1, 3, 4, 7, 10, 14, 7,
                 10, 9, 15, 5, 6, 0, 8, 15,
                 0, 14, 5, 2, 9, 3, 2, 12]
        sbox8 = [13, 1, 2, 15, 8, 13, 4, 8,
                 6, 10, 15, 3, 11, 7, 1, 4,
                 10, 12, 9, 5, 3, 6, 14, 11,
                 5, 0, 0, 14, 12, 9, 7, 2,
                 7, 2, 11, 1, 4, 14, 1, 7,
                 9, 4, 12, 10, 14, 8, 2, 13,
                 0, 15, 6, 12, 10, 9, 13, 0,
                 15, 3, 3, 5, 5, 6, 8, 11]
        # [13, 1, 2, 15, 8, 13, 4, 8,6, 10, 15, 3, 11, 7, 1, 4,10, 12, 9, 5, 3, 6, 14, 11,5, 0, 0, 14, 12, 9, 7, 2,7, 2, 11, 1, 4, 14, 1, 7,9, 4, 12, 10, 14, 8, 2, 13,0, 15, 6, 12, 10, 9, 13, 0, 15, 3, 3, 5, 5, 6, 8, 11]
        # self.sbox = [sbox1, sbox2, sbox3, sbox4, sbox5, sbox6, sbox7, sbox8]
        initial_permutation = [58, 50, 42, 34, 26, 18, 10, 2,
                               60, 52, 44, 36, 28, 20, 12, 4,
                               62, 54, 46, 38, 30, 22, 14, 6,
                               64, 56, 48, 40, 32, 24, 16, 8,
                               57, 49, 41, 33, 25, 17, 9, 1,
                               59, 51, 43, 35, 27, 19, 11, 3,
                               61, 53, 45, 37, 29, 21, 13, 5,
                               63, 55, 47, 39, 31, 23, 15, 7]
        final_permutation = [39, 7, 47, 15, 55, 23, 63, 31,
                             38, 6, 46, 14, 54, 22, 62, 30,
                             37, 5, 45, 13, 53, 21, 61, 29,
                             36, 4, 44, 12, 52, 20, 60, 28,
                             35, 3, 43, 11, 51, 19, 59, 27,
                             34, 2, 42, 10, 50, 18, 58, 26,
                             33, 1, 41, 9, 49, 17, 57, 25,
                             32, 0, 40, 8, 48, 16, 56, 24]
        middle_permutation = [16, 7, 20, 21, 29, 12, 28, 17,
                              1, 15, 23, 26, 5, 18, 31, 10,
                              2, 8, 24, 14, 32, 27, 3, 9,
                              19, 13, 30, 6, 22, 11, 4, 25]
        middle_permutation = [x-1 for x in middle_permutation]
        extension = [31, 0, 1, 2, 3, 4,
                     3, 4, 5, 6, 7, 8,
                     7, 8, 9, 10, 11, 12,
                     11, 12, 13, 14, 15, 16,
                     15, 16, 17, 18, 19, 20,
                     19, 20, 21, 22, 23, 24,
                     23, 24, 25, 26, 27, 28,
                     27, 28, 29, 30, 31, 0]

        sbox = [sbox1, sbox2, sbox3, sbox4, sbox5, sbox6, sbox7, sbox8]
        pbox = [initial_permutation, middle_permutation, final_permutation]

        super().__init__("des", sbox, pbox, num_rounds, input_string)
        self.extension = extension

        # Do all the ddts of the sboxes
        #print(self.sbox)
        for sb in self.sbox:
            #print(sb)
            self.ddt.append(self.calculate_ddt(self, sb))
        self.trail.append(input_string)

    def get_trail(self, num_rounds, input_string):
        # s_trail = []  # Keep track of the substituted values, useful for representation
        trail = [] # Keep track of the generated trail
        trail.append(input_string)
        probs = [] # Keep track of the probability of each round
        for i in range(num_rounds):
            right_side = trail[i][8:]
            left_side = trail[i][:8]

            expanded = self.extend_binary(right_side)
            expanded_dec = []
            for j in range(int(len(expanded) / 6)):
                expanded_dec.extend(fromBinary(expanded[j*6:6*(j+1)]))

            # Get the ddt highest value for each of the eight values
            substituted_values = []
            for k in range(len(expanded_dec)):
                ddt_use = self.calculate_ddt(self, self.sbox[k])
                new_value, prob = self.high_prob(expanded_dec[k], ddt_use)
                # print(new_value)
                substituted_values.append(new_value)
                probs.append(prob)

            # print(substituted_values)
            # We have the right before the permutation, so do the permutation
            permuted = self.p_box_swaps(substituted_values, self.pbox[1])

            # We have before the xor, do that now
            new_right = xor(left_side, permuted)
            right_side.extend(new_right)
            trail.append(right_side)
        return trail, probs

    def check_trail(self, trail, lst_right =False):
        prob = 1
        for index, tr in enumerate(trail[:-1]):  # Do not want to do it on the last one as there is no next trail for it
            # Get the correct pbox to use in the round
            pbox_use = 1
            """if index == 0:
                pbox_use = 0
            if index == len(trail - 2):
                pbox_use = 2"""
            #print(tr)
            # Get the left and the right of each
            left_in = trail[index][:8]
            right_in = trail[index][8:]
            left_out = trail[index+1][:8]
            right_out = trail[index+1][8:]
            # print("Checking", right_in, "with", right_out)

            # Start undoing from the bottom, ie: the output
            # First need to xor the left_in with right_out
            after_permutation = xor(left_in, right_out)

            # Undo the permutation, gets result in decimal. Use result for the sbox later
            undone_permutation = self.undo_permutation(after_permutation, self.pbox[pbox_use])

            # Work from the top now
            expanded = self.extend_binary(right_in)
            # Get the expanded in decimal for the sbox
            expanded_dec = []
            for i in range(int(len(expanded) / 6)):
                expanded_dec.extend(fromBinary(expanded[i*6:6*(i+1)]))

            # Get the probability of the sbox substitution
            for index, value in enumerate(expanded_dec):
                # print(undone_permutation[index])
                p = self.undo_sbox_possible_des([value], [undone_permutation[index]], self.sbox[index])
                #if p == 0:
                    #print("NOOOOOOOOOOOOOOOO")
                prob = prob*p
            #print(prob) #  TODO: put this in log2
        if prob ==0:
            return 0
        return math.log2(prob)

    def sboxes_fun(self):
        dic_sboxes = {1: self.sbox[0].copy(), 2: self.sbox[1].copy(), 3: self.sbox[2].copy(), 4: self.sbox[3].copy(),
                      5: self.sbox[4].copy(), 6: self.sbox[5].copy(), 7: self.sbox[6].copy(), 8: self.sbox[7].copy()}
        # TODO
        box_numbers = [1,2,3,4,5,6,7,8]
        #pmt = itertools.product(box_numbers, repeat = len(box_numbers))
        pmt = [[1,1,1,1,1,1,1,1],
               [2,2,2,2,2,2,2,2],
               [3,3,3,3,3,3,3,3],
               [4,4,4,4,4,4,4,4],
               [5,5,5,5,5,5,5,5],
               [6,6,6,6,6,6,6,6],
               [7,7,7,7,7,7,7,7],
               [8,8,8,8,8,8,8,8]]
        pmt = list(itertools.permutations(box_numbers))
        for permutation in pmt:
            # if(len(set(permutation)) ==1):
            #    print("started number ", permutation[0])
            new_DES = DESDifferential()
            new_sbox = []
            for val in permutation:
                new_sbox.append(dic_sboxes[val])
            new_DES.sbox = new_sbox
            p = new_DES.check_trail(trails.trail_des3)
            # print(new_DES.sbox[7][:10])
            with open("permutations_sbox_smaller.txt", 'a') as f:
                if p < (-50):
                    to_write = str(str(permutation) + ": "+ str(p)+ "\n")
                    f.write(to_write)

    def undo_permutation(self, trail, pbox=None):
        if pbox ==None:
            pbox = self.pbox[1]
        binary = []
        for c in trail:
            binary.extend(getBinary(c))
        undone_permutation = [0]*len(binary)
        # print(pbox)
        for i in range(len(pbox)):
            # print(pbox.index(i))
            # print(binary[i])
            undone_permutation[pbox.index(i)] = binary[i]
        # Undo the binary and return that
        undone = []
        for i in range(int(len(pbox) / 4)):
            undone.extend(fromBinary(undone_permutation[i*4:4*(i+1)]))
        return undone

    def extend_binary(self, inputs):
        extended = [0] * 48
        # print(self.extension)
        # Get the input in binary:
        bin_in = []
        for ch in inputs:
            bin_in.extend(getBinary(ch))

        for i in range(len(extended)):
            extended[i] = bin_in[self.extension[i]]
        return extended

    def undo_extension_des(self, ext_table, output):
        # Output is what came out of extension table, so want to undo that
        input = [0] * 32
        for index, val in enumerate(ext_table):
            input[ext_table[index]] = output[ext_table[index]]
        return input

    def des_sbox(self, sbox, value):
        f, s = ex.sbox_values(value)
        s = sbox[f][s]
        return s

    def undo_sbox_possible_des(self, inputs, outputs, sbox):
        # The inputs are what goes into sbox, check possible to map to outputs
        # Receive the values in decimal
        probability = 1
        # print(inputs)
        for index, val in enumerate(inputs):
            dif_dis_t = self.calculate_ddt(self, sbox)
            # Probability of value to svalue
            probability = probability * dif_dis_t[inputs[index]][outputs[index]] / len(dif_dis_t)
            #print("Probability of", inputs, "to", outputs, ":", probability)
        return probability



    ################
    # LINEAR CLASS #
    ################


class Linear(Cryptanalysis):
    # Own variables
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


# Get the svalue and probabilities in the middle of two characteristics, based on done by the check_trail
def get_in_between(charac_before, charac_after, sbox, pbox):
    #raise NameError("hey")
    prob = 1
    svalue = []
    ddt = diff.diffDistTable(sbox)
    print(pbox)

    new_bin = []
    for c in charac_after:
        new_bin.extend(diff.getBinary(c))
    undone_binary = [0]*len(pbox)
    for i in range(len(pbox)):
        undone_binary[pbox.index(i)] = new_bin[i]
    for i in range(int(len(pbox)/4)):
        interm = [undone_binary[i * 4], undone_binary[i * 4 + 1], undone_binary[i * 4 + 2],
                  undone_binary[i * 4 + 3]]
        svalue.extend(diff.fromBinary(interm))
    for i in range(len(svalue)):
        np = ddt[charac_before[i]][svalue[i]]/(len(pbox)/4)
        # print("From ", charac_before[i], "to", svalue[i], np)
        prob = prob*np
    # print(math.log2(prob))
    print()
    return svalue, prob

# Get the integer related to the input
def getInts(str):
    # Pattern of the input
    pattern = re.compile("([abcdefABCDEF][0-9])*")
    nums = []
    if pattern.match(str):
        for c in str:
            nums.append(int(c,16))
            # print(c)
            #if (c == '0'): nums.append(0)
            #if (c == '1'): nums.append(1)
            #if (c == '2'): nums.append(2)
            #if (c == '3'): nums.append(3)
            #if (c == '4'): nums.append(4)
            #if (c == '5'): nums.append(5)
            #if (c == '6'): nums.append(6)
            #if (c == '7'): nums.append(7)
            #if (c == '8'): nums.append(8)
            #if (c == '9'): nums.append(9)
            #if (c == 'a' or c == 'A'): nums.append(10)
            #if (c == 'b' or c == 'B'): nums.append(11)
            #if (c == 'c' or c == 'C'): nums.append(12)
            #if (c == 'd' or c == 'D'): nums.append(13)
            #if (c == 'e' or c == 'E'): nums.append(14)
            #if (c == 'f' or c == 'F'): nums.append(15)
    else:
        nums.append(9999)
    return nums


def getBinary(c, num_bits = 4):
    # print(c, " is the received")
    #if (c == 0): return [0, 0, 0, 0]
    #if (c == 1): return [1, 0, 0, 0]
    #if (c == 2): return [0, 1, 0, 0]
    #if (c == 3): return [1, 1, 0, 0]
    #if (c == 4): return [0, 0, 1, 0]
    #if (c == 5): return [1, 0, 1, 0]
    #if (c == 6): return [0, 1, 1, 0]
    #if (c == 7): return [1, 1, 1, 0]
    #if (c == 8): return [0, 0, 0, 1]
    #if (c == 9): return [1, 0, 0, 1]
    #if (c == 10 or c == 'A'): return [0, 1, 0, 1]
    #if (c == 11 or c == 'B'): return [1, 1, 0, 1]
    #if (c == 12 or c == 'C'): return [0, 0, 1, 1]
    #if (c == 13 or c == 'D'): return [1, 0, 1, 1]
    #if (c == 14 or c == 'E'): return [0, 1, 1, 1]
    #if (c == 15 or c == 'F'):
    #    return [1, 1, 1, 1]
    #else:
    #    try:
    #        sys.exit(0)
    #    except SystemExit:
    #        print("The numbers were not correct, so no match could be found")
    string_bits = '{0:0' +str(num_bits) + 'b}'
    return [int(v) for v in string_bits.format(c)]


def fromBinary(c):
    # print(c)
    return [int("".join(str(i) for i in c), 2)]
    # if (c == [0, 0, 0, 0]): return [0]
    # if (c == [1, 0, 0, 0]): return [1]
    # if (c == [0, 1, 0, 0]): return [2]
    # if (c == [1, 1, 0, 0]): return [3]
    # if (c == [0, 0, 1, 0]): return [4]
    # if (c == [1, 0, 1, 0]): return [5]
    # if (c == [0, 1, 1, 0]): return [6]
    # if (c == [1, 1, 1, 0]): return [7]
    # if (c == [0, 0, 0, 1]): return [8]
    # if (c == [1, 0, 0, 1]): return [9]
    # if (c == [0, 1, 0, 1]): return [10]
    # if (c == [1, 1, 0, 1]): return [11]
    # if (c == [0, 0, 1, 1]): return [12]
    # if (c == [1, 0, 1, 1]): return [13]
    # if (c == [0, 1, 1, 1]): return [14]
    # if (c == [1, 1, 1, 1]): return [15]


def vals_string(vals):
    """Return a string of the list of integers given"""
    stn = "["
    sep = ""
    for val in vals:
        # print(val)
        stn = stn + sep
        sep = ","
        stn = stn + str(val)
    stn = stn + "]"
    return stn


def xor(a, b):
    """Do the xor between two lists of integers"""
    if not len(a) == len(b):
        raise Exception("The two lists must be of the same length")
    new = [el[0] ^ el[1] for el in list(zip(a, b))]
    return new
