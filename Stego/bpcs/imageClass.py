import os
from itertools import product
import numpy as np
from PIL import Image
from functools import reduce

from .misc import board, calComplexity


class imageClass():
    def __init__(self, infile, outfile, alpha, gridSize):
        self.infile = infile
        self.outfile = outfile
        self.alpha = alpha
        self.gridSize = gridSize

        # Will be stored as an numpy array of gray codes. (3 per pixel for R, G, B)
        self.arr = None
        self.cap = None
        self.totalGrids = None
        self.usableGrids = None
        self.usableSpace = None
        self.vesselUsage = None

        self.messageGrids = None
        self.conjugateGrids = None

        self.i = 0

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

    def toImage(self):
        """
        Converts the numpy array back into an image.
        Stores the image in the given outfile

        Does not return anything
        """
        # Conversion to binary
        for i in range(1, self.arr.shape[-1]):
            self.arr[..., i] = self.arr[..., i-1] ^ self.arr[..., i]

        # Converting to decimal
        self.arr = self.arr.dot(2**np.arange(self.arr.shape[3])[::-1])

        # Saving image
        Image.fromarray(np.uint8(self.arr)).save(self.outfile)

    def cal_capacity(self):
        """
        Calculates the space in the vessel image that can be used to store messages
        """
        print("Calculating Capacity...")
        self.totalGrids = [[y, y+self.gridSize, x, x+self.gridSize, param, bits]
                           for param in range(3)
                           for bits in range(int(self.gridSize/2), self.gridSize)
                           for y in range(0, self.arr.shape[0], self.gridSize)
                           for x in range(0, self.arr.shape[1], self.gridSize)]

        self.usableGrids = [grid for grid in self.totalGrids
                            if self.high_complexity(self.arr[grid[0]: grid[1], grid[2]:grid[3], grid[4], grid[5]], grid)]

        self.usableSpace = len(self.usableGrids)

        self.messageGrids, self.conjugateGrids = self.separateGrids(
            self.usableGrids)

        print("With an alpha of {0}, there is {1:.2%} ({2} bytes) usable space".format(
            self.alpha, self.vesselUsage, len(self.messageGrids) * 4))

    def separateGrids(self, grids):
        """
        Returns message grids and conjugate grids
        """
        bitsPerGrid = self.gridSize*self.gridSize
        len_grids = len(grids)
        for x in range(len(grids)):
            if (bitsPerGrid*x) >= (len_grids-x):
                self.vesselUsage = int(self.gridSize/2) * (len_grids - x) / \
                    os.path.getsize(self.infile)
                return grids[:len_grids-x], grids[len_grids-x:]

        # edge case
        return 1

    def high_complexity(self, arr, g):
        """
        Checks complexity of grid is higher than alpha
        """
        max_complexity = arr.shape[0] * \
            (arr.shape[1] - 1) + (arr.shape[0] - 1) * arr.shape[1]

        complexity = ((sum(reduce(lambda x, y: np.abs(x) + np.abs(y), np.diff(arr))) +
                       sum(reduce(lambda x, y: np.abs(x) + np.abs(y), np.diff(arr.transpose())))) /
                      max_complexity)

        if ((arr.shape[1] != 8) or (arr.shape[0] != 8)) and complexity >= self.alpha:
            # Ensuring non-8 grids are low complexity, for simplicity
            a = self.arr[g[0]: g[1], g[2]: g[3], g[4], g[5]]
            self.arr[g[0]: g[1], g[2]: g[3], g[4], g[5]] = np.zeros(a.shape)
            return False

        return complexity >= self.alpha

    def getGrid(self):
        ys = self.usableGrids[self.i][0]
        ye = self.usableGrids[self.i][1]
        xs = self.usableGrids[self.i][2]
        xe = self.usableGrids[self.i][3]
        param = self.usableGrids[self.i][4]
        bits = self.usableGrids[self.i][5]

        self.i += 1

        return ys, ye, xs, xe, param, bits

    def replace(self, msg):
        ys, ye, xs, xe, param, bits = self.getGrid()
        self.arr[ys: ye, xs: xe, param, bits] = msg

    def cleanup(self):
        for i in range(self.i, self.usableSpace):
            ys, ye, xs, xe, param, bits = self.getGrid()
            self.arr[ys: ye, xs: xe, param, bits] = np.zeros(
                self.arr[ys: ye, xs: xe, param, bits].shape)


if __name__ == "__main__":
    alpha = 0.45
    gridSize = 8
    im = imageClass('testFiles/vessel.png',
                    'testFiles/output.png', alpha, gridSize)
    im.toArray()
    im.cal_capacity()

    # # print("For an alpha of {0}, there is {1:.1}% usable space".format(
    # #     alpha, im.vesselUsage))
    im.toImage()
