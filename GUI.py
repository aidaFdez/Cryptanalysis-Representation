from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import visual
import sys
import re
import numpy as np
import diff
import trails
import cipher
import math
import os
import json
import visual_des

# from sage.all import *


if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        if args[1] == "present":
            print("hey")

            pbox = [x % 63 for x in (np.arange(64) * 16)]
            pbox[63] = 63
            print(pbox)
            input_string = "4004000000000000"
            visual.visual(input_string, 2, 30, len(input_string), [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2],
                          pbox, "Differential", True, [], [], 1, [])
            exit()

        if args[1] == "check_trail_present":
            print("Checking trail for PRESENT")
            sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]

            # Trail from the
            pbox = [x % 63 for x in (np.arange(64) * 16)]
            pbox[63] = 63
            print(pbox)
            print(diff.check_trail(trails.trail_diff2, sbox, pbox, False))
            exit()

        if args[1] == "check_trail_gift":
            print("Checking trail for GIFT")
            sbox = [1, 10, 4, 12, 6, 15, 3, 9, 2, 13, 11, 7, 5, 0, 8, 14]
            pbox = [0, 17, 34, 51, 48, 1, 18, 35, 32, 49, 2, 19, 16, 33, 50, 3,
                    4, 21, 38, 55, 52, 5, 22, 39, 36, 53, 6, 23, 20, 37, 54, 7,
                    8, 25, 42, 59, 56, 9, 26, 43, 40, 57, 10, 27, 24, 41, 58, 11,
                    12, 29, 46, 63, 60, 13, 30, 47, 44, 61, 14, 31, 28, 45, 62, 15]

            pbox2 = [0, 17, 34, 51, 48, 1, 18, 35, 32, 49, 2, 19, 16, 33, 50, 3,
                     4, 21, 38, 55, 52, 5, 22, 39, 36, 53, 6, 23, 20, 37, 54, 7,
                     8, 25, 42, 59, 56, 9, 26, 43, 40, 57, 10, 27, 24, 41, 58, 11,
                     12, 29, 46, 63, 60, 13, 30, 47, 44, 61, 14, 31, 28, 45, 62, 15]
            pbox3 = [63 - x for x in pbox2]
            # pbox3.reverse()

            pbox4 = [0, 33, 66, 99, 96, 1, 34, 67, 64, 97, 2, 35, 32, 65, 98, 3,
                     4, 37, 70, 103, 100, 5, 38, 71, 68, 101, 6, 39, 36, 69, 102, 7,
                     8, 41, 74, 107, 104, 9, 42, 75, 72, 105, 10, 43, 40, 73, 106, 11,
                     12, 45, 78, 111, 108, 13, 46, 79, 76, 109, 14, 47, 44, 77, 110, 15,
                     16, 49, 82, 115, 112, 17, 50, 83, 80, 113, 18, 51, 48, 81, 114, 19,
                     20, 53, 86, 119, 116, 21, 54, 87, 84, 117, 22, 55, 52, 85, 118, 23,
                     24, 57, 90, 123, 120, 25, 58, 91, 88, 121, 26, 59, 56, 89, 122, 27,
                     28, 61, 94, 127, 124, 29, 62, 95, 92, 125, 30, 63, 60, 93, 126, 31]

            print(pbox3)
            # visual.visual("[0c00000000600000", 6, 30, 16, sbox,
            #              pbox3, "Differential", True, [], [], 1, [])
            # pbox.reverse()
            # print(pbox)
            # visual.visual("0c00000000600000", 10, 30, 16, sbox,
            #              pbox, "Differential", True, [], [], 1, [])
            print(diff.check_trail(trails.trail_gift1, sbox, pbox, False))
            exit()

        if args[1] == "check_des":
            print("Checking for DES")
            trail = trails.trail_des1
            des = cipher.DESDifferential()
            print(des.check_trail(trail))
            exit()
        if args[1] == "sboxes_fun":
            trail = trails.trail_des2
            des = cipher.DESDifferential()
            des.sboxes_fun()
            exit()


# Create the window with the input for all linear and differential


