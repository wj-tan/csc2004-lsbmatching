import tkinter as tk    #tkinter python user interface
from tkinter import filedialog  #import filedialog module
# pip install pillow
from PIL import ImageTk, Image, ImageFile #import modules for image manipulation functions

from kurapan.encode import runEncode    #use Kurapan Hide image in image library for enconding image
from kurapan.decode import runDecode    #use Kurapan Hide image in image library for decoding image

def main():
    #function to upload payload image
    def UploadPL(event=None):
        encryptedImgLbl["image"] = ""
        decryptLbl["image"] = ""
        decryptLbl["text"] = ""
        actionLbl["text"] = ""
        filename = filedialog.askopenfilename() #UI prompt to upload file
        if filename == "":
            plImgLbl["text"] = ""
            plImgLbl["image"] = ""
            plImgHiddenLbl["text"] = ""
            return 0
        plImgHiddenLbl["text"] = filename   #store payload to be encoded
        #for image payload
        try:
            img = Image.open(filename)  #open payload image
            width, height = img.size    #get width and height of image
            newHeight = int(height / (width / 250))  #resize image for UI
            img = img.resize((250, int(newHeight)), Image.ANTIALIAS)  #fit resized image to the UI
            img = ImageTk.PhotoImage(img)   #initialize image for UI
            payloadCanvas.image = img  #set image canvas for UI
            plImgLbl["image"] = img   #display payload image in UI
            actionLbl["text"] = ""
        #for text payload
        except:
            f = open(filename, 'r', encoding='latin-1')  # open text file
            payloadText = f.readlines() #read payload text
            plImgLbl["image"] = ""
            plImgLbl["text"] = "\n".join(payloadText) #display payload text in UI
            actionLbl["text"] = ""
            f.close()   #close text file

    #function to upload cover image
    def UploadImage(event=None):
        encryptedImgLbl["image"] = ""
        decryptLbl["image"] = ""
        decryptLbl["text"] = ""
        actionLbl["text"] = ""
        filename = filedialog.askopenfilename() #UI prompt to upload file
        if filename == "":
            imgLbl["image"] = ""
            imgHiddenLbl["text"] = ""
            actionLbl["text"] = ""
            return 0

        img = Image.open(filename)  #open cover image
        imgHiddenLbl["text"] = filename #store cover image for encoding
        width, height = img.size   #get width and height of image
        newHeight = int(height / (width / 250))  #resize image for UI
        img = img.resize((250, int(newHeight)), Image.ANTIALIAS) #fit resized image to the UI
        img = ImageTk.PhotoImage(img)   #initialize image for UI
        imgCanvas.image = img   #set image canvas for UI
        imgLbl["image"] = img   #display cover image in UI
        actionLbl["text"] = ""

    #function to encode payload into image and display encoded image
    def encode():
        payload = plImgHiddenLbl["text"]    #access payload from UploadPL function
        vslImg = imgHiddenLbl["text"]   #access cover image from UploadImage function
        actionLbl["text"] = "Encrypting... Please Wait..."   #display encrypting in progress message
        actionLbl["fg"] = "black" #set text colour for the image
        #for image payload
        try:
            Image.open(payload) #open the image payload
            runEncode(vslImg, payload, ENCRYPTFILE,True)    #run encode function from the Kurapan Hide image in image library
        #for text payload
        except IOError:
            runEncode(vslImg, payload, ENCRYPTFILE, False)    #run encode function from the Kurapan Hide image in image library
        #if cover image is too small for the payload, output error message
        except Exception as e:
            print(e)
            actionLbl["text"] = e
            actionLbl["fg"] = "red"
            encryptedImgLbl["image"] = ""
            decryptLbl["image"] = ""
            decryptLbl["text"] = ""
            return 0

        img = Image.open(ENCRYPTFILE)  #open encoded image
        width, height = img.size   #get width and height of image
        newHeight = int(height / (width / 250))  #resize image for UI
        img = img.resize((250, int(newHeight)), Image.ANTIALIAS) #fit resized image to the UI
        img = ImageTk.PhotoImage(img)   #initialize image for UI
        encryptedImgCanvas.image = img  #set image canvas for UI
        encryptedImgLbl["image"] = img   #display encoded image in UI

        actionLbl["text"] = "Steganography Done!"   #display success message
        actionLbl["fg"] = "black" #set text colour for the image
        decrypt()

    #function to decode encoded image and display payload
    def decrypt():
        #for image payload
        try:
            isImage, decryptFile = runDecode(ENCRYPTFILE)   #run decode function from the Kurapan Hide image in image library 
            if isImage:
                img = Image.open(decryptFile)  #open decrypted image file
                width, height = img.size   #get width and height of image
                newHeight = int(height / (width / 250))  #resize image for UI
                img = img.resize((250, int(newHeight)), Image.ANTIALIAS) #fit resized image to the UI
                img = ImageTk.PhotoImage(img)   #initialize image for UI
                decryptedImgCanvas.image = img  #set image canvas for UI
                decryptLbl["image"] = img   #display decrypted payload image in UI
            #for text payload
            else:
                f = open(decryptFile, 'r', encoding='latin-1')  #open decrypted payload file
                decryptText = f.readlines() #output payload lines
                decryptLbl["image"] = ""
                decryptLbl["text"] = "\n".join(decryptText) #display decrypted payload text in UI
        except Exception as e:
            print(e)
            actionLbl["text"] = e
            actionLbl["fg"] = "red"
            encryptedImgLbl["image"] = ""
            decryptLbl["image"] = ""
            decryptLbl["text"] = ""
            return 0

    #function for image processing
    def processImage():
        if imgHiddenLbl["text"] != "" and plImgHiddenLbl["text"] != "": #if cover image and payload files are not empty
            encode()    #run encode function
        else:
            actionLbl["text"] = "Please upload a valid text file or an image" #display error message if uploaded file is not a text or image file
            actionLbl["fg"] = "red" #set text colour for the image

    #Styling parameters for UI
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
ENCRYPTFILE = "encode.png"  #file name for saving the encoded file
vslImg = ""
main()