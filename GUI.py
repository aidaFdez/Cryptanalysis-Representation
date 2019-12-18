from tkinter import *
from tkinter.ttk import *
import visual
import sys


if __name__ == '__main__':
    print("ENTERED")
    #Pass the differential values automatically, no need to input them everytime.
    if len(sys.argv)>1:
        if sys.argv[1] == "diff":
            sBox = [6,4,12,5,0,7,2,14,1,15,3,13,8,10,9,11]
            pBox =[11,12,15,6,0,9,5,3,4,14,8,7,10,1,2,13]
            visual.visual("aa", 2, 2, 4, sBox, pBox, "Differential")

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
Label(window, text="Write input").grid(row = 5, column=0)
input = Entry(window, width = 10)
input.grid(row = 6, column=0)

#choosing number of S-box

sbox = []
entries = []
entry_titles = []
    #while j<boxes.get():
for i in range(1,17):
    Label(text = i-1, relief=RIDGE, width=10).grid(row = 9, column=i)
    #entry_titles.append(et)
    ent = Entry(width = 10)
    ent.grid(row = 10, column=i)
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
        et.grid(row = 12, column=j+1)
        pentry_titles.append(et)
        ent = Entry(width = 10)
        ent.grid(row = 13, column=j+1)
        pBox.append(ent)
        j +=1

Label(text = "x", relief=RIDGE, width=10).grid(row = 12, column=0)

Label(text = "P[x]", relief=RIDGE, width=10).grid(row = 13, column=0)

boxes = IntVar(window)
box_choices = (2,2,3,4,5)
boxpopupMenu = OptionMenu(window, boxes, *box_choices, command = createPbox)
Label(window, text="Choose the number of S-boxes").grid(row = 7, column=0)
boxpopupMenu.grid(row = 8, column = 0)

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

Label(text = "x", relief=RIDGE, width=10).grid(row = 9, column=0)

Label(text = "S[x]", relief=RIDGE, width=10).grid(row = 10, column=0)


def printSbox():
    for en in entries:
        number = en.get()
        if (number != ""):
            print(number)


def create():
    #Get the input string
    inputString = input.get()
    #Get the pBox
    send = []
    for en in pBox:
        send.append(int(en.get()))
    #Get the sbox
    sbox = []
    for en in entries:
        sbox.append(int(en.get()))

    print(type.get())
    visual.visual(inputString, len(inputString), rounds.get(), boxes.get(), sbox, send, type.get())

generateButton = Button(window, text = "Generate", command = create)
generateButton.grid(row = 14, column = 0)

window.mainloop()
