from initial import *

interface = Init()

while True:
    interface.print_global()
    x = float(input("Input x: "))
    y = float(input("Input y: "))
    interface.navigateToWaypoint(x, y)
interface.terminate()