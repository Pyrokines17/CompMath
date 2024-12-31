from matplotlib.animation import FuncAnimation
from solver import resCross, implicit, error

import matplotlib.pyplot as plt
import numpy as np

A = 1
B = 0
C = 1

T = 70

ASEGMS = int(100)
BSEGMS = int(1100)
FRAMES = int(500)

AEND = 4
BEND = 5

choose1 = None

def u1(x, t):
    x = x - C*t
    if x >= 0 and x < 1:
        return 0
    elif x >= 1 and x < 4:
        return np.sin(np.pi * (x-1) / 3)
    elif x >= 4 and x <= 5:
        return 0
    else:
        return 0

def u2(x, t):
    x = x - C*t
    if x < 0:
        return A
    elif x >= 0:
        return B
    else:
        return B

def chooseMethod(len, end, u, segms):
    choose = input("Choose the method (a or b): ")

    global result
    global ht

    ht = end / FRAMES
    h = len / segms
    a = C
    t = end / FRAMES
    n = FRAMES + 1
    
    if choose == "a":
        result = resCross(h, a, t, u, n)
    elif choose == "b":
        result = implicit(h, a, t, u, n)
    else:
        print("Invalid input. Please try again.")
        chooseMethod(end, u, segms)

def chooseMethod1(len, end, u, segms, argt = None):
    global choose1
    
    if choose1 is None:
        choose1 = input("Choose the method (a or b): ")

    h = len / segms
    a = C

    if argt == None:
        t = end / FRAMES
    else:
        t = end / FRAMES / argt
    
    n = FRAMES + 1

    if choose1 == "a":
        result = resCross(h, a, t, u, n, T)
    elif choose1 == "b":
        result = implicit(h, a, t, u, n, T)
    else:
        print("Invalid input. Please try again.")
        chooseMethod1(end, u, segms)

    return result[-1]

def animate1(t):
    y = [u1(xi, t) for xi in x]
    y1 = result[int(t//ht)]

    line.set_ydata(y)
    line1.set_ydata(y1)
    
    return line, line1

def animate2(t):
    y = [u2(xi, t) for xi in x]
    y1 = result[int(t//ht)]
    
    line.set_ydata(y)
    line1.set_ydata(y1)
    
    return line, line1

def main():
    global x, line, line1

    choose = input("Choose the function (a or b): ")

    if choose == "a":
        x = np.linspace(0, 5, ASEGMS+1)
        fig, (ax, ax1) = plt.subplots(2, 1)

        u = [u1(xi, 0) for xi in x]

        line, = ax.plot(x, u)
        line1, = ax1.plot(x, u)

        ax.set_xlim(0, 5)
        ax.set_ylim(-1, 1)

        ax1.set_xlim(0, 5)
        ax1.set_ylim(-1, 1)

        chooseMethod(5, AEND, u, ASEGMS)

        ani = FuncAnimation(fig, animate1, frames=np.linspace(0, AEND, FRAMES+1), blit=True)
        
        plt.show()
    elif choose == "b":
        x = np.linspace(-1, 10, BSEGMS+1)
        fig, (ax, ax1) = plt.subplots(2, 1)

        u = [u2(xi, 0) for xi in x]

        line, = ax.plot(x, u)
        line1, = ax1.plot(x, u)

        border = max(np.abs(A), np.abs(B)) + 1

        ax.set_xlim(-1, 10)
        ax.set_ylim(-0.1, 1.1)

        ax1.set_xlim(-1, 10)
        ax1.set_ylim(-0.1, 1.1)

        chooseMethod(11, BEND, u, BSEGMS)

        ani = FuncAnimation(fig, animate2, frames=np.linspace(0, BEND, FRAMES+1), blit=True)
        plt.show()
    else:
        print("Invalid input. Please try again.")
        main()

def main1():
    fig, (ax, ax1) = plt.subplots(2, 1)
    choose = input("Choose the function (a or b): ")

    if choose == "a":
        x = np.linspace(0, 5, ASEGMS+1)
        ht = AEND / FRAMES

        u = [u1(xi, 0) for xi in x]
        ur = [u1(xi, T*ht) for xi in x]

        line, = ax.plot(x, ur)

        ax.set_xlim(0, 5)
        ax.set_ylim(-1, 1)

        ax1.set_xlim(0, 5)
        ax1.set_ylim(-1, 1)

        ur1 = chooseMethod1(5, AEND, u, ASEGMS)

        line1, = ax1.plot(x, ur1)

        plt.show()

        res = u[-2]
        oldRes = ur1[-2]
        
        points = ASEGMS
        ht = AEND / FRAMES
        id = -1
        k = 1

        pTests = int(input("Enter the number of tests: "))

        for _ in range(pTests):
            points = points * 2
            id = id * 2
            k = k * 2

            x = np.linspace(0, 5, int(points+1))
            u = [u1(xi, 0) for xi in x]

            ur1 = chooseMethod1(5, AEND, u, points, k)
            tempRes = ur1[id-1]

            print("Error: ", error(res, oldRes, tempRes))

            oldRes = tempRes

    elif choose == "b":
        x = np.linspace(-1, 1, BSEGMS+1)
        ht = BEND / FRAMES

        u = [u2(xi, 0) for xi in x]
        ur = [u2(xi, T*ht) for xi in x]

        line, = ax.plot(x, ur)

        border = max(np.abs(A), np.abs(B)) + 1

        ax.set_xlim(-1, 1)
        ax.set_ylim(-1 * border, border)

        ax1.set_xlim(-1, 1)
        ax1.set_ylim(-1 * border, border)

        ur1 = chooseMethod1(2, BEND, u, BSEGMS)

        line1, = ax1.plot(x, ur1)

        plt.show()

if __name__ == "__main__":
    fix_choose = input("Fix or not? (y/n): ")

    if fix_choose == "n":
        main()
    elif fix_choose == "y":
        main1()
    else:
        print("Invalid input.")
