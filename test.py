import curses
import threading
import numpy as np
import time
import random

class Magnet:
    def __init__(self, tracker):
        self.x = random.randint(0,55)
        self.y = random.randint(0,55)
        self.intensities = []
        self.tracker = tracker

def writeHazardsList():
    fh = open("hazardslist.csv", "w")
    fh.write("Hazard Type,Parameter of Interest,Parameter Value,Hazard X Coordinate,Hazard Y Coordinate \n")
    for i in range(len(magHazards)):
        fh.write("Electrical / Magnetic Activity Source,Field Strength (mT),")
        fh.write("0," + str(magHazards[i].x) + "," + str(magHazards[i].y) + "\n")

    for i in range(len(irHazards)):
        fh.write("Biohazard / IR Activity Source,Mass (g),")
        fh.write("0," + str(irHazards[i].x) + "," + str(irHazards[i].y) + "\n")
    fh.close()

magHazards = []
for x in range(3):
    magHazards.append(Magnet(None))

irHazards = []
for x in range(3):
    irHazards.append(Magnet(None))

writeHazardsList()
