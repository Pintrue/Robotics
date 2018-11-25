from initial import *

interface = Init()

interface.global_x = 84
interface.global_y = 30
interface.global_theta = 0
while True:
    interface.print_global()
    x = float(input("Input x: "))
    y = float(input("Input y: "))
    interface.navigateToWaypoint(x, y)
interface.terminate()