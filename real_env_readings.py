import brickpi
from initial import *

interface = Init()

point_i = int(input("Enter the point you want to log on"))
log_name = "./readings_" + str(point_i) + ".txt"
f = open(log_name, "w+")

steps = int(input("Enter how many steps you want to log"))
hist = interface.depth_histogram(steps)

f.write(str(hist))
f.close()

interface.reset_sensor()

interface.terminate()