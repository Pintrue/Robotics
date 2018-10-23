import brickpi
import time
import math

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
motorParams0.pidParameters.k_p = 100.0
motorParams0.pidParameters.k_i = 0.0
motorParams0.pidParameters.k_d = 0.0

motorParams1 = interface.MotorAngleControllerParameters()
motorParams1.maxRotationAcceleration = 6.0
motorParams1.maxRotationSpeed = 12.0
motorParams1.feedForwardGain = 255/20.0
motorParams1.minPWM = 18.0
motorParams1.pidParameters.minOutput = -255
motorParams1.pidParameters.maxOutput = 255
motorParams1.pidParameters.k_p = 100.0
motorParams1.pidParameters.k_i = 0.0
motorParams1.pidParameters.k_d = 0.0

interface.setMotorAngleControllerParameters(motors[0],motorParams0)
interface.setMotorAngleControllerParameters(motors[1],motorParams1)

def left90deg():
    increaseMotorAngleReferences(motors,[math.pi * 2, math.pi * -2])

def right90deg():
    increaseMotorAngleReferences(motors,[math.pi * -2, math.pi * 2])

def move_in_square():
    for i in range(4):
        interface.setMotorRotationSpeedReferences(motors,[speed,speed])
        time.sleep(4)
        interface.setMotorRotationSpeedReferences(motors,[0,0])
        left90deg();


print "Press Ctrl+C to exit"
counter = 0
while True:
        if (input("Enter y to move") == 'y'):
            move_in_square()
	    counter += 1
        else:
            interface.terminate()
