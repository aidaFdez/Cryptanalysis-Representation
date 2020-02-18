from tkinter import *
from tkinter.ttk import *
import visual
import sys
import re


if __name__ == '__main__':
    print("ENTERED")
    #Pass the differential values automatically, no need to input them everytime.
    if len(sys.argv)>1:
        pBox =[11,12,15,6,0,9,5,3,4,14,8,7,10,1,2,13]
        if sys.argv[1] == "diff":
            sBox = [6,4,12,5,0,7,2,14,1,15,3,13,8,10,9,11]
            pBox =[0,4,8,12,1,5,9,13,2,6,10,14,3,7,11, 15]
            #sBox = [1,2,3,0, 5, 6, 7, 4]
            #pBox = [2,3,0,1, 5, 6, 7, 4, 9, 10, 11, 8]
            #000f
            visual.visual("000f", 2, 3,len("000f") , sBox, pBox, "Differential")
            exit()
        if sys.argv[1] == "lin":
            sBox = [15,14,11,12,6,13,7,8,0,3,9,10,4,2,1,5]
            pBox =[11,12,15,6,0,9,5,3,4,14,8,7,10,1,2,13]
            visual.visual("0000110011110011", 2, 2, 4, sBox, pBox, "Linear")
            exit()


window =Tk()
window.title("Cryptanalysis")

#GUI for choosing the kind of cryptanalysis
messKind = Label(window, text="Choose the kind of cryptanalysis")
messKind.grid(column = 0, row  = 0)
type = StringVar()
linear = Radiobutton(window, text ="Linear", value = "Linear", variable = type)
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
#TODO get the number of bits, the length of the sbox depends on it
sbox = []
entries = []
entry_titles = []
    #while j<boxes.get():
for i in range(1,17):
    Label(text = i-1, relief=RIDGE, width=10).grid(row = 11, column=i)
    #entry_titles.append(et)
    ent = Entry(width = 10)
    ent.grid(row = 12, column=i)
    entries.append(ent)
    #j +=1
    """cell.grid(row =0,column= i)
for i in range(0,17):
    ent = Entry(table, text="")
    ent.grid(row = 1, column = i)
#table.pack()"""

#pBox
pBox = []
pentry_titles = []
    #while j<boxes.get():
"""for i in range(1,4*boxes.get()):
    Label(text = i-1, relief=RIDGE, width=10).grid(row = 12, column=i)
    #entry_titles.append(et)
    ent = Entry(width = 10)
    ent.grid(row = 13, column=i)
    pBox.append(ent.get())"""

def createPbox(self):
    j = 0
    #delete all of previous ones
    for et in pentry_titles[:]:
        et.grid_forget()
        pentry_titles.remove(et)
    for en in pBox[:]:
        en.grid_forget()
        pBox.remove(en)

    while j<4*boxes.get():
        et = Label(text = j, relief=RIDGE, width=10)
        et.grid(row = 14, column=j+1)
        pentry_titles.append(et)
        ent = Entry(width = 10)
        ent.grid(row = 15, column=j+1)
        pBox.append(ent)
        j +=1

Label(text = "x", relief=RIDGE, width=10).grid(row = 14, column=0)

Label(text = "P[x]", relief=RIDGE, width=10).grid(row = 15, column=0)

boxes = IntVar(window)
box_choices = (0,2,3,4,5)
boxpopupMenu = OptionMenu(window, boxes, *box_choices, command = createPbox)
Label(window, text="Choose the length of permutation box").grid(row = 9, column=0)
boxpopupMenu.grid(row = 10, column = 0)

#create S-box tables
height = 2
width = 8
cells = {}
#for i in range(height): #rows
#    for j in range(width): #columns
#        b = Entry(window, text="")
#        b.grid(row = i+9, column = j )
#        cells[(i,j)]=b
table = Frame(window)

Label(text = "x", relief=RIDGE, width=10).grid(row = 11, column=0)

Label(text = "S[x]", relief=RIDGE, width=10).grid(row = 12, column=0)


def printSbox():
    for en in entries:
        number = en.get()
        #if (number != ""):
            #print(number)

def popupmsg(msg):
    popup = Tk()
    popup.wm_title("ERROR")
    label = Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()


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
        popupmsg("A hexadecimal string is required for Differential Cryptanalysis")
        return

    if (type.get() == "Linear" and (len(inputString) != 16 or not(all(c in '01' for c in str(inputString))))):
        popupmsg("A 16 bit binary string is required for Linear Cryptanalysis")
        return

    if (int(boxes.get()) == 0):
        popupmsg("Please select the number of P-boxes")
        return
    if (type.get() == "Differential" and not(len(inputString) == int(boxes.get()))):
        popupmsg("The number of P-boxes has to be 4 times the length of the input")
        return
    if (type.get() == "Linear" and not(len(inputString) == 16)):
        popupmsg("The number of P-boxes has to be the same size as the S-box")
        return
    #Get the pBox
    send = []
    for en in pBox:
        #checks to correct values
        if(en.get() == ""):
            popupmsg("Empty P-box value")
        if (int(en.get()) < 0 or int(en.get()) > 4*int(boxes.get())):
            popupmsg("pbox values out of range")
            return
        if (int(en.get()) in send):
            popupmsg("Repeated pbox values")
            return
        send.append(int(en.get()))

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


    #inset output string TODO
    print(type.get())
    if(type.get() == "Linear") :
        visual.visual(inputString, 2, rounds.get(), int(len(inputString)/4), sbox, send, type.get())
    if(type.get() == "Differential") :
        visual.visual(inputString, 2, rounds.get(), len(inputString), sbox, send, type.get())

generateButton = Button(window, text = "Generate", command = create)
generateButton.grid(row = 16, column = 0)

window.mainloop()
