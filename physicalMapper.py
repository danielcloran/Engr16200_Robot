import brickpi3
import grovepi
import math

BP = brickpi3.BrickPi3()

wheel_d = 7

MOTOR_ONE = BP.PORT_C
MOTOR_TWO = BP.PORT_B
GYRO_SENSE = BP.PORT_1

grovepi.set_bus("RPI_1")
ultrasonic_1 = 2

BP.reset_all()

# Init all ports
BP.offset_motor_encoder(MOTOR_ONE, BP.get_motor_encoder(MOTOR_ONE) )
BP.set_motor_limits(MOTOR_ONE, power=80, dps=200)
BP.offset_motor_encoder(MOTOR_TWO, BP.get_motor_encoder(MOTOR_TWO) )
BP.set_motor_limits(MOTOR_TWO, power=50, dps=200)

BP.set_sensor_type(GYRO_SENSE, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)

motor_power = 20

# Init sensor readings
sensorData = 0
while not sensorData:
    try:
        sensorData = BP.get_sensor(BP.PORT_1)   # print the gyro sensor values
    except brickpi3.SensorError as error:
        print(error)

class PhysicalMapper:
    def __init__(self, robot):
        self.robot = robot
        # Scanning Threads
        # self.scannerOne = Scanner(self.conveyor, 1)
        # self.scan1Thread = threading.Thread(target=self.scannerOne.startScanning, args=(), daemon=True)
        # self.scan1Thread.start()

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

    def drive(self, power):
        BP.set_motor_power(BP.PORT_C, power+1)
        BP.set_motor_power(BP.PORT_B, power)
        
    def getUltrasonic(self):
        return grovepi.ultrasonicRead(ultrasonic_1)

    def getHeading(self):
        return BP.get_sensor(GYRO_SENSE)[0]

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

    def cleanup(self):
        BP.reset_all()
        # self.scan1Thread.join()