def create_own():
    n_root = Toplevel()

    def update_scrollregion(event):
        wdw.configure(scrollregion=window.bbox("all"))

    photo_frame = Frame(n_root, width=1550, height=500)
    photo_frame.grid()
    photo_frame.rowconfigure(0, weight=1)
    photo_frame.columnconfigure(0, weight=1)

    wdw = Canvas(photo_frame, height=500, width=1000)
    wdw.grid(row=0, column=0, sticky="nsew")

    window = Frame(wdw, width=1550, height=400)
    wdw.create_window(0, 0, window=window, anchor='nw')

    photo_scroll = Scrollbar(photo_frame, orient=HORIZONTAL)
    photo_scroll.config(command=wdw.xview)
    wdw.config(xscrollcommand=photo_scroll.set)
    photo_scroll.grid(row=1, column=0, sticky="we")

    window.bind("<Configure>", update_scrollregion)

    # GUI for choosing the kind of cryptanalysis
    mess_kind = Label(window, text="Choose type of attack")
    mess_kind.grid(column=0, row=0)
    tpe = StringVar()
    linear = Radiobutton(window, text="Linear       ", value="Linear", variable=tpe)
    differential = Radiobutton(window, text="Differential", value="Differential", variable=tpe)
    differential.grid(column=0, row=1)
    linear.grid(column=0, row=2)

    # choosing number of rounds
    rounds = IntVar(window)
    choices = (2, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    popup_menu = OptionMenu(window, rounds, *choices)
    Label(window, text="Choose the number of rounds").grid(row=3, column=0)
    popup_menu.grid(row=4, column=0)

    # Getting the input
    Label(window, text="Write input difference/mask").grid(row=5, column=0)
    input = Entry(window, width=10)
    input.grid(row=6, column=0)

    # choosing number of S-box
    sbox = []
    entries = []
    entry_titles = []
    for i in range(1, 17):
        Label(window, text=i - 1, relief=RIDGE, width=10).grid(row=11, column=i)
        ent = Entry(window, width=10)
        ent.grid(row=12, column=i)
        entries.append(ent)

    # pbox
    pbox = []
    pentry_titles = []

    def createpbox(self):
        j = 0
        # delete all of previous ones
        for et in pentry_titles[:]:
            et.grid_forget()
            pentry_titles.remove(et)
        for en in pbox[:]:
            en.grid_forget()
            pbox.remove(en)

        while j < 4 * boxes.get():  # for any number
            et = Label(window, text=j, relief=RIDGE, width=10)
            et.grid(row=14, column=j + 1)
            pentry_titles.append(et)
            ent = Entry(window, width=10)
            ent.grid(row=15, column=j + 1)
            pbox.append(ent)
            j += 1

    Label(window, text="x", relief=RIDGE, width=10).grid(row=14, column=0)

    Label(window, text="P[x]", relief=RIDGE, width=10).grid(row=15, column=0)

    boxes = IntVar(window)
    box_choices = (0, 1, 2, 3, 4, 5)
    # SAVE THIS FOR ANY NUMBER BOXES
    boxpopup_menu = OptionMenu(window, boxes, *box_choices, command=createpbox)
    Label(window, text="Choose the length of permutation box").grid(row=9, column=0)
    boxpopup_menu.grid(row=10, column=0)

    # create S-box tables
    height = 2
    width = 8
    cells = {}
    table = Frame(window)

    Label(window, text="x", relief=RIDGE, width=10).grid(row=11, column=0)

    Label(window, text="S[x]", relief=RIDGE, width=10).grid(row=12, column=0)

    def printSbox():
        for en in entries:
            number = en.get()

    def creatediff():
        sBox = [6, 4, 12, 5, 0, 7, 2, 14, 1, 15, 3, 13, 8, 10, 9, 11]
        pbox = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
        # pbox = [0,1,2,3,4,5,6,7,8,9,10,11]

        pbox = [x % 63 for x in (np.arange(64) * 16)]
        pbox[63] = 63
        print(pbox)
        input_string = "0700000000000700"
        visual.visual(input_string, 2, 30, len(input_string), [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2],
                      pbox,
                      "Differential", True, [], [], 1, [])
        # visual.visual("000f", 2, 5,len("000f") , sBox, pbox, "Differential", True, [],[],1, [])
        # exit()

    def createlin():
        sBox = [15, 14, 11, 12, 6, 13, 7, 8, 0, 3, 9, 10, 4, 2, 1, 5]
        pbox = [11, 12, 15, 6, 0, 9, 5, 3, 4, 14, 8, 7, 10, 1, 2, 13]
        visual.visual("0000110011110011", 2, 6, 4, sBox, pbox, "Linear", True, [], [], 1, [])
        # exit()

    def create():
        # Get the input string
        input_string = input.get()

        # check linear/differential selected
        if (not tpe.get()):
            popupmsg("Please select the type of cryptanalysis you want to use")
            return

        # check written fields not blank
        if (input_string == ""):
            popupmsg("You have a blank input field")
            return
        pattern = re.compile("([abcdefABCDEF][0-9])*")
        if (tpe.get() == "Differential" and not (pattern.match(input_string))):
            popupmsg("A hexadecimal string is required for Differential Cryptanalysis, of the type \"0a3d\"")
            return

        if (tpe.get() == "Linear" and (len(input_string) != 16 or not (all(c in '01' for c in str(input_string))))):
            popupmsg("A 16 bit binary string is required for Linear Cryptanalysis")
            return
        # NOT DELETE needed for any number boxes
        if (int(boxes.get()) == 0):
            popupmsg("Please select the number of P-boxes")
            return
        if (tpe.get() == "Differential" and not (len(input_string) == int(boxes.get()))):
            popupmsg("The number of P-boxes has to be 4 times the length of the input")
            return
        if (tpe.get() == "Linear" and not (len(input_string) == 16)):
            popupmsg("The number of P-boxes has to be the same size as the S-box for a linear cryptanalysis")
            return
        # Get the pbox
        pbox2 = []
        for en in pbox:
            # checks to correct values
            if (en.get() == ""):
                popupmsg("Empty P-box value")
            # NOT DELETE
            if (int(en.get()) < 0 or int(en.get()) > 4 * int(boxes.get())):
                popupmsg("pbox values out of range, these must be from 0 to " + str(4 * int(boxes.get())))
                return
            if (int(en.get()) in pbox):
                popupmsg("Repeated pbox values")
                return
            print("adding", int(en.get()))
            pbox2.append(int(en.get()))

        # Get the sbox
        sbox2 = []

        for en in entries:
            # checks for correct values
            if (en.get() == ""):
                popupmsg("Empty S-box value")
            if (int(en.get()) < 0 or int(en.get()) > 15):
                popupmsg("sbox values out of range")
                return
            if (int(en.get()) in sbox):
                popupmsg("Repeated sbox values")
                return
            sbox2.append(int(en.get()))

        print(tpe.get())
        if (tpe.get() == "Linear"):
            visual.visual(input_string, 2, rounds.get(), int(len(input_string) / 4), sbox, pbox, tpe.get(), True, [], [],
                          1, [])
        if (tpe.get() == "Differential"):
            print("absolute pbox", pbox)
            visual.visual(input_string, 2, rounds.get(), len(input_string), sbox2, pbox2, tpe.get(), True, [], [], 1, [])

    generate_button = Button(window, text="Generate", command=create)
    generate_button.grid(row=16, column=0)

    generate_differential = Button(window, text="Default Differential Trail", command=creatediff)
    generate_differential.grid(row=17, column=0)

    generate_linear = Button(window, text="Default Linear Trail", command=createlin)
    generate_linear.grid(row=18, column=0)

    n_root.mainloop()

    # default_diff_trail_button = Button(window, text="Default GIFT/PRESENT trail", command=default_diff_trail)
    # default_diff_trail_button.grid(row=20, column=0)

    # check_diff_trail_button = Button(window, text="Input differential trail", command=check_diff_trail)
    # check_diff_trail_button.grid(row=19, column=0)


def popupmsg(msg):
    popup = Tk()
    popup.wm_title("ERROR")
    label = Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    b1 = Button(popup, text="Okay", command=popup.destroy)
    b1.pack()
    popup.mainloop()


def get_present_data():
    get_data_window = Tk()
    Label(get_data_window, text= "Input the PRESENT difference").grid()

    input_diff = Entry(get_data_window, width=10)
    input_diff.grid()
    Label(get_data_window, text="Input the number of rounds").grid()
    input_rounds = Entry(get_data_window, width=10)
    input_rounds.grid()

    def collect_data():
        in_string = input_diff.get()
        in_rounds = input_rounds.get()
        pattern = re.compile("([abcdefABCDEF][0-9])*")
        if not (pattern.match(in_string)):
            popupmsg("A hexadecimal string is required for Differential Cryptanalysis, of the type \"0a3d\"")
            return
        if not len(in_string)==16:
            popupmsg("The length of the input difference must be 16")
            return
        pattern_numbers = re.compile("[0-9]+")
        if not(pattern_numbers.match(in_rounds)):
            popupmsg("A decimal number is required for the rounds")
            return

        sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
        pbox = [x % 63 for x in (np.arange(64) * 16)]
        pbox[63]=63
        print(in_string)
        in_diff_num = diff.getInts(in_string)
        round_string=""
        for v in in_rounds:
            round_string = round_string+str(v)

        in_r_num = int(round_string)
        print(in_r_num)
        ddt = diff.diffDistTable(sbox)
        trail, probabilities, general_prob, smt = diff.diffTrail(sbox, in_string, ddt, pbox, in_r_num)
        #trail.insert(0, in_diff_num)
        visual.visual(in_string, 2, in_r_num, len(trail[0]), sbox,
                      pbox, "Differential", False, trail, probabilities, math.log2(general_prob), smt, "present")
        #show_trail_present(trail)

    button_sbox = Button(get_data_window, text="Visualise", command=collect_data)
    button_sbox.grid()



def show_trail_present(tr = None):
    sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]

    # Trail from the
    pbox = [x % 63 for x in (np.arange(64) * 16)]
    if tr ==None:
        print("NOOOOOO")
        tr = trails.trail_diff1
    pbox[63] = 63
    #print(pbox)
    string_in = ""
    for val in tr[0]:
        string_in = string_in+str(val)
    print("Input string", string_in)
    svalues= []
    probs =[]
    new_prob = np.prod(probs)
    for i in range(len(tr)-1):
        sval, p = cipher.get_in_between(tr[i], tr[i+1], sbox, pbox)
        print(sval)
        svalues.append(sval)
        probs.append(p)
    print("Probabilities",probs)
    visual.visual(string_in, 2, len(tr)-1, len(tr[0]), sbox,
                  pbox, "Differential", False, tr[1:], probs, math.log2(new_prob), svalues, "present")
    exit()


