from tkinter import *
from tkinter.ttk import *

window =Tk()
window.title("Cryptanalysis")

#GUI for choosing the kind of cryptanalysis
messKind = Label(window, text="Choose the kind of cryptanalysis")
messKind.grid(column = 0, row  = 0)
linear = Radiobutton(window, text ="Linear", value = 1)
differential = Radiobutton(window, text ="Differential", value = 2)
differential.grid(column = 0, row = 1)
linear.grid(column = 0, row = 2)

#choosing number of rounds
rounds = IntVar(window)
choices = ('2','3','4','5','6','7','8','9','10')
popupMenu = OptionMenu(window,rounds, *choices)
Label(window, text="Choose the number of rounds").grid(row = 3, column=0)
popupMenu.grid(row = 4, column = 0)

#choosing number of bits
bits = IntVar(window)
bit_choices = ('8','16','32','64')
bitpopupMenu = OptionMenu(window, bits, *bit_choices)
Label(window, text="Choose the number of bits").grid(row = 5, column=0)
bitpopupMenu.grid(row = 6, column = 0)

#choosing number of S-box
boxes = IntVar(window)
box_choices = ('2','3','4','5')
boxpopupMenu = OptionMenu(window, boxes, *box_choices)
Label(window, text="Choose the number of bits").grid(row = 7, column=0)
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

for i in range(1,17):
    Label(text = i-1, relief=RIDGE, width=10).grid(row = 9, column=i)
    Entry(width = 10).grid(row = 10, column=i)
    """cell.grid(row =0,column= i)
for i in range(0,17):
    ent = Entry(table, text="")
    ent.grid(row = 1, column = i)
#table.pack()"""


window.mainloop()
