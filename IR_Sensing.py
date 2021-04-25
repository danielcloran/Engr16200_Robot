 #!/usr/bin/env python
#
# GrovePi Example for using the analog read command to read analog sensor values
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import time
import grovepi
import math
from IR_Functions import *

IR_SLOPE = -0.0878
IR_Y_INTERCEPT = 13.8
IR_setup(grovepi)

class IRTracker:
    def __init__(self):
        self.beacon_intensity = []
        self.hazardsList = []
        self.hazardsList.append(Beacon())
        self.dataInBeacon = False

    # returns a list of all known hazards
    def getHazards(self, x_pos, y_pos, theta):
        #try:
        [sensor1_value, sensor2_value] = IR_Read(grovepi)
        print('s1:',sensor1_value,'s2:',sensor2_value )
        sensor_mag = math.sqrt(sensor1_value**2 + sensor2_value**2)

        if self.dataInBeacon == True and sensor1_value == 0 and sensor2_value == 0:
            self.dataInBeacon = False
            self.hazardsList.append(Beacon())

        if len(self.hazardsList) > 0 and sensor_mag > 0:
            self.dataInBeacon = True
            self.hazardsList[len(self.hazardsList)-1].update(theta, sensor_mag, x_pos, y_pos)
        #print('Getting IR x: ', self.hazardsList[0].x, 'y:', self.hazardsList[0].y)
        return self.hazardsList
        #except Exception as err:
        #    print(err)

class Beacon:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.intesities = []

    def getIntensity(self):
        return [self.sensor1_value, self.sensor2_value]   # returns latest readings from sensor 1 and 2

    def update(self, theta, sensor_mag, robot_x, robot_y):
        self.intesities.append({'x': robot_x, 'y': robot_y, 'theta': theta, 'mag': sensor_mag})
        x_sum = 0
        y_sum = 0
        for i in self.intesities:
            dist = IR_SLOPE * i['mag'] + IR_Y_INTERCEPT

            x_dist = math.cos(i['theta']) * dist
            y_dist = math.sin(i['theta']) * dist

            x_sum += x_dist
            y_sum += y_dist

        self.x = x_sum / len(self.intesities)
        self.y = y_sum / len(self.intesities)

        return self.x, self.y
