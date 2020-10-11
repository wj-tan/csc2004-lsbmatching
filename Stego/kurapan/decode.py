#!/usr/bin/python

import os, sys
from PIL import Image
from kurapan.utils import rgb_to_binary

def runDecode(img_path):
	"""
	Opens an image which contains information of a hidden image,
	recovers the hidden image and saves it in a specified or
	default location.

	"""

	print("Decoding...")
	isImage ,decoded = decode(Image.open(img_path))
	print(isImage)
	if isImage:
		decoded.save('decrypt.png')
		return isImage, 'decrypt.png'
	else:
		f = open('decrypt.txt', 'w+') # Output the extracted payload write it in text file
		f.write(decoded)
		f.close()
		return isImage, 'decrypt.txt'
	print("Decoded!")


def extract_hidden_pixels(image, width_visible, height_visible, pixel_count):
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
	hidden_image_pixels = ''
	idx = 0
	for col in range(width_visible):
		for row in range(height_visible):
			if row == 0 and col == 0:
				continue
			if row == 1 and col == 0:
				continue
			if row == 2 and col == 0:
				continue
			if len(image[col, row]) == 4:
				r, g, b, a = image[col, row]
			else:
				r, g, b = image[col, row]
			r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
			hidden_image_pixels += r_binary[4:8] + g_binary[4:8] + b_binary[4:8]
			if idx >= pixel_count * 2:
				return hidden_image_pixels
	return hidden_image_pixels

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
	image = Image.new("RGB", (width, height))
	image_copy = image.load()
	idx = 0
	for col in range(width):
		for row in range(height):
			r_binary = image_pixels[idx:idx+8] # bit pos: 0-7
			g_binary = image_pixels[idx+8:idx+16] # bit pos: 8-15
			b_binary = image_pixels[idx+16:idx+24]# bit pos: 16-23
			try:
				image_copy[col, row] = (int(r_binary, 2), int(g_binary, 2), int(b_binary, 2))
			except:
				print("Error: Cover Image too small")
				return image
			idx += 24
	return image

def reconstruct_text(text_pixels,noOfChar):
	idx = 0
	payload = ""
	for c in range(noOfChar):
		payload += chr(int(text_pixels[idx:idx+8],2))
		idx += 8
	return payload

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
	image_copy = image.load()
	width_visible, height_visible = image.size
	if len(image_copy[0, 0]) == 4:
		firstR, firstG, firstB, a = image_copy[0, 0]
		secR, secG, secB, a = image_copy[0, 1]
		r, g, b, a = image_copy[0, 2]
	else:
		firstR, firstG, firstB = image_copy[0, 0]
		secR, secG, secB = image_copy[0, 1]
		r, g, b = image_copy[0, 2]

	r_binary, g_binary, b_binary = rgb_to_binary(r, g, b)
	w_h_binary = r_binary + g_binary + b_binary
	#is image
	print(firstR, firstG, firstB,secR, secG, secB)
	if firstR == 255 and firstG == 255 and firstB == 255 and secR == 0 and secG == 0 and secB == 0:

		width_hidden = int(w_h_binary[0:12], 2)
		height_hidden = int(w_h_binary[12:24], 2)
		pixel_count = width_hidden * height_hidden
		hidden_image_pixels = extract_hidden_pixels(image_copy, width_visible, height_visible, pixel_count)
		decoded= reconstruct_image(hidden_image_pixels, width_hidden, height_hidden)
		return True,decoded
	#is txt
	elif firstR == 0 and firstG == 0 and firstB == 0 and secR == 255 and secG == 255 and secB == 255:
		noOfChar = int(w_h_binary, 2)
		hidden_text_pixels = extract_hidden_pixels(image_copy, width_visible, height_visible, noOfChar)
		decoded = reconstruct_text(hidden_text_pixels,noOfChar)
		return False, decoded
	else:
		raise Exception("Image is not encrypted")

	return decoded
