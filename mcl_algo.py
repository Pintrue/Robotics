import math

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
            line = lines[i][0]
    return line


print calculate_likelihood(1, 1, 0, 90)
