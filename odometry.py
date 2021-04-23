import time
from physicalMapper import PhysicalMapper
from mapOutputter import MapOutputter
from IR_Sensing import IRTracker
from magTracker import MagTracker

import math

# Constants
map_length = 671 # cm
map_width = 366 # cm
class Robot:
    def __init__(self):
        self.width = 14
        self.wheel_d = 7
        self.irTracker = IRTracker()
        self.irHazards = []

        self.magTracker = MagTracker()
        self.magHazards = []

        self.x = 0
        self.y = 0
        self.theta = 0

        self.mag = 0
        self.magx = 0
        self.magy = 0
        self.magz = 0
        self.maglocx = 0
        self.maglocy = 0

        self.mapper = MapOutputter(self, map_length, map_width)
        self.mapper.setOrigin(self.x, self.y)

        self.physical = PhysicalMapper(self)

    def savePosToFile(self, x, y):
        with open("robotPos.txt","w") as fh:
            fh.write(str(x) + "," + str(y)+ "\n")

    def determineOpenSides(self, ultrasonicList):
        leftOpen = False
        middleOpen = False
        rightOpen = False
        if (ultrasonicList[0] > 25):
            leftOpen = True
        if (ultrasonicList[1] > 25):
            middleOpen = True
        if (ultrasonicList[2] > 25):
            rightOpen = True
        return leftOpen, middleOpen, rightOpen

    def run(self):
        # main logic
        mili_interrupt = 10
        mili_counter = 0
        intendedAngle = 0
        notTurned = True
        turnable = [False, False, False]
        sameRightTurn = False
        while True:
            try:
                self.theta = self.physical.getHeading()
                self.x, self.y = self.physical.updatePosition(self.x, self.y, self.theta)

                if (mili_counter == mili_interrupt):
                    self.irHazards = self.irTracker.getHazards(self.x, self.y, self.theta)
                    self.magHazards = self.magTracker.getHazards(self.x, self.y, self.theta)
                    mili_counter = 0
                    self.mapper.setPath(self.x, self.y)

                #self.magneticHazards = self.magnetic.getHazards(self.x, self.y, self.theta)
                ultrasonicReadings = self.physical.getUltrasonic()
                turnable = self.determineOpenSides(ultrasonicReadings)
                #print(turnable)


                #self.physical.driveStraight(30, intendedAngle, turnable, ultrasonicReadings)
                if not turnable[2]: sameRightTurn = False

                # If ANY right turn is available
                if turnable[2] and not sameRightTurn:
                    sameRightTurn = True
                    print('RIGHT TURN')
                    newAngle = self.theta-90
                    self.theta = self.turnUntil(newAngle)
                    intendedAngle = newAngle
                # If ONLY left turn is available
                elif turnable[0] and not turnable[1]:
                    newAngle = self.theta+90
                    print('LEFT TURN')
                    self.theta = self.turnUntil(newAngle)
                    intendedAngle = newAngle
                # DEAD END
                elif not turnable[0] and not turnable[1] and not turnable[2]:
                    print('NO OPTIONS 180')

                    self.theta = self.turnUntil(self.theta+180)
                    intendedAngle = self.theta

                #print('x:', self.x, 'y:', self.y, 'theta:', self.theta)
                #print('ultrasonic: ', ultrasonicReadings)
                #print('ir:', self.irHazards)
                mili_counter += 1
                time.sleep(0.01)

            except Exception as err:
                print(err)
            except KeyboardInterrupt:
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
        return current_heading;

robot = Robot()
robot.run()
