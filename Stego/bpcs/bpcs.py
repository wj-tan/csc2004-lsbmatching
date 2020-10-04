#!/usr/bin/env python
"""
BPCS Steganography: encoding/decoding messages hidden in a vessel image
Source: http://web.eece.maine.edu/~eason/steg/SPIE98.pdf
BEHAVIORS:
    encoding
        * expects a vessel image file, message file, and alpha value
        * hides the contents of a file inside a vessel image
    decoding
        * expects a vessel image file, and alpha value
        * recovers the message stored inside a vessel image
    capacity
        * expects a vessel image file and alpha value
        * assesses the maximum size of a message that could be encoded within the vessel image
"""

import os.path
import argparse

from .imageClass import imageClass
from .messageClass import messageClass
from .encodeClass import encoderClass
from .decodeClass import decoderClass


# alpha = 0.45
# vslfile = 'bpcs/files/vessel.png'
# msgfile = 'bpcs/files/message.txt'  # Accepts strings too
# encfile = 'bpcs/files/encoded.png'
# msgfile_decoded = 'bpcs/files/output.txt'

# # check max size of message you can embed in vslfile
# en = encoderClass(vslfile, msgfile, encfile, alpha)
# de = decoderClass(encfile, msgfile_decoded, alpha)

# en.getCapacity()
# en.encode()
# de.decode()

parser = argparse.ArgumentParser()

valid_opt_behaviors = {
    'encode': ['infile', 'message', 'alpha'],
    'decode': ['infile', 'outfile', 'alpha'],
    'capacity': ['infile', 'outfile', 'alpha'],
    'test': []
}

parser.add_argument('behavior', type=str, help='interaction modes: {0}'.format(
    valid_opt_behaviors.keys()))
parser.add_argument('-i', '--infile', type=str,
                    help='path to vessel image (.png)')
parser.add_argument('-o', '--outfile', type=str,
                    help='path to write output file')
parser.add_argument('-m', '--message', type=str,
                    help='path to message file')
parser.add_argument('-a', '--alpha', type=float,
                    help='complexity threshold', default=0.45)
opts = parser.parse_args()


def check_file_exists(filename):
    if not os.path.exists(filename):
        parser.error('The file "{0}" could not be found.'.format(filename))


if opts.behavior == 'decode':
    check_file_exists(opts.infile)
    decoderClass(opts.infile, opts.outfile, opts.alpha).decode()
elif opts.behavior == 'encode':
    check_file_exists(opts.infile)
    encoderClass(opts.infile, opts.message, opts.outfile, opts.alpha).encode()
elif opts.behavior == 'capacity':
    check_file_exists(opts.infile)
    encoderClass(opts.infile, "", "", opts.alpha).getCapacity()
