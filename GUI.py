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



window.mainloop()
