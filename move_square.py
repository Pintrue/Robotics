import brickpi
import time
import math

interface=brickpi.Interface()
interface.initialize()

motors = [0,1]
speed = 6.0
angle_ratio = 1.66

interface.motorEnable(motors[0])
interface.motorEnable(motors[1])

motorParams0 = interface.MotorAngleControllerParameters()
motorParams0.maxRotationAcceleration = 6.0
motorParams0.maxRotationSpeed = 12.0
motorParams0.feedForwardGain = 255/20.0
motorParams0.minPWM = 18.0
motorParams0.pidParameters.minOutput = -255
motorParams0.pidParameters.maxOutput = 255
motorParams0.pidParameters.k_p = 670.0
motorParams0.pidParameters.k_i = 400.0
motorParams0.pidParameters.k_d = 200.0

motorParams1 = interface.MotorAngleControllerParameters()
motorParams1.maxRotationAcceleration = 6.0
motorParams1.maxRotationSpeed = 12.0
motorParams1.feedForwardGain = 255/20.0
motorParams1.minPWM = 18.0
motorParams1.pidParameters.minOutput = -255
motorParams1.pidParameters.maxOutput = 255
motorParams1.pidParameters.k_p = 570.0
motorParams1.pidParameters.k_i = 400.0
motorParams1.pidParameters.k_d = 200.0

interface.setMotorAngleControllerParameters(motors[0],motorParams0)
interface.setMotorAngleControllerParameters(motors[1],motorParams1)

def right90deg():
    interface.increaseMotorAngleReferences(motors,[math.pi * angle_ratio, math.pi * -angle_ratio])
    while not interface.motorAngleReferencesReached(motors) :
      #motorAngles = interface.getMotorAngles(motors)
      time.sleep(0.1)
	
def left90deg():
    interface.increaseMotorAngleReferences(motors,[math.pi * -angle_ratio, math.pi * angle_ratio])
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

def turn_test():
    left90deg()
    time.sleep(1)
    move(3)
    right90deg()

def move_test():
    move(11.6)
    time.sleep(1)
    move(-11.6)

def covariance_matrix(xs, ys):
    n = len(xs)
    xs = map(lambda x: float(x), xs)
    ys = map(lambda x: float(x), ys)
    mean_x = reduce(lambda x, y: x + y, xs) / n
    mean_y = reduce(lambda x, y: x + y, ys) / n
    x_term = round(reduce(lambda x, y: x + y, map(lambda x: (x - mean_x)**2, xs))/ n, 3)
    y_term = round(reduce(lambda x, y: x + y, map(lambda x: (x - mean_y)**2, ys))/ n, 3)
    zs = []
    for i in range(n):
        zs.append((xs[i] - mean_x) * (ys[i] - mean_y))
    same_term = round(reduce(lambda x, y: x + y, zs) / n, 3)
    return [[x_term, same_term],[same_term, y_term]]

print "Press Ctrl+C to exit"
counter = 0
exclaimation = ""
while True:
    select = input("Enter 1-4 for : square_move, turn_test, move_test, covariance_matrix : ")
    if select == 1:
        counter += 1
        exclaimation += "!"
        move_in_square()
        print("You have tried square moving" + str(counter) + " times" + exclaimation)
    elif select == 2:
        turn_test()
        print("Turn test finished!")
    elif select == 3:
        move_test()
        print("Move test finished!")
    elif select == 4:
	xs = [1.9, 0.3, -0.7, -0.8, -0.5, -3.3, 0.9, 0.4, -4.0, 0.3]
	ys = [-4.1, -4.6, -0.3, -0.6, -2.9, 2.5, -2.0, -1.2, -0.3, 0.9]
	print("Covariance matrix is below: ")
	print(covariance_matrix(xs, ys))
    else:
        break
interface.terminate()

