from initial import *


points = [(84, 30), (180, 30), (180, 54), (138, 54), (138, 168)]

interface = Init()



while True:
    interface.print_global()
    x = float(input("Input x: "))
    y = float(input("Input y: "))
    interface.navigateToWaypoint(x, y)
interface.terminate()
