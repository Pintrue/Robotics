import brickpi
import time
import math
#from enum import Enum

r_1 = [127, 255, 82, 28]
r_2 = [30, 50, 182, 28]
r_3 = [31, 27, 179, 52]
r_4 = [73, 154, 137, 53]
r_5 = [30, 39, 48, 167]
wall_rds = [r_1, r_2, r_3, r_4, r_5]
waypoints = [(84,30), (180,30), (180,54), (138,54), (138,168)]
'''
class Direction(Enum):
    EAST = 0
    NORTH = 1
    WEST = 2
    SOUTH = 3
'''
class Init:
    def __init__(self):
        self.interface = brickpi.Interface()
        self.interface.initialize()
        
        #0 and 1 are for wheels, 3 is for sonar sensor on the top
        self.motors = [0,1,3]
        
        self.angle_ratio_left = 1.1 / 90
        self.angle_ratio_right = 1.0 / 90
        self.sensor_angle_ratio = 0.53 / 90
        self.move_ratio = 0.3
        
        #current status (positon, angle)
        self.global_x = 0
        self.global_y = 0
        self.global_theta = 0
        self.global_sensor_theta = 0
        

        self.interface.motorEnable(self.motors[0])
        self.interface.motorEnable(self.motors[1])
        self.interface.motorEnable(self.motors[2])
        #left wheel 
        motorParams0 = self.interface.MotorAngleControllerParameters()
        motorParams0.maxRotationAcceleration = 6.0
        motorParams0.maxRotationSpeed = 12.0
        motorParams0.feedForwardGain = 255/20.0 #319/20
        motorParams0.minPWM = 18.0
        motorParams0.pidParameters.minOutput = -255
        motorParams0.pidParameters.maxOutput = 255
        motorParams0.pidParameters.k_p = 675
        motorParams0.pidParameters.k_i = 400
        motorParams0.pidParameters.k_d = 200
        #right wheel
        motorParams1 = self.interface.MotorAngleControllerParameters()
        motorParams1.maxRotationAcceleration = 6.0
        motorParams1.maxRotationSpeed = 16.3
        motorParams1.feedForwardGain = 300/20.0
        motorParams1.minPWM = 18.0
        motorParams1.pidParameters.minOutput = -255
        motorParams1.pidParameters.maxOutput = 255
        motorParams1.pidParameters.k_p = 900
        motorParams1.pidParameters.k_i = 400
        motorParams1.pidParameters.k_d = 200

        #sonar sensor on top
        sensorParam = self.interface.MotorAngleControllerParameters()
        sensorParam.maxRotationAcceleration = 3.0
        sensorParam.maxRotationSpeed = 7.5
        sensorParam.feedForwardGain = 255/20.0
        sensorParam.minPWM = 18.0
        sensorParam.pidParameters.minOutput = -255
        sensorParam.pidParameters.maxOutput = 255
        sensorParam.pidParameters.k_p = 300
        sensorParam.pidParameters.k_i = 200
        sensorParam.pidParameters.k_d = 100

        self.interface.setMotorAngleControllerParameters(self.motors[0],motorParams0)
        self.interface.setMotorAngleControllerParameters(self.motors[1],motorParams1)
        self.interface.setMotorAngleControllerParameters(self.motors[2],sensorParam)

        self.sensor_port = 3
        self.interface.sensorEnable(self.sensor_port, brickpi.SensorType.SENSOR_ULTRASONIC)

        '''
        self.touch_port_left = 0
        self.touch_port_right = 1
        self.interface.sensorEnable(self.touch_port_left, brickpi.SensorType.SENSOR_TOUCH)
        self.interface.sensorEnable(self.touch_port_right, brickpi.SensorType.SENSOR_TOUCH)
        '''
        
    def init(self):
        return self.interface
    
    def terminate(self):
        self.interface.terminate()
        
    def motor_position(self):
        # start logging time and reference angles of the two motors
        self.interface.startLogging("./refangle.txt")
        
        while True:
            angle = float(input("Enter a angle to rotate (in radians): "))

            self.interface.increaseMotorAngleReferences(self.motors[:2],[angle,angle])

            while not self.interface.motorAngleReferencesReached(self.motors[:2]) :
                motorAngles = self.interface.getMotorAngles(self.motors[:2])
                if motorAngles :
                    print "Motor angles: ", motorAngles[0][0], ", ", motorAngles[1][0]
            time.sleep(0.1)

        print "Destination reached!"
    
        # stop logging
        self.interface.stopLogging("./refangle.txt")
    
    def turn(self, degree):
        print "turning " + str(degree) + " degrees"
        
        if degree < 0:
            self.interface.increaseMotorAngleReferences(self.motors[:2],[math.pi * -self.angle_ratio_left * degree, math.pi * self.angle_ratio_right * degree])
        else:
            self.interface.increaseMotorAngleReferences(self.motors[:2],[math.pi * -self.angle_ratio_left * degree, math.pi * self.angle_ratio_right * degree])
        while not self.interface.motorAngleReferencesReached(self.motors[:2]) :
            #motorAngles = interface.getMotorAngles(motors)
            time.sleep(0.1)
        self.global_theta += degree
        self.global_theta %= 360
    
    #p_idx: index of point the robot is currently on
    def turnToWall(self, p_idx):
        #reading index to which the direct reading is compared
        rd_idx = [0, 1, 2, 1, 3]
        std_rd = wall_rds[p_idx][rd_idx[p_idx]]
        angle, df, rd  = self.minimum_difference(std_rd, 36)
        self.turn(angle * 10)
        return angle, df, rd
    
    #1 for clockwise, 0 for anti-clockwise
    def minimum_difference(self, std_rd, steps, direction=0 ,stride=10):
        print "comparing readings with " + str(std_rd)
        angle = 0
        reading = self.ultrasonic_direct_reading()
        print "reading: " + str(reading)
        diff = reading - std_rd
        candidate = []
        if diff**2 < 10:
            candidate.append(0)
        print "difference: " + str(diff)
        for i in range(1,steps):
            self.turn_sensor(stride, direction=direction)
            reading = self.ultrasonic_direct_reading()
            print "reading: " + str(reading)
            newDiff = reading - std_rd
            if newDiff**2 < 10:
                candidate.append(i)
            diff, angle = (newDiff, i) if newDiff**2 <= diff**2 else (diff, angle)
            print "difference " + str(diff)
            if len(candidate) > 3:
                break
        self.reset_sensor()
        print "candidate number: " + str(len(candidate))
        print "sum of candidate: " + str(sum(candidate))
        if len(candidate) > 0:
            angle = sum(candidate) / float(len(candidate))
        if angle > 18:
            angle = angle - 36
        return angle, diff, self.ultrasonic_average_reading()


    #p_idx: index of point from which the robot set off
    #1 for clockwise turn, 0 for anti-clockwise turn
    def trial_run_and_update(self, p_idx):
        rd_idx = [3, 0, 3, 2, 0]
        std_rd = wall_rds[p_idx][rd_idx[p_idx]]
        trial_distance = 15

        #td: trial_distance
        angle_f1 = lambda diff, td: math.asin(diff/float(td))
        angle_f2 = lambda diff, td: math.asin(diff/float(td)) + 90
        angle_f3 = lambda diff, td: -180 - math.asin(diff/float(td))
        angle_f4 = lambda diff, td: 90 - math.asin(diff/float(td))
        angle_f5 = lambda diff, td: -90 - math.asin(diff/float(td))
        angle_function = [angle_f1, angle_f2, angle_f3, angle_f4, angle_f5]

        
        direction = 0
        if p_idx in [0,1]:
            direction = 1
            
        self.move(trial_distance)
        _, diff, _ = self.minimum_difference(std_rd, 18, direction=direction)
        print "std_rd " + str(std_rd)
        print "difference" + str(diff)
        curr_angle = angle_function[p_idx](diff, trial_distance)
        self.global_theta = curr_angle
        print "Angle after trial is " + str(curr_angle)
        self.global_x = int(waypoints[p_idx][0] + trial_distance * math.cos(math.radians(curr_angle)))
        self.global_y = int(waypoints[p_idx][1] + trial_distance * math.sin(math.radians(curr_angle)))
        return curr_angle
        

    def navigation(self, p_idx):
        routes = waypoints[p_idx + 1:] + waypoints[:p_idx + 1]
        for r in routes:
            self.navigateToWaypoint(r[0], r[1])
        
    #1 for clockwise, 0 for anti-clockwise
    def turn_sensor(self, degree, direction=0):
        if degree == 0:
            return
        if direction:
            self.interface.increaseMotorAngleReferences(self.motors[2:],[math.pi * self.sensor_angle_ratio * -degree])
        else:
            self.interface.increaseMotorAngleReferences(self.motors[2:],[math.pi * self.sensor_angle_ratio * degree])
        while not self.interface.motorAngleReferencesReached(self.motors[2:]):
            time.sleep(0.05)
        self.global_sensor_theta += degree


    def reset_sensor(self):
        degree = -self.global_sensor_theta
        self.interface.increaseMotorAngleReferences(self.motors[2:],[math.pi * self.sensor_angle_ratio * degree])
        while not self.interface.motorAngleReferencesReached(self.motors[2:]):
            time.sleep(0.05)
        self.global_sensor_theta = 0
    
    #return depth to angle histogram, steps indicate number of angles at which sensor reading is taken
    def depth_histogram(self, steps):
        stride = int(360 / steps)
        fstReading = self.ultrasonic_average_reading()
        hist = [fstReading]
        for _ in range(1, steps):
            self.turn_sensor(stride)
            nxtReading = self.ultrasonic_average_reading()
            hist.append(nxtReading)
        return hist
        
    def right90deg(self):
        self.turn(-90)
    
    def left90deg(self):
        self.turn(90)
        
    def stop(self):
        self.interface.setMotorPwm(self.motors[0], 0)
        self.interface.setMotorPwm(self.motors[1], 0)


    def move(self, distance):
        radian = distance * self.move_ratio
        self.interface.increaseMotorAngleReferences(self.motors[:2], [radian, radian])
        while not self.interface.motorAngleReferencesReached(self.motors[:2]):
            time.sleep(0.1)
    
    def move_xy(self, delta_x, delta_y):
        distance = math.sqrt(delta_x**2 + delta_y**2)
        self.move(distance)
        self.global_x += delta_x
        self.global_y += delta_y
    
    def move_in_square_particle(self):
        for _ in range(4):
            print("moving forward")
            for _ in range(4):
                self.move(10)
                time.sleep(0.25)
            print("turning")
            self.right90deg()
            
    def adjustArctan(self, delta_y, delta_x):
        ratio = delta_y / delta_x
        angle = math.degrees(math.atan(ratio))
        if delta_x < 0:
            angle += 180
        return angle
    
    
    def turnToPoint(self, x, y):
        delta_y = y - self.global_y
        delta_x = x - self.global_x
        target_theta = 0
        
        if delta_x == 0 and delta_y == 0:
            return
        
        
        if delta_x == 0:
            if delta_y > 0:
                target_theta = 90
            elif delta_y < 0:
                target_theta = -90
        elif delta_y == 0:
            if delta_x > 0:
                target_theta = 0
            elif delta_x < 0:
                target_theta = 180
        else:
            target_theta = self.adjustArctan(delta_y, delta_x)
            
            #if ratio < 0:
            #    target_theta = angle
            #else:
            #    if delta_y < 0:
            #        target_theta = angle + 180
            #    else:
            #        target_theta = angle
                
        delta_theta = target_theta - self.global_theta
        
        if delta_theta > 180:
            delta_theta -= 360
        elif delta_theta < -180:
            delta_theta += 360

        self.turn(delta_theta)
        return (delta_x, delta_y)
            
    def navigateToWaypoint(self, x, y):
        delta_x, delta_y = self.turnToPoint(x, y)
        time.sleep(0.1)
        self.move_xy(delta_x, delta_y)
        
    def print_global(self):
        print("x was " + str(self.global_x) + ", y was " + str(self.global_y) + ", theta was " + str(self.global_theta) + ", sensor at angle " + str(self.global_sensor_theta))
    
    def ultrasonic(self):
        counter = 0
        start_time = time.time()
        while True:
            usReading = self.interface.getSensorValue(self.sensor_port)
            if usReading :
                print(usReading[0])
            else:
                print "Failed US reading"
            time.sleep(0.05)   
            counter += 1
        print("counter is " + counter + " with time " + str(time.time() - start_time))
    
    def ultrasonic_average_reading(self):
        readings = []
        for _ in range(10):
            usReading = self.interface.getSensorValue(self.sensor_port)
            if usReading:
                readings.append(usReading[0])
            time.sleep(0.05)
        readings.sort()
        
        return readings[len(readings) / 2]
    
    def ultrasonic_direct_reading(self):
        usReading = [255]
        for _ in range(10):
            usReading = self.interface.getSensorValue(self.sensor_port)
            if usReading:
                break
        
        return usReading[0]
    
    
    '''
    previous assessment
    '''
    def covariance_matrix(self, xs, ys):
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

    def move_in_square(self):
        for _ in range(4):
            print("moving forward")
            self.move(40)
            print("turning")
            self.right90deg()

    def turn_test(self):
        self.left90deg()
        time.sleep(1)
        self.move(10)
        self.right90deg()

    def move_test(self):
        self.move(40)
        time.sleep(1)
        self.move(-40)

