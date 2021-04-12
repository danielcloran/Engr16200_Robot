import time
from physicalMapper import PhysicalMapper
import math

# Constants
map_length = 671 # cm
map_width = 366 # cm


class Robot:
    def __init__(self):
        self.width = 14
        self.wheel_d = 7

        self.x = 0
        self.y = 0
        self.theta = 0

        self.physical = PhysicalMapper(self)

    def savePosToFile(self, x, y):
        with open("robotPos.txt","w") as fh:
            fh.write(str(x) + "," + str(y)+ "\n")

    def run(self):
        # main logic
        while True:
            try:
                self.theta = physical.getHeading()
                #self.pointsToAvoid = magnetic.getPoints()
                self.x, self.y = physical.updatePosition(self.x, self.y, self.theta)

                self.savePosToFile()
                time.sleep(0.01)

            except KeyboardInterrupt as err:
                self.physical.cleanup()
                break

    def turnUntil(self, deg):
        current_heading = self.physical.getHeading()
        if(deg < current_heading):
            while current_heading >= deg:
                self.physical.turn('right')
                current_heading = self.physical.getHeading()
        else:
            while current_heading <= deg:
                self.physical.turn('left')
                current_heading = self.physical.getHeading()

    def test(self):
        try:
            current_heading = self.physical.getHeading()
            while self.x <= 40:
                self.theta = self.physical.getHeading()
                self.x, self.y = self.physical.updatePosition(self.x, self.y, self.theta)#

                print('X: ', self.x, '  Y: ', self.y)
                self.physical.drive(25)
                
            self.turnUntil(270)
            # self.physical.stopAndTakeMeasurements()
            while True:
                self.physical.drive(25)
        except KeyboardInterrupt:
            self.physical.cleanup()

robot = Robot()
robot.test()
