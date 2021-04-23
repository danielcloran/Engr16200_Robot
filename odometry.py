import time
from physicalMapper import PhysicalMapper
from mapOutputter import MapOutputter
from IR_Sensing import IRTracker
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

    def determineOpenSides(ultrasonicList):
        leftOpen = False
        middleOpen = False
        rightOpen = False
        if (ultrasonicReadings[0] > 30):
            leftOpen = True
        if (ultrasonicReadings[1] > 30):
            rightOpen = True
        if (ultrasonicReadings[2] > 30):
            middleOpen = True
        return leftOpen, middleOpen, rightOpen

    def run(self):
        # main logic
        ir_interrupt = 10
        ir_counter = 0
        intendedAngle = 0
        notTurned = True
        turnable = [False, False, False]
        while True:
            try:
                self.theta = self.physical.getHeading()
                self.x, self.y = self.physical.updatePosition(self.x, self.y, self.theta)

                if (ir_counter == ir_interrupt):
                    self.irHazards = self.irTracker.getHazards(self.x, self.y, self.theta)
                    ir_counter = 0

                #self.magneticHazards = self.magnetic.getHazards(self.x, self.y, self.theta)
                ultrasonicReadings = self.physical.getUltrasonic()
                turnable = determineOpenSides(ultrasonicReadings)

                self.physical.driveStraight(30, intendedAngle)

                # If ANY right turn is available
                if turnable[2]:
                    self.theta = self.turnUntil(self.theta-90)
                    intendedAngle = self.theta
                # If ONLY left turn is available
                elif turnable[0] and not turnable[1]:
                    self.theta = self.turnUntil(self.theta+90)
                    intendedAngle = self.theta
                # DEAD END
                elif not turnable[0] and not turnable[1] and not turnable[2]:
                    self.theta = self.turnUntil(self.theta+180)
                    intendedAngle = self.theta


                #print('x:', self.x, 'y:', self.y, 'theta:', self.theta)
                #print('ultrasonic: ', ultrasonicReadings)
                #print('ir:', self.irHazards)
                ir_counter += 1
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

    # Test magnetic readouts
    def magReadTest(self):
        try:
            while True:
                self.theta = self.physical.getHeading()
                self.physical.updateMag()
                self.mag = self.physical.getMag()

                print('Theta: ', self.theta, ' Mag: ', self.physical.getMag(), ' X: ', self.physical.getMagX(), ' Y: ', self.physical.getMagY(), 'Z: ', self.physical.getMagZ())

                if(self.physical.checkMagNear()):
                    print('Magnet Near')
                else:
                    print('Magnet Not Near')

                if(self.physical.checkMagDanger()):
                    print('Danger Zone Close')
                else:
                    print('Danger Zone Not Close')

                time.sleep(0.01)
        except KeyboardInterrupt:
            self.physical.cleanup()

    # Test guessing magnet location and avoiding while driving
    def magDriveTest(self):
        try:
            while True:
                self.theta = self.physical.getHeading()
                self.physical.updateMag()

                self.physical.drive(25)
                print('Magnitude: ', self.physical.getMag())
                if(self.physical.checkMagNear()):
                    self.maglocx, self.maglocy = self.physical.markMagnet(self.x, self.y, self.theta)
                    print('Robot Pos: ', self.x, ' ', self.y, '   Magnet Location Guess: ', self.maglocx, ' ', self.maglocy)

                if(self.physical.checkMagDanger()):
                    print('Avoiding Magnet')
                    self.physical.drive(-25)
                    time.sleep(1)
                    self.physical.drive(25)
                    self.physical.turnUntil(self.theta + 10)
                    print('Resume Driving')
                time.sleep(0.01)
        except KeyboardInterrupt:
            self.physical.cleanup()


robot = Robot()
robot.run()
