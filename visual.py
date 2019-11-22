import tkinter as tk

#Difference distribution table hardcoded
ddft = [[16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,6,0,0,0,0,2,0,2,0,0,2,0,4,0],
        [0,6,6,0,0,0,0,0,0,0,2,2,0,0,0,0],
        [0,0,0,6,0,2,0,0,2,0,0,0,4,0,2,0],
        [0,0,0,2,0,2,4,0,0,2,2,2,0,0,2,0],
        [0,2,2,0,4,0,0,4,2,0,0,2,0,0,0,0],
        [0,0,2,0,4,0,0,2,2,0,2,2,2,0,0,0],
        [0,0,0,0,0,4,4,0,2,2,2,2,0,0,0,0],
        [0,0,0,0,0,2,0,2,4,0,0,4,0,2,0,2],
        [0,2,0,0,0,2,2,2,0,4,2,0,0,0,0,2],
        [0,0,0,0,2,2,0,0,0,4,4,0,2,2,0,0],
        [0,0,0,2,2,0,2,2,2,0,0,4,0,0,2,0],
        [0,4,0,2,0,2,0,0,2,0,0,0,0,0,6,0],
        [0,0,0,0,0,0,2,2,0,0,0,0,6,2,0,4],
        [0,2,0,4,2,0,0,0,0,0,2,0,0,0,0,6],
        [0,0,0,0,2,0,2,0,0,0,0,0,0,10,0,2]]


def visual(inputString, numOfBits, numOfRounds, sBoxes, sBox, pBox, type):
    print(inputString)

    """def __init__(self,inputString, numOfBits, numOfRounds, sBoxes, sBox, pBox):
        self.inputString = inputString
        self.numOfBits = numOfBits
        self.numOfRounds = numOfRounds
        self.sBoxes = sBoxes
        self.sBox = sBox
        self.pBox = pBox"""
    window =tk.Tk()
    window.title("Visualisation")
#window.resizable(height = True, width =True)
#window.geometry('300x400')
    scrollbar = tk.Scrollbar(window)
    scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

