import tkinter as tk
import re

import cipher
import diff
import lin
import math
from decimal import Decimal
import sys
import os
from tkinter import filedialog
import json

# Variables to keep the trails and probabilities
trail = []
lintrail = []
probs = []

# Difference distribution table hardcoded for testing
ddft = [[16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 6, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0, 4, 0],
        [0, 6, 6, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 0, 2, 0, 0, 2, 0, 0, 0, 4, 0, 2, 0],
        [0, 0, 0, 2, 0, 2, 4, 0, 0, 2, 2, 2, 0, 0, 2, 0],
        [0, 2, 2, 0, 4, 0, 0, 4, 2, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 2, 0, 4, 0, 0, 2, 2, 0, 2, 2, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 4, 4, 0, 2, 2, 2, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 2, 0, 2, 4, 0, 0, 4, 0, 2, 0, 2],
        [0, 2, 0, 0, 0, 2, 2, 2, 0, 4, 2, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 2, 2, 0, 0, 0, 4, 4, 0, 2, 2, 0, 0],
        [0, 0, 0, 2, 2, 0, 2, 2, 2, 0, 0, 4, 0, 0, 2, 0],
        [0, 4, 0, 2, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 6, 0],
        [0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 6, 2, 0, 4],
        [0, 2, 0, 4, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 6],
        [0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 10, 0, 2]]

# Linear approximation table hardcoded for testing
lat = [[16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 6, 0, 10, 0, 6, 12, 6, 10, 12, 10, 0, 6, 0, 10, 0],
       [0, 10, 6, 0, 6, 0, 0, 10, 10, 12, 0, 10, 12, 6, 6, 0],
       [0, 12, 10, 10, 6, 10, 0, 0, 0, 0, 10, 6, 6, 6, 0, 12],
       [0, 0, 6, 10, 10, 6, 0, 0, 4, 0, 10, 10, 10, 10, 0, 12],
       [0, 6, 10, 0, 10, 12, 0, 10, 6, 12, 0, 6, 0, 10, 6, 0],
       [0, 6, 0, 10, 0, 10, 12, 10, 10, 4, 10, 0, 10, 0, 6, 0],
       [0, 0, 0, 0, 0, 12, 0, 4, 0, 0, 0, 0, 12, 0, 12, 0],
       [0, 0, 6, 10, 4, 0, 10, 10, 4, 0, 6, 6, 0, 0, 10, 6],
       [0, 6, 2, 0, 0, 10, 6, 0, 10, 0, 0, 6, 6, 0, 0, 10],
       [0, 6, 0, 2, 6, 0, 10, 0, 6, 0, 10, 0, 0, 6, 0, 10],
       [0, 0, 0, 0, 10, 6, 10, 6, 0, 0, 4, 4, 10, 6, 6, 10],
       [0, 0, 0, 0, 6, 6, 6, 6, 0, 0, 12, 4, 10, 10, 6, 6],
       [0, 6, 0, 10, 10, 0, 6, 0, 6, 0, 10, 0, 0, 2, 0, 6],
       [0, 10, 6, 0, 0, 10, 10, 4, 6, 0, 0, 10, 6, 0, 4, 6],
       [0, 4, 10, 10, 4, 0, 6, 6, 0, 0, 6, 10, 0, 0, 6, 10]]


def show_ddft(wn, cip, sbox=None):
    # Create a new window for the DDFT, on top of the visual one
    ddft_wnw = tk.Toplevel(wn)
    fr = tk.Frame(ddft_wnw)
    fr.pack()
    if sbox==None:
        ddft2 = cip.ddt
    else:
        ddft2=cipher.Differential.calculate_ddt(None, sbox=sbox)
    for i in range(len(ddft2)):
        row = tk.Label(fr, text=i, relief=tk.RIDGE, width=10, bg='gray')
        row.grid(row=0, column=i + 1)
        col = tk.Label(fr, text=i, relief=tk.RIDGE, width=10, bg='gray')
        col.grid(row=i + 1, column=0)
        for j in range(len(ddft2[i])):
            prob = tk.Label(fr, text=ddft2[i][j], relief=tk.RIDGE, width=10)
            # Depending on the parity of the index, paint one colour or another
            if i % 2 == 0:
                prob = tk.Label(fr, text=ddft2[i][j], relief=tk.RIDGE, width=10)
            else:
                prob = tk.Label(fr, text=ddft2[i][j], relief=tk.RIDGE, width=10, bg='LightSkyBlue1')
            prob.grid(row=i + 1, column=j + 1)
            # if not(ddft [i][j] == ddft2[i][j]):
            #    print("The one in ", i, ", ", j, " is different")


