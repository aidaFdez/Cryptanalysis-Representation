from tkinter import *
from tkinter.ttk import *
import visual
import sys
import re
import numpy as np
import diff
import trails
#from sage.all import *



if __name__ == "__main__":
    args = sys.argv
    if len(args)>1:
        if args[1] == "present":
            print("hey")

            pbox = [x%63 for x in (np.arange(64)*16)]
            pbox[63] = 63
            print(pbox)
            inputString = "4004000000000000"
            visual.visual(inputString, 2, 30, len(inputString), [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2], pbox, "Differential", True, [], [], 1, [])
            exit()

        if args[1] == "check_trail_present":
            print("Checking trail for PRESENT")
            sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]

            #Trail from the
            pbox = [x % 63 for x in (np.arange(64) * 16)]
            pbox[63] = 63
            print(pbox)
            print(diff.check_trail(trails.trail_diff2, sbox, pbox, False))
            exit()

        if args[1] == "check_trail_gift":
            print("Checking trail for GIFT")
            sbox = [1,10,4,12,6,15,3,9,2,13,11,7,5,0,8,14]
            pbox = [0,17,34,51,48,1,18,35,32,49,2,19,16,33,50,3,
                    4,21,38,55,52,5,22,39,36,53,6,23,20,37,54,7,
                    8,25,42,59,56,9,26,43,40,57,10,27,24,41,58,11,
                    12,29,46,63,60,13,30,47,44,61,14,31,28,45,62,15]
            visual.visual("0000000000001010", 2, 30, 16, sbox,
                          pbox, "Differential", True, [], [], 1, [])
            print(diff.check_trail(trails.trail_gift1, sbox, pbox, True))
            exit()


root =Tk()
root.title("Cryptanalysis")
root.geometry("1000x500")

def update_scrollregion(event):
    wdw.configure(scrollregion=window.bbox("all"))

photoFrame = Frame(root, width=1550, height=500)
photoFrame.grid()
photoFrame.rowconfigure(0, weight=1)
photoFrame.columnconfigure(0, weight=1)

wdw = Canvas(photoFrame, height=500, width = 1000 )
wdw.grid(row=0, column=0, sticky="nsew")

window = Frame(wdw,width=1550, height=400 )
wdw.create_window(0, 0, window=window, anchor='nw')

photoScroll = Scrollbar(photoFrame, orient=HORIZONTAL)
photoScroll.config(command=wdw.xview)
wdw.config(xscrollcommand=photoScroll.set)
photoScroll.grid(row=1, column=0, sticky="we")

window.bind("<Configure>", update_scrollregion)



#GUI for choosing the kind of cryptanalysis
messKind = Label(window, text="Choose type of attack")
messKind.grid(column = 0, row  = 0)
type = StringVar()
linear = Radiobutton(window, text ="Linear       ", value = "Linear", variable = type)
differential = Radiobutton(window, text ="Differential", value = "Differential", variable = type)
differential.grid(column = 0, row = 1)
linear.grid(column = 0, row = 2)

#choosing number of rounds
rounds = IntVar(window)
choices = (2, 2,3,4,5,6,7,8,9,10)
popupMenu = OptionMenu(window,rounds, *choices)
Label(window, text="Choose the number of rounds").grid(row = 3, column=0)
popupMenu.grid(row = 4, column = 0)

#Getting the input
Label(window, text="Write input difference/mask").grid(row = 5, column=0)
input = Entry(window, width = 10)
input.grid(row = 6, column=0)

#choosing number of S-box
sbox = []
entries = []
entry_titles = []
for i in range(1,17):
    Label(window, text = i-1, relief=RIDGE, width=10).grid(row = 11, column=i)
    ent = Entry(window, width = 10)
    ent.grid(row = 12, column=i)
    entries.append(ent)

#pBox
pBox = []
pentry_titles = []

