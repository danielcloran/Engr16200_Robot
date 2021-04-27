import brickpi3
import grovepi
import math
import sys
import time

BP = brickpi3.BrickPi3()

wheel_d = 7

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
sensorData3 = 0
sensorData4 = 0
while not sensorData or not sensorData2 or not sensorData3 or not sensorData4:
    try:
        sensorData = BP.get_sensor(GYRO_SENSE)   # print the gyro sensor values
        sensorData2 = BP.get_sensor(ULTRASONIC_LEFT)
        sensorData3 = grovepi.ultrasonicRead(ultrasonic_middle)
        sensorData4 = grovepi.ultrasonicRead(ultrasonic_right)

    except Exception as error:
        pass
        #print(error)

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

    def driveStraight(self, power, initialHeading, turnable, ultrasonicReadings):
        kp_angle = 1.5
        kp_wall = 1.5
        try:
            wall_gain = 0
            if (not turnable[0] and not turnable[2]):
                wall_err = ultrasonicReadings[0] - ultrasonicReadings[2]
                wall_gain = kp_wall * wall_err

            angle_err = initialHeading - self.getHeading()
            angle_gain = kp_angle * angle_err

            p_gain = angle_gain + wall_gain

            if p_gain > 0:
                self.drive(power, -p_gain, p_gain)
            elif angle_gain < 0:
                self.drive(power, -p_gain, p_gain)
            else:
                self.drive(power, 0, 0)
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

    def turnNoRadius(self,direction):
        BP.set_motor_power(BP.PORT_C, -30)
        BP.set_motor_power(BP.PORT_B, 30)

    def turn(self,direction):
        if direction == 'left':
            #BP.set_motor_power(BP.PORT_C, -motor_power)
            BP.set_motor_power(BP.PORT_C, 0)
            BP.set_motor_power(BP.PORT_B, 40)
        else:
            BP.set_motor_power(BP.PORT_C, 40)
            BP.set_motor_power(BP.PORT_B, 0)
            #BP.set_motor_power(BP.PORT_B, -motor_power)

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

    def cleanup(self):
        BP.reset_all()
