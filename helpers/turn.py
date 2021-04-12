import brickpi3


BP = brickpi3.BrickPi3()
BP.reset_all()

BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C) )
BP.set_motor_limits(BP.PORT_C, power=80, dps=200)
BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B) )
BP.set_motor_limits(BP.PORT_B, power=50, dps=200)

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)


sensorData = 0
while not sensorData:
    try:
        sensorData = BP.get_sensor(BP.PORT_1)   # print the gyro sensor values
    except brickpi3.SensorError as error:
        print(error)

power = 80

#angle = int(input("Enter an angle to turn to: "))
theta = 0
kp = .4
while True:
    BP.set_motor_power(BP.PORT_C, -power)
    BP.set_motor_power(BP.PORT_B, power)
    print('Theta: ', theta)

BP.reset_all()
