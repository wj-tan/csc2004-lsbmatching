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
        if filename == "":
            plImgLbl["text"] = ""
            plImgLbl["image"] = ""
            plImgHiddenLbl["text"] = ""
            return 0
        encryptedImgLbl["image"] = ""
        decryptLbl["image"] = ""
        decryptLbl["text"] = ""
        actionLbl["text"] = ""
        plImgHiddenLbl["text"] = filename
        try:
            img = Image.open(filename)
            width, height = img.size
            newHeight = int(height / (width / 250))
            img = img.resize((250, int(newHeight)), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            payloadCanvas.image = img
            plImgLbl["image"] = img
            actionLbl["text"] = ""
        except:
            f = open(filename, 'r', encoding='latin-1')  # Added Latin 1 here too
            payloadText = f.readlines()
            plImgLbl["image"] = ""
            plImgLbl["text"] = "\n".join(payloadText)
            actionLbl["text"] = ""
            f.close()
        #This thing is required for your button
        # if imgHiddenLbl["text"] != "":
        #     encode()

    def UploadImage(event=None):
        filename = filedialog.askopenfilename()
        if filename == "":
            imgLbl["image"] = ""
            imgHiddenLbl["text"] = ""
            actionLbl["text"] = ""
            return 0
        encryptedImgLbl["image"] = ""
        decryptLbl["image"] = ""
        decryptLbl["text"] = ""

        img = Image.open(filename)
        imgHiddenLbl["text"] = filename
        width, height = img.size
        newHeight = int(height / (width / 250))
        img = img.resize((250, int(newHeight)), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        imgCanvas.image = img
        imgLbl["image"] = img
        actionLbl["text"] = ""
        #This thing is required for your button
        # if plImgHiddenLbl["text"] != "":
        #     encode()


    def encode():
        payload = plImgHiddenLbl["text"]
        vslImg = imgHiddenLbl["text"]
        actionLbl["text"] = "Encrypting... Please Wait..."
        actionLbl["fg"] = "black"
        #if is image
        try:
            Image.open(payload)
            runEncode(vslImg, payload, ENCRYPTFILE,True)

        #if not image
        except IOError:
            runEncode(vslImg, payload, ENCRYPTFILE, False)
           # bpcs.encoderClass(vslImg, payload, ENCRYPTFILE, ALPHA).encode()
        except Exception as e:
            print(e)
            actionLbl["text"] = e
            actionLbl["fg"] = "red"
            encryptedImgLbl["image"] = ""
            decryptLbl["image"] = ""
            decryptLbl["text"] = ""
            return 0

        img = Image.open(ENCRYPTFILE)
        width, height = img.size
        newHeight = int(height / (width / 250))
        img = img.resize((250, int(newHeight)), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        encryptedImgCanvas.image = img
        encryptedImgLbl["image"] = img

        actionLbl["text"] = "Steganography Done!"
        actionLbl["fg"] = "black"
        decrypt()

    def decrypt():
        try:
            isImage, decryptFile = runDecode(ENCRYPTFILE)
            if isImage:
                img = Image.open(decryptFile)
                width, height = img.size
                newHeight = int(height / (width / 250))
                img = img.resize((250, int(newHeight)), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)
                decryptedImgCanvas.image = img
                decryptLbl["image"] = img
            else:
                f = open(decryptFile, 'r', encoding='latin-1')  # Added Latin 1 here too
                decryptText = f.readlines()
                decryptLbl["image"] = ""
                decryptLbl["text"] = "\n".join(decryptText)
        except Exception as e:
            print(e)
            actionLbl["text"] = e
            actionLbl["fg"] = "red"
            encryptedImgLbl["image"] = ""
            decryptLbl["image"] = ""
            decryptLbl["text"] = ""
            return 0


    def processImage():
        if imgHiddenLbl["text"] != "" and plImgHiddenLbl["text"] != "":
            encode()
        else:
            actionLbl["text"] = "Please upload a text file or an image"
            actionLbl["fg"] = "red"

    window = tk.Tk()
    window.configure(background="white")
    window.title("Main Menu")
    mainFrame = tk.Frame(window, bg="white")
    mainFrame.pack(padx=20, pady=5)
    imgCanvas = tk.Canvas()
    payloadCanvas = tk.Canvas()
    encryptedImgCanvas = tk.Canvas()
    decryptedImgCanvas = tk.Canvas()
    plFrame = tk.Frame(mainFrame, bg="white")
    plFrame.pack(padx=20, pady=5)
    plTextLbl = tk.Label(plFrame, text="Upload Payload: ", font="Ariel 16 normal", bg="white")
    plTextLbl.pack(side=tk.LEFT, padx=20, pady=5)
    plbtn = tk.Button(plFrame, text='Upload', command=UploadPL)
    plbtn.pack(side=tk.RIGHT, padx=20, pady=5)
    plImgLbl = tk.Label(plFrame)
    plImgLbl.pack()
    plImgHiddenLbl = tk.Label(plFrame)
    plFileType = tk.Label(plFrame)

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
    plProcessButton = tk.Button(mainFrame, text='Process', command=processImage)
    plProcessButton.pack(side=tk.TOP, padx=20, pady=5)

    imgHiddenLbl = tk.Label(uploadImgFrame)

    encryptedImgFrame = tk.Frame(imgFrame, bg="white")
    encryptedImgFrame.pack(side=tk.RIGHT, padx=20, pady=5)
    encryptedTextLbl = tk.Label(encryptedImgFrame, text="Encrypted Image", font="Ariel 16 normal", bg="white")
    encryptedTextLbl.pack(padx=20, pady=5)
    encryptedImgLbl = tk.Label(encryptedImgFrame, bg="white")
    encryptedImgLbl.pack()
    plTextLbl = tk.Label(mainFrame, text="Payload", font="Ariel 16 underline", bg="white")
    plTextLbl.pack(padx=20, pady=5)
    decryptLbl = tk.Label(mainFrame)
    decryptLbl.pack(padx=20, pady=5)
    actionLbl = tk.Label(mainFrame, font="Ariel 16", bg="white")
    actionLbl.pack(padx=20, pady=5)

    window.mainloop()


global ALPHA, ENCRYPTFILE
ALPHA = 0.45
ENCRYPTFILE = "encode.png"
vslImg = ""
main()