def showLAT(wn, sbox):
    # Creatw window to display LAT
    lanWnw = tk.Toplevel(wn)
    lanfr = tk.Frame(lanWnw)
    lanfr.pack()
    lat2 = lin.linApptable(sbox)
    for i in range(16):
        row = tk.Label(lanfr, text=i, relief=tk.RIDGE, width=10, bg='gray')
        row.grid(row=0, column=i + 1)
        col = tk.Label(lanfr, text=i, relief=tk.RIDGE, width=10, bg='gray')
        col.grid(row=i + 1, column=0)
        for j in range(16):
            prob = tk.Label(lanfr, text=lat2[i][j], relief=tk.RIDGE, width=10)
            if (i % 2 == 0):
                prob = tk.Label(lanfr, text=lat2[i][j], relief=tk.RIDGE, width=10)
            else:
                prob = tk.Label(lanfr, text=lat2[i][j], relief=tk.RIDGE, width=10, bg='LightSkyBlue1')
            prob.grid(row=i + 1, column=j + 1)


# For popping up useful messages
def popupmsg(title, msg, wn):
    popup = tk.Toplevel(wn)
    popup.wm_title(title)
    label = tk.Label(popup, text=msg)
    fr = tk.Frame(popup)
    fr.pack()
    label.pack(side="top", fill="x", pady=10)


def diff_edition(wn, round, sbox, pbox, numRounds, tr, pbs, inputString, svalues):
    # Set up of the window to be used for the input
    edit_window = tk.Toplevel(wn)
    # print(round)
    info = tk.Label(edit_window, text="Write new difference")
    info.grid(column=0, row=0)
    input = tk.Entry(edit_window)
    input.grid(row=1, column=0)

    # print(inputString ," is the inpStr")
    # print(round, " is the number of the round")

    # function to be called by the button to change all the data
    def change(wn):
        new_diff = input.get()
        pattern = re.compile("([abcdefABCDEF][0-9])*")
        if not (len(new_diff) == int(len(pbox) / 4)) or not (pattern.match(new_diff)):
            popup = tk.Tk()
            popup.wm_title("ERROR")
            label = tk.Label(popup, text=str(
                "The new difference needs to be of length " + str(int(len(pbox) / 4)) + " and of the type \"0a3d\""))
            label.pack(side="top", fill="x", pady=10)
            b1 = tk.Button(popup, text="Okay", command=popup.destroy)
            b1.pack()
            popup.mainloop()
        else:
            old_trail = tr
            old_probs = pbs
            new_round = diff.getInts(new_diff)
            old_round = old_trail[round - 1]
            next_round = old_trail[round + 1]
            new_prob = 1
            ddt = diff.diffDistTable(sbox)

            # binary representation of the  new round, to undo it
            new_bin = []
            for c in new_round:
                # print(c)
                new_bin.extend(diff.getBinary(c))
            # binary result of undoing the pbox
            undone_binary = [0] * len(pbox)
            # print(undone_binary)
            # print(new_bin)
            for i in range(len(pbox)):
                # print(pbox.index(i))
                # print(new_bin[i])
                undone_binary[pbox.index(i)] = new_bin[i]
            # get the int values of the undone
            new_svalue = []
            for i in range(int(len(pbox) / 4)):
                interm = [undone_binary[i * 4], undone_binary[i * 4 + 1], undone_binary[i * 4 + 2],
                          undone_binary[i * 4 + 3]]
                new_svalue.extend(diff.fromBinary(interm))
            error = ""

            # now that we have the new svalues, check that they can match the dfft
            # print(new_svalue)
            # print(old_round)
            # print(old_trail)
            inp_data = diff.getInts(inputString)
            for i in range(len(new_svalue)):
                # for each of the rows in the ddft, calculate new probability
                np = ddt[old_round[i]][new_svalue[i]] / 16
                if round == 0:
                    np = ddt[inp_data[i]][new_svalue[i]] / 16
                new_prob = new_prob * np

                # if the new probability is 0, then add it to the error string
                # print(ddt[old_round[i]][new_svalue[i]])
                if (np <= 0):
                    error = error + str(
                        "Not possible to go from " + str(new_svalue[i]) + " to " + str(old_round[i]) + "\n")
            # print(error)
            final_trail = old_trail
            final_trail[round] = new_round

            svalues[round] = new_svalue

            final_probs = old_probs
            final_probs[round] = new_prob

            # Need to check that the new round values fit with the ones from that round's substitution
            # print(svalues[round+1])
            second_prob = 1
            for i in range(len(new_svalue)):
                # print("from ",next_round[i]," to ",new_svalue[i] )
                np = ddt[next_round[i]][new_svalue[i]] / len(sbox)
                second_prob = second_prob * np
                # print(np)
            final_probs[round + 1] = second_prob

            fin_prob = 1
            for p in final_probs:
                fin_prob = fin_prob * p
            visual(inputString, 2, numRounds, len(inputString), sbox, pbox, "Differential", False, final_trail,
                   final_probs, fin_prob, svalues)

    bt = tk.Button(edit_window, text="Ok", command=lambda: change(wn))
    bt.grid(row=2, column=0)


