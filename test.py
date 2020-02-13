maskin = "0110011001100110"
noOfS = 4
mask = [maskin[i:i+noOfS] for i in range (0, len(maskin), noOfS)]

print(mask)