def get_gift_data():
    get_data_window = Tk()
    Label(get_data_window, text= "Input the GIFT difference").grid()

    input_diff = Entry(get_data_window, width=10)
    input_diff.grid()
    Label(get_data_window, text="Input the number of rounds").grid()
    input_rounds = Entry(get_data_window, width=10)
    input_rounds.grid()

    def collect_data():
        in_string = input_diff.get()
        in_rounds = input_rounds.get()
        pattern = re.compile("([abcdefABCDEF][0-9])*")
        if not (pattern.match(in_string)):
            popupmsg("A hexadecimal string is required for Differential Cryptanalysis, of the type \"0a3d\"")
            return
        if not len(in_string)==16:
            popupmsg("The length of the input difference must be 16")
            return
        pattern_numbers = re.compile("[0-9]+")
        if not(pattern_numbers.match(in_rounds)):
            popupmsg("A decimal number is required for the rounds")
            return

        sbox = [1, 10, 4, 12, 6, 15, 3, 9, 2, 13, 11, 7, 5, 0, 8, 14]
        pbox = [0, 17, 34, 51, 48, 1, 18, 35, 32, 49, 2, 19, 16, 33, 50, 3,
                4, 21, 38, 55, 52, 5, 22, 39, 36, 53, 6, 23, 20, 37, 54, 7,
                8, 25, 42, 59, 56, 9, 26, 43, 40, 57, 10, 27, 24, 41, 58, 11,
                12, 29, 46, 63, 60, 13, 30, 47, 44, 61, 14, 31, 28, 45, 62, 15]
        print(pbox)

        print(in_string)
        in_diff_num = diff.getInts(in_string)
        round_string=""
        for v in in_rounds:
            round_string = round_string+str(v)

        in_r_num = int(round_string)
        print(in_r_num)
        ddt = diff.diffDistTable(sbox)
        trail, probabilities, general_prob, smt = diff.diffTrail(sbox, in_string, ddt, pbox, in_r_num)
        #trail.insert(0, in_diff_num)
        visual.visual(in_string, 2, in_r_num, len(trail[0]), sbox,
                      pbox, "Differential", False, trail, probabilities, math.log2(general_prob), smt, "gift")
        #show_trail_present(trail)

    button_sbox = Button(get_data_window, text="Visualise", command=collect_data)
    button_sbox.grid()


