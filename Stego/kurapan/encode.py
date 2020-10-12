#!/usr/bin/python
import math
import os, sys
from PIL import Image
from kurapan.utils import rgb_to_binary, add_leading_zeros

#Starting function of this py
def runEncode(img_visible_path,hidden_file_path,output_path,isImage):
	"""
	Opens two specified images, an image we want to conceal and an image we want to use for concealing,
	hides the image information in the binary pixel values of the other image and saves
	the resulting image in a specified location or the default location if no location is specified.

	The number of pixels in the image used for hiding an image must be at least (2 * number of pixels in the image to be
	hidden + 1)

	"""
	#open the cover image
	img_visible = Image.open(img_visible_path)
	print("Initiate Encoding...")
	#If is image
	if isImage:
		print("Payload is image...")
		#Load the image and run the image encode function
		img_hidden = Image.open(hidden_file_path)
		#Get the encoded image
		encoded_image = encodeImage(img_visible, img_hidden)
	#If is text
	else:
		print("Payload is text...")
		#Open the payload to get text
		f = open(hidden_file_path, 'r', encoding='latin-1')
		payloadText = f.read()
		#Get the encoded image
		encoded_image = encodeText(img_visible, payloadText)
	#Save the encoded image
	encoded_image.save(output_path)
	print("Encoded")

#Encoding preparation for text
def encodeText(img_visible, payload):
	#Load the image
	cover_image = img_visible.load()
	#Get the height and width of the cover image
	width_visible, height_visible = img_visible.size
	#Calculate the number of pixel
	img_visible_noOfPixel = width_visible * height_visible
	#Calculate if the cover image is large enough to store the payload
	#2 px can store 3 char of payload hence * 2/3
	#4 px used for verification and keeping payload len
	if img_visible_noOfPixel < math.ceil(len(payload) * 2 / 3) + 4:
		#If not large enough, throw error message
		raise Exception("Cover image too small for the payload!")
	#Convert text to binary
	binary = convert_text_to_binary(payload)
	#Get payload length
	textCount = len(payload)
	#Call the function to do the encoding
	encode_payload(cover_image, binary, width_visible, height_visible, 0, 0, False, textCount)
	#Return the encrypted image
	return img_visible

#Encoding preparation for image
def encodeImage(img_visible, img_hidden):
	"""
	Loads the image to be hidden and the image used for hiding and conceals the pixel information from one image
	in the other one.

	Args:
	    img_visible:    An RGB image used for hiding another image
	    img_hidden:     An RGB image to be concealed

	Returns:
	    An RGB image which is supposed to be not very different visually from img_visible, but contains all the information
	    necessary to recover an identical copy of the image we want to hide.
	"""
	#Load both cover and payload image
	cover_image = img_visible.load()
	img_hidden_copy = img_hidden.load()
	#Get their width and height, and calculate their no. of px
	width_visible, height_visible = img_visible.size
	width_hidden, height_hidden = img_hidden.size
	img_visible_noOfPixel = width_visible * height_visible
	img_hidden_noOfPixel = width_hidden * height_hidden
	#Calculate if the cover image is large enough to store the payload
	#2 px of cover image is needed to store 1 px of payload hence * 2
	#4 px used for verification and keeping payload width and height
	if img_visible_noOfPixel < img_hidden_noOfPixel * 2 + 4:
		#If not large enough, throw error message
		raise Exception("Cover image too small for the payload!")

	#Convert image to binary
	hidden_image_binary = convert_image_rbg_to_binary(img_hidden_copy, width_hidden, height_hidden)
	#Call the function to do the encoding
	encode_payload(cover_image, hidden_image_binary, width_visible, height_visible, width_hidden, height_hidden,True, 0)
	return img_visible

#Convert text to binary
def convert_text_to_binary(payload):
	iBlist = [add_leading_zeros(bin(ord(b))[2:], 8) for b in payload]  # Convert each character into ASCI representation in int and then into binary
	print("Text converted to binary...")
	return "".join(iBlist)   # Combine all the bin into a single string and return it

#Convert image to binary
def convert_image_rbg_to_binary(img, width, height):
	"""
	Retrieves a string of concatenated binary representations of RGB channel values of all pixels in an image.

	Args:
	    img:    An RGB image
	    width:  Width of the image
	    height: Height of the image

	Returns:
	    A string with concatenated binary numbers representing the RGB channel values of all pixels in the image
	    where each binary number representing one channel value is 8 bits long, padded with leading zeros
	    when necessary. Therefore, each pixel in the image is represented by 24 bit long binary sequence.
	"""
	hidden_image_binary = ''
	#Loop through every pixel by its column and row
	for col in range(width):
		for row in range(height):
			#Get the pixel of each pane
			pixel = img[col, row]
			r = pixel[0]
			g = pixel[1]
			b = pixel[2]
			#Convert it to binary
			r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
			#Add the binary together
			hidden_image_binary += r_binary + g_binary + b_binary

	print("Image converted to binary...")
	#Return the binary
	return hidden_image_binary

