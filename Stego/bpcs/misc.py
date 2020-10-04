import numpy as np
from functools import reduce


def calComplexity(arr):
    mc = arr.shape[0] * \
        (arr.shape[1] - 1) + (arr.shape[0] - 1) * arr.shape[1]

    c = ((sum(reduce(lambda x, y: np.abs(x) + np.abs(y), np.diff(arr))) +
          sum(reduce(lambda x, y: np.abs(x) + np.abs(y), np.diff(arr.transpose())))) /
         mc)

    return c


def board(x, y):
    b = np.zeros((x, y), np.int32)
    b[::2, ::2] = 1
    b[1::2, 1::2] = 1
    return b