#inputString = "aa"
#numOfBits = 8
#numOfRounds = 5
#sBoxes = 4
#sBox = [6,4,'C',5,0,7,2,'E',1,'F',3,'D',8,'A',9,'B']
#pBox =[11,12,15,6,0,9,5,3,4,14,8,7,10,1,2,13]
    end_y = 0

    def configure(event, num_arrows, num_rounds):
        end_arrow= 150
        arrow1_canvas.delete("all")
        height = window.winfo_height()
        width = window.winfo_width()
        length_box =(width-width/5)
    #input
        arrow1_canvas.create_text(width/2, 20, text=inputString)
        arrow1_canvas.create_line(width/2,40, width/2,end_arrow,arrow=tk.LAST)
        arrow1_canvas.create_rectangle((width/10), end_arrow+20, (width-width/10), 220)
    #calculates permutation of each arrow
        positions_x = []
        for a in range(sBoxes):
            positions_x.append(width/(num_arrows+1)*(a+1)-20)
            positions_x.append(width/(num_arrows+1)*(a+1)-7)
            positions_x.append(width/(num_arrows+1)*(a+1)+7)
            positions_x.append(width/(num_arrows+1)*(a+1)+20)

    #print(positions_x)

        #Drawing the xor for round 1
        arrow1_canvas.create_oval(width/2-20, end_arrow+25, width/2+20, end_arrow+65)
        arrow1_canvas.create_line(width/2-20,end_arrow+45 , width/2+20, end_arrow+45)
        arrow1_canvas.create_line(width/2,end_arrow+25 , width/2, end_arrow+65)
        arrow1_canvas.create_line((width/10)-15,end_arrow+45, (width/10),end_arrow+45,arrow=tk.LAST)
        arrow1_canvas.create_text((width/10)-20, end_arrow+45, text="k0")

        #loop through each round
        for r in range(num_rounds):
            for a in range(num_arrows):
                #arrows to sboxes
                #round 1
                if (r == 0) :
                    #Arrow to the left
                    arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)-20,(r+1)*end_arrow+75, width/(num_arrows+1)*(a+1)-20,(r+1)*end_arrow+105,arrow=tk.LAST)
                    #Arrow to the RIGHT
                    arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)+20,(r+1)*end_arrow+75, width/(num_arrows+1)*(a+1)+20,(r+1)*end_arrow+105,arrow=tk.LAST)
                    #Arrow to the center left
                    arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)-7,(r+1)*end_arrow+75, width/(num_arrows+1)*(a+1)-7,(r+1)*end_arrow+105,arrow=tk.LAST)
                    #Arrow to the center right
                    arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)+7,(r+1)*end_arrow+75, width/(num_arrows+1)*(a+1)+7,(r+1)*end_arrow+105,arrow=tk.LAST)
                #all other rounds
                else:
                    #Arrow to the left
                    arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)-20,end_arrow+75, width/(num_arrows+1)*(a+1)-20,end_arrow+105,arrow=tk.LAST)
                    #Arrow to the RIGHT
                    arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)+20,end_arrow+75, width/(num_arrows+1)*(a+1)+20,end_arrow+105,arrow=tk.LAST)
                    #Arrow to the center left
                    arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)-7,end_arrow+75, width/(num_arrows+1)*(a+1)-7,end_arrow+105,arrow=tk.LAST)
                    #Arrow to the center right
                    arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)+7,end_arrow+75, width/(num_arrows+1)*(a+1)+7,end_arrow+105,arrow=tk.LAST)

                #sboxes
                #Creating the rectangle with the text
                arrow1_canvas.create_rectangle(width/(num_arrows+1)*(a+1)-25, end_arrow+105, width/(num_arrows+1)*(a+1)+25, end_arrow+155)
                arrow1_canvas.create_text(width/(num_arrows+1)*(a+1), end_arrow+130, text="S")

                #arrows from s boxes
                #left arrow
                print("*********************************")
                print(a)
                print(4*a)
                print(pBox[4*a])
                print(positions_x[pBox[4*a]])
                arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)-20,end_arrow+155, positions_x[pBox[4*a]], end_arrow+325,arrow=tk.LAST)
                arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)+20,end_arrow+155, positions_x[pBox[4*a+1]],end_arrow+325,arrow=tk.LAST, fill='green')
                arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)-7,end_arrow+155, positions_x[pBox[4*a+2]],end_arrow+325,arrow=tk.LAST, fill='red')

                #print(str(4*a+3))
                #print("pbox " + str(pBox[4*a+3]))
                #print("positions_x "+str(positions_x[pBox[4*a+3]]))
                arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)+7,end_arrow+155, positions_x[pBox[4*a+3]],end_arrow+325,arrow=tk.LAST,fill='blue')
            #output box
            arrow1_canvas.create_rectangle((width/10), end_arrow+325, (width-width/10), end_arrow+375)
            end_arrow = end_arrow+300

            #If it's not the last one, then draw the XOR
            if (r != num_rounds-1) :
                #xor
                arrow1_canvas.create_oval(width/2-15, end_arrow+35, width/2+15, end_arrow+65)
                arrow1_canvas.create_line(width/2-15,end_arrow+50 , width/2+15, end_arrow+50)
                arrow1_canvas.create_line(width/2,end_arrow+35 , width/2, end_arrow+65)
                arrow1_canvas.create_line((width/10)-15,end_arrow+50, (width/10),end_arrow+50,arrow=tk.LAST)
                arrow1_canvas.create_text((width/10)-20, end_arrow+50, text="k"+str(r+1))

            else:
                #output
                arrow1_canvas.create_text(width/2, end_arrow+50, text="Output")
                end_y = (r+1)*end_arrow+200
                #arrow1_canvas.create_line(width/2,end_y, (width/10),width/2, end_y + 40,arrow=tk.LAST)
                        #input_frame = tk.Frame(width=768, height=576,bg="", master = window, colormap="new")
                        #input_frame.pack()
                        #input_label = tk.Label(input_frame, text="Input = "+ inputString)
                        #input_label.pack()

    arrow1_canvas = tk.Canvas(window, yscrollcommand = scrollbar.set, scrollregion=(0,0,(numOfRounds+1)*300, (numOfRounds+1)*300))
    arrow1_canvas.pack(fill=tk.BOTH, expand = 1)

                        # height = window.winfo_height()
                        # width = window.winfo_width()
                        # print(height)
                        # print(width)

                        # arr=arrow1_canvas.create_line(width/2,40, width/2,300,arrow=tk.LAST)
                        # arrow1_canvas.coords(arr, (384, 40, 384 , 200))
                        #lambda event, a=10, b=20, c=30:
                            #self.rand_func(a, b, c)
                            #https://stackoverflow.com/questions/7299955/tkinter-binding-a-function-with-arguments-to-a-wid
    arrow1_canvas.bind("<Configure>", lambda event, num_arrows = sBoxes, num_rounds=numOfRounds: configure(event,sBoxes, numOfRounds))
    scrollbar.config(command=arrow1_canvas.yview)
    window.mainloop()