def lin_edition(wn, round, sboxnumber, sbox, pbox, numRounds, trail, sboxMasks, totalCorr, inputString):
    # Set up of the window to be used for the input
    edit_window = tk.Toplevel(wn)
    info = tk.Label(edit_window, text="Write new mask")
    info.grid(column=0, row=0)
    input = tk.Entry(edit_window)
    input.grid(row=1, column=0)

    def check(wn):
        if (len(input.get()) != 4 or not (all(c in '01' for c in str(input.get())))):
            # print("Input must be a 4 bit binary string")
            popup = tk.Toplevel(wn)
            popup.wm_title("ERROR")
            label = tk.Label(popup, text="Input must be a 4 bit binary string")
            label.pack(side="top", fill="x", pady=10)
            B1 = tk.Button(popup, text="Okay", command=popup.destroy)
            B1.pack()
            popup.mainloop()

        else:
            change(wn)

    # function to change the linear data
    def change(wn):
        # convert to tuples to list to be able to modify
        temptrail = [list(elem) for elem in trail]

        # get new input mask
        new_inp = input.get()
        edit_window.destroy()

        # update mask
        sboxMasks[round][sboxnumber] = new_inp

        mask = [m for i in temptrail[round - 1][1] for m in i]
        # recalulate previous round
        for i in range(sboxnumber * 4, (4 * sboxnumber) + 4):
            x = pbox.index(i)
            mask[x] = new_inp[i % 4]
        tempmask = [''.join(mask[i:i + 4]) for i in range(0, len(mask), 4)]
        temptrail[round - 1][1] = tempmask

        # recalculate correlations for previous round
        for i in range(4):
            temptrail[round - 1][2][i] = lin.linApptable(sbox)[int(new_inp, 2)][int(temptrail[round][1][sboxnumber], 2)]

        # calculate total correlation of previous round
        totprevroundcorr = sum(temptrail[round - 1][2])
        temptrail[round - 1][0] = totprevroundcorr

        # update correlation
        if (lin.linApptable(sbox)[int(new_inp, 2)][int(temptrail[round][1][sboxnumber], 2)] == 0):
            temptrail[round][2][sboxnumber] = "inf"
            temptrail[round][0] = "inf"
            totalCorr = "inf"
        else:
            temptrail[round][2][sboxnumber] = math.log(
                abs(lin.linApptable(sbox)[int(new_inp, 2)][int(temptrail[round][1][sboxnumber], 2)]), 2)
            # calculate the total correlation
            totroundcorr = sum(temptrail[round][2])
            temptrail[round][0] = totroundcorr
            # update the total correlation
            totalCorr = 0
            for r in temptrail:
                totalCorr = totalCorr + r[0]

        # convert back to a list
        newtrail = [tuple(l) for l in temptrail]

        # call visual method to display
        wn.destroy()
        visual(inputString, 2, numRounds, int(len(inputString) / 4), sbox, pbox, "Linear", False, newtrail, sboxMasks,
               totalCorr, [])

    bt = tk.Button(edit_window, text="Ok", command=lambda: check(wn))
    bt.grid(row=2, column=0)


def calculate_diff(sBox, inputString, pBox, numOfRounds, wdw):
    bt = tk.Button(wdw, text = "Difference distribution table", command = lambda: show_ddft(wdw, sBox))
    bt.pack()
    trail, probs, prob_fin, svalues = diff.diffTrail(sBox, inputString, diff.diffDistTable(sBox), pBox, numOfRounds)
    #If the number of rounds is more than the one of the trail, then more rounds were chosen than it is worth calculating
    if(len(trail)<numOfRounds):
        prev = numOfRounds
        numOfRounds = len(trail)
        #diff.popup("Number of rounds",("You chose " + str(numOfRounds) + " but/ it is efficient to calculate up to " + str(len(trail)) + ", so this was used"))
        popupmsg("Number of rounds",("You chose " + str(prev) + " but it is efficient to calculate up to " + str(len(trail)) + ", so this was used"), wdw )
    return trail, probs, prob_fin, svalues

