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
motorParams0.pidParameters.k_p = 510.0
motorParams0.pidParameters.k_i = 150.0
motorParams0.pidParameters.k_d = 95.0

motorParams1 = interface.MotorAngleControllerParameters()
motorParams1.maxRotationAcceleration = 6.0
motorParams1.maxRotationSpeed = 12.0
motorParams1.feedForwardGain = 255/20.0
motorParams1.minPWM = 18.0
motorParams1.pidParameters.minOutput = -255
motorParams1.pidParameters.maxOutput = 255
motorParams1.pidParameters.k_p = 570.0
motorParams1.pidParameters.k_i = 150.0
motorParams1.pidParameters.k_d = 70.0

interface.setMotorAngleControllerParameters(motors[0],motorParams0)
interface.setMotorAngleControllerParameters(motors[1],motorParams1)

def left90deg():
    interface.increaseMotorAngleReferences(motors,[math.pi * 3.2, math.pi * 12])
    while not interface.motorAngleReferencesReached(motors) :
      motorAngles = interface.getMotorAngles(motors)
      print(motorAngles[0])
      print(motorAngles[1])
      time.sleep(0.1)
def right90deg():
    interface.increaseMotorAngleReferences(motors,[math.pi * -1.2, math.pi * 1.2])
    while not interface.motorAngleReferencesReached(motors) :
      motorAngles = interface.getMotorAngles(motors)
      time.sleep(0.1)

def move_in_square():
    for i in range(4):
        interface.setMotorRotationSpeedReferences(motors,[speed,speed])
        time.sleep(1.3)
        interface.setMotorRotationSpeedReferences(motors,[0,0])
        left90deg()



print "Press Ctrl+C to exit"
counter = 0
exclaimation = ""
while True:
    if(input("Enter 1 to try again: ") == 1):
        counter += 1
        exclaimation += "!"
        move_in_square()
        #print(covariance_matrix([1,2,3,4], [2,4,6,8]))
        print("You have tried " + str(counter) + " times" + exclaimation)
    else:
        break
interface.terminate()

