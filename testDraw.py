import time
import sys
import random
import math
import numpy as np

"""
c = 0;
def getRandomX():
    return random.randint((c%10)*50, (c%10 + 1)*50)

def getRandomY():
    return random.randint((c%10)*50, (c%10 + 1)*50)

def getRandomTheta(): 
    return random.randint(0, 360)

numberOfParticles = 100

line1 = (10, 10, 10, 500) # (x0, y0, x1, y1)
line2 = (20, 20, 500, 200)  # (x0, y0, x1, y1)

print "drawLine:" + str(line1)
print "drawLine:" + str(line2)

"""
"""
while True:
    # Create a list of particles to draw. This list should be filled by tuples (x, y, theta).
    #particles = [(getRandomX(), getRandomY(), getRandomTheta()) for i in range(numberOfParticles)]
    particles = [(0,0,0)]*100
    for x,y,z in particles:
        x = getRandomX()
        y = getRandomY()
        z = getRandomTheta()
    print(particles)
    print "drawParticles:" + str(particles)
    
    c += 1;
    time.sleep(0.25)
    
    
"""   
   

    
t = 0
numberOfParticles = 100

particles = [(300, 200, 0)] * numberOfParticles
final_particles = []

print "drawLine:" + str((300, 200, 300, 600))
print "drawLine:" + str((300, 600, 700, 600))
print "drawLine:" + str((700, 600, 700, 200))
print "drawLine:" + str((700, 200, 300, 200))
sigma = 0.55
while t < 4:
    d = 0
    while d < 4:
        temp = []
        for (x, y, theta) in particles:
            e = random.gauss(0, sigma)
            x += (10 + e) * 10 * math.cos(math.radians(theta))
            y += (10 + e) * 10 * math.sin(math.radians(theta))
            theta += random.gauss(0, sigma)
            theta %= 360
            temp.append((x,y,theta))
        particles = temp
        d += 1

        print "drawParticles:" + str(particles)
        time.sleep(0.5)
        
    temp = []
    for (x, y, theta) in particles:
        theta += 90 + random.gauss(0, sigma)
        theta %= 360
        temp.append((x,y,theta))

    particles = temp
    if t == 3:
        final_particles = [(x - 300, y - 200) for x, y, _ in particles]
    print "drawParticles:" + str(particles)
    time.sleep(0.25)

    t += 1
    
def calc_sd(final_particles):
    xs,ys = zip(*final_particles)
    x_mean = np.array(xs).mean()
    y_mean = np.array(ys).mean()
    res = 0.0
    for i in range(len(xs)):
        res += (xs[i] - x_mean)**2 + (ys[i] - y_mean)**2
    res = math.sqrt(res/len(xs))
    return res

    
print ("Simulating standard deviation is: " + str(calc_sd([(x/10, y/10) for x,y in final_particles])))
print ("Actual standard deviation is: " + str(calc_sd([(-4.5, -0.9),(-2.6, -1.4),(-4.7, 4.2),(-7.6, 2.8),(-6.2, 3.0)])))

    
