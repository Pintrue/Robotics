from mcl_algo import lines

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