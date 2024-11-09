import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

from solver import rungeRule
from solver import simpsonRule
from solver import trapezoidRule
from solver import analyticalSolv

from solver import simpsonError
from solver import trapezoidError

from solver import simpsonGraph
from solver import trapezoidGraph

def f1(x):
    return np.log(1+x)

def f2(x):
    return np.exp(x) * np.cos(x)

def spf1():
    x = sp.symbols('x')
    return [sp.log(1+x), x]

def spf2():
    x = sp.symbols('x')
    return [sp.exp(x) * sp.cos(x), x]

def example(x):
    return np.sin(x)

def solv(x):
    return -np.cos(x)

def getP(J1, J2, J):
    return np.log2(np.abs(J2-J)/np.abs(J1-J))

def getRelErr(absErr, J):
    return np.log10(absErr/J)

def main():
    nPoints = int(input("Enter the number of base points(n): "))
    print()

    funcs = [f1, f2]
    spFuncs = [spf1(), spf2()]

    for i in range(len(funcs)):
        func = funcs[i]
        spFunc = spFuncs[i]

        res1 = simpsonRule(func, 0, 2, nPoints)
        res2 = simpsonRule(func, 0, 2, 2*nPoints)

        rungeErr = rungeRule(res1, res2, 4)
        err = simpsonError(spFunc, 0, 2, 2*nPoints)

        print(func.__name__+":", "simp(n)-"+str(res1), "simp(2n)-"+str(res2))
        print("rungeErr-"+str(rungeErr), "simpErr-"+str(err))
        print()

    for i in range(len(funcs)):
        func = funcs[i]
        spFunc = spFuncs[i]

        res1 = trapezoidRule(func, 0, 2, nPoints)
        res2 = trapezoidRule(func, 0, 2, 2*nPoints)
        
        rungeErr = rungeRule(res1, res2, 2)
        err = trapezoidError(spFunc, 0, 2, 2*nPoints)

        print(func.__name__+":", "trap(n)-"+str(res1), "trap(2n)-"+str(res2))
        print("rungeErr-"+str(rungeErr), "trapErr-"+str(err))
        print()

    iters = int(input("Enter count of iters: "))
    tmp = simpsonRule(example, 0, np.pi, nPoints)
    J = analyticalSolv(solv, 0, np.pi)
    newPoints = 2 * nPoints - 1

    for i in range(iters):
        J1 = simpsonRule(example, 0, np.pi, newPoints)
        J2 = tmp
        tmp = J1

        absErr = rungeRule(J2, J1, 4)

        print(f"p for {i+1} iter:", str(getP(J1, J2, J)))
        print(f"relErr for {i+1} iter:", str(getRelErr(absErr, J2)))
        newPoints = 2 * newPoints - 1

    print()

    fun = 0
    choise = int(input("Enter the function number(1 or 2): "))

    if choise == 1:
        fun = f1
    elif choise == 2:
        fun = f2
    else:
        print("Invalid function number")
        return

    x_simp, y_simp = simpsonGraph(fun, 0, 2, nPoints)
    x_trap, y_trap = trapezoidGraph(fun, 0, 2, nPoints)

    plt.plot(x_simp, y_simp, label="Simpson")
    plt.plot(x_trap, y_trap, label="Trapezoid")
    
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
