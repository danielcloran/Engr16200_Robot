import brickpi3
import grovepi
import math
import sys
import time
from IMUCode.MPU9250 import MPU9250

mpu = MPU9250()

mag = 0
magX = 0
magY = 0
magZ = 0

class magSensor:
    def __init__(self):
        self.mag = 0
        self.magX = 0
        self.magY = 0
        self.magZ = 0

    # Update magnetic readings
    def updateMag(self):
        m = mpu.readMagnet()
        self.magX = m['x']
        self.magY = m['y']
        self.magZ = m['z']
        self.mag = math.sqrt(self.magX ** 2 + self.magY ** 2 + self.magZ ** 2)

    # Magnetic magnitude
    def getMag(self):
        return self.mag

    # Magnetic x vector component
    def getMagX(self):
        return self.magX

    # Magnetic y vector component
    def getMagY(self):
        return self.magY

    # Magnetic z vector component
    def getMagZ(self):
        return self.magZ

    # Difference between mag reading and background mag field
    def magDiff(self):
        return abs(self.getMag() - 100)

    # Scalar distance to nearby magnet
    def magDist(self):
        # B = mu0M/(4piR^3) = K/R^3 --> R = (K/B)^(1/3)
        # k = r^3 * magDiff --> k = 1350000 guess using mag of 150 at 30 cm from magnet
        k = 1350000 # can probably get a better value by fine tuning during testing
        mag = self.getMag()
        r = 0
        if mag != 0:
            r = (k / self.magDiff()) ** (1/3)
        return r

    # Guess magnet position as some distance in front of robot
    def markMagnet(self, x, y, theta):
        deltaX = self.magDist() * math.cos(math.radians(theta))
        deltaY = self.magDist() * math.sin(math.radians(theta))
        return x + deltaX, y + deltaY

    # Check if magnet is nearby to guess location
    def checkMagNear(self):
        if(self.magDiff() > 30):
            return True
        return False

    # Check if getting close to no-enter radius
    def checkMagDanger(self):
        if(self.magDiff() > 60):
            return True
        return False
