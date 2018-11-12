import math
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
    return t1 / t2

def calculate_likelihood(x, y, theta, z):