"""def calculate_diff(cip, wdw):
    bt = tk.Button(wdw, text="Difference distribution table", command=lambda: show_ddft(wdw, cip))
    bt.pack()
    trail, probs, prob_fin, svalues = diff.diffTrail(cip.sbox, cip.input_string, cip.ddt, cip.pbox, cip.num_rounds)
    # If the number of rounds is more than the one of the trail, then more rounds were chosen than it is worth calculating
    if (len(trail) < cip.num_rounds):
        prev = cip.num_rounds
        numOfRounds = len(cip.trail)
        # diff.popup("Number of rounds",("You chose " + str(numOfRounds) + " but/ it is efficient to calculate up to " + str(len(trail)) + ", so this was used"))
        popupmsg("Number of rounds", ("You chose " + str(prev) + " but it is efficient to calculate up to " + str(
            len(trail)) + ", so this was used"), wdw)
    return trail, probs, prob_fin, svalues"""



def calculate_lin(sBoxes, sBox, inputString, pBox, numOfRounds, wdw):
    trail = []
    sboxMasks = []
    # calculate the masks
    sboxMasks.append([inputString[i:i + 4] for i in range(0, len(inputString), 4)])
    for corrPerRound in range(numOfRounds):
        trail.append(lin.linTrail(sBoxes, inputString, lin.linApptable(sBox)))
        for i in range(4):
            get_bin = lambda x, n: format(x, 'b').zfill(n)
            trail[corrPerRound][1][i] = get_bin(trail[corrPerRound][1][i], 4)
        tempMask = ''.join(trail[corrPerRound][1])
        permutedMask = []
        # find the permuted masks
        for n in range(len(pBox)):
            permutedMask.append(tempMask[pBox.index(n)])
        inputString = ''.join(permutedMask)
        sboxMasks.append([inputString[i:i + 4] for i in range(0, len(inputString), 4)])
    # calculate the correlation
    totalCorr = 0
    for r in trail:
        totalCorr = totalCorr + r[0]

    return trail, sboxMasks, totalCorr