def show_trail_gift(tr):
    sbox = [1, 10, 4, 12, 6, 15, 3, 9, 2, 13, 11, 7, 5, 0, 8, 14]
    pbox_g = [0, 17, 34, 51, 48, 1, 18, 35, 32, 49, 2, 19, 16, 33, 50, 3,
            4, 21, 38, 55, 52, 5, 22, 39, 36, 53, 6, 23, 20, 37, 54, 7,
            8, 25, 42, 59, 56, 9, 26, 43, 40, 57, 10, 27, 24, 41, 58, 11,
            12, 29, 46, 63, 60, 13, 30, 47, 44, 61, 14, 31, 28, 45, 62, 15]

    string_in = ""
    for val in tr[0]:
        string_in = string_in + str(val)
    print("Input string", string_in)
    svalues = []
    probs = []
    new_prob = np.prod(probs)
    for i in range(len(tr) - 1):
        sval, p = cipher.get_in_between(tr[i], tr[i + 1], sbox, pbox_g)
        svalues.append(sval)
        probs.append(p)

    visual.visual(string_in, 2, len(tr) - 1, len(tr[0]), sbox,
                  pbox_g, "Differential", False, tr, probs, math.log2(new_prob), svalues, "gift")

    exit()


def get_des_data():
    get_data_window = Tk()
    Label(get_data_window, text="Input the DES difference").grid()

    input_diff = Entry(get_data_window, width=10)
    input_diff.grid()
    Label(get_data_window, text="Input the number of rounds").grid()
    input_rounds = Entry(get_data_window, width=10)
    input_rounds.grid()

    def collect_data():
        in_string = input_diff.get()
        in_rounds = input_rounds.get()
        pattern = re.compile("([abcdefABCDEF][0-9])*")
        if not (pattern.match(in_string)):
            popupmsg("A hexadecimal string is required for Differential Cryptanalysis, of the type \"0a3d\"")
            return
        if not len(in_string) == 16:
            popupmsg("The length of the input difference must be 16")
            return
        pattern_numbers = re.compile("[0-9]+")
        if not (pattern_numbers.match(in_rounds)):
            popupmsg("A decimal number is required for the rounds")
            return
        print(type(in_string))
        in_nums = cipher.getInts(in_string)
        num_rounds = (int(in_rounds))
        print(type(num_rounds))
        print(in_nums)
        des = cipher.DESDifferential()
        trail, probs = des.get_trail(num_rounds, in_nums)
        des.trail = trail
        des.probabilities = probs
        show_des_trail(des)

    button_sbox = Button(get_data_window, text="Visualise", command=collect_data)
    button_sbox.grid()

