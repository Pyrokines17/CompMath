import numpy as np

def appForK1(y0, h):
    return y0 * (1 - h)

def appForK2(y1, y0, h):
    return -2 * h * y1 + y0

def appForK4(y1, y0, h):
    return (-4 * h * y1 - (h - 3) * y0) / (h + 3)

def getY1(h):
    return (6-h*h)/(2*(3+3*h+h*h))

def rungeError(y1, y2, k):
    return np.abs(y1 - y2) / (2 ** k - 1)

def getP(diffAbs1, diffAbs2):
    return np.log2(diffAbs1 / diffAbs2)

def eqForK1(y0, g0, h):
    return g0 * h + y0

def eqForK2(y0, g1, h):
    return 2 * g1 * h + y0

def eqForK4(g0, g1, g2, y0, h):
    return (g0 * h + 4 * h * g1 + g2 * h + 3 * y0) / 3

def geteqY1(y0, g0, g1, g2, h):
    return (8*h*g1-h*g2+5*h*g0+12*y0)/12
