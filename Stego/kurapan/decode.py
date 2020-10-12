#!/usr/bin/python

import math
from PIL import Image
from kurapan.utils import rgb_to_binary

#Starting function of this py
def runDecode(img_path):
	"""
	Opens an image which contains information of a hidden image,
	recovers the hidden image and saves it in a specified or
	default location.

	"""
	print("Initiate Decoding...")
	#Call decode to get file type and decoded payload
	isImage, decoded = decode(Image.open(img_path))
	#If is image
	if isImage:
		#Save it as png and return isImage the file path
		decoded.save('decrypt.png')
		print("Decoded!")
		return isImage, 'decrypt.png'
	#If is text
	else:
		#Save it as txt and return isImage the file path
		f = open('decrypt.txt', 'w+') # Output the extracted payload write it in text file
		f.write(decoded)
		f.close()
		print("Decoded!")
		return isImage, 'decrypt.txt'

#Decoding check and preparation
def decode(image):
	"""
	Loads the image to recover a hidden image from, retrieves the information about the
	size of the hidden image stored in the top left pixel of the visible image,
	extracts the hidden binary pixel values from the image and reconstructs the hidden
	image.

	Args:
	    image:    An RGB image to recover a hidden image from

	Returns:
	    A recovered image, which was hidden in the binary representation of the visible image
	"""
	#Load the image
	image_copy = image.load()
	#Get the width and height of the image
	width_visible, height_visible = image.size
	#Function to check for checking condition and get file type
	#True for image, False for txt
	isImage = check_Payload_Type(image_copy[0, 0], image_copy[0, 1])
	#is image
	if isImage:
		print("Payload is image...")
		#Get width and height of the payload
		width_hidden, height_hidden = get_payload_measurement(image_copy[0, 2], image_copy[0, 3])
		#Calculate the number of binary of the payload
		binary_count = (width_hidden * height_hidden) * 24
		#Get the payload binary
		hidden_binary = extract_hidden_binary(image_copy, width_visible, height_visible, binary_count, isImage)
		#Reconstruct the image using the binary
		decoded= reconstruct_image(hidden_binary, width_hidden, height_hidden)
	#is txt
	else:
		print("Payload is text...")
		#Get text count of the payload
		textCount = get_payload_textCount(image_copy[0, 2], image_copy[0, 3])
		#Calculate the number of binary of the payload
		binary_count = textCount * 8
		#Get the payload binary
		hidden_binary = extract_hidden_binary(image_copy, width_visible, height_visible, binary_count, isImage)
		#Reconstruct the text using the binary
		decoded = reconstruct_text(hidden_binary,textCount)
	#return if its image and the payload
	return isImage, decoded

#Check the checking condition and payload type
def check_Payload_Type(firstPx, secPx):
	print("Checking payload type...")
	#Retrieve all panes of first 2 px
	if len(firstPx) == 4:
		firstPxR, firstPxG, firstPxB, a = firstPx
		secPxR, secPxG, secPxB, a = secPx
	else:
		firstPxR, firstPxG, firstPxB = firstPx
		secPxR, secPxG, secPxB = secPx

	#Convert all panes to binary
	firstR_binary, firstG_binary, firstB_binary = rgb_to_binary(firstPxR, firstPxG, firstPxB)
	secR_binary, secG_binary, secB_binary = rgb_to_binary(secPxR, secPxG, secPxB)
	# print(firstR_binary, firstG_binary, firstB_binary,secR_binary, secG_binary, secB_binary )
	# print((firstR_binary[4:8], firstG_binary[4:8], firstB_binary[4:8]))
	# print((firstR_binary[4:8], firstG_binary[4:8], firstB_binary[4:8]) == ("1111","1111","1111"))
	# print((secR_binary, secG_binary, secB_binary))
	# print((secR_binary, secG_binary, secB_binary) == ("0000","0000","0000"))
	# print((firstR_binary[4:8], firstG_binary[4:8], firstB_binary[4:8]) == ("1111","1111","1111") and (secR_binary, secG_binary, secB_binary) == ("0000","0000","0000"))
	#Check if the 4 least significant bit of all panes contains corrosponding bit set during encode
	#For image, first px contains "1111" and second px contains "0000"
	if (firstR_binary[4:8], firstG_binary[4:8], firstB_binary[4:8]) == ("1111", "1111", "1111") and (
	secR_binary[4:8], secG_binary[4:8], secB_binary[4:8]) == ("0000", "0000", "0000"):
		return True
	# For text, first px contains "0000" and second px contains "1111"
	elif (firstR_binary[4:8], firstG_binary[4:8], firstB_binary[4:8]) == ("0000", "0000", "0000") and (
	secR_binary[4:8], secG_binary[4:8], secB_binary[4:8]) == ("1111", "1111", "1111"):
		return False
	# If do not fulfill the checking condition
	else:
		# Throw error message
		raise Exception("Image is not encrypted by this algorithm!")

