import json
import math
import os
import tkinter as tk
from tkinter import filedialog

import numpy as np

import cipher
import trails


def show_ddt(wn, cip, sbox):

    # Create a new window for the DDFT, on top of the visual one
    n_root = tk.Tk()
    n_root.geometry("800x900")
    n_root.grid_rowconfigure(0, minsize=400, weight=1)
    n_root.grid_columnconfigure(0, minsize=800, weight=1)

    def update_scrollregion(event):
        wdw.configure(scrollregion=window.bbox("all"))

    photo_frame = tk.Frame(n_root, width=900, height=400)
    photo_frame.grid(row=0, column=0, sticky = "nsew")
    photo_frame.rowconfigure(0, weight=1)
    photo_frame.columnconfigure(0, weight=1)

    wdw = tk.Canvas(photo_frame)
    wdw.grid(row=0, column=0, sticky="nsew")

    window = tk.Frame(wdw, width=900, height=400)
    wdw.create_window(0, 0, window=window, anchor='nw')

    ddt2 = cip.calculate_ddt(cip, sbox)

    photo_scroll = tk.Scrollbar(photo_frame, orient=tk.VERTICAL)
    photo_scroll.config(command=wdw.yview)
    wdw.config(yscrollcommand=photo_scroll.set)
    photo_scroll.grid(row=0, column=1, sticky="ns")

    window.bind("<Configure>", update_scrollregion)

    for i in range(len(ddt2)):
        col = tk.Label(window, text=i, relief=tk.RIDGE, width=10, bg='gray')
        col.grid(row=i + 1, column=0)
        for j in range(16):
            row = tk.Label(window, text=j, relief=tk.RIDGE, width=10, bg='gray')
            row.grid(row=0, column=j + 1)
            prob = tk.Label(window, text=ddt2[i][j], relief=tk.RIDGE, width=10)
            # Depending on the parity of the index, paint one colour or another
            if i % 2 == 0:
                prob = tk.Label(window, text=ddt2[i][j], relief=tk.RIDGE, width=10)
            else:
                prob = tk.Label(window, text=ddt2[i][j], relief=tk.RIDGE, width=10, bg='LightSkyBlue1')
            prob.grid(row=i + 1, column=j + 1)

    n_root.mainloop()


