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
        
        self.mag = 0
        self.magx = 0
        self.magy = 0
        self.magz = 0
        self.maglocx = 0
        self.maglocy = 0

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
    
    # Test magnetic readouts
    def magReadTest(self):
        try:
            while True:
                self.theta = self.physical.getHeading()
                self.mag = self.physical.getMag()
                self.magx = self.physical.getMagX()
                self.magy = self.physical.getMagY()
                self.magz = self.physical.getMagZ()
                
                print('Theta: ', self.theta, ' Mag: ', self.mag, ' X: ', self.magx, ' Y: ', self.magy, 'Z: ', self.magz)
                
                if(self.physical.checkMagNear):
                    print('Magnet Near')
                else:
                    print('Magnet Not Near')
                
                if(self.physical.checkMagDanger):
                    print('Danger Zone Close')
                else:
                    print('Danger Zone Not Close')
        except KeyboardInterrupt:
            self.physical.cleanup()
            
    # Test guessing magnet location and avoiding while driving
    def magDriveTest(self):
        try:
            while True:
                self.theta = self.physical.getHeading()
                self.mag = self.physical.getMag()
                self.magx = self.physical.getMagX()
                self.magy = self.physical.getMagY()
                self.magz = self.physical.getMagZ()
                
                self.physical.drive(25)
                
                if(self.physical.checkMagNear):
                    self.maglocx, self.maglocy = self.physical.markMagnet(self.x, self.y, self.theta)
                    print('Robot Pos: ', self.x, ' ', self.y, '   Magnet Location Guess: ', self.maglocx, ' ', self.maglocy)
                
                if(self.physical.checkMagDanger):
                    print('Avoiding Magnet')
                    self.physical.drive(-25)
                    time.sleep(1.5)
                    self.physical.drive(25)
                    self.physical.turnUntil(self.theta + 10)
                    print('Resume Driving')
                
        except KeyboardInterrupt:
            self.physical.cleanup()
            
            
robot = Robot()
robot.test()
