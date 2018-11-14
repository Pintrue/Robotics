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
        if m >= 0 and is_on_the_line(pa, pb, calculate_intersect(x, y, theta, m)) and m < res:
            res = m
    sd = 1
    return math.exp(-(z - m)** 2 / 2 / sd ** 2)

def normalise(ps):
    tp = reduce(lambda x, y: x + y, map(lambda p: p[3], ps))
    return [(x, y, theta, float(p) / tp) for (x, y, theta, p) in ps]

def sample(ori, dest, sigma=0.55, z):
    dx = dest[0] - ori[0]
    dy = dest[1] - ori[1]
    theta = ori[2]
    particles = []
    dist = math.sqrt(dx**2 + dy**2)
    for _ in range(100):
        e = random.gauss(0, sigma)
        x += (dist + e) * math.cos(theta)
        y += (dist + e) * math.sin(theta)
        theta += random.gauss(0, sigma)
        theta %= 2 * math.pi
        p = calculate_likelihood(x, y, theta, z)
        particles.append((x,y,theta, p))
    return normalise(particles)
    # return particles

def resample(particles):
    acc = 0
    cdf = [0]
    for (_, _, _, p) in particles:
        acc += p
        cdf.append(acc)

    tp = cdf[len(cdf) - 1]
    for _ in range(100):
        rnm = random.uniform(tp)
        # TODO: wo ri ni xue ma

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


print(normalise([1,2,3]))

print calculate_likelihood(1, 1, 0, 90)
