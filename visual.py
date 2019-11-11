import tkinter as tk

window =tk.Tk()
window.title("Visualisation")
#window.resizable(height = True, width =True)
#window.geometry('300x400')
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

inputString = "aa"
numOfBits = 8
numOfRounds = 5
sBoxes = 5
sBox = [6,4,'C',5,0,7,2,'E',1,'F',3,'D',8,'A',9,'B']
pBox =[11,12,15,6,0,9,5,3,4,14,8,7,10,1,2,13,17,16,18,19]
end_y = 0



def configure(event, num_arrows, num_rounds):
    end_arrow= 150
    arrow1_canvas.delete("all")
    height = window.winfo_height()
    width = window.winfo_width()
    length_box =(width-width/5)
    arrow1_canvas.create_text(width/2, 20, text=inputString)
    arrow1_canvas.create_line(width/2,40, width/2,end_arrow,arrow=tk.LAST)
    arrow1_canvas.create_rectangle((width/10), end_arrow+20, (width-width/10), 220)
    positions_x = []
    for a in range(sBoxes):
        positions_x.append(width/(num_arrows+1)*(a+1)-20)
        positions_x.append(width/(num_arrows+1)*(a+1)-7)
        positions_x.append(width/(num_arrows+1)*(a+1)+7)
        positions_x.append(width/(num_arrows+1)*(a+1)+20)

    #print(positions_x)

    #Drawing the xor
    arrow1_canvas.create_oval(width/2-20, end_arrow+25, width/2+20, end_arrow+65)
    arrow1_canvas.create_line(width/2-20,end_arrow+45 , width/2+20, end_arrow+45)
    arrow1_canvas.create_line(width/2,end_arrow+25 , width/2, end_arrow+65)
    arrow1_canvas.create_line((width/10)-15,end_arrow+45, (width/10),end_arrow+45,arrow=tk.LAST)
    arrow1_canvas.create_text((width/10)-20, end_arrow+45, text="k0")

    for r in range(num_rounds):
        for a in range(num_arrows):
            #Arrow to the left
            arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)-20,(r+1)*end_arrow+75, width/(num_arrows+1)*(a+1)-20,(r+1)*end_arrow+105,arrow=tk.LAST)
            #Arrow to the RIGHT
            arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)+20,(r+1)*end_arrow+75, width/(num_arrows+1)*(a+1)+20,(r+1)*end_arrow+105,arrow=tk.LAST)
            #Arrow to the center left
            arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)-7,(r+1)*end_arrow+75, width/(num_arrows+1)*(a+1)-7,(r+1)*end_arrow+105,arrow=tk.LAST)
            #Arrow to the center right
            arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)+7,(r+1)*end_arrow+75, width/(num_arrows+1)*(a+1)+7,(r+1)*end_arrow+105,arrow=tk.LAST)

            #Creating the rectangle with the text
            arrow1_canvas.create_rectangle(width/(num_arrows+1)*(a+1)-25, (r+1)*end_arrow+105, width/(num_arrows+1)*(a+1)+25, (r+1)*end_arrow+155)
            arrow1_canvas.create_text(width/(num_arrows+1)*(a+1), (r+1)*end_arrow+130, text="S")
            #left arrow
            arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)-20,(r+1)*end_arrow+155, positions_x[pBox[4*a]],(r+1)*end_arrow+180,arrow=tk.LAST)
            arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)+20,(r+1)*end_arrow+155, positions_x[pBox[4*a+1]],(r+1)*end_arrow+180,arrow=tk.LAST)
            arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)-7,(r+1)*end_arrow+155, positions_x[pBox[4*a+2]],(r+1)*end_arrow+180,arrow=tk.LAST)

            print(str(4*a+3))
            print("pbox " + str(pBox[4*a+3]))
            print("positions_x "+str(positions_x[pBox[4*a+3]]))
            arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)+7,(r+1)*end_arrow+155, positions_x[pBox[4*a+3]],(r+1)*end_arrow+180,arrow=tk.LAST)
        arrow1_canvas.create_rectangle((width/10), (r+1)*end_arrow+180, (width-width/10), (r+1)*end_arrow+225)

        #If it's not the last one, then draw the XOR
        if (r != num_rounds-1) :
            arrow1_canvas.create_oval(width/2-15, (r+1)*end_arrow+185, width/2+15, (r+1)*end_arrow+215)
            arrow1_canvas.create_line(width/2-15,(r+1)*end_arrow+200 , width/2+15, (r+1)*end_arrow+200)
            arrow1_canvas.create_line(width/2,(r+1)*end_arrow+185 , width/2, (r+1)*end_arrow+215)
            arrow1_canvas.create_line((width/10)-15,(r+1)*end_arrow+200, (width/10),(r+1)*end_arrow+200,arrow=tk.LAST)
            arrow1_canvas.create_text((width/10)-20, (r+1)*end_arrow+200, text="k"+str(r+1))

        else:
            arrow1_canvas.create_text(width/2, (r+1)*end_arrow+200, text="Output")
            end_y = (r+1)*end_arrow+200
    #arrow1_canvas.create_line(width/2,end_y, (width/10),width/2, end_y + 40,arrow=tk.LAST)





#input_frame = tk.Frame(width=768, height=576,bg="", master = window, colormap="new")
#input_frame.pack()
#input_label = tk.Label(input_frame, text="Input = "+ inputString)
#input_label.pack()

arrow1_canvas = tk.Canvas(window, yscrollcommand = scrollbar.set, scrollregion=(0,0,(numOfRounds+1)*200, (numOfRounds+1)*200))
arrow1_canvas.pack(fill=tk.BOTH, expand = 1)

# height = window.winfo_height()
# width = window.winfo_width()
# print(height)
# print(width)

# arr=arrow1_canvas.create_line(width/2,40, width/2,300,arrow=tk.LAST)
# arrow1_canvas.coords(arr, (384, 40, 384 , 200))
#lambda event, a=10, b=20, c=30:
                            #self.rand_func(a, b, c)
#https://stackoverflow.com/questions/7299955/tkinter-binding-a-function-with-arguments-to-a-widget
arrow1_canvas.bind("<Configure>", lambda event, num_arrows = sBoxes, num_rounds=numOfRounds: configure(event,sBoxes, numOfRounds))
scrollbar.config(command=arrow1_canvas.yview)
window.mainloop()
