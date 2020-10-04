import numpy as np
import os
from functools import reduce
from .misc import calComplexity, board


class messageClass():
    def __init__(self, infile, alpha, gridSize):
        self.infile = infile
        self.alpha = alpha
        self.gridSize = gridSize

        self.conjMap = []

        self.arr = None
        self.length = None

        self.nullbits = 0

        self.board = board(self.gridSize, self.gridSize)

        self.tbSize = int(
            round((self.alpha + 0.1)*self.gridSize * self.gridSize))

        self.tb = self.board.reshape(
            -1).tolist()[:self.tbSize]

    def toArray(self):

        char_list = None

        file = open(self.infile, 'r').read() if os.path.isfile(
            self.infile) else self.infile

        char_list = [ord(c) for c in file]

        # Ensuring char array can be reshaped into the gridSize
        while len(char_list) % self.gridSize != 0:
            self.nullbits += 1
            char_list.append(0)

        tmparr = np.array(char_list)

        tmparr = np.reshape(
            tmparr, (int(np.ceil(tmparr.shape[0]/self.gridSize)), self.gridSize))

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

        self.length = self.arr.shape[0]

    def prepareConjMap(self):
        """ Converts conjugation map from list into numpy array, ready for insertion """

        # Convert nullbits count into binary
        self.nullbits = [int(x) for x in np.binary_repr(
            self.nullbits).zfill(self.gridSize)]

        # Add nullbits count at the start of conjMap
        self.conjMap = self.nullbits + self.conjMap

        # Add trash bits to conjMap at appropriate intervals
        tmparr = []
        while self.conjMap:
            self.conjMap = self.tb + self.conjMap
            b = self.conjMap[:self.gridSize * self.gridSize]
            self.conjMap = self.conjMap[len(b):]
            while len(b) < self.gridSize*self.gridSize:
                b.append(0)
            b = np.array(b).reshape((self.gridSize, self.gridSize))
            tmparr.append(b)

        self.conjMap = np.array(tmparr)

    def fixComplexity(self):
        for i, x in enumerate(self.arr):
            if self.low_complexity(x):
                self.conjMap.append(1)
                self.arr[i] = self.complexify(x)
            else:
                self.conjMap.append(0)

    def low_complexity(self, arr):
        return calComplexity(arr) < self.alpha

    def complexify(self, arr):
        # Conjugation
        arr = arr+self.board if arr[0][0] == 0 else arr + (1 - self.board)
        arr %= 2

        return arr


if __name__ == "__main__":
    alpha = 0.45
    gridSize = 8
    msg = messageClass('files/message.txt', alpha, gridSize)
    msg.toArray()
    msg.fixComplexity()
    msg.prepareConjMap()
