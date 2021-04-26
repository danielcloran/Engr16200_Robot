import time
import grovepi
import math

from IMUCode.MPU9250 import MPU9250

mpu = MPU9250()

magRead = 0
while not magRead:
    try:
        magRead = mpu.readMagnet()
    except Exception as error:
        pass

class MagTracker:
    def __init__(self):
        self.beacon_intensity = []
        self.hazardsList = {}
        self.beaconNumber = 0
        self.magnetNear = False
        self.mag = 100
        self.magX = 0
        self.magY = 0
        self.magZ = 0

    # returns a list of all known hazards
    def getHazards(self, x_pos, y_pos, theta):
        try:
            self.updateMag();
            # print('mag: ', self.mag)
            if self.mag == 0 : self.mag = 100

            if self.magnetNear == True and self.mag == 0:
                self.beaconNumber += 1
                self.magnetNear = False
                self.hazardsList[self.beaconNumber] = magnet(self)

            if self.checkMagNear():
                self.magnetNear = True
                self.hazardsList[len(self.hazardsList)-1].update(theta, self.mag, x_pos, y_pos)
            #print('Getting Mag x: ', self.hazardsList[0].x, 'y:', self.hazardsList[0].y)
            return self.hazardsList
        except Exception as err:
            print(err)

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
        return abs(self.getMag() - 95)

    # Scalar distance to nearby magnet

    # Check if magnet is nearby to guess location
    def checkMagNear(self):
        if(self.magDiff() > 15):
            return True
        return False

    # Check if getting close to no-enter radius
    def checkMagDanger(self):
        # print('Mag Diff: ', self.magDiff())
        if(self.getMag() < 70 || self.getMag() > 150):
            return True
        return False

class magnet:
    def __init__(self, tracker):
        self.x = 0
        self.y = 0
        self.intesities = []
        self.tracker = tracker

    def magDist(self):
        # B = mu0M/(4piR^3) = K/R^3 --> R = (K/B)^(1/3)
        # mag = 700000 / (r + 11)^3 + 95 regression equation
        # magDiff = 700000 / (r + 11)^3
        # r = (700000 / magDiff)^(1/3) - 11
        mag = self.tracker.magDiff()
        r = 0
        if mag != 0:
            r = (700000 / self.tracker.magDiff()) ** (1/3) - 11
        return r

        # Guess magnet position as some distance in front of robot
    def markMagnet(self, x, y, theta):
        deltaX = self.magDist() * math.cos(math.radians(theta))
        deltaY = self.magDist() * math.sin(math.radians(theta))
        return x + deltaX, y + deltaY

    def getIntensity(self):
        return self.sensor_mag

    def update(self, theta, sensor_mag, robot_x, robot_y):
        self.intesities.append({'x': robot_x, 'y': robot_y, 'theta': theta, 'mag': sensor_mag})
        x_sum = 0
        y_sum = 0
        for i in self.intesities:

            x_sum, y_sum = self.markMagnet(robot_x, robot_y, theta)

        self.x = x_sum / len(self.intesities)
        self.y = y_sum / len(self.intesities)

        return self.x, self.y