def show_des_trail(cip):
    probs = []
    for v in range(len(cip.trail)-1):
        new_trail = [cip.trail[v], cip.trail[v+1]]
        prob_new = cip.check_trail(new_trail)
        probs.append(prob_new)
    cip.probabilities = probs
    visual_des.show_cipher(cip)


def default_diff_trail():
    print("Checking trail for PRESENT")
    trail = trails.trail_diff2
    popup = Tk()
    popup.wm_title("PRESENT trail")
    sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
    # Trail from the
    pbox = [x % 63 for x in (np.arange(64) * 16)]
    pbox[63] = 63
    print(pbox)
    pr = diff.check_trail(trail, sbox, pbox, False)
    message = "This trail is not possible"
    if not pr == 0:
        message = "The probability of this trail is " + str(pr)
    label = Label(popup, text=str(message))
    label.pack()

    print("*************************************" + str(pr))
    b1 = Button(popup, text="Okay", command=popup.destroy)
    b1.pack()
    b2 = Button(popup, text="Visualise", command=lambda trail=trail: show_trail_present(trail))
    b2.pack()
    # visual.visual("0000000000000011", 2, 30, 16, sbox,
    #              pbox, "Differential", True, [], [], 1, [])
    popup.mainloop()
    exit()


def check_diff_trail():
    print("Checking trail for GIFT")
    popup = Tk()
    popup.wm_title("GIFT trail")
    sbox = [1, 10, 4, 12, 6, 15, 3, 9, 2, 13, 11, 7, 5, 0, 8, 14]
    pbox = [0, 17, 34, 51, 48, 1, 18, 35, 32, 49, 2, 19, 16, 33, 50, 3,
            4, 21, 38, 55, 52, 5, 22, 39, 36, 53, 6, 23, 20, 37, 54, 7,
            8, 25, 42, 59, 56, 9, 26, 43, 40, 57, 10, 27, 24, 41, 58, 11,
            12, 29, 46, 63, 60, 13, 30, 47, 44, 61, 14, 31, 28, 45, 62, 15]

    pr = diff.check_trail(trails.trail_gift1, sbox, pbox, True)
    tr = trails.trail_gift1
    message = "This trail is not possible"
    if not pr == 0:
        message = "The probability of this trail is " + str(pr)
    label = Label(popup, text=str(message))
    label.pack()
    print("*************************************" + str(pr))
    b1 = Button(popup, text="Okay", command=popup.destroy)
    b1.pack()
    b2 = Button(popup, text="Visualise", command=lambda tr=tr: show_trail_gift(tr))
    b2.pack()

    popup.mainloop()
    exit()


