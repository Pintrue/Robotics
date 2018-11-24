import mcl_algo as mcl

points = [(84, 30),(180,30),(180,54),(138,54),(138,168),(114,168),(114,84),(84,84),(84,30)]
initial = (84, 30)

def waypoints_readings(interval):
    read_times = 360 / interval
    waypoints = []
    
    for (x, y) in points:
        readings = []
        
        for i in range(read_times):
            readings.append(mcl.calculate_correct_m(x, y, interval * i))
        
        waypoints.append(readings)
        
    return waypoints

print waypoints_readings(45)