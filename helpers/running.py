import time
import random
import math

currentLocation = [50, 50]

while True:
    with open("sampleText.txt","a") as fh:
        fh.write((str(random.randint(0,200)) + "," + str(random.randint(0,200))+ "\n"))
    time.sleep(0.0001)