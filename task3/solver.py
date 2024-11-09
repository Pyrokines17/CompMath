import numpy as np
import sympy as sp

# n -- number of points

def simpsonRule(f, a, b, n):
    if n % 2 != 1:
        n += 1

    h = (b - a) / (n - 1)
    x = np.linspace(a, b, n)
    y = f(x)

    ISim = (h/3) * (y[0] + 2 * np.sum(y[:n-2:2]) + 4 * np.sum(y[1:n-1:2]) + y[n-1])

    return ISim

def trapezoidRule(f, a, b, n):
    h = (b - a) / (n - 1)
    x = np.linspace(a, b, n)
    y = f(x)

    ITra = (h/2) * (y[0] + 2 * np.sum(y[1:n-1]) + y[n-1])

    return ITra

def rungeRule(I1, I2, p):
    return np.abs(I1 - I2) / (2**p - 1) 

def simpsonError(f, a, b, n):
    if n % 2 != 1:
        n += 1
    
    func4der = sp.diff(f[0], f[1], 4)
    f4der = sp.lambdify(f[1], func4der)

    x = np.linspace(a, b, n)
    max = np.max(np.abs(f4der(x)))
    
    return ((b - a)**5 / (180 * (n - 1)**4)) * max

def trapezoidError(f, a, b, n):
    func2der = sp.diff(f[0], f[1], 2)
    f2der = sp.lambdify(f[1], func2der)

    x = np.linspace(a, b, n)
    max = np.max(np.abs(f2der(x)))

    return ((b - a)**3 / (12 * (n - 1)**2)) * max

def simpsonGraph(f, a, b, n):
    if n % 2 != 1:
        n += 1

    x = np.linspace(a, b, n)
    y = np.zeros(n)

    for i in range(2, n, 1):
        y[i] = simpsonRule(f, a, x[i], i+1)

    return x, y

def trapezoidGraph(f, a, b, n):
    x = np.linspace(a, b, n)
    y = np.zeros(n)

    for i in range(1, n):
        y[i] = trapezoidRule(f, a, x[i], i+1)

    return x, y

def analyticalSolv(func, a, b):
    return func(b) - func(a)