def visual(inputString, numOfBits, numOfRounds, sBoxes, sBox, pBox, tpe, first, tr, pbs, p_fin, svalues, type2=None):
    wdw = tk.Tk()
    wdw.geometry("500x600")
    if type2 == None:
        type2 = "own"
    # svalues = []
    if tpe == "Differential" and first:
        bt = tk.Button(wdw, text="Differential Distribution Table", command=lambda: show_ddft(wdw, None, sBox))
        bt.pack()
        #cp_diff = cipher.Differential("present", sBox, pBox, numOfRounds, inputString)
        print("pbox main is", pBox)
        trail, probs, prob_fin, svalues = calculate_diff(sBox, inputString, pBox, numOfRounds, wdw)
        # show_ddft(wdw, cp_diff)
        print("The trail is",tr)
    if tpe == "Differential" and not first:
        bt = tk.Button(wdw, text="Differential Distribution Table", command=lambda: show_ddft(wdw, None,sBox))
        bt.pack()
        #print(inputString)
        trail = tr
        probs = pbs
        prob_fin = p_fin

    if tpe == "Linear" and first:
        bt = tk.Button(wdw, text="Linear Approximation table", command=lambda: showLAT(wdw, sBox))
        bt.pack()
        trail, sboxMasks, totalCorr = calculate_lin(sBoxes, sBox, inputString, pBox, numOfRounds, wdw)

    if tpe == "Linear" and not first:
        bt = tk.Button(wdw, text="Linear Approximation table", command=lambda: showLAT(wdw, sBox))
        bt.pack()
        # assigment the variables for linear
        trail = tr
        sboxMasks = pbs
        totalCorr = p_fin

    def save_file():
        curr_dir = os.getcwd()
        file_to_save = filedialog.asksaveasfilename(initialdir = curr_dir)
        # print(pBox)
        # print(type(pBox[1]))
        first = []
        for c in inputString:
            first.append(int(c))
        trail.insert(0, first)
        # print("The type is", type2)
        for i in range(len(pBox)):
            pBox[i] = int(pBox[i])
        dic_json = {"type1": tpe, "type2": type2, "trail": trail, "sbox": sBox, "pbox": pBox}
        if type2 == "own":
            dic_json["in_str"] = inputString
            dic_json["num_rounds"] = numOfRounds
            dic_json["probs"] = probs
            dic_json["fin_prob"] = p_fin
            dic_json["svalues"] = svalues

        with open(file_to_save, 'w') as f:
            json.dump(dic_json, f)

    # Do the file saving thing
    save_button = tk.Button(wdw, text="Save trail", command = save_file)
    save_button.pack()

    wdw.title("Visualisation")

    scrollbar = tk.Scrollbar(wdw)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    end_y = 0

    # Set so the scrolling fits the window
    def update_scrollregion(event, sBoxes, numOfRounds, wdw, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))
        configure(event, sBoxes, numOfRounds)

    def configure(event, num_arrows, num_rounds):
        end_arrow = 150
        arrow1_canvas.delete("all")
        height = wdw.winfo_height()
        width = wdw.winfo_width()
        length_box = (width - width / 5)
        ft = str(num_arrows*80)+"x600"
        wdw.geometry(ft)

        # input
        arrow1_canvas.create_text(width / 2, 20, text=inputString)
        arrow1_canvas.create_line(width / 2, 40, width / 2, end_arrow, arrow=tk.LAST)
        arrow1_canvas.create_rectangle((width / 30), end_arrow + 20, (width - width / 30), 220)
        if (tpe == "Linear"):
            arrow1_canvas.create_text(width / 2 + 200, 20, text="Correlations and Complexities\n are in log base 2")

        # calculates permutation of each arrow
        positions_x = []
        for a in range(sBoxes):
            positions_x.append(width / (num_arrows + 1) * (a + 1) - 20)
            positions_x.append(width / (num_arrows + 1) * (a + 1) - 7)
            positions_x.append(width / (num_arrows + 1) * (a + 1) + 7)
            positions_x.append(width / (num_arrows + 1) * (a + 1) + 20)

        # Drawing the xor for round 1
        arrow1_canvas.create_oval(width / 20 - 20, end_arrow + 25, width / 20 + 20, end_arrow + 65)
        arrow1_canvas.create_line(width / 20 - 20, end_arrow + 45, width / 20 + 20, end_arrow + 45)
        arrow1_canvas.create_line(width / 20, end_arrow + 25, width / 20, end_arrow + 65)
        arrow1_canvas.create_line((width / 40) - 15, end_arrow + 45, (width / 40), end_arrow + 45, arrow=tk.LAST)
        arrow1_canvas.create_text((width / 40) - 20, end_arrow + 45, text="k0")

        # add linear probability for round one
        if (tpe == "Linear"):
            arrow1_canvas.create_text(width / 2 + 110, end_arrow + 45,
                                      text=" correlation of round: " + str(round(trail[0][0], 2)))

        # loop through each round
        if (num_rounds > len(trail) and tpe == "Differential"):
            num_rounds = len(trail)

        for r in range(num_rounds):
            # print(r)
            # Get the binary stuff for differential:
            if (tpe == "Differential"):
                bin = []
                # For each value in the trail of this round
                # print("Printing values")
                for val in trail[r]:
                    # print(val)
                    bin.extend(diff.getBinary(val))
                # print(bin)
            for a in range(num_arrows):
                # arrows to sboxes
                # round 1
                if (r == 0):
                    # Arrow to the left
                    arrow1_canvas.create_line(width / (num_arrows + 1) * (a + 1) - 20, (r + 1) * end_arrow + 75,
                                              width / (num_arrows + 1) * (a + 1) - 20, (r + 1) * end_arrow + 105,
                                              arrow=tk.LAST)
                    # Arrow to the RIGHT
                    arrow1_canvas.create_line(width / (num_arrows + 1) * (a + 1) + 20, (r + 1) * end_arrow + 75,
                                              width / (num_arrows + 1) * (a + 1) + 20, (r + 1) * end_arrow + 105,
                                              arrow=tk.LAST)
                    # Arrow to the center left
                    arrow1_canvas.create_line(width / (num_arrows + 1) * (a + 1) - 7, (r + 1) * end_arrow + 75,
                                              width / (num_arrows + 1) * (a + 1) - 7, (r + 1) * end_arrow + 105,
                                              arrow=tk.LAST)
                    # Arrow to the center right
                    arrow1_canvas.create_line(width / (num_arrows + 1) * (a + 1) + 7, (r + 1) * end_arrow + 75,
                                              width / (num_arrows + 1) * (a + 1) + 7, (r + 1) * end_arrow + 105,
                                              arrow=tk.LAST)
                # all other rounds
                else:
                    # Arrow to the left
                    arrow1_canvas.create_line(width / (num_arrows + 1) * (a + 1) - 20, end_arrow + 75,
                                              width / (num_arrows + 1) * (a + 1) - 20, end_arrow + 105, arrow=tk.LAST)
                    # Arrow to the RIGHT
                    arrow1_canvas.create_line(width / (num_arrows + 1) * (a + 1) + 20, end_arrow + 75,
                                              width / (num_arrows + 1) * (a + 1) + 20, end_arrow + 105, arrow=tk.LAST)
                    # Arrow to the center left
                    arrow1_canvas.create_line(width / (num_arrows + 1) * (a + 1) - 7, end_arrow + 75,
                                              width / (num_arrows + 1) * (a + 1) - 7, end_arrow + 105, arrow=tk.LAST)
                    # Arrow to the center right
                    arrow1_canvas.create_line(width / (num_arrows + 1) * (a + 1) + 7, end_arrow + 75,
                                              width / (num_arrows + 1) * (a + 1) + 7, end_arrow + 105, arrow=tk.LAST)

                # sboxes
                # Creating the rectangle with the text
                if ((tpe == "Linear" and trail[r][0] != "inf") or (tpe == "Differential" and probs[r] > 0)):
                    arrow1_canvas.create_rectangle(width / (num_arrows + 1) * (a + 1) - 25, end_arrow + 105,
                                                   width / (num_arrows + 1) * (a + 1) + 25, end_arrow + 155)
                else:
                    arrow1_canvas.create_rectangle(width / (num_arrows + 1) * (a + 1) - 25, end_arrow + 105,
                                                   width / (num_arrows + 1) * (a + 1) + 25, end_arrow + 155,
                                                   outline="red", fill="#ff8080")
                if (tpe == "Linear"):
                    arrow1_canvas.create_text(width / (num_arrows + 1) * (a + 1), end_arrow + 130, text="S")
                    arrow1_canvas.create_text(width / (num_arrows + 1) * (a + 1) - 50, end_arrow + 110,
                                              text=sboxMasks[r][a])
                    arrow1_canvas.create_text(width / (num_arrows + 1) * (a + 1) - 50, end_arrow + 130, text="mask")
                    arrow1_canvas.create_text(width / (num_arrows + 1) * (a + 1) - 50, end_arrow + 150,
                                              text=trail[r][1][a])

                    arrow1_canvas.create_text(width / (num_arrows + 1) * (a + 1) + 50, end_arrow + 110, text="Corr:")
                    if (trail[r][2][a] == "inf"):
                        rc = "inf"
                    else:
                        rc = round(trail[r][2][a], 2)
                    arrow1_canvas.create_text(width / (num_arrows + 1) * (a + 1) + 50, end_arrow + 130, text=rc)
                # Print the before and after the substitution happens
                if (tpe == "Differential"):
                    w = ""
                    if (r == 0):
                        #print(len(inputString))
                        w = inputString[a]
                    else:
                        w = trail[r - 1][a]
                    sus, discard = diff.doSbox(w, 1, ddft)
                    arrow1_canvas.create_text(width / (num_arrows + 1) * (a + 1), end_arrow + 130,
                                              text=(str(w) + "\nS\n" + str(svalues[r][a])))

                # First arrow
                if ((tpe == "Differential" and bin[pBox[4 * a]] == 0) or (
                        tpe == "Linear" and (trail[r][1][a])[0] == '0')):
                    arrow1_canvas.create_line(width / (num_arrows + 1) * (a + 1) - 20, end_arrow + 155,
                                              positions_x[pBox[4 * a]], end_arrow + 325, arrow=tk.LAST, fill='blue')
                else:
                    arrow1_canvas.create_line(width / (num_arrows + 1) * (a + 1) - 20, end_arrow + 155,
                                              positions_x[pBox[4 * a]], end_arrow + 325, arrow=tk.LAST, fill='red')
                # Second arrow
                if ((tpe == "Differential" and bin[pBox[4 * a + 1]] == 0) or (
                        tpe == "Linear" and (trail[r][1][a])[1] == '0')):
                    arrow1_canvas.create_line(width / (num_arrows + 1) * (a + 1) - 7, end_arrow + 155,
                                              positions_x[pBox[4 * a + 1]], end_arrow + 325, arrow=tk.LAST, fill='blue')
                else:
                    arrow1_canvas.create_line(width / (num_arrows + 1) * (a + 1) - 7, end_arrow + 155,
                                              positions_x[pBox[4 * a + 1]], end_arrow + 325, arrow=tk.LAST, fill='red')
                # Third arrow
                if ((tpe == "Differential" and bin[pBox[4 * a + 2]] == 0) or (
                        tpe == "Linear" and (trail[r][1][a])[2] == '0')):
                    arrow1_canvas.create_line(width / (num_arrows + 1) * (a + 1) + 7, end_arrow + 155,
                                              positions_x[pBox[4 * a + 2]], end_arrow + 325, arrow=tk.LAST, fill='blue')
                else:
                    arrow1_canvas.create_line(width / (num_arrows + 1) * (a + 1) + 7, end_arrow + 155,
                                              positions_x[pBox[4 * a + 2]], end_arrow + 325, arrow=tk.LAST, fill='red')
                # Fourth arrow:
                if ((tpe == "Differential" and bin[pBox[4 * a + 3]] == 0) or (
                        tpe == "Linear" and (trail[r][1][a])[3] == '0')):
                    arrow1_canvas.create_line(width / (num_arrows + 1) * (a + 1) + 20, end_arrow + 155,
                                              positions_x[pBox[4 * a + 3]], end_arrow + 325, arrow=tk.LAST, fill='blue')
                else:
                    arrow1_canvas.create_line(width / (num_arrows + 1) * (a + 1) + 20, end_arrow + 155,
                                              positions_x[pBox[4 * a + 3]], end_arrow + 325, arrow=tk.LAST, fill='red')

            # output box
            arrow1_canvas.create_rectangle((width / 35), end_arrow + 325, (width - width / 35), end_arrow + 375)
            end_arrow = end_arrow + 300

            # If it's not the last one, then draw the XOR and put the entering values
            if (r != num_rounds - 1):
                # xor
                arrow1_canvas.create_oval(width / 20 - 15, end_arrow + 35, width / 20 + 15, end_arrow + 65)
                arrow1_canvas.create_line(width / 20 - 15, end_arrow + 50, width / 20 + 15, end_arrow + 50)
                arrow1_canvas.create_line(width / 20, end_arrow + 35, width / 20, end_arrow + 65)
                arrow1_canvas.create_line((width / 40) - 15, end_arrow + 50, (width / 40), end_arrow + 50,
                                          arrow=tk.LAST)
                arrow1_canvas.create_text((width / 40) - 20, end_arrow + 50, text="k" + str(r + 1))

                # The text with the round
                if (tpe == "Differential"):
                    # print(probs[r])
                    if (probs[r] > 0):
                        pr = Decimal(math.log2(probs[r]))
                        arrow1_canvas.create_text(width / 2 + 100, end_arrow + 50,
                                                  text=(diff.vals_string(trail[r]) + " P (log2)= " + str(round(pr, 3))))
                    else:
                        arrow1_canvas.create_text(width / 2 + 100, end_arrow + 50, text="Not possible")
                    # probability up to this point
                    prob_here = 1
                    for i in range(r + 1):
                        prob_here = prob_here * probs[i]
                    if (prob_here > 0):
                        prb = Decimal(math.log2(prob_here))
                        # print(prob_here)
                        arrow1_canvas.create_text(19 * width / 20, end_arrow + 50, text=(str(round(prb, 3))))
                    else:
                        arrow1_canvas.create_text(19 * width / 20, end_arrow + 50, text="Not possible")

                    # arrow1_canvas.create_text(width/3, end_arrow+50, text="Button")
                    # edit = tk.Button(arrow1_canvas)
                    # edit.place(x=19*width/20, y=end_arrow+50)
                    # edit.pack()

                    button1 = tk.Button(master=arrow1_canvas, text="Edit round", anchor=tk.W,
                                        command=lambda r=r: diff_edition(wdw, r, sBox, pBox, numOfRounds, trail, probs,
                                                                         inputString, svalues))
                    button1_window = arrow1_canvas.create_window(width / 3 - 15, end_arrow + 39, anchor=tk.NW,
                                                                 window=button1)

                if (tpe == "Linear"):
                    # TODO stop text moving
                    if (totalCorr == "inf"):
                        arrow1_canvas.create_text(width / 2 + 110, end_arrow + 50, text="correlation of round: inf")
                        pMask = ''.join(sboxMasks[r + 1])
                        arrow1_canvas.create_text(width / 2 - 150, end_arrow + 50, text="Permuted mask " + str(pMask))
                    else:
                        arrow1_canvas.create_text(width / 2 + 110, end_arrow + 50,
                                                  text="correlation of round: " + str(round(trail[r + 1][0], 2)))
                        pMask = ''.join(sboxMasks[r + 1])
                        arrow1_canvas.create_text(width / 2 - 150, end_arrow + 50, text="Permuted mask " + str(pMask))

                    for i in range(4):
                        button1 = tk.Button(master=arrow1_canvas, text="Edit", anchor=tk.W,
                                            command=lambda r=r, i=i: lin_edition(wdw, r + 1, i, sBox, pBox, numOfRounds,
                                                                                 trail, sboxMasks, totalCorr,
                                                                                 inputString))
                        button1.pack()
                        button1_window = arrow1_canvas.create_window(width / (num_arrows + 1) * (i + 1) - 120,
                                                                     end_arrow + 100, anchor=tk.NW, window=button1)


            else:

                if (tpe == "Differential"):
                    pr =0
                    if not probs[r] == 0:
                        pr = Decimal(math.log2(probs[r]))
                    arrow1_canvas.create_text(width / 2, end_arrow + 50, text=(
                                diff.vals_string(trail[r]) + " with probability (log2) " + str(round(pr, 3))))
                    prob_here = 1
                    for i in range(r + 1):
                        prob_here = prob_here * probs[i]

                    if prob_here > 0:
                        prb = Decimal(math.log2(prob_here))
                    else:
                        prb = 0
                    # print(prob_here)
                    arrow1_canvas.create_text(19 * width / 20, end_arrow + 50, text=(str(round(prb, 3))))
                    # print(prob_fin)
                    if (prob_fin < 0):
                        # print("final prob", prob_fin)
                        arrow1_canvas.create_text(width / 2, end_arrow + 100, text=(
                                    "An attack would be efficient until round " + str(
                                len(trail)) + " with probability (log2) " + str(prob_fin)))
                    else:
                        arrow1_canvas.create_text(width / 2, end_arrow + 100,
                                                  text="No attack is possible with these settings as they are not possible")
                    if (prob_here > 0):
                        arrow1_canvas.create_text(width / 2, end_arrow + 120, text=(
                                    "The attack complexity in this number of rounds would be 2^" + str(
                                -math.log2(prob_here))))
                    else:
                        arrow1_canvas.create_text(width / 2, end_arrow + 120,
                                                  text="No attack is possible with these settings, so no complexity can be calculated")

                if (tpe == "Linear"):
                    # TODO stop text moving
                    stop_prop = math.log(2.0 ** (-(16 / 2)), 2.0)
                    if (totalCorr == "inf"):
                        arrow1_canvas.create_text(width / 2, end_arrow + 50, text="Total correlation: inf")
                        # output
                        m = ''.join(sboxMasks[-1])
                        arrow1_canvas.create_text(width / 2, end_arrow + 100, text="Output Mask: " + str(m))
                    else:
                        if (totalCorr < stop_prop):
                            arrow1_canvas.create_text(width / 2, end_arrow + 50, text="Total correlation: " + str(
                                round(totalCorr,
                                      2)) + " This is not an efficient attack, the correlation is lower than " + str(
                                stop_prop))
                        else:
                            arrow1_canvas.create_text(width / 2, end_arrow + 50,
                                                      text="Total correlation: " + str(round(totalCorr, 2)))
                        # output
                        m = ''.join(sboxMasks[-1])
                        arrow1_canvas.create_text(width / 2, end_arrow + 100, text="Output Mask: " + str(m))
                        complexity = ((2 ** totalCorr) ** (-2.0))
                        complexity = math.log(complexity, 2)
                        arrow1_canvas.create_text(width / 2, end_arrow + 130, text="Complexity " + str(complexity))

                end_y = (r + 1) * end_arrow + 200

    arrow1_canvas = tk.Canvas(wdw, yscrollcommand=scrollbar.set)
    arrow1_canvas.pack(fill=tk.BOTH, expand=1)
    arrow1_canvas.configure(scrollregion=arrow1_canvas.bbox("all"))

    arrow1_canvas.bind("<Configure>",
                       lambda event, num_arrows=sBoxes, num_rounds=numOfRounds: update_scrollregion(event, sBoxes,
                                                                                                    numOfRounds, wdw,
                                                                                                    arrow1_canvas))
    scrollbar.config(command=arrow1_canvas.yview)
    wdw.mainloop()
