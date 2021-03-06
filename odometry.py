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
        self.width = 14 # cm
        self.wheel_d = 7 # cm
        self.irTracker = IRTracker()
        self.irHazards = []

        self.magTracker = MagTracker()
        self.magHazards = []

        self.x = 0
        self.y = 0
        self.theta = 0

        self.mapper = MapOutputter(self, map_length, map_width)
        self.mapper.setOrigin(self.x, self.y)

        self.running = True

        self.physical = PhysicalMapper(self)

    def determineOpenSides(self, ultrasonicList):
        leftOpen = False
        middleOpen = False
        rightOpen = False
        reachedEnd = False
        if (ultrasonicList[0] > 25):
            leftOpen = True
        if (ultrasonicList[1] > 24):
            middleOpen = True
        if (ultrasonicList[2] > 25):
            rightOpen = True
        if (ultrasonicList[0] > 100 and ultrasonicList[1] > 100 and ultrasonicList[2] > 100):
            reachedEnd = True
        return leftOpen, middleOpen, rightOpen, reachedEnd

    def run(self):
        # main logic
        mili_interrupt = 10
        mili_counter = 10
        intendedAngle = 0
        notTurned = True
        turnable = [False, False, False, False]
        sameRightTurn = 11
        while self.running:
            try:
                # Update robots position and heading
                self.theta = self.physical.getHeading()
                self.x, self.y = self.physical.updatePosition(self.x, self.y, self.theta)
                self.mapper.setPath(self.x, self.y)

                # Read magnet hazards only once every 0.1 seconds (polling rate of sensor)
                if (mili_counter >= mili_interrupt):
                    mili_counter = 0
                    self.magHazards = self.magTracker.getHazards(self.x, self.y, self.theta)

                self.irHazards = self.irTracker.getHazards(self.x, self.y, self.theta)

                # Plot hazards on map.
                for hazard in self.irHazards:
                    self.mapper.setHeat(hazard.x, hazard.y)
                for hazard in self.magHazards:
                    self.mapper.setMagnet(hazard.x, hazard.y)

                # Determine which directions the has open to turn
                ultrasonicReadings = self.physical.getUltrasonic()
                turnable = self.determineOpenSides(ultrasonicReadings)
                self.physical.driveStraight(30, intendedAngle, turnable, ultrasonicReadings)

                # Robot must see another wall on the right before it turns right again...
                if not turnable[2]: sameRightTurn += 1

                #########################
                ### ROBOT STATE CASES ###
                #########################
                # If at end
                if turnable[3]:
                    self.running = False
                    time.sleep(1)
                    self.physical.drive(0)
                    time.sleep(1)
                    self.mapper.setExit(self.x, self.y)
                    self.physical.dropCargo()
                    self.physical.signalCargo()
                    self.writeHazardsList()
                    self.mapper.save_to_csv()
                    self.mapper.cleanup()
                    time.sleep(5)
                # If ANY right turn is available
                elif turnable[2] and sameRightTurn > 0:
                    sameRightTurn = 0
                    self.physical.driveStraight(30, intendedAngle, turnable, ultrasonicReadings)
                    time.sleep(.2)
                    intendedAngle -= 90
                    self.turnUntil(intendedAngle+10)
                # If ONLY left turn is available
                elif turnable[0] and not turnable[1]:
                    intendedAngle += 90
                    self.turnUntil(intendedAngle-10)
                # DEAD END
                elif self.irTracker.checkIRDanger() or self.magTracker.checkMagDanger() or not turnable[0] and not turnable[1] and not turnable[2]:
                    intendedAngle += 180
                    self.turn180(intendedAngle - 20)

                mili_counter += 1
                time.sleep(0.01)
            except Exception as err:
                pass
            except KeyboardInterrupt:
                self.physical.cleanup()
                break

    def turn180(self, deg):
        self.physical.drive(-60, 50)
        time.sleep(.8)
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

    def writeHazardsList(self):
        with open("hazardslist.csv", "w") as fh:
            fh.write("Hazard Type,Parameter of Interest,Parameter Value,Hazard X Coordinate,Hazard Y Coordinate \n")
            for mag in self.magHazards:
                maxIntensity = 0
                for intensity in mag.intensities:
                    if intensity['mag'] > maxIntensity: maxIntensity = intensity['mag']
                fh.write("Electrical Activity Source,Field Strength (uT),")
                fh.write(str(int(maxIntensity)) + "," + str(int(mag.x/10) - self.mapper.negativeBoundX) + "," + str(int(mag.y/10) - self.mapper.negativeBoundY) + "\n")

            for ir in self.irHazards:
                maxIntensity = 0
                for intensity in ir.intensities:
                    if intensity['mag'] > maxIntensity: maxIntensity = intensity['mag']

                fh.write("High Temperature Heat Source,Radiation Strength (Unitless),")
                fh.write(str(int(maxIntensity)) + "," + str(int(ir.x/10) - self.mapper.negativeBoundX) + "," + str(int(ir.y/10) - self.mapper.negativeBoundY) + "\n")

robot = Robot()
robot.run()