def createPbox(self):
    j =0
    #delete all of previous ones
    for et in pentry_titles[:]:
        et.grid_forget()
        pentry_titles.remove(et)
    for en in pBox[:]:
        en.grid_forget()
        pBox.remove(en)

    while j<4*boxes.get(): # for any number
        et = Label(window, text = j, relief=RIDGE, width=10)
        et.grid(row = 14, column=j+1)
        pentry_titles.append(et)
        ent = Entry(window, width = 10)
        ent.grid(row = 15, column=j+1)
        pBox.append(ent)
        j +=1

Label(window,text = "x", relief=RIDGE, width=10).grid(row = 14, column=0)

Label(window, text = "P[x]", relief=RIDGE, width=10).grid(row = 15, column=0)

boxes = IntVar(window)
box_choices = (0,1,2,3,4,5)
 #SAVE THIS FOR ANY NUMBER BOXES
boxpopupMenu = OptionMenu(window, boxes, *box_choices, command = createPbox)
Label(window, text="Choose the length of permutation box").grid(row = 9, column=0)
boxpopupMenu.grid(row = 10, column = 0)

#create S-box tables
height = 2
width = 8
cells = {}
table = Frame(window)

Label(window,text = "x", relief=RIDGE, width=10).grid(row = 11, column=0)

Label(window,text = "S[x]", relief=RIDGE, width=10).grid(row = 12, column=0)


def printSbox():
    for en in entries:
        number = en.get()

def popupmsg(msg):
    popup = Tk()
    popup.wm_title("ERROR")
    label = Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def creatediff():
    sBox = [6,4,12,5,0,7,2,14,1,15,3,13,8,10,9,11]
    pBox =[0,4,8,12,1,5,9,13,2,6,10,14,3,7,11, 15]
    #pBox = [0,1,2,3,4,5,6,7,8,9,10,11]

    pbox = [x % 63 for x in (np.arange(64) * 16)]
    pbox[63] = 63
    print(pbox)
    inputString = "0700000000000700"
    visual.visual(inputString, 2, 30, len(inputString), [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2], pbox,
                  "Differential", True, [], [], 1, [])
    #visual.visual("000f", 2, 5,len("000f") , sBox, pBox, "Differential", True, [],[],1, [])
    #exit()
def createlin():
    sBox = [15,14,11,12,6,13,7,8,0,3,9,10,4,2,1,5]
    pBox =[11,12,15,6,0,9,5,3,4,14,8,7,10,1,2,13]
    visual.visual("0000110011110011", 2, 6 , 4, sBox, pBox, "Linear", True, [],[],1, [])
    #exit()

def create():
    #Get the input string
    inputString = input.get()

    #check linear/differential selected
    if(not type.get()):
        popupmsg("Please select the type of cryptanalysis you want to use")
        return

    #check written fields not blank
    if (inputString == ""):
        popupmsg("You have a blank input field")
        return
    pattern = re.compile("([abcdefABCDEF][0-9])*")
    if (type.get() == "Differential" and not(pattern.match(inputString))):
        popupmsg("A hexadecimal string is required for Differential Cryptanalysis, of the type \"0a3d\"")
        return

    if (type.get() == "Linear" and (len(inputString) != 16 or not(all(c in '01' for c in str(inputString))))):
        popupmsg("A 16 bit binary string is required for Linear Cryptanalysis")
        return
    #NOT DELETE needed for any number boxes
    if (int(boxes.get()) == 0):
       popupmsg("Please select the number of P-boxes")
       return
    if (type.get() == "Differential" and not(len(inputString) == int(boxes.get()))):
       popupmsg("The number of P-boxes has to be 4 times the length of the input")
       return
    if (type.get() == "Linear" and not(len(inputString) == 16)):
       popupmsg("The number of P-boxes has to be the same size as the S-box for a linear cryptanalysis")
       return
    #Get the pBox
    pbox = []
    for en in pBox:
        #checks to correct values
        if(en.get() == ""):
            popupmsg("Empty P-box value")
        #NOT DELETE
        if (int(en.get()) < 0 or int(en.get()) > 4*int(boxes.get())):
           popupmsg("pbox values out of range, these must be from 0 to " + str(4*int(boxes.get())))
           return
        if (int(en.get()) in pbox):
            popupmsg("Repeated pbox values")
            return
        pbox.append(int(en.get()))

    #Get the sbox
    sbox = []

    for en in entries:
        #checks for correct values
        if(en.get() == ""):
            popupmsg("Empty S-box value")
        if (int(en.get()) < 0 or int(en.get()) > 15):
            popupmsg("sbox values out of range")
            return
        if (int(en.get()) in sbox):
            popupmsg("Repeated sbox values")
            return
        sbox.append(int(en.get()))

    if(type.get() == "Linear") :
        visual.visual(inputString, 2, rounds.get(), int(len(inputString)/4), sbox, pbox, type.get(), True, [],[],1, [])
    if(type.get() == "Differential") :
        visual.visual(inputString, 2, rounds.get(), len(inputString), sbox, pbox, type.get(), True, [],[],1, [])

