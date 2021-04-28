import time
import grovepi
import math

from IMUCode.MPU9250 import MPU9250

mpu = MPU9250()

MAG_BASE_READ = 190

magRead = 0
while not magRead:
    try:
        magRead = mpu.readMagnet()
    except Exception as error:
        pass

class MagTracker:
    def __init__(self):
        self.hazardsList = []
        self.hazardsList.append(Magnet(self))
        self.gettingMagData = False
        self.mag = MAG_BASE_READ
        self.magX = 0
        self.magY = 0
        self.magZ = 0

    # returns a list of all known hazards
    def getHazards(self, x_pos, y_pos, theta):
        try:
            self.updateMag();
            if self.mag == 0 : self.mag = MAG_BASE_READ

            if not self.checkMagNear() and self.gettingMagData:
                self.gettingMagData = False
                self.hazardsList.append(Magnet(self))

            if self.checkMagNear():
                self.gettingMagData = True
                self.hazardsList[len(self.hazardsList)-1].update(theta, self.mag, x_pos, y_pos)
            return self.hazardsList
        except Exception as err:
            pass

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
        return abs(self.getMag() - MAG_BASE_READ)

    # Check if magnet is nearby to guess location
    def checkMagNear(self):
        if(self.magDiff() > 15):
            return True
        return False

    # Check if getting close to no-enter radius
    def checkMagDanger(self):
        if(self.getMag() < 165 or self.getMag() > 245):
            return True
        return False

class Magnet:
    def __init__(self, tracker):
        self.x = 0
        self.y = 0
        self.intensities = []
        self.tracker = tracker

    def magDist(self, mag):
        # B = mu0M/(4piR^3) = K/R^3 --> R = (K/B)^(1/3)
        # mag = 700000 / (r + 11)^3 + 95 regression equation
        # magDiff = 700000 / (r + 11)^3
        # r = (700000 / magDiff)^(1/3) - 11
        r = 0
        if mag != 0:
            r = (700000 / self.tracker.magDiff()) ** (1/3) - 11
        return r

        # Guess magnet position as some distance in front of robot
    def markMagnet(self, x, y, theta, mag):
        deltaX = self.magDist(mag) * math.cos(math.radians(theta))
        deltaY = self.magDist(mag) * math.sin(math.radians(theta))
        return x + deltaX, y + deltaY

    def update(self, theta, sensor_mag, robot_x, robot_y):
        self.intensities.append({'x': robot_x, 'y': robot_y, 'theta': theta, 'mag': sensor_mag})
        x_sum = 0
        y_sum = 0
        for i in self.intensities:
            tempList = self.markMagnet(i['x'], i['y'], i['theta'], i['mag'])
            x_sum += tempList[0]
            y_sum += tempList[1]

        self.x = x_sum / len(self.intensities)
        self.y = y_sum / len(self.intensities)

        return self.x, self.y