def show_cipher(cip):
    wdw = tk.Tk()
    wdw.geometry("500x600")

    def save_file():
        curr_dir = os.getcwd()
        file_to_save = filedialog.asksaveasfilename(initialdir = curr_dir)
        first = []
        dic_json = {"type1": "Differential", "type2": "des", "trail": cip.trail}
        with open(file_to_save, 'w') as f:
            json.dump(dic_json, f)

    # Do the file saving thing
    save_button = tk.Button(wdw, text="Save trail", command = save_file)
    save_button.pack()

    # Button for sboxes

    def on_click():
        sbox_window = tk.Tk()
        tk.Label(sbox_window, text="Choose which sbox's Difference Distribution Table to visualise").grid()

        sbox_options = (1, 2, 3, 4, 5, 6, 7, 8)
        option = tk.IntVar(sbox_window)
        option.set(1)
        option_menu = tk.OptionMenu(sbox_window, option, *sbox_options).grid()

        def show_ddt_sbox():
            show_ddt(sbox_window, cip, sbox=cip.sbox[option.get()])

        button_sbox = tk.Button(sbox_window, text="Visualise", command=show_ddt_sbox)
        button_sbox.grid()

        sbox_window.mainloop()

        print("sboxes thingy")

    button_sboxes = tk.Button(wdw, text="Show DDT", command = on_click)
    button_sboxes.pack()

    scrollbar = tk.Scrollbar(wdw)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


    def update_scrollregion(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))
        showing()

    def showing():
        trail = cip.trail
        num_rounds = len(trail)
        final_prob = np.prod(cip.probabilities)
        if not final_prob == 0:
            final_prob = final_prob
        width = 500 # TODO change this when getting the right width

        length_box = (width - width/5)

        end_prev = 80
        canvas.delete("all")

        for round in range(num_rounds):
            def visualise_function(event, r):
                wdw_function = tk.Tk()
                wdw_function.geometry("500x400")
                w =500
                canvas_func = tk.Canvas(wdw_function)

                canvas_func.create_text(w/2, 40, text=cip.trail[r][8:])
                canvas_func.create_rectangle(w/40, 20, w-w/40, 60)

                canvas_func.pack(fill=tk.BOTH, expand=1)

                canvas_func.create_text(3*w / 4, 80, text="Expansion")
                canvas_func.create_line(w/2, 60, w/2, 100, arrow=tk.LAST)

                # Get the the expansion
                expansion = cip.extend_binary(cip.trail[r][8:])
                expanded_dec = []
                for j in range(int(len(expansion) / 6)):
                    expanded_dec.extend(cipher.fromBinary(expansion[j * 6:6 * (j + 1)]))
                canvas_func.create_text(w / 2, 120, text=expanded_dec)
                canvas_func.create_rectangle(w / 40, 100, w - w / 40, 140)

                canvas_func.create_text(3*w / 4, 160, text="Substitution")
                canvas_func.create_line(w/2, 140, w/2, 180, arrow=tk.LAST)

                # Print substitution
                pre_sub = cipher.xor(cip.trail[r][:8], cip.trail[r+1][8:])
                subst = cip.undo_permutation(pre_sub, cip.pbox[1])
                canvas_func.create_text(w / 2, 200, text=subst)
                canvas_func.create_rectangle(w / 40, 180, w - w / 40, 220)

                canvas_func.create_text(3*w / 4, 250, text="Permutation")
                canvas_func.create_line(w/2, 220, w/2, 260, arrow=tk.LAST)

                # Print permutation
                canvas_func.create_text(w / 2, 280, text=pre_sub)
                canvas_func.create_rectangle(w / 40, 260, w - w / 40, 300)
                wdw_function.mainloop()

            if not round == len(trail)-1: # If it is not the last round
                #Doing the arrow on the left
                canvas.create_text(3*width/8, end_prev-20, text=trail[round][:8], fill='blue')
                canvas.create_text(5 * width / 8, end_prev - 20, text=trail[round][8:], fill='red')
                canvas.create_line(3*width/8, end_prev, 3*width/8, end_prev+60)  # First part
                canvas.create_line(3 * width / 8, end_prev+60, 5 * width / 8-10, end_prev+90, arrow=tk.LAST)  # Second part


                # Doing the arrow on the right
                canvas.create_line(5 * width / 8, end_prev, 5 * width / 8, end_prev+20, arrow=tk.LAST)
                rectangle_bt = canvas.create_rectangle(5 * width / 8-20, end_prev+20, 5*width/8 +20, end_prev+60, fill="grey100") # The rectangle
                text_bt = canvas.create_text(5*width/8, end_prev+40, text="F")
                canvas.create_line(5 * width / 8, end_prev+60, 5 * width / 8, end_prev + 80, arrow=tk.LAST)
                canvas.tag_bind(rectangle_bt, "<Button-1>", func = lambda event, r=round:visualise_function(event, r))
                canvas.tag_bind(text_bt, "<Button-1>", func = lambda event, r=round:visualise_function(event, r))

                canvas.create_text(7*width/8, end_prev+40, text=cip.probabilities[round])

                # Doing the xor
                canvas.create_oval(5*width/8-10, end_prev+80, 5*width/8+10, end_prev+100)
                canvas.create_line(5*width/8, end_prev+80, 5*width/8, end_prev+100)
                canvas.create_line(5*width/8-10, end_prev+90, 5*width/8+10, end_prev+90)

                #Doing the end of the right arrow
                canvas.create_line(5*width/8, end_prev+100, 5*width/8, end_prev+120, arrow=tk.LAST)

                # Doing the other right arrow
                canvas.create_line(5*width/8, end_prev+7, 4*width/8, end_prev+7)
                canvas.create_line(4*width/8, end_prev+7, 3*width/8, end_prev+90)
                canvas.create_line(3*width/8, end_prev+90, 3*width/8, end_prev+120, arrow=tk.LAST)

            else:
                final_rectangle = canvas.create_rectangle(width/8-20, end_prev-30, 7*width/8+20, end_prev+30)
                canvas.create_text(4*width/8-10, end_prev-10, text=trail[round])
                txt = "Probability = " + str(sum(cip.probabilities))
                canvas.create_text(4 * width / 8 - 10, end_prev +20, text=txt)



            end_prev = end_prev+150

        #print("showing cipher")
        canvas.pack(fill =tk.BOTH, expand=1)

    canvas = tk.Canvas(wdw, yscrollcommand=scrollbar.set)
    canvas.pack(fill=tk.BOTH, expand=1)
    canvas.configure(scrollregion=canvas.bbox("all"))

    canvas.bind("<Configure>", lambda event, canvas=canvas:update_scrollregion(canvas))
    scrollbar.config(command=canvas.yview)

    wdw.mainloop()





#des = cipher.DESDifferential()
#des.trail = trails.trail_des1
#des.probabilities = [2**-2]*len(des.trail)
# Set the window
# root = tk.Tk()
# root.geometry("500x600")
# scrollbar = tk.Scrollbar(root)
# scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# canvas = tk.Canvas(root, yscrollcommand=scrollbar.set)
# canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# show_ddt(root, des, sbox=des.sbox[0])
#show_cipher(des)
# root.mainloop()


