#!/usr/bin/python

import sys
import cv2
import numpy as np
import random

# Soln
# The problem was that there was no stopping criteria hence the algorithm continued to decode beyond the payload data
# Line 30, 31, 49

# This method is for extracting the payload message from the stego object
def extract():
    J = cv2.imread('stego.png') # Open the stego object
    f = open('output_payload.txt', 'w+', errors="ignore") # Output the extracted payload write it in text file

    bitidx=0
    bitval=0
    count=0
    breakloop=False
    for i in range(J.shape[0]): # Number of rows in stego.png
        if (I[i, 0, 0] == '-'):
            break
        if breakloop:
            break
        for j in range(J.shape[1]): # Number of columns in stego.png
            if (I[i, j, 0] == '-'):
                break
            if breakloop:
                break
            for k in range(3):
                if (I[i, j, k] == '-'):
                    break
                if bitidx == 8:
                    #Soln
                    if bitval == 61: # 61 is the ASCI for '=' which we set as the stopping criteria
                        count+=1
                    else:
                        for l in range(count):
                            f.write(chr(61))
                        count=0
                        f.write(chr(bitval))
                    if count == 6:
                        breakloop=True
                        break
                    #Soln

                    print(bitval, count)
                    bitidx=0
                    bitval=0
                bitval |= (I[i, j, k] % 2)<<bitidx # Left shift for multiplying number by 2

                bitidx+=1

    f.close()




txtfile = open('payload2.txt', 'r') # Open the payload text file you want to hide
sPayload_msg = txtfile.read()

#Soln
sPayload_msg += "======" # Setting a stopping criteria
print(sPayload_msg)

iBlist = [ord(b) for b in sPayload_msg] # Convert each character into ASCI representation in int
#print(iBlist)


# Converts each ASCI character of the payload into binary
iBits = []
for b in iBlist:
    for i in range(8):
        #print(b >> i)
        #print((b >> i) & 1)
        iBits.append((b >> i) & 1) # Right shift is dividing a number by 2
#print(iBits)
#print(len(iBits))


I = np.asarray(cv2.imread('cover.png')) #Converts the cover object into rgb values
#print(I)

#white = np.asarray(cv2.imread('white.png'))
#print(white)


sign = [1,-1]
idx = 0
for i in range(I.shape[0]): # I.shape[0] is the number of rows
    # i is 0 to 449 (450 rows)
    #print(i)
    for j in range(I.shape[1]): # I.shape[1] is the number of columns
        # j is 0 to 359 (360 columns)
        #print(j)
        for k in range(3): # k in range 0 1 2
            #print('I[i][j][k] % 2 is', I[i][j][k] % 2)
            #print('I[i][j][k] is ', I[i][j][k])
            if idx < len(iBits): #len(bits) = 1248
                if I[i][j][k] % 2 != iBits[idx]:
                    s = sign[random.randint(0, 1)]
                    #print('s is ', s)
                    if I[i][j][k] == 0: s = 1
                    if I[i][j][k] == 255: s = -1
                    I[i][j][k]+=s
                idx+=1

cv2.imwrite('stego.png', I)

print("Extracting ... ")
extract()
print("Completed")