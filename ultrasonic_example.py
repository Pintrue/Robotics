import brickpi
import time
from initial import *

interface = Init()

while True:
    a = float(input("Input angle: "))
    interface.turn_sensor(a)
    interface.ultrasonic()

interface.terminate()