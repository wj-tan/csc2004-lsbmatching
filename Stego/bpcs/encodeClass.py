import numpy as np
from functools import reduce

from .misc import calComplexity

from .imageClass import imageClass
from .messageClass import messageClass


class encoderClass():
    def __init__(self, vesselPath, messagePath, outputPath, alpha):
        self.alpha = alpha
        self.gridSize = 8

        self.outfile = outputPath

        self.vessel = imageClass(vesselPath, outputPath, alpha, self.gridSize)
        self.message = messageClass(messagePath, alpha, self.gridSize)

    def getCapacity(self):
        self.vessel.toArray()
        self.vessel.cal_capacity()

    def preProcess(self):
        print("Loading files...")
        self.vessel.toArray()
        self.vessel.cal_capacity()
        self.message.toArray()
        self.message.fixComplexity()
        self.message.prepareConjMap()

    def verify(self):
        if self.message.length > self.vessel.usableSpace:
            print("Message too big for current parameters")
            exit()
        else:
            print("Verified size!")
            print("Message Length: \t{0}\tgrid(s)\nVessel Usable Space:\t{1}\tgrid(s)".format(
                self.message.length, self.vessel.usableSpace))

    def encode(self):
        self.preProcess()
        self.verify()

        print("Encoding...")

        for msg in self.message.arr:
            self.vessel.replace(msg)

        for cm in self.message.conjMap:
            self.vessel.replace(cm)

        self.vessel.cleanup()

        # for msg in self.message.arr:
        print("Encoded!")

        self.vessel.toImage()


if __name__ == "__main__":
    alpha = 0.45
    vessel = 'testFiles/vessel.png'
    msg = 'testFiles/message.txt'
    outfile = 'testFiles/output.png'

    encoder = encoderClass(vessel, msg, outfile, alpha)
    encoder.encode()
