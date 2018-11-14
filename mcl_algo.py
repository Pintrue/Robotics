import math
import random
import sys

lines = [("OA", (0, 0), (0, 168)),
("OH", (0, 0), (210, 0)),
("AB", (0, 168), (84, 168)),
("BC", (84, 168), (84, 126)),
("BD", (84, 168), (84, 210)),
("CD", (84, 126), (84, 210)),
("DE", (84, 210), (168, 210)),
("EF", (168, 210), (168, 84)),
("FG", (168, 84), (210, 84)),
("GH", (210, 84), (210, 0))]

def calculate_intersect(x, y, theta, m):
    xn = x + m * math.cos(theta)
    yn = y + m * math.sin(theta)
    return (xn, yn)

def calculate_m(x, y, theta, pa, pb):
    ax = pa[0]
    ay = pa[1]
    bx = pb[0]
    by = pb[1]
    t1 = (by-ay) * (ax-x) - (bx-ax) * (ay-y)
    t2 = (by-ay) * math.cos(theta) - (bx-ax) * math.sin(theta)
    return float('inf') if t2 == 0 else t1 / t2

def is_on_the_line(pa, pb, p):
    ax = pa[0]
    ay = pa[1]
    bx = pb[0]
    by = pb[1]
    px = p[0]
    py = p[1]
    #horizontal
    if ay == by:
        return ax < px < bx if bx > ax else bx < px < ax
    #vertical or oblique
    else:
        return ay < py < by if by > ay else by < py < ay


def calculate_likelihood(x, y, theta, z):
    res = float('inf')
    for i in range(len(lines)):
        pa = lines[i][1]
        pb = lines[i][2]
        m = calculate_m(x, y, theta, pa, pb)
        #print "THIS IS " + str(m)
        if m >= 0 and is_on_the_line(pa, pb, calculate_intersect(x, y, theta, m)) and m < res:
            res = m
    sd = 1
    return math.exp(-(z - m)** 2 / 2 / sd ** 2)

def normalise(ps):
    probs = map(lambda p: p[3], ps)
    #print probs
    tp = reduce(lambda x, y: x + y, probs)
    print tp
    return [(x, y, theta, float(p) / tp) for (x, y, theta, p) in ps]

def sample(ori, dest, z, sigma=0.55):
    dx = dest[0] - ori[0]
    dy = dest[1] - ori[1]
    theta = ori[2]
    particles = []
    dist = math.sqrt(dx**2 + dy**2)
    x = ori[0]
    y = ori[1]
    for _ in range(100):
        e = random.gauss(0, sigma)
        new_x = x + (dist + e) * math.cos(theta)
        new_y = y + (dist + e) * math.sin(theta)
        theta += random.gauss(0, sigma)
        theta %= 2 * math.pi
        p = calculate_likelihood(new_x, new_y, theta, z)
        #print p
        particles.append((new_x,new_y,theta, p))
    return normalise(particles)
    # return particles

def resample(particles):
    acc = 0
    cdf = [0]
    resampled_particles = []
    for (_, _, _, p) in particles:
        acc += p
        cdf.append(acc)

    tp = cdf[len(cdf) - 1]
    for _ in range(100):
        rnm = random.uniform(0, tp)
        # TODO: wo ri ni xue ma
        idx = binary_lookup(cdf, rnm)
        x, y, theta, _ = particles[idx]
        resampled_particles.append((x, y, theta, 0.01))

    return resampled_particles

#calculate mean of the resampled particals
def averageOf(particles):
    p_sum = reduce(lambda x, y: [sum(x) for x in zip(x, y)], particles)
    return [x / 100 for x in p_sum]

#return index
def binary_lookup(cdf, rnm):
    start = 0
    end = len(cdf) - 1
    mid = int((start + end) / 2)
    if rnm > cdf[end]:
        print("Error: rnm greater than largest of cdf")
        sys.exit(1)
    while rnm > cdf[mid + 1] or rnm < cdf[mid]:
        if rnm > cdf[mid + 1]:
            start = mid
            mid = int((mid + end) / 2)
        else:
            end = mid
            mid = int((start + mid) / 2)
    return mid

def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def nextMove(ori, dst, interval):
    d = distance(ori, dst)
    if d < interval:
        return dst
    else:
        print ori[2]
        dx = float("{:.2f}".format(math.cos(ori[2]))) * interval
        dy = float("{:.2f}".format(math.sin(ori[2]))) * interval
        return (dx, dy)

def displayParticles(particles):
    print "drawParticles:" + str(particles)
    return

# from initial import *
# initial = (84, 30)
# points = [(180,30),(180,54),(138,54),(138,168),(114,168),(114,84),(84,84),(84,30)]

# interface = Init()
# interface.global_x = initial[0]
# interface.global_y = initial[1]
# interface.global_theta = 0

# interval = 20

# for i in range(len(points)):
#     next_dst = points[i]
#     ori = (interface.global_x, interface.global_y, interface.global_theta)
#     remaining_distance = distance(ori, next_dst)
#     while True:
#         next_mov = nextMove(ori, next_dst, interval)
#         interface.move(next_mov)
#         sonar_reading = interface.ultrasonic_average_reading
#         resampled_particles = resample(sample(ori, next_mov, sonar_reading))
#         displayParticles(resampled_particles)
#         current_pos = averageOf(resampled_particles)
#         interface.global_x, interface.global_y, interface.global_theta = current_pos
#         if next_mov == next_dst:
#             break
    
    



#print(normalise([1,2,3]))

#print calculate_likelihood(1, 1, 0, 90)