def get_payload_measurement(thirdPx, fourthPx):
	#Retrieve all panes of 3rd and 4th px
	if len(thirdPx) == 4:
		thirdPxR, thirdPxG, thirdPxB, a = thirdPx
		fourthPxR, fourthPxG, fourthPxB, a = fourthPx
	else:
		thirdPxR, thirdPxG, thirdPxB = thirdPx
		fourthPxR, fourthPxG, fourthPxB = fourthPx

	#Convert all panes to binary
	thirdR_binary, thirdG_binary, thirdB_binary = rgb_to_binary(thirdPxR, thirdPxG, thirdPxB)
	fourthR_binary, fourthG_binary, fourthB_binary = rgb_to_binary(fourthPxR, fourthPxG, fourthPxB)
	#Combine the 4 least significant bit of all panes and convert back to decimal to get the width and height
	#3rd and 4th px store width and height corrospondinglu
	width = int(thirdR_binary[4:] + thirdG_binary[4:] + thirdB_binary[4:], 2)
	height = int(fourthR_binary[4:] + fourthG_binary[4:] + fourthB_binary[4:], 2)
	print("Payload width and height retrieved...")
	return width, height

def get_payload_textCount(thirdPx, fourthPx):
	#Retrieve all panes of 3rd and 4th px
	if len(thirdPx) == 4:
		thirdPxR, thirdPxG, thirdPxB, a = thirdPx
		fourthPxR, fourthPxG, fourthPxB, a = fourthPx
	else:
		thirdPxR, thirdPxG, thirdPxB = thirdPx
		fourthPxR, fourthPxG, fourthPxB = fourthPx

	#Convert all panes to binary
	thirdR_binary, thirdG_binary, thirdB_binary = rgb_to_binary(thirdPxR, thirdPxG, thirdPxB)
	fourthR_binary, fourthG_binary, fourthB_binary = rgb_to_binary(fourthPxR, fourthPxG, fourthPxB)
	#Combine the 4 least significant bit of all panes and convert back to decimal to get the text count
	textCount = int(thirdR_binary[4:] + thirdG_binary[4:] + thirdB_binary[4:] + fourthR_binary[4:] + fourthG_binary[4:] + fourthB_binary[4:], 2)
	print("Payload text count retrieved...")
	return textCount

#Retrieve the payload binary
def extract_hidden_binary(image, width_visible, height_visible, binary_count, isImage):
	"""
	Extracts a sequence of bits representing a sequence of binary values of
	all pixels of the hidden image.
	The information representing a hidden image is stored in the 4 least significant
	bits of a subset of pixels of the visible image.

	Args:
	    image:            An RGB image to recover a hidden image from
	    width_visible:    Width of the visible image
	    height_visible:   Height of the visible image
	    pixel_count:      Number of pixels in the hidden image

	Returns:
	    A binary string representing pixel values of the hidden image
	"""
	print("Decoding...")
	hidden_binary = ''
	#Number of bit retrieved
	idx = 0
	#Loop through all px of the encrypted image by col and row
	for col in range(width_visible):
		for row in range(height_visible):
			#Skip the first 4 px
			if row == 0 and col == 0:
				continue
			if row == 1 and col == 0:
				continue
			if row == 2 and col == 0:
				continue
			if row == 3 and col == 0:
				continue
			#Get each pane
			pixel = image[col, row]
			r = pixel[0]
			g = pixel[1]
			b = pixel[2]
			#Convert each pane to binary
			r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
			#If retrieved all, return binary
			if isImage:
				#Combine the binary
				hidden_binary += r_binary[4:8] + g_binary[4:8] + b_binary[4:8]
				#Increment the no. of binary accordingly
				idx += 12
				#Check if entire payload is retrieved
				if idx >= binary_count:
					print("Payload binary fully retrieved...")
					#If retrieved, return the binary
					return hidden_binary
			else:
				#Loop through each pane as not all pane may be used
				for b in (r_binary, g_binary, b_binary):
					#Append 4 least significant bit
					hidden_binary += b[4:8]
				#Increment the no. of binary accordingly
					idx += 4
					#Check if entire payload is retrieved
					if idx >= binary_count:
						print("Payload binary fully retrieved...")
						#If retrieved, return the binary
						return hidden_binary
	#If code reach here, it indicates that the payload unable to be fully retrieved from the encrypted image
	raise Exception("Payload failed to be fully retrieved from the encrypted image!")

#Reconstruct the image payload
def reconstruct_image(image_pixels, width, height):
	"""
	Recontructs the hidden image using the extracted string of pixel binary values.

	Args:
	    image_pixels:    A string of binary values of all pixels of the image to be recovered
	    width:           Width of the image to be recovered
	    height:          Height of the image to be recovered

	Returns:
	    The recovered image
	"""
	#Initalise new image
	image = Image.new("RGB", (width, height))
	image_copy = image.load()
	#Starting position of the binary
	idx = 0
	#Loop through each px of the payload by col and row
	for col in range(width):
		for row in range(height):
			#Fill in the binary for each pane
			r_binary = image_pixels[idx:idx+8] # bit pos: 0-7
			g_binary = image_pixels[idx+8:idx+16] # bit pos: 8-15
			b_binary = image_pixels[idx+16:idx+24]# bit pos: 16-23
			try:
				#Convert it back to value of each pane
				image_copy[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
			#If the payload is corrupted or incomplete
			except:
				raise Exception("Error: Unable to reconstruct image payload")
			#Increment the starting pos of binary accordingly
			idx += 24
	print("Payload image reconstructed...")
	#return the payload
	return image

#Reconstruct the text payload
def reconstruct_text(text_pixels,textCount):
	#Starting position of the binary
	idx = 0
	payload = ""
	#Loop the number of character
	for c in range(textCount):
		#Convert it from binary to ASCII then back to char
		payload += chr(int(text_pixels[idx:idx+8],2))
		#Increment the starting pos of binary accordingly
		idx += 8
	print("Payload text reconstructed...")
	#return the payload
	return payload