#Encode payload into the cover image
def encode_payload(img_visible, hidden_file_binary, width_visible, height_visible, width_hidden, height_hidden, isImage, textCount):
	"""
	Replaces the 4 least significant bits of a subset of pixels in an image with bits representing a sequence of binary
	values of RGB channels of all pixels of the image to be concealed.

	The first pixel in the top left corner is used to store the width and height of the image to be hidden, which is
	necessary for recovery of the hidden image.

	Args:
	    img_visible:          An RGB image to be used for hiding another image
	    hidden_file_binary:   Binary string representing all pixel values of the image to be hidden
	    width_visible:        Width of the image to be used for hiding another image
	    height_visible:       Height of the image to be used for hiding another image
	    width_hidden:         Width of the image to be hidden
	    height_hidden:        Height of the image to be hidden

	Returns:
	    An RGB image which is a copy of img_visible where the 4 least significant bits of a subset of pixels
	    are replaced with bits representing the hidden image.
	"""
	print("Encoding...")
	#Starting position of the binary
	idx = 0
	#Convert the height, width and text count to binary
	#Height and width is set to 0 for text while text count is set to 0 for image
	width_hidden_binary = add_leading_zeros(bin(width_hidden)[2:], 12)
	height_hidden_binary = add_leading_zeros(bin(height_hidden)[2:], 12)
	text_count_binary = add_leading_zeros(bin(textCount)[2:], 24)
	#Loop through each px of the cover image by row and column
	for col in range(width_visible):
		for row in range(height_visible):
			#Convert each pane of the px to binary
			pixel = img_visible[col, row]
			r = pixel[0]
			g = pixel[1]
			b = pixel[2]
			r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
			#Checking condition
			#For image:
			#   4 least significant bit of each pane for first px is change to 1
			#   4 least significant bit of each pane for second px is change to 0
			#For txt:
			#   4 least significant bit of each pane for first px is change to 0
			#   4 least significant bit of each pane for second px is change to 1
			#First px
			if row == 0 and col == 0:
				#If is image
				if isImage:
					#Set 4 least significant bit to 1
					r_binary = r_binary[0:4] + "1111"
					g_binary = g_binary[0:4] + "1111"
					b_binary = b_binary[0:4] + "1111"
					img_visible[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
				#If is txt
				else:
					#Set 4 least significant bit to 0
					r_binary = r_binary[0:4] + "0000"
					g_binary = g_binary[0:4] + "0000"
					b_binary = b_binary[0:4] + "0000"
					img_visible[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
				continue
			#Second px
			if row == 1 and col == 0:
				#If is image
				if not isImage:
					#Set 4 least significant bit to 0
					r_binary = r_binary[0:4] + "1111"
					g_binary = g_binary[0:4] + "1111"
					b_binary = b_binary[0:4] + "1111"
					img_visible[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
				#If is txt
				else:
					#Set 4 least significant bit to 1
					r_binary = r_binary[0:4] + "0000"
					g_binary = g_binary[0:4] + "0000"
					b_binary = b_binary[0:4] + "0000"
					img_visible[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
				continue

			#Third px
			elif row == 2 and col == 0:
				#If is image
				#Store width
				if isImage:
					#Width is set to 12 bit and split into 3 and replace 4 least significant of each pane
					r_binary = r_binary[0:4] + width_hidden_binary[0:4]
					g_binary = g_binary[0:4] + width_hidden_binary[4:8]
					b_binary = b_binary[0:4] + width_hidden_binary[8:12]
					img_visible[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
				#If is txt
				#Store first half of text count
				else:
					#Text count is set to 24 bit, first 12 bit store here, split into 3 and replace 4 least significant of each pane
					r_binary = r_binary[0:4] + text_count_binary[0:4]
					g_binary = g_binary[0:4] + text_count_binary[4:8]
					b_binary = b_binary[0:4] + text_count_binary[8:12]
					img_visible[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
				continue

			#Fourth px
			elif row == 3 and col == 0:
				#If is image
				#Store height
				if isImage:
					#Height is set to 12 bit and split into 3 and replace 4 least significant of each pane
					r_binary = r_binary[0:4] + height_hidden_binary[0:4]
					g_binary = g_binary[0:4] + height_hidden_binary[4:8]
					b_binary = b_binary[0:4] + height_hidden_binary[8:12]
					img_visible[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
				#If is txt
				#Store second half of text count
				else:
					#Text count is set to 24 bit, last 12 bit store here, split into 3 and replace 4 least significant of each pane
					r_binary = r_binary[0:4] + text_count_binary[12:16]
					g_binary = g_binary[0:4] + text_count_binary[16:20]
					b_binary = b_binary[0:4] + text_count_binary[20:24]
					img_visible[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
				continue
			#After fourth px
			else:
				#Replace 4 least significant of each pane with 4 bit of payload in sequence
				r_binary = r_binary[0:4] + hidden_file_binary[idx:idx+4]
				g_binary = g_binary[0:4] + hidden_file_binary[idx+4:idx+8]
				b_binary = b_binary[0:4] + hidden_file_binary[idx+8:idx+12]
				#Increment the starting position of binary by 12 since 12 bit is inserted
				idx += 12
			img_visible[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
			#If starting position exceed the number of binary
			#Indicate all bit is encrypted into the cover image
			if idx >= len(hidden_file_binary):
				#Return the encrypted image
				return img_visible
	#If code reach here, it indicates that the payload unable to be fully encrypted into the cover image
	raise Exception("Payload failed to be fully encrypt into the cover image!")