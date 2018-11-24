import mcl_algo as mcl

def waypoints_readings(interval, points):
    read_times = 360 / interval
    waypoints = []
    
    for (x, y) in points:
        readings = []
        
        for i in range(read_times):
            readings.append(mcl.calculate_correct_m(x, y, interval * i))
        
        waypoints.append(readings)
        
    return waypoints