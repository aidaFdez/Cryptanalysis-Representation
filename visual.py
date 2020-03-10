import tkinter as tk
import diff
import lin
import math
from decimal import Decimal
import sys

#Variables to keep the trails and probabilities
trail = []
lintrail = []
probs = []


#Difference distribution table hardcoded
ddft = [[16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,6,0,0,0,0,2,0,2,0,0,2,0,4,0],
        [0,6,6,0,0,0,0,0,0,2,2,0,0,0,0,0],
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

#Linear approximation table hardcoded
lat = [[16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,6,0,10,0,6,12,6,10,12,10,0,6,0,10,0],
        [0,10,6,0,6,0,0,10,10,12,0,10,12,6,6,0],
        [0,12,10,10,6,10,0,0,0,0,10,6,6,6,0,12],
        [0,0,6,10,10,6,0,0,4,0,10,10,10,10,0,12],
        [0,6,10,0,10,12,0,10,6,12,0,6,0,10,6,0],
        [0,6,0,10,0,10,12,10,10,4,10,0,10,0,6,0],
        [0,0,0,0,0,12,0,4,0,0,0,0,12,0,12,0],
        [0,0,6,10,4,0,10,10,4,0,6,6,0,0,10,6],
        [0,6,2,0,0,10,6,0,10,0,0,6,6,0,0,10],
        [0,6,0,2,6,0,10,0,6,0,10,0,0,6,0,10],
        [0,0,0,0,10,6,10,6,0,0,4,4,10,6,6,10],
        [0,0,0,0,6,6,6,6,0,0,12,4,10,10,6,6],
        [0,6,0,10,10,0,6,0,6,0,10,0,0,2,0,6],
        [0,10,6,0,0,10,10,4,6,0,0,10,6,0,4,6],
        [0,4,10,10,4,0,6,6,0,0,6,10,0,0,6,10]]

def showDdft(wn, sbox):
    #Create a new window for the DDFT, on top of the visual one
    ddftWnw = tk.Toplevel(wn)
    fr = tk.Frame(ddftWnw)
    fr.pack()
    ddft2 = diff.diffDistTable(sbox)
    for i in range(16):
        #TODO change colour depending on the row for easiness to read
        row = tk.Label(fr,text = i, relief=tk.RIDGE, width=10, bg = 'gray')
        row.grid(row = 0, column = i+1)
        col = tk.Label(fr,text = i, relief=tk.RIDGE, width=10, bg = 'gray')
        col.grid(row = i+1, column = 0)
        for j in range(16):
            prob = tk.Label(fr,text =ddft2[i][j], relief=tk.RIDGE, width=10)
            if (i % 2 == 0):
                prob = tk.Label(fr,text =ddft2[i][j], relief=tk.RIDGE, width=10)
            else:
                prob = tk.Label(fr,text =ddft2[i][j], relief=tk.RIDGE, width=10, bg = 'LightSkyBlue1')
            prob.grid(row = i+1, column = j+1)
            if not(ddft [i][j] == ddft2[i][j]):
                print("The one in ", i, ", ", j, " is different")
            #print(ddft[i][j])

def showLAT(wn, sbox):
    lanWnw = tk.Toplevel(wn)
    lanfr = tk.Frame(lanWnw)
    lanfr.pack()
    lat2 = lin.linApptable(sbox)
    for i in range(16):
        row = tk.Label(lanfr,text = i, relief=tk.RIDGE, width=10, bg = 'gray')
        row.grid(row = 0, column = i+1)
        col = tk.Label(lanfr,text = i, relief=tk.RIDGE, width=10, bg = 'gray')
        col.grid(row = i+1, column = 0)
        for j in range(16):
            prob = tk.Label(lanfr,text =lat2[i][j], relief=tk.RIDGE, width=10)
            if (i % 2 == 0):
                prob = tk.Label(lanfr,text =lat2[i][j], relief=tk.RIDGE, width=10)
            else:
                prob = tk.Label(lanfr,text =lat2[i][j], relief=tk.RIDGE, width=10, bg = 'LightSkyBlue1')
            prob.grid(row = i+1, column = j+1)

#For popping up useful messages
def popupmsg(title, msg, wn):
    popup = tk.Toplevel(wn)
    popup.wm_title(title)
    label = tk.Label(popup, text=msg)
    fr = tk.Frame(popup)
    fr.pack()
    label.pack(side="top", fill="x", pady=10)

def diff_edition(wn, round, sbox, pbox, numRounds, tr, pbs, inputString):
    #Set up of the window to be used for the input
    edit_window = tk.Toplevel(wn)
    print(round)
    info = tk.Label(edit_window, text="Write new difference")
    info.grid(column = 0, row = 0)
    input = tk.Entry(edit_window)
    input.grid(row = 1, column=0)

    #function to be called by the button to change all the data
    def change():
        new_diff = input.get()
        old_trail = tr
        old_probs = pbs
        #old_prob_fin = diff.diffTrail(sbox, inputString, diff.diffDistTable(sbox), pbox, numRounds)
        #print(new_diff)
        new_round = diff.getInts(new_diff)
        print((old_trail), " This is the old trail")
        old_round = old_trail[round-1]
        print(old_round, " This is the old round")
        print(old_trail[round-1], " This is the previous of the old round")
        #Get the data from the new input
        new_trail, new_probs, new_fin_prob = diff.diffTrail(sbox, new_diff, diff.diffDistTable(sbox), pbox, numRounds)
        print(new_trail, " This is the new trail")
        new_prob = 1
        ddt = diff.diffDistTable(sbox)
        #Calculate the probability with the edited round
        """for i in old_round:
            for j in new_round:"""
        for i in range(4):
            old = old_round[i]
            new = new_round[i]
            pr = ddt[old][new]
            print("Probability of ", old, " to ", new, " is ", pr)
            if(pr == 0):
                print("Probability of ", old, " to ", new, " is 0")
                sys.exit()

            new_prob = new_prob* (pr/16)

        final_trail = []
        final_trail.extend(old_trail[:round])
        final_trail.append(new_round)
        final_trail.extend(new_trail)
        final_probs = []
        final_probs.extend(old_probs[:round])
        final_probs.append(new_prob)
        final_probs.extend(new_probs)
        print(final_probs)
        fin_prob = 1
        for pr in final_probs:
            fin_prob = fin_prob*pr
        visual(inputString, 2, numRounds, len(inputString), sbox, pbox, "Differential", False, final_trail, final_probs, fin_prob)


    bt = tk.Button(edit_window, text = "Ok", command = change)
    bt.grid(row=2, column=0)

def lin_edition(wn, round, sboxnumber, sbox, pbox, numRounds, trail, sboxMasks, totalCorr, inputString):
    #Set up of the window to be used for the input
    edit_window = tk.Toplevel(wn)
    print(round)
    info = tk.Label(edit_window, text="Write new mask")
    info.grid(column = 0, row = 0)
    input = tk.Entry(edit_window)
    input.grid(row = 1, column=0)

    #function to change the linear data
    def change():
        new_inp = input.get()
        print(round)
        #new_mask = 
        #for i in range 
        print(sboxMasks, "sboxMasks")
        #print(trail, "trail")

    bt = tk.Button(edit_window, text = "Ok", command = change)
    bt.grid(row=2, column=0)
        

def calculate_diff(sBox, inputString, pBox, numOfRounds, wdw):
    bt = tk.Button(wdw, text = "Difference distribution table", command = lambda: showDdft(wdw, sBox))
    bt.pack()
    trail, probs, prob_fin = diff.diffTrail(sBox, inputString, diff.diffDistTable(sBox), pBox, numOfRounds)
    #If the number of rounds is more than the one of the trail, then more rounds were chosen than it is worth calculating
    if(len(trail)<numOfRounds):
        prev = numOfRounds
        numOfRounds = len(trail)
        #diff.popup("Number of rounds",("You chose " + str(numOfRounds) + " but it is efficient to calculate up to " + str(len(trail)) + ", so this was used"))
        popupmsg("Number of rounds",("You chose " + str(prev) + " but it is efficient to calculate up to " + str(len(trail)) + ", so this was used"), wdw )
    return trail, probs, prob_fin

def calculate_lin(sBoxes, sBox, inputString, pBox, numOfRounds, wdw):
    bt = tk.Button(wdw, text = "Linear Approximation table", command = lambda: showLAT(wdw, sBox))
    bt.pack()
    trail = []
    sboxMasks = []
    sboxMasks.append([inputString[i:i+4] for i in range(0,len(inputString), 4)])
    for corrPerRound in range(numOfRounds):
        trail.append(lin.linTrail(sBoxes, inputString, lin.linApptable(sBox)))
        for i in range(4):
            get_bin = lambda x, n: format(x, 'b').zfill(n)
            trail[corrPerRound][1][i] = get_bin(trail[corrPerRound][1][i], 4)
        tempMask = ''.join(trail[corrPerRound][1])
        permutedMask = []
        for n in range(len(pBox)):
            permutedMask.append(tempMask[pBox.index(n)])
        inputString = ''.join(permutedMask)
        sboxMasks.append([inputString[i:i+4] for i in range(0,len(inputString), 4)])

    totalCorr = 0
    for r in trail:
        totalCorr = totalCorr + r[0]
    
    return trail, sboxMasks, totalCorr

def visual(inputString, numOfBits, numOfRounds, sBoxes, sBox, pBox, type, first, tr, pbs, p_fin):

    wdw =tk.Tk()

    if(type == "Differential" and first):
        trail, probs, prob_fin = calculate_diff(sBox, inputString, pBox, numOfRounds, wdw)
        print(trail)
    if(type == "Differential" and not first):
        trail = tr
        probs = pbs
        prob_fin = p_fin

        """for i in range(len(trail)):
            print(i," ",trail[i])"""

    """def __init__(self,inputString, numOfBits, numOfRounds, sBoxes, sBox, pBox):
        self.inputString = inputString
        self.numOfBits = numOfBits
        self.numOfRounds = numOfRounds
        self.sBoxes = sBoxes
        self.sBox = sBox
        self.pBox = pBox"""
    # TODO check trail values
    if(type == "Linear" and first):
        trail, sboxMasks, totalCorr = calculate_lin(sBoxes, sBox, inputString, pBox, numOfRounds, wdw)
        #print(trail)
        #print(sboxMasks)
        #print(totalCorr)


    wdw.title("Visualisation")
#wdw.resizable(height = True, width =True)
#wdw.geometry('300x400')
    scrollbar = tk.Scrollbar(wdw)
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
        height = wdw.winfo_height()
        width = wdw.winfo_width()
        length_box =(width-width/5)
    #input
        arrow1_canvas.create_text(width/2, 20, text=inputString)
        arrow1_canvas.create_line(width/2,40, width/2,end_arrow,arrow=tk.LAST)
        arrow1_canvas.create_rectangle((width/10), end_arrow+20, (width-width/10), 220)
        if (type == "Linear"):
            arrow1_canvas.create_text(width/2 + 200, 20, text="Correlations and Complexities\n are in log base 2")
    #calculates permutation of each arrow
        positions_x = []
        for a in range(sBoxes):
            positions_x.append(width/(num_arrows+1)*(a+1)-20)
            positions_x.append(width/(num_arrows+1)*(a+1)-7)
            positions_x.append(width/(num_arrows+1)*(a+1)+7)
            positions_x.append(width/(num_arrows+1)*(a+1)+20)

        #Drawing the xor for round 1
        arrow1_canvas.create_oval(width/2-20, end_arrow+25, width/2+20, end_arrow+65)
        arrow1_canvas.create_line(width/2-20,end_arrow+45 , width/2+20, end_arrow+45)
        arrow1_canvas.create_line(width/2,end_arrow+25 , width/2, end_arrow+65)
        arrow1_canvas.create_line((width/10)-15,end_arrow+45, (width/10),end_arrow+45,arrow=tk.LAST)
        arrow1_canvas.create_text((width/10)-20, end_arrow+45, text="k0")
        #add linear probability for round one
        if(type == "Linear"):
            arrow1_canvas.create_text(width/2+110, end_arrow+45, text=" correlation of round: " + str(round(trail[0][0],2)))


        #loop through each round
        if(num_rounds>len(trail) and type == "Differential"):
            num_rounds = len(trail)
        for r in range(num_rounds):
            #Get the binary stuff for differential:
            if(type == "Differential"):
                bin = []
                #For each value in the trail of this round
                for val in trail[r]:
                    bin.extend(diff.getBinary(val))
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
                if(type == "Linear"):
                    arrow1_canvas.create_text(width/(num_arrows+1)*(a+1), end_arrow+130, text="S")
                    #print(r)
                    #print(sboxMasks[r])
                    arrow1_canvas.create_text(width/(num_arrows+1)*(a+1)-50, end_arrow+110, text=sboxMasks[r][a])
                    arrow1_canvas.create_text(width/(num_arrows+1)*(a+1)-50, end_arrow+130, text="mask")
                    arrow1_canvas.create_text(width/(num_arrows+1)*(a+1)-50, end_arrow+150, text=trail[r][1][a])

                    arrow1_canvas.create_text(width/(num_arrows+1)*(a+1)+50, end_arrow+110, text="Corr:")
                    arrow1_canvas.create_text(width/(num_arrows+1)*(a+1)+50, end_arrow+130, text=trail[r][2][a])
                #Print the before and after the substitution happens
                if(type == "Differential"):
                    w = ""
                    if(r == 0):
                        w = inputString[a]
                    else:
                        w = trail[r-1][a]
                    arrow1_canvas.create_text(width/(num_arrows+1)*(a+1), end_arrow+130, text=( str(w) + "\nS\n" + str(diff.fromBinary([bin[a%4],bin[a%4+4], bin[a%4+8], bin[a%4+12]])[0])))
                #arrows from s boxes
                #left arrow
                #print("*********************************")
                #print(a)
                #print(4*a)
                #print(pBox[4*a])
                #print(positions_x[pBox[4*a]])

                #make green arrows for 0s, red for 1sgit push --set-upstream origin master
                #if(type == "Differential"):

                #First arrow
                if((type == "Differential" and bin[pBox[4*a]] == 0) or (type == "Linear" and (trail[r][1][a])[0] == '0')):
                    arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)-20,end_arrow+155, positions_x[pBox[4*a]], end_arrow+325,arrow=tk.LAST, fill = 'blue')
                else:
                    arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)-20,end_arrow+155, positions_x[pBox[4*a]], end_arrow+325,arrow=tk.LAST, fill = 'red')
                #Second arrow
                if((type == "Differential" and bin[pBox[4*a+1]] == 0) or (type == "Linear" and (trail[r][1][a])[1] == '0')):
                    arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)-7,end_arrow+155, positions_x[pBox[4*a+1]],end_arrow+325,arrow=tk.LAST, fill='blue')
                else:
                    arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)-7,end_arrow+155, positions_x[pBox[4*a+1]],end_arrow+325,arrow=tk.LAST, fill='red')
                #Third arrow
                if((type == "Differential" and bin[pBox[4*a+2]] == 0) or (type == "Linear" and (trail[r][1][a])[2] == '0')):
                    #print((trail[r][1][a]))
                    #print((trail[r][1][a])[1])
                    arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)+7,end_arrow+155, positions_x[pBox[4*a+2]],end_arrow+325,arrow=tk.LAST,fill='blue')
                else:
                    arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)+7,end_arrow+155, positions_x[pBox[4*a+2]],end_arrow+325,arrow=tk.LAST,fill='red')
                #Fourth arrow:
                if((type == "Differential" and bin[pBox[4*a+3]] == 0) or (type == "Linear" and (trail[r][1][a])[3] == '0')):
                    #print("here4")
                    arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)+20,end_arrow+155, positions_x[pBox[4*a+3]],end_arrow+325,arrow=tk.LAST, fill='blue')
                else:
                    arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)+20,end_arrow+155, positions_x[pBox[4*a+3]],end_arrow+325,arrow=tk.LAST, fill='red')

                #If it is not differential, do the following (just as before I touched the code)
                #else:
                #arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)-20,end_arrow+155, positions_x[pBox[4*a]], end_arrow+325,arrow=tk.LAST)
                #arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)+20,end_arrow+155, positions_x[pBox[4*a+1]],end_arrow+325,arrow=tk.LAST, fill='green')
                #arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)-7,end_arrow+155, positions_x[pBox[4*a+2]],end_arrow+325,arrow=tk.LAST, fill='red')

                #print(str(4*a+3))
                #print("pbox " + str(pBox[4*a+3]))
                #print("positions_x "+str(positions_x[pBox[4*a+3]]))
                #arrow1_canvas.create_line(width/(num_arrows+1)*(a+1)+7,end_arrow+155, positions_x[pBox[4*a+3]],end_arrow+325,arrow=tk.LAST,fill='blue')
            #output box
            arrow1_canvas.create_rectangle((width/10), end_arrow+325, (width-width/10), end_arrow+375)
            end_arrow = end_arrow+300


            #If it's not the last one, then draw the XOR and put the entering values
            if (r != num_rounds-1) :
                #xor
                arrow1_canvas.create_oval(width/2-15, end_arrow+35, width/2+15, end_arrow+65)
                arrow1_canvas.create_line(width/2-15,end_arrow+50 , width/2+15, end_arrow+50)
                arrow1_canvas.create_line(width/2,end_arrow+35 , width/2, end_arrow+65)
                arrow1_canvas.create_line((width/10)-15,end_arrow+50, (width/10),end_arrow+50,arrow=tk.LAST)
                arrow1_canvas.create_text((width/10)-20, end_arrow+50, text="k"+str(r+1))

                #The text with the round
                if(type == "Differential"):
                    #print(probs[r])
                    pr = Decimal(math.log2(probs[r]))
                    arrow1_canvas.create_text(width/2+100, end_arrow+50, text=(diff.vals_string(trail[r])+" P (log2)= "+str(round(pr,3))))
                    #probability up to this point
                    prob_here = 1
                    for i in range(r+1):
                        prob_here = prob_here * probs[i]
                    prb = Decimal(math.log2(prob_here))
                    #print(prob_here)
                    arrow1_canvas.create_text(19*width/20, end_arrow+50, text=(str(round(prb, 3))))

                    arrow1_canvas.create_text(width/3, end_arrow+50, text="Button")
                    #edit = tk.Button(arrow1_canvas)
                    #edit.place(x=19*width/20, y=end_arrow+50)
                    #edit.pack()
                    
                    button1 = tk.Button(master = arrow1_canvas,text = "Edit round", anchor = tk.W, command = lambda r =r: diff_edition(wdw, r, sBox, pBox, numOfRounds, trail, probs, inputString))
                    button1_window = arrow1_canvas.create_window(width/3-15, end_arrow+39, anchor=tk.NW, window=button1)


                if(type == "Linear"):
                    #TODO stop text moving
                    arrow1_canvas.create_text(width/2+110, end_arrow+50, text="correlation of round: " + str(round(trail[r][0],2)))
                    #print("r", r)
                    pMask = ''.join(sboxMasks[r+1])
                    arrow1_canvas.create_text(width/2-150, end_arrow+50, text="Permuted mask " + str(pMask))
                    #print(trail)
                    for i in range(4):
                        button1 = tk.Button(master = arrow1_canvas,text = "Edit", anchor = tk.W, command = lambda r =r: lin_edition(wdw, r+1, i, sBox, pBox, numOfRounds, trail, sboxMasks, totalCorr, inputString))
                        button1.pack()
                        button1_window = arrow1_canvas.create_window(width/(num_arrows+1)*(i+1) - 120, end_arrow+100, anchor=tk.NW, window=button1)


            else:


                if(type == "Differential"):
                    pr = Decimal(math.log2(probs[r]))
                    arrow1_canvas.create_text(width/2, end_arrow+50, text=(diff.vals_string(trail[r])+ " with probability (log2) " +str(round(pr, 3))))
                    prob_here = 1
                    for i in range(r+1):
                        prob_here = prob_here * probs[i]
                    prb = Decimal(math.log2(prob_here))
                    #print(prob_here)
                    arrow1_canvas.create_text(19*width/20, end_arrow+50, text=(str(round(prb, 3))))
                    arrow1_canvas.create_text(width/2, end_arrow+100, text=("An attack would be efficient until round " +str(len(trail)) + " with probability (log2) " + str(math.log2(prob_fin))))
                    arrow1_canvas.create_text(width/2, end_arrow+120, text=("The attack complexity in this number of rounds would be 2^" + str(-math.log2(prob_here))))

                if(type == "Linear"):
                    #TODO stop text moving
                    stop_prop = math.log(2.0**(-(16/2)), 2.0)
                    #print(stop_prop)
                    if (totalCorr < stop_prop):
                        arrow1_canvas.create_text(width/2, end_arrow+50, text="This is not an efficient attack, the correlation is too low")
                    else:
                        arrow1_canvas.create_text(width/2, end_arrow+50, text="Total correlation: "+ str(round(totalCorr,2)))
                    #output
                    m = ''.join(sboxMasks[-1])
                    arrow1_canvas.create_text(width/2, end_arrow+100, text="Output Mask: " + str(m))
                    complexity = ((2**totalCorr) ** (-2.0))
                    complexity = math.log(complexity, 2)
                    arrow1_canvas.create_text(width/2, end_arrow+130, text="Complexity " + str(complexity))

                end_y = (r+1)*end_arrow+200
                #arrow1_canvas.create_line(width/2,end_y, (width/10),width/2, end_y + 40,arrow=tk.LAST)
                        #input_frame = tk.Frame(width=768, height=576,bg="", master = wdw, colormap="new")
                        #input_frame.pack()
                        #input_label = tk.Label(input_frame, text="Input = "+ inputString)
                        #input_label.pack()

    arrow1_canvas = tk.Canvas(wdw, yscrollcommand = scrollbar.set, scrollregion=(0,0,(numOfRounds+1)*300, (numOfRounds+1)*300))
    arrow1_canvas.pack(fill=tk.BOTH, expand = 1)

                        # height = wdw.winfo_height()
                        # width = wdw.winfo_width()
                        # print(height)
                        # print(width)

                        # arr=arrow1_canvas.create_line(width/2,40, width/2,300,arrow=tk.LAST)
                        # arrow1_canvas.coords(arr, (384, 40, 384 , 200))
                        #lambda event, a=10, b=20, c=30:
                            #self.rand_func(a, b, c)
                            #https://stackoverflow.com/questions/7299955/tkinter-binding-a-function-with-arguments-to-a-wid
    arrow1_canvas.bind("<Configure>", lambda event, num_arrows = sBoxes, num_rounds=numOfRounds: configure(event,sBoxes, numOfRounds))
    scrollbar.config(command=arrow1_canvas.yview)
    wdw.mainloop()
