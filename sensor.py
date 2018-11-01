import brickpi
import time
import math
import random

interface=brickpi.Interface()
interface.initialize()

motors = [0,1]
speed = 6.0

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

motorParams0 = interface.MotorAngleControllerParameters()
motorParams0.maxRotationAcceleration = 6.0
motorParams0.maxRotationSpeed = 12.0
motorParams0.feedForwardGain = 255/20.0
motorParams0.minPWM = 18.0
motorParams0.pidParameters.minOutput = -255
motorParams0.pidParameters.maxOutput = 255
motorParams0.pidParameters.k_p = 510.0
motorParams0.pidParameters.k_i = 1300.0
motorParams0.pidParameters.k_d = 95.0

motorParams1 = interface.MotorAngleControllerParameters()
motorParams1.maxRotationAcceleration = 6.0
motorParams1.maxRotationSpeed = 12.0
motorParams1.feedForwardGain = 255/20.0
motorParams1.minPWM = 18.0
motorParams1.pidParameters.minOutput = -255
motorParams1.pidParameters.maxOutput = 255
motorParams1.pidParameters.k_p = 570.0
motorParams1.pidParameters.k_i = 1300.0
motorParams1.pidParameters.k_d = 70.0

interface.setMotorAngleControllerParameters(motors[0],motorParams0)
interface.setMotorAngleControllerParameters(motors[1],motorParams1)

touch_port_left = 0
touch_port_right = 1
interface.sensorEnable(touch_port_left, brickpi.SensorType.SENSOR_TOUCH)
interface.sensorEnable(touch_port_right, brickpi.SensorType.SENSOR_TOUCH)



def right90deg():
    interface.increaseMotorAngleReferences(motors,[math.pi * 1.155, math.pi * -1.155])
    while not interface.motorAngleReferencesReached(motors) :
      #motorAngles = interface.getMotorAngles(motors)
      time.sleep(0.1)

def left90deg():
    interface.increaseMotorAngleReferences(motors,[math.pi * -1.155, math.pi * 1.155])
    while not interface.motorAngleReferencesReached(motors) :
      #motorAngles = interface.getMotorAngles(motors)
      time.sleep(0.1)


def move(radian):
    interface.increaseMotorAngleReferences(motors, [radian, radian])
    while not interface.motorAngleReferencesReached(motors):
        time.sleep(0.1)

def move_in_square():
    for i in range(4):
        print("moving forward")
        move(11.0)
        print("turning")
        right90deg()

def stop():
    interface.setMotorPwm(motors[0], 0)
    interface.setMotorPwm(motors[1], 0)

distance = 5

while True:
    bump1 = interface.getSensorValue(touch_port_left)
    bump2 = interface.getSensorValue(touch_port_right)
    if bump1 and bump2:
        touch1 = bump1[0]
        touch2 = bump2[0]
        if touch1 and touch2:
            stop()
	    print(touch1, touch2)
            move(-distance)
            rand = random.randint(0, 1)
            if rand:
                right90deg()
            else:
                left90deg()
        elif touch1 and not touch2:
            stop()
	    print(touch1, touch2)
            move(-distance)
            right90deg()
        elif not touch1 and touch2:
            stop()
	    print(touch1, touch2)
            move(-distance)
            left90deg()
        else:
	    pass
            move(distance)
            #interface.setMotorRotationSpeedReference(motors, [speed, speed])

interface.terminate()

