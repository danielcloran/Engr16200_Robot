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

        #self.mapper = MapOutputter(self, map_length, map_width)
        #self.mapper.setOrigin(self.x, self.y)

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
        if (ultrasonicList[1] > 22):
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
        sameRightTurn = 11
        while True:
            try:
                self.theta = self.physical.getHeading()
                self.x, self.y = self.physical.updatePosition(self.x, self.y, self.theta)

                #self.mapper.setPath(self.x, self.y)
                #self.irHazards = self.irTracker.getHazards(self.x, self.y, self.theta)
                #self.magHazards = self.magTracker.getHazards(self.x, self.y, self.theta)


                ultrasonicReadings = self.physical.getUltrasonic()
                #print('ultrasonic: ', ultrasonicReadings)

                turnable = self.determineOpenSides(ultrasonicReadings)

                #print(self.irHazards)
                #for hazard in range(len(self.irHazards)):
                    #print('Hazard '+ str(hazard) +':'+ str(self.irHazards[hazard].x) + ',' + str(self.irHazards[hazard].y))

                #print(turnable)
                print(intendedAngle)

                self.physical.driveStraight(35, intendedAngle, turnable, ultrasonicReadings)
                if not turnable[2]: sameRightTurn += 1

                # If ANY right turn is available
                if turnable[2] and sameRightTurn > 5:
                    sameRightTurn = 0
                    #print('RIGHT TURN')
                    self.physical.driveStraight(30, intendedAngle, turnable, ultrasonicReadings)
                    time.sleep(.2)
                    intendedAngle -= 90
                    self.turnUntil(intendedAngle+10)
                # If ONLY left turn is available
                elif turnable[0] and not turnable[1]:
                    intendedAngle += 90
                    #print('LEFT TURN')
                    self.turnUntil(intendedAngle-10)
                # DEAD END
                elif not turnable[0] and not turnable[1] and not turnable[2]:
                    #print('NO OPTIONS 180')

                    self.turn180(intendedAngle + 180)
                    intendedAngle = intendedAngle + 180

                #print('x:', self.x, 'y:', self.y, 'theta:', self.theta)
                #print('ir:', self.irHazards)
                mili_counter += 1
                time.sleep(0.01)

            #except Exception as err:
            #    print(err)
            except KeyboardInterrupt:
                self.physical.cleanup()
                break

    def turn180(self, deg):
        self.physical.drive(-50, 40)
        time.sleep(.6)
        current_heading = self.physical.getHeading()
        while current_heading <= deg:
            self.physical.turnNoRadius('right')
            current_heading = self.physical.getHeading()

    def turnUntil(self, deg):
        current_heading = self.physical.getHeading()
        if(deg < current_heading-20):
            while current_heading >= deg:
                self.physical.turn('right')
                current_heading = self.physical.getHeading()
        else:
            while current_heading+20 <= deg:
                self.physical.turn('left')
                current_heading = self.physical.getHeading()
        return current_heading;

robot = Robot()
robot.run()
