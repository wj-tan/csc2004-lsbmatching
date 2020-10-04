import numpy as np
from PIL import Image
from functools import reduce
import os

from .misc import board, calComplexity


class decoderClass():
    def __init__(self, infile, outfile, alpha):
        self.infile = infile
        self.outfile = outfile
        self.alpha = alpha
        self.gridSize = 8

        # Will be stored as an numpy array of gray codes. (3 per pixel for R, G, B)
        self.arr = None
        self.cap = None
        self.grids = None
        self.messages = None
        self.map = None

        self.nullbits = 0

        self.board = board(self.gridSize, self.gridSize)

    def toArray(self):
        """
        Converts image to numpy array.
        First converts images into a numpy array of RGB values
        Then converts the RGB values into canonical gray code

        Does not return any value
        """
        # Loading initial values from image
        tmparr = np.array(Image.open(
            self.infile).convert('RGB'),)

        # Lambda function to generate binary vectors
        to_str_func = np.vectorize(
            lambda x: np.binary_repr(x).zfill(self.gridSize))

        # Calling the function
        strs = to_str_func(tmparr)

        # Creating empty nparray with the correct size
        self.arr = np.zeros(list(tmparr.shape) +
                            [self.gridSize], dtype=np.int8)

        # Filling up the elements with the generated vectors
        for bit_ix in range(self.gridSize):
            fetch_bit_func = np.vectorize(lambda x: x[bit_ix] == '1')
            self.arr[..., bit_ix] = fetch_bit_func(strs).astype("int8")

        tmparr = np.copy(self.arr)

        # Conversion to Canonical Gray Code (Each bit is xor-ed with the previous one)
        for i in range(1, self.arr.shape[-1]):
            self.arr[..., i] = tmparr[..., i-1] ^ tmparr[..., i]

    def findGrids(self):
        """
        Find grids
        """
        print("Finding grids!")
        self.grids = [[y, y+self.gridSize, x, x+self.gridSize, param, bits]
                      for param in range(3)
                      for bits in range(int(self.gridSize/2), self.gridSize)
                      for y in range(0, self.arr.shape[0], self.gridSize)
                      for x in range(0, self.arr.shape[1], self.gridSize)]

        self.grids = [grid for grid in self.grids
                      if self.high_complexity(self.arr[grid[0]: grid[1], grid[2]:grid[3], grid[4], grid[5]])]

        self.messages, self.map = self.separateGrids()

        print("Found grids!")

    def high_complexity(self, arr):
        """
        Calculates the high_complexity of the current grid
        """
        return calComplexity(arr) >= self.alpha

    def separateGrids(self):
        """
        Returns message grids and conjugate grids
        """
        bitsPerGrid = self.gridSize*self.gridSize
        len_grids = len(self.grids)
        for x in range(len(self.grids)):
            if (bitsPerGrid*x*(1-(self.alpha+0.1))) >= (len_grids-x):
                return self.grids[:len_grids-x], self.grids[len_grids-x:]

    def unscrambleMap(self):
        """Removes trash bits from maps"""
        tbSize = int(round((self.alpha+0.1)*self.gridSize * self.gridSize))

        tmparr = []
        for m in self.map:
            g = self.arr[m[0]:m[1], m[2]:m[3], m[4],
                         m[5]].reshape(-1).tolist()[tbSize:]
            tmparr += g

        # First 8 bits of self.map is nullbits count
        self.map = tmparr

    def simplify(self, arr):
        arr = arr+self.board if arr[0][0] == 0 else arr + (1 - self.board)
        arr %= 2
        arr += 1
        arr %= 2

        return arr

    def extractData(self):
        """Gets message according to map"""

        # First 8 bits of self.map is nullbits count
        self.nullbits = np.array(self.map[:8])
        self.map = self.map[8:]

        # Convert nullbits into decimal
        self.nullbits = self.nullbits.dot(
            2**np.arange(self.nullbits.shape[0])[::-1])

        for i, m in enumerate(self.messages):
            g = self.arr[m[0]:m[1], m[2]:m[3], m[4], m[5]]
            self.messages[i] = self.simplify(g) if self.map[i] else g

        self.messages = np.array(self.messages)

    def decode(self):
        self.toArray()
        self.findGrids()
        self.unscrambleMap()
        self.extractData()

        self.messages = self.messages.dot(
            2**np.arange(self.messages.shape[2])[::-1])
        bits = np.hstack(self.messages).flatten().tolist()

        # Remove nullbits
        bits = bits[:(-self.nullbits)]
        string = ''.join([chr(b) for b in bits])

        with open(self.outfile, 'w') as f:
            f.write(string)


if __name__ == "__main__":
    alpha = 0.45
    infile = 'testFiles/output.png'
    msg = 'testFiles/message.txt'
    outfile = 'testFiles/output.txt'

    decoder = decoderClass(infile, outfile, alpha)
    decoder.decode()
