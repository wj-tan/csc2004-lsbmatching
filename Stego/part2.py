import tkinter as tk
from tkinter import filedialog
# pip install pillow
from PIL import ImageTk, Image, ImageFile

import bpcs
from kurapan.encode import runEncode
from kurapan.decode import runDecode

def main():
    def UploadPL(event=None):
        filename = filedialog.askopenfilename()
        plImgLbl["text"] = filename
        if vslImg != "":
            encode(plImgLbl["text"])

    def UploadImage(event=None):
        global vslImg
        filename = filedialog.askopenfilename()
        img = Image.open(filename)
        vslImg = filename
        width, height = img.size
        newHeight = int(height / (width / 250))
        img = img.resize((250, int(newHeight)), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        imgCanvas.image = img
        imgLbl["image"] = img
        if plImgLbl["text"] != "":
            encode(plImgLbl["text"])

    def encode(payload):
        actionLbl["text"] = "Encrypting... Please Wait..."
        try:
            Image.open(payload)
            runEncode(vslImg, payload, encryptFile)
        except IOError:
            bpcs.encoderClass(vslImg, payload, encryptFile, alpha).encode()

        img = Image.open(encryptFile)
        width, height = img.size
        newHeight = int(height / (width / 250))
        img = img.resize((250, int(newHeight)), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        encryptedImgCanvas.image = img
        encryptedImgLbl["image"] = img

        actionLbl["text"] = "Encryption Done!"
        decrypt()

    def decrypt():
        try:
            decryptFile = "decrypt.png"
            runDecode(encryptFile, decryptFile)
            img = Image.open(decryptFile)
            width, height = img.size
            newHeight = int(height / (width / 250))
            img = img.resize((250, int(newHeight)), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            decryptedImgCanvas.image = img
            decryptLbl["text"] = ""
            decryptLbl["image"] = img
        except IOError:
            decryptFile = "decrypt.txt"
            bpcs.decoderClass(encryptFile, decryptFile, alpha).decode()
            f = open(decryptFile, 'r', encoding='latin-1')  # Added Latin 1 here too
            decryptText = f.readlines()
            decryptLbl["image"] = ""
            decryptLbl["text"] = "\n".join(decryptText)
            f.close()


    window = tk.Tk()
    window.configure(background="white")
    window.title("Main Menu")
    mainFrame = tk.Frame(window, bg="white")
    mainFrame.pack(padx=20, pady=5)
    imgCanvas = tk.Canvas()
    encryptedImgCanvas = tk.Canvas()
    decryptedImgCanvas = tk.Canvas()
    plFrame = tk.Frame(mainFrame, bg="white")
    plFrame.pack(padx=20, pady=5)
    plTextLbl = tk.Label(plFrame, text="Upload Payload: ", font="Ariel 16 normal", bg="white")
    plTextLbl.pack(side=tk.LEFT, padx=20, pady=5)
    plbtn = tk.Button(plFrame, text='Upload', command=UploadPL)
    plbtn.pack(side=tk.RIGHT, padx=20, pady=5)
    plImgLbl = tk.Label(plFrame, bg="white")
    plImgLbl.pack()

    imgFrame = tk.Frame(mainFrame, bg="white")
    imgFrame.pack(padx=20, pady=5)

    uploadImgFrame = tk.Frame(imgFrame, bg="white")
    uploadImgFrame.pack(side=tk.LEFT, padx=20, pady=5)
    imgBtnFrame = tk.Frame(uploadImgFrame, bg="white")
    imgBtnFrame.pack()
    imgTextLbl = tk.Label(imgBtnFrame, text="Upload Image: ", font="Ariel 16 normal", bg="white")
    imgTextLbl.pack(side=tk.LEFT, padx=20, pady=5)
    imgbtn = tk.Button(imgBtnFrame, text='Upload', command=UploadImage)
    imgbtn.pack(side=tk.RIGHT, padx=20, pady=5)
    imgLbl = tk.Label(uploadImgFrame, bg="white")
    imgLbl.pack()

    encryptedImgFrame = tk.Frame(imgFrame, bg="white")
    encryptedImgFrame.pack(side=tk.RIGHT, padx=20, pady=5)
    encryptedTextLbl = tk.Label(encryptedImgFrame, text="Encrypted Image", font="Ariel 16 normal", bg="white")
    encryptedTextLbl.pack(padx=20, pady=5)
    encryptedImgLbl = tk.Label(encryptedImgFrame, bg="white")
    encryptedImgLbl.pack()
    actionLbl = tk.Label(mainFrame, bg="white")
    actionLbl.pack(padx=20, pady=5)
    plTextLbl = tk.Label(mainFrame, text="Payload", font="Ariel 16 underline", bg="white")
    plTextLbl.pack(padx=20, pady=5)
    decryptLbl = tk.Label(mainFrame)
    decryptLbl.pack(padx=20, pady=5)

    window.mainloop()


global alpha, vslImg, encryptFile
alpha = 0.45
encryptFile = "encode.png"
vslImg = ""
main()
