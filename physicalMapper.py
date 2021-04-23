import brickpi3
import grovepi
import math
import sys
import time
from IMUCode.MPU9250 import MPU9250

BP = brickpi3.BrickPi3()
mpu = MPU9250()

wheel_d = 7

mag = 0
magX = 0
magY = 0
magZ = 0

MOTOR_ONE = BP.PORT_C
MOTOR_TWO = BP.PORT_B
GYRO_SENSE = BP.PORT_1

ULTRASONIC_LEFT = BP.PORT_2

grovepi.set_bus("RPI_1")
ultrasonic_middle = 2
ultrasonic_right = 8

BP.reset_all()

# Init all ports
BP.offset_motor_encoder(MOTOR_ONE, BP.get_motor_encoder(MOTOR_ONE) )
BP.set_motor_limits(MOTOR_ONE, power=80, dps=200)
BP.offset_motor_encoder(MOTOR_TWO, BP.get_motor_encoder(MOTOR_TWO) )
BP.set_motor_limits(MOTOR_TWO, power=50, dps=200)

BP.set_sensor_type(GYRO_SENSE, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)
BP.set_sensor_type(ULTRASONIC_LEFT, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)

motor_power = 20

# Init sensor readings
sensorData = 0
sensorData2 = 0
while not sensorData and not sensorData2:
    try:
        sensorData = BP.get_sensor(GYRO_SENSE)   # print the gyro sensor values
        sensorData2 = BP.get_sensor(ULTRASONIC_LEFT)   # print the gyro sensor values
    except brickpi3.SensorError as error:
        print(error)

class PhysicalMapper:
    def __init__(self, robot):
        self.robot = robot

    def getChangeMotors(self):
        one = BP.get_motor_encoder(BP.PORT_C)
        BP.offset_motor_encoder(BP.PORT_C, one)
        two = BP.get_motor_encoder(BP.PORT_B)
        BP.offset_motor_encoder(BP.PORT_B, two)
        return one, two

    def getDeltaXY(self, delta_Sr, delta_Sl, theta):
        delta_s = (delta_Sr + delta_Sl) / 2
        delta_x = delta_s * math.cos(math.radians(theta))
        delta_y = delta_s * math.sin(math.radians(theta))
        return delta_x, delta_y

    def updatePosition(self, x, y, theta):
        motor1Diff, motor2Diff = self.getChangeMotors()
        delta1Pos = (motor1Diff/360) * (math.pi * self.robot.wheel_d)
        delta2Pos = (motor2Diff/360) * (math.pi * self.robot.wheel_d)
        tmpX, tmpY = self.getDeltaXY(delta1Pos, delta2Pos, theta)
        return x+tmpX, y+tmpY

    def drive(self, power, adjL = 0, adjR = 0):
        BP.set_motor_power(BP.PORT_C, adjL + power)
        BP.set_motor_power(BP.PORT_B, adjR + power)

    def getUltrasonic(self):
        return BP.get_sensor(ULTRASONIC_LEFT), grovepi.ultrasonicRead(ultrasonic_middle), grovepi.ultrasonicRead(ultrasonic_right)



    def getHeading(self):
        return BP.get_sensor(GYRO_SENSE)[0]

    def driveStraight(self, power, initialHeading):
        kp = 1.5
        try:
            err = initialHeading - self.getHeading()
            p_gain = kp * err
            p_gain = (kp * abs(err))
            if err > 1:
                self.drive(power, -p_gain, p_gain)
            elif err < -1:
                self.drive(power, p_gain, -p_gain)
            else:
                self.drive(power, p_gain, p_gain)
        except KeyboardInterrupt:
            BP.reset_all()

    def stopAndTakeMeasurements(self):
        final_heading = self.robot.theta + 359
        current_heading = self.robot.theta
        while current_heading <= final_heading:
            self.turn('left')
            current_heading = self.getHeading()
            distance = self.getUltrasonic()
            print(distance)
            if (distance < 100):
                x_diff = distance * math.cos(math.radians(current_heading))
                y_diff = distance * math.sin(math.radians(current_heading))
                with open("wallPos.txt","a") as fh:
                    fh.write(str(self.robot.x + x_diff) + "," + str(self.robot.y + y_diff)+ "\n")

    def turn(self,direction):
        if direction == 'left':
            BP.set_motor_power(BP.PORT_C, -motor_power)
            BP.set_motor_power(BP.PORT_B, motor_power)
        else:
            BP.set_motor_power(BP.PORT_C, motor_power)
            BP.set_motor_power(BP.PORT_B, -motor_power)

    def turnUntil(self, deg):
        current_heading = self.getHeading()
        if(deg < current_heading):
            while current_heading >= deg:
                self.turn('right')
                current_heading = self.getHeading()
        else:
            while current_heading <= deg:
                self.turn('left')
                current_heading = self.getHeading()

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
        return abs(self.getMag() - 100)

    # Scalar distance to nearby magnet
    def magDist(self):
        # B = mu0M/(4piR^3) = K/R^3 --> R = (K/B)^(1/3)
        # k = r^3 * magDiff --> k = 1350000 guess using mag of 150 at 30 cm from magnet
        k = 1350000 # can probably get a better value by fine tuning during testing
        mag = self.getMag()
        r = 0
        if mag != 0:
            r = (k / self.magDiff()) ** (1/3)
        return r

    # Guess magnet position as some distance in front of robot
    def markMagnet(self, x, y, theta):
        deltaX = self.magDist() * math.cos(math.radians(theta))
        deltaY = self.magDist() * math.sin(math.radians(theta))
        return x + deltaX, y + deltaY

    # Check if magnet is nearby to guess location
    def checkMagNear(self):
        if(self.magDiff() > 30):
            return True
        return False

    # Check if getting close to no-enter radius
    def checkMagDanger(self):
        if(self.magDiff() > 60):
            return True
        return False

    def cleanup(self):
        BP.reset_all()
        # self.scan1Thread.join()
