
from mcl_algo import *
import math
from initial import *

def shiftHistLeft(hist, n):
    shift = n % len(hist)
    return hist[shift:] + hist[:shift]

def shiftHistRight(hist, n):
    shift = n % len(hist)
    return hist[len(hist) - shift:] + hist[:len(hist) - shift]

def histError(actualHist, standardHist):
    return reduce(lambda x, y: x + y, map(lambda x: (x[0] - x[1])**2 if x[0] < 255 else 0, zip(actualHist, standardHist)))

def localize(actualHist, standardHists, ground_truth=None):
    histSize = len(actualHist)
    sampleSize = len(standardHists)
    errors = [0] * sampleSize
    shifts = [0] * sampleSize
    for idx in range(0, sampleSize):
        nxtStandardHist = standardHists[idx]
        minError = float('inf')
        for shift in range(0, histSize):
            newError = histError(shiftHistLeft(actualHist, shift), nxtStandardHist)
            minError, shifts[idx] = (minError, shifts[idx]) if minError < newError else (newError, shift)
        print "histError at " + str(idx) + " is: " + str(minError)
        errors[idx] = minError
        minimalErrIdx = errors.index(min(errors))
    
    if ground_truth is not None:
        minimalErrIdx_g, shift_g = localize(actualHist, ground_truth)
        if minimalErrIdx_g < minimalErrIdx:
            minimalErrIdx, shifts[minimalErrIdx] = minimalErrIdx_g, shift_g
    
    return (minimalErrIdx, shifts[minimalErrIdx])

#p: point, m: length
def possibleAngles(p, m):
    res = []
    for i in range(len(lines)):
        pa = lines[i][1]
        pb = lines[i][2]
        angles = calculateAngle(p[0], p[1], m, pa, pb)
        print "line " + str(lines[i]) + ": " + str(angles)
        res += angles
    #print "before filtering " + str(res)
    toBeRemoved = []
    for idx in range(len(res)):
        cm = calculate_correct_m(p[0], p[1], res[idx])
        #print "cm at angle: " + str(res[idx]) + " is " + str(cm)
        if cm < m - 1 or cm > m + 1:
            toBeRemoved.append(idx)
    ret = []
    #print "toberemoved: " + str(toBeRemoved)
    for idx in range(len(res)):
        if idx in toBeRemoved:
            continue
        ret.append(res[idx])
    return ret

#solve equation Acos(theta) - Bsin(theta) = C
def calculateAngle(x, y, m, pa, pb):
    pa_x = pa[0]
    pa_y = pa[1]
    pb_x = pb[0]
    pb_y = pb[1]
    const_a = pb_y - pa_y
    const_b = pa_x - pb_x
    const_c = (const_a * (pa_x - x) + const_b * (pa_y - y)) / float(m)
    const_d_sqr = const_a**2 + const_b**2 - const_c**2
    if const_d_sqr >= 0:
        const_d = math.sqrt(const_d_sqr)
        if const_b == 0:
            #print "const_c " + str(const_c)
            #print "const_a " + str(const_a)
            res1 = math.acos(float(const_c) / const_a)
            res2 = -res1
            return [math.degrees(res1), math.degrees(res2)]
        if const_a == 0:
            #print "const_c " + str(const_c)
            #print "const_b" + str(const_b)
            res1 = math.asin(float(const_c) / const_b)
            degree = math.degrees(res1)
            return [degree, 180 - degree]
        res1 = math.atan(float(const_a) / const_b) + math.atan(float(const_d) / const_c)
        res2 = math.atan(float(const_a) / const_b) - math.atan(float(const_d) / const_c)
        return [math.degrees(res1), math.degrees(res2)]
    #print "const_d: " + str(const_d_sqr)
    return []

