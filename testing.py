import cipher
"""sBox = [6,4,12,5,0,7,2,14,1,15,3,13,8,10,9,11]
    pBox =[0,4,8,12,1,5,9,13,2,6,10,14,3,7,11, 15]
    #pBox = [0,1,2,3,4,5,6,7,8,9,10,11]
    visual.visual("000f", 2, 5,len("000f") , sBox, pBox, "Differential", True, [],[],1, [])"""

cip = cipher.Differential([6,4,12,5,0,7,2,14,1,15,3,13,8,10,9,11], [0,1,2,3,4,5,6,7,8,9,10,11], 4)
print(cip.ddt)