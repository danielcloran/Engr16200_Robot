import time
import grovepi
import math
from IR_Functions import *

IR_SLOPE = -43.1
IR_Y_INTERCEPT = 201
IR_setup(grovepi)
class IRTracker:
    def __init__(self):
        self.beacon_intensity = []
        self.hazardsList = []
        self.hazardsList.append(Beacon())
        self.dataInBeacon = False
        self.sensor_mag = 0

    # returns a list of all known hazards
    def getHazards(self, x_pos, y_pos, theta):
        try:
            [sensor1_value, sensor2_value] = IR_Read(grovepi)
            self.sensor_mag = math.sqrt(sensor1_value**2 + sensor2_value**2)

            if self.dataInBeacon == True and self.sensor_mag == 0:
                self.dataInBeacon = False
                self.hazardsList.append(Beacon())

            if len(self.hazardsList) > 0 and self.sensor_mag > 0:
                self.dataInBeacon = True
                self.hazardsList[len(self.hazardsList)-1].update(theta, self.sensor_mag, x_pos, y_pos)
            return self.hazardsList
        except Exception as err:
            return self.hazardsLists
            pass

    # Check if getting close to no-enter radius
    def checkIRDanger(self):
        if self.sensor_mag > 70:
            return True
        return False

class Beacon:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.intensities = []

    def update(self, theta, sensor_mag, robot_x, robot_y):
        self.intensities.append({'x': robot_x, 'y': robot_y, 'theta': theta, 'mag': sensor_mag})
        x_sum = 0
        y_sum = 0
        count = 0
        for i in self.intensities:
            if i['mag'] > 40:
                count += 1
                dist = IR_SLOPE * math.log(i['mag']) + IR_Y_INTERCEPT

                x_dist = math.cos(i['theta']) * dist
                y_dist = math.sin(i['theta']) * dist

                x_sum += (i['x'] + x_dist)
                y_sum += (i['y'] + y_dist)

        self.x = x_sum / count
        self.y = y_sum / count
        return self.x, self.y