'''
    def detect_bump(self):
        distance = 5
        while True:
            bump1 = self.interface.getSensorValue(self.touch_port_left)
            bump2 = self.interface.getSensorValue(self.touch_port_right)
            usReading = self.interface.getSensorValue(self.sensor_port)
            if usReading :
                print(usReading[0])
                if usReading[0] > 30:
                    #interface.setMotorRotationSpeedReferences(motors, [speed, speed * 1.3])
                    print("Turn towards wall")
                else:
                    #interface.setMotorRotationSpeedReferences(motors, [speed * 1.3, speed])
                    print("Turn away from the wall")
            else:
                print "Failed US reading"
            time.sleep(0.05)
            if bump1 and bump2:
                touch1 = bump1[0]
                touch2 = bump2[0]
                if touch1 and touch2:
                    self.stop()
                    print(touch1, touch2)
                    self.move(-distance)
                    rand = random.randint(0, 1)
                    if rand:
                        self.right90deg()
                    else:
                        self.left90deg()
                elif touch1 and not touch2:
                    self.stop()
                    print(touch1, touch2)
                    self.move(-distance)
                    self.right90deg()
                elif not touch1 and touch2:
                    self.stop()
                    print(touch1, touch2)
                    self.move(-distance)
                    self.left90deg()
                else:
                    self.interface.setMotorRotationSpeedReferences(self.motors[:2], [self.speed, self.speed])
'''