def load_file():
    current_dir = os.getcwd()
    filename = filedialog.askopenfilename(initialdir=current_dir)
    with open(filename, 'r') as f:
        dic_data = json.load(f)
        f.close()
    tr = dic_data["trail"]
    tp = dic_data["type2"]
    if tp == "present":
        show_trail_present(tr)
    if tp == "gift":
        show_trail_gift(tr)
    if tp == "des":
        des = cipher.DESDifferential(trail = tr)
        des.trail = tr
        show_des_trail(des)
    if tp == "own":
        inputString = dic_data["in_str"]
        numRounds = dic_data["num_rounds"]
        final_probs = dic_data["probs"]
        # print(final_probs)
        fin_prob = dic_data["fin_prob"]
        svalues = dic_data["svalues"]
        visual.visual(inputString, 2, numRounds, len(inputString), dic_data["sbox"], dic_data["pbox"], "Differential", False, tr[1:],
               final_probs, fin_prob, svalues)


# Get the menu window, the initial one
root = Tk()
root.title("Cryptanalysis")
root.geometry("300x200")

frame = Frame(root, width=1550, height=500)
frame.grid()
menu = Canvas(frame, height=500, width=1000)


diff_button = Button(menu, text="Input own Differential", command=create_own)
diff_button.grid(row=1, column=1)

lin_button = Button(menu, text="Input own Linear", command=create_own)
lin_button.grid(row=2, column=1)

gift_button = Button(menu, text="Input GIFT difference", command=get_gift_data)
gift_button.grid(row=3, column=1)

present_button = Button(menu, text="Input PRESENT difference", command=get_present_data)
present_button.grid(row=4, column=1)

des_button = Button(menu, text="Input DES difference", command=get_des_data)
des_button.grid(row=5, column=1)

load_button = Button(menu, text="Load trail", command=load_file)
load_button.grid(row=6, column=1)

#load_button = Button(menu, text="Load GIFT trail", command=load_gift_file)
#load_button.grid(row=6, column=0)

#load_button = Button(menu, text="Load DES trail", command=load_own_differential)
#load_button.grid(row=7, column=0)

#load_button = Button(menu, text="Load DES trail", command=load_des_file)
#load_button.grid(row=8, column=0)

menu.grid()

# create_own()
root.mainloop()
