import tkinter as tk

window =tk.Tk()
window.title("Visualisation")
#window.resizable(height = True, width =True)
#window.geometry('300x400')

inputString = "aa"
numOfBits = 8
numOfRounds = 2
sBoxes = 2
sBox = [6,4,'C',5,0,7,2,'E',1,'F',3,'D',8,'A',9,'B']

def configure(event):
    arrow1_canvas.delete("all")
    height = window.winfo_height()
    width = window.winfo_width()
    arrow1_canvas.create_line(width/2,40, width/2,300,arrow=tk.LAST)


input_frame = tk.Frame(width=768, height=576,bg="", master = window, colormap="new")
input_frame.pack()
input_label = tk.Label(input_frame, text="Input = "+ inputString)
input_label.pack()

arrow1_canvas = tk.Canvas()
arrow1_canvas.pack(fill=tk.BOTH, expand = 1)

# height = window.winfo_height()
# width = window.winfo_width()
# print(height)
# print(width)

# arr=arrow1_canvas.create_line(width/2,40, width/2,300,arrow=tk.LAST)
# arrow1_canvas.coords(arr, (384, 40, 384 , 200))
arrow1_canvas.bind("<Configure>", configure)

window.mainloop()