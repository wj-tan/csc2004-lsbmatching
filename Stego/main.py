#!/usr/bin/python

import sys
import cv2
import numpy as np
import random

#decode
def extract():
    J=cv2.imread('plane_stego.png') #open stego encoded image
    f = open('output_payload.txt', 'w+', errors="ignore")   #output payload file

    bitidx=0
    bitval=0
    stopcount=0 #variable to keep track of whether the stopping criteria has been reached

    for i in range(J.shape[0]): #for pixel in image row
        if (I[i, 0, 0] == '-'): #if not a valid image pixel
            break      #stop decoding
        for j in range(J.shape[1]): #for pixel in image column
            if (I[i, j, 0] == '-'): #if not a valid image pixel
                break      #stop decoding
            for k in range(3):  #for r, g, b in pixel
                if (I[i, j, k] == '-'): #if not a valid image pixel
                    break
                if bitidx==8:   #if bit index is 8
                    if bitval == 61:    #check for presence of equal symbol (ascii)
                        stopcount+=1    #increment stopping criteria by 1
                    else:
                        for l in range(stopcount):
                            f.write(chr(61)) #write equal symbol ascii back to character if part of decoded text
                        stopcount=0 #set stopcount back to zero since it does not meet the stopping criteria
                        f.write(chr(bitval))    #write ascii back to character
                    if stopcount == 6:  #if stopping criteria detected
                        f.close()  #close the file
                        return 0   #stop decoding
                    bitidx=0    #set bit index back to 0
                    bitval=0    #set bit value back to 0
                bitval |= (I[i, j, k]%2)<<bitidx    #convert bit value back to ascii
                bitidx+=1   #increment bit index by 1
    f.close()   #close the file

#open and convert payload data to bits
bits=[] #for storing binary of converted ascii character
f=open('payload2.txt', 'r') #open payload file to read
payload = f.read() + "======" #adds a stopping criteria
blist = [ord(b) for b in payload] #converts payload2.txt characters plus stopping criteria into ascii and put into list
for b in blist: #for each of the coverted ascii character
    for i in range(8): #for i in range 1 to 8
        bits.append((b >> i) & 1) #convert into binary

#open image
I = np.asarray(cv2.imread('plane.png'))

#encoding
sign=[1,-1] #bit sign for random function
idx=0
for i in range(I.shape[0]): #for pixel in image row
    for j in range(I.shape[1]): #for pixel in image column
        for k in range(3): #for r, g, b in pixel
            if idx<len(bits):   #if index is smaller than size of bits (indicate space avaliable to store)
                if I[i][j][k]%2 != bits[idx]:   #if rgb value mod 2 is not equal to the image pixel bit (need perform LSB matching)
                    s=sign[random.randint(0, 1)]    #random between bit sign 1 or -1
                    if I[i][j][k]==0: s=1   #if rgb value = 0, use bit sign 1
                    if I[i][j][k]==255: s=-1    #if rgb value = 255, use bit sign -1
                    I[i][j][k]+=s   #assign the bit sign value (perform LSB matching)
                idx+=1  #increment index by 1

#output stego image after encode
cv2.imwrite('plane_stego.png', I)   #write to new image file

#run decode function
print("Extracting ... ")
extract()   #run extract function
print("Completed")