generateButton = Button(window, text = "Generate", command = create)
generateButton.grid(row = 16, column = 0)

generateDifferential = Button(window, text = "Default Differential Trail", command = creatediff)
generateDifferential.grid(row = 17, column = 0)

generateLinear = Button(window, text = "Default Linear Trail", command = createlin)
generateLinear.grid(row = 18, column = 0)



def show_trail_present():
    sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]

    # Trail from the
    pbox = [x % 63 for x in (np.arange(64) * 16)]
    pbox[63] = 63
    print(pbox)
    visual.visual("0000000000000011", 2, 30, 16, sbox,
                  pbox, "Differential", True, [], [], 1, [])
    exit()

def show_trail_gift():
    sbox = [1, 10, 4, 12, 6, 15, 3, 9, 2, 13, 11, 7, 5, 0, 8, 14]
    pbox = [0, 17, 34, 51, 48, 1, 18, 35, 32, 49, 2, 19, 16, 33, 50, 3,
            4, 21, 38, 55, 52, 5, 22, 39, 36, 53, 6, 23, 20, 37, 54, 7,
            8, 25, 42, 59, 56, 9, 26, 43, 40, 57, 10, 27, 24, 41, 58, 11,
            12, 29, 46, 63, 60, 13, 30, 47, 44, 61, 14, 31, 28, 45, 62, 15]

    visual.visual("0000000000001010", 2, 30, 16, sbox,
                  pbox, "Differential", True, [], [], 1, [])

    exit()

def default_diff_trail():
    print("Checking trail for PRESENT")
    popup = Tk()
    popup.wm_title("PRESENT trail")
    sbox = [12, 5, 6, 11, 9, 0, 10, 13, 3, 14, 15, 8, 4, 7, 1, 2]
    # Trail from the
    pbox = [x % 63 for x in (np.arange(64) * 16)]
    pbox[63] = 63
    print(pbox)
    pr = diff.check_trail(trails.trail_diff2, sbox, pbox, False)
    message = "This trail is not possible"
    if not pr == 0:
        message = "The probability of this trail is " + str(pr)
    label = Label(popup, text=str(message))
    label.pack()

    print("*************************************"+str(pr))
    B1 = Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    B2 = Button(popup, text="Visualise", command=show_trail_present)
    B2.pack()
    #visual.visual("0000000000000011", 2, 30, 16, sbox,
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

    message = "This trail is not possible"
    if not pr == 0:
        message = "The probability of this trail is " + str(pr)
    label = Label(popup, text=str(message))
    label.pack()
    print("*************************************"+str(pr))
    B1 = Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    B2 = Button(popup, text="Visualise", command=show_trail_gift)
    B2.pack()

    popup.mainloop()
    exit()



default_diff_trail_button = Button(window, text = "Default GIFT/PRESENT trail", command  = default_diff_trail)
default_diff_trail_button.grid(row=20, column=0)

check_diff_trail_button = Button(window, text = "Input differential trail", command  = check_diff_trail)
check_diff_trail_button.grid(row=19, column=0)

root.mainloop()

