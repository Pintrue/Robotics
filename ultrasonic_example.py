import brickpi
import time
from initial import *

interface = Init()

while True:
    a = int(input("Input angle: "))
    print "turning " + str(a)
    interface.turn_sensor(a)

interface.terminate()