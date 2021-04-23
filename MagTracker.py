import time
import grovepi
import math
from physicalMapper import *

class MagTracker:
    def __init__(self):
        self.beacon_intensity = []
        self.hazardsList = {}
        self.beaconNumber = 0
        self.dataInBeacon = False

    # returns a list of all known hazards
    def getHazards(self, x_pos, y_pos, theta):
        try:
            sensor_mag = getMag();
            print('mag:',sensor_mag)

            if self.dataInBeacon == True and sensor_mag == 0:
                self.beaconNumber += 1
                self.dataInBeacon = False
                self.hazardsList[self.beaconNumber] = Beacon()
                
            if magDiff() > 20:
                self.dataInBeacon = True
                self.hazardsList[len(self.hazardsList)-1].update(theta, sensor_mag, x_pos, y_pos)
            #print('Getting Mag x: ', self.hazardsList[0].x, 'y:', self.hazardsList[0].y)
            return self.hazardsList
        except Exception as err:
            print(err)

class Beacon:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.intesities = []

    def getIntensity(self):
        return self.sensor_mag

    def update(self, theta, sensor_mag, robot_x, robot_y):
        self.intesities.append({'x': robot_x, 'y': robot_y, 'theta': theta, 'mag': sensor_mag})
        x_sum = 0
        y_sum = 0
        for i in self.intesities:
            dist = magDist();

            x_dist = math.cos(i['theta']) * dist
            y_dist = math.sin(i['theta']) * dist

            x_sum = i['x'] + x_dist
            y_sum = i['y'] + y_dist

        self.x = x_sum / len(self.intesities)
        self.y = y_sum / len(self.intesities)

        return self.x, self.y
