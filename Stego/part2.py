import tkinter as tk  # tkinter python user interface
from tkinter import filedialog  # import filedialog module
# pip install pillow
from PIL import ImageTk, Image  # import modules for image manipulation functions
from kurapan.decode import runDecode  # use Kurapan Hide image in image library for decoding image
from kurapan.encode import runEncode  # use Kurapan Hide image in image library for encoding image


def main():
    #function to upload payload image
    def UploadPL(event=None):
        # Empty all encrypted and decrypted image, and message label
        encryptedImgLbl["image"] = ""
        decryptLbl["image"] = ""
        decryptLbl["text"] = ""
        messageLbl["text"] = ""
        filename = filedialog.askopenfilename() #UI prompt to upload file
        #If nothing is selected
        if filename == "":
            #Empty payload filepath and label
            plLbl["text"] = ""
            plLbl["image"] = ""
            plImgHiddenLbl["text"] = ""
            #Show error message
            messageLbl["text"] = "No file is selected for payload!"
            messageLbl["fg"] = "red"
            #stop the function
            return 0
        #Something is selected
        plImgHiddenLbl["text"] = filename   #store payload filepath to be encoded
        #Try image payload
        try:
            #If is not image, this will throw error executing the code in except instead
            img = Image.open(filename)  #open payload image
            width, height = img.size    #get width and height of image
            newHeight = int(height / (width / 250))  #resize image for UI
            img = img.resize((250, int(newHeight)), Image.ANTIALIAS)  #fit resized image to the UI
            img = ImageTk.PhotoImage(img)   #initialize image for UI
            payloadCanvas.image = img  #set image canvas for UI
            plLbl["image"] = img   #display payload image in UI
            messageLbl["text"] = "" #empty error message text in UI
        #For text payload
        except IOError:
            filetype = str.split(filename,".")[-1]
            if(filetype == "txt"):
                f = open(filename, 'r', encoding='latin-1')  # open text file
                payloadText = f.readlines() #retrieve payload text
                plLbl["image"] = "" #empty image in UI
                plLbl["text"] = "\n".join(payloadText) #display payload text in UI
                messageLbl["text"] = "" #empty error message text in UI
                f.close()   #close text file
            else:
                #Empty payload filepath and label
                plLbl["text"] = ""
                plLbl["image"] = ""
                plImgHiddenLbl["text"] = ""
                #Show error message
                messageLbl["text"] = "File selected is not image or .txt!"
                messageLbl["fg"] = "red"


    #function to upload cover image
    def UploadImage(event=None):
        # Empty all encrypted and decrypted image, and message label
        encryptedImgLbl["image"] = ""
        decryptLbl["image"] = ""
        decryptLbl["text"] = ""
        messageLbl["text"] = ""
        filename = filedialog.askopenfilename() #UI prompt to upload file
        #If nothing is selected
        if filename == "":
            #Empty cover image filepath and image
            imgLbl["image"] = ""
            imgHiddenLbl["text"] = ""
            #Show error message
            messageLbl["text"] = "No file is selected for cover image!"
            messageLbl["fg"] = "red"
            #stop the function
            return 0
        try:
            img = Image.open(filename)  #open cover image
            imgHiddenLbl["text"] = filename #store cover image for encoding
            width, height = img.size   #get width and height of image
            newHeight = int(height / (width / 250))  #resize image for UI
            img = img.resize((250, int(newHeight)), Image.ANTIALIAS) #fit resized image to the UI
            img = ImageTk.PhotoImage(img)   #initialize image for UI
            imgCanvas.image = img   #set image canvas for UI
            imgLbl["image"] = img   #display cover image in UI
            messageLbl["text"] = "" #empty error message text in UI
        except IOError:
            #Empty cover image filepath and image
            imgLbl["image"] = ""
            imgHiddenLbl["text"] = ""
            #Show error message
            messageLbl["text"] = "File selected is not image!"
            messageLbl["fg"] = "red"

    #function to encode payload into image and display encoded image
    def encode():
        payload = plImgHiddenLbl["text"]    #access payload from UploadPL function
        vslImg = imgHiddenLbl["text"]   #access cover image from UploadImage function
        messageLbl["text"] = "Encrypting... Please Wait..."   #display encrypting in progress message
        messageLbl["fg"] = "black" #set text colour for the image
        #Try image payload
        try:
            #If is not image, this will throw error executing the code in except instead
            Image.open(payload)  #open the image payload
            runEncode(vslImg, payload, ENCRYPTFILE,True)    #run encode function from the Kurapan Hide image in image library
        #for text payload
        except IOError:
            runEncode(vslImg, payload, ENCRYPTFILE, False)    #run encode function from the Kurapan Hide image in image library
        #Error is thrown if cover image is too small for the payload
        except Exception as e:
            #Output error message
            print(e)
            messageLbl["text"] = e
            # Empty all encrypted and decrypted image, and message label
            messageLbl["fg"] = "red"
            encryptedImgLbl["image"] = ""
            decryptLbl["image"] = ""
            decryptLbl["text"] = ""
            #stop the function
            return 0

        img = Image.open(ENCRYPTFILE)  #open encoded image
        width, height = img.size   #get width and height of image
        newHeight = int(height / (width / 250))  #resize image for UI
        img = img.resize((250, int(newHeight)), Image.ANTIALIAS) #fit resized image to the UI
        img = ImageTk.PhotoImage(img)   #initialize image for UI
        encryptedImgCanvas.image = img  #set image canvas for UI
        encryptedImgLbl["image"] = img   #display encoded image in UI

        messageLbl["text"] = "Steganography Done!"   #display success message
        messageLbl["fg"] = "black" #set text colour for the image
        decrypt() #initialise decryption

    #function to decode encoded image and display payload
    def decrypt():
        try:
            #retrieve if is image (bool), and decrypted filepath
            isImage, decryptFile = runDecode(ENCRYPTFILE)   #run decode function from the Kurapan Hide image in image library
            #for image payload
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
                decryptLbl["image"] = "" #empty image in UI
                decryptLbl["text"] = "\n".join(decryptText) #display decrypted payload text in UI
        #Error is thrown if image is not encrypted by our encryption function
        except Exception as e:
            #Output error message
            print(e)
            messageLbl["text"] = e
            # Empty all encrypted and decrypted image, and message label
            messageLbl["fg"] = "red"
            encryptedImgLbl["image"] = ""
            decryptLbl["image"] = ""
            decryptLbl["text"] = ""
            #stop the function
            return 0

    #function for image processing
    def processImage():
        if imgHiddenLbl["text"] != "" and plImgHiddenLbl["text"] != "": #if cover image and payload files are not empty
            encode()    #run encode function
        else:
            messageLbl["text"] = "Please upload a valid cover image and payload" #display error message if uploaded file is not a text or image file
            messageLbl["fg"] = "red" #set text colour for the image

    #Styling parameters for UI
    window = tk.Tk()
    window.configure(background="white")
    window.title("Main Menu")
    mainFrame = tk.Frame(window, bg="white")
    mainFrame.pack(padx=20, pady=5)

    #Canvas to store images
    imgCanvas = tk.Canvas()
    payloadCanvas = tk.Canvas()
    encryptedImgCanvas = tk.Canvas()
    decryptedImgCanvas = tk.Canvas()

    #UI for payload
    plFrame = tk.Frame(mainFrame, bg="white")
    plFrame.pack(padx=20, pady=5)
    plInputLbl = tk.Label(plFrame, text="Upload Payload: ", font="Ariel 16 normal", bg="white")
    plInputLbl.pack(side=tk.LEFT, padx=20, pady=5)
    plbtn = tk.Button(plFrame, text='Upload', command=UploadPL)
    plbtn.pack(side=tk.RIGHT, padx=20, pady=5)
    plLbl = tk.Label(plFrame)
    plLbl.pack()
    #hidden label to store the file path
    plImgHiddenLbl = tk.Label(plFrame)

    #UI for cover image
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
    #hidden label to store the file path
    imgHiddenLbl = tk.Label(uploadImgFrame)

    #UI for encrypted image
    encryptedImgFrame = tk.Frame(imgFrame, bg="white")
    encryptedImgFrame.pack(side=tk.RIGHT, padx=20, pady=5)
    encryptedTextLbl = tk.Label(encryptedImgFrame, text="Encrypted Image", font="Ariel 16 normal", bg="white")
    encryptedTextLbl.pack(padx=20, pady=5)
    encryptedImgLbl = tk.Label(encryptedImgFrame, bg="white")
    encryptedImgLbl.pack()

    #UI for decrypted payload
    plOutputLbl = tk.Label(mainFrame, text="Payload", font="Ariel 16 underline", bg="white")
    plOutputLbl.pack(padx=20, pady=5)
    decryptLbl = tk.Label(mainFrame)
    decryptLbl.pack(padx=20, pady=5)
    messageLbl = tk.Label(mainFrame, font="Ariel 16", bg="white")
    messageLbl.pack(padx=20, pady=5)
    #Loop the window
    window.mainloop()

#encrypted filepath
global ENCRYPTFILE
ENCRYPTFILE = "encode.png"  #file name for saving the encoded file
#Run main function
main()