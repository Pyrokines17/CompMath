import matplotlib.pyplot as plt

from solver import *

def intInput(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")

def y(x):
    return np.exp(-x)

def g(x):
    return np.exp(x) * np.cos(x)

def solvG(x):
    return np.exp(x) * (np.cos(x) + np.sin(x)) / 2

def diffInPoint(y1, y2, orig, id):
    print("Difference for n in point", id, ":", np.abs(y1[id] - orig[2*id]))
    print("Difference for 2n in point", id, ":", np.abs(y2[2*id] - orig[2*id]))

def main():
    plt.figure()

    pCount = intInput("Enter segment count: ")
    begin = intInput("Enter begin: ")
    end = intInput("Enter end: ")

    if begin >= end:
        print("Invalid input. Begin must be less than end.")
        return

    if pCount < 1:
        print("Invalid input. Segment count must be greater than 1.")
        return
    
    h = (end - begin) / pCount
    print("h:", h)

    x1 = np.linspace(begin, end, pCount+1)
    x2 = np.linspace(begin, end, pCount*2+1)
    
    yr1 = [1]
    yr2 = [1]

    k = intInput("Enter k (1, 2 or 4): ")

    if k not in (1, 2, 4):
        print("Invalid input. k must be 1, 2 or 4.")
        return
    
    if k == 1:
        for _ in range(1, pCount+1):
            y0 = appForK1(yr1[-1], h)
            yr1.append(y0)
        
        absDiff1 = np.abs(yr1 - y(x1)).max()

        for _ in range(1, 2*pCount+1):
            y0 = appForK1(yr2[-1], h/2)
            yr2.append(y0)

        absDiff2 = np.abs(yr2 - y(x2)).max()
    elif k == 2:
        y0 = appForK1(yr1[-1], h)
        yr1.append(y0)

        for _ in range(2, pCount+1):  
            y0 = appForK2(yr1[-1], yr1[-2], h)
            yr1.append(y0)

        absDiff1 = np.abs(yr1 - y(x1)).max()

        y0 = appForK1(yr2[-1], h/2)
        yr2.append(y0)

        for _ in range(2, 2*pCount+1):
            y0 = appForK2(yr2[-1], yr2[-2], h/2)
            yr2.append(y0)

        absDiff2 = np.abs(yr2 - y(x2)).max()
    elif k == 4:
        y0 = getY1(h)
        yr1.append(y0)

        for _ in range(2, pCount+1):
            y0 = appForK4(yr1[-1], yr1[-2], h)
            yr1.append(y0)

        absDiff1 = np.abs(yr1 - y(x1)).max()

        y0 = getY1(h/2)
        yr2.append(y0)

        for _ in range(2, 2*pCount+1):
            y0 = appForK4(yr2[-1], yr2[-2], h/2)
            yr2.append(y0)

        absDiff2 = np.abs(yr2 - y(x2)).max()

    print("Absolute difference for n points:", absDiff1)
    print("Absolute difference for 2n points:", absDiff2)

    diffInPoint(yr1, yr2, y(x2), 5)

    print("Runge error:", rungeError(yr1[-1], yr2[-2], k))

    plt.plot(x2, yr2, 'bo')
    plt.plot(x1, yr1, 'ro')
    plt.plot(x1, y(x1))

    plt.show()

    iteration = intInput("Enter p tests: ")

    if iteration < 1:
        print("Invalid input. Tests must be greater than 0.")
        return
    
    dRes1 = yr1[-2]
    dRes2 = yr2[-3]

    pCount *= 2
    h /= 2

    id = -2
    
    for _ in range(iteration):
        pCount *= 2
        h /= 2

        id *= 2

        oldRes = dRes1
        dRes1 = dRes2

        yr = [1]

        if k == 1:
            for _ in range(1, pCount):
                y0 = appForK1(yr[-1], h)
                yr.append(y0)
            
            dRes2 = yr[id]
        elif k == 2:
            y0 = appForK1(yr[-1], h)
            yr.append(y0)

            for _ in range(2, pCount):  
                y0 = appForK2(yr[-1], yr[-2], h)
                yr.append(y0)

            dRes2 = yr[id]
        elif k == 4:
            y0 = getY1(h)
            yr.append(y0)

            for _ in range(2, pCount):
                y0 = appForK4(yr[-1], yr[-2], h)
                yr.append(y0)

            dRes2 = yr[id]

        print("P:", getP(np.abs(oldRes-dRes1), np.abs(dRes1-dRes2)))

def main1():
    plt.figure()

    pCount = intInput("Enter segment count: ")
    begin = intInput("Enter begin: ")
    end = intInput("Enter end: ")

    if begin >= end:
        print("Invalid input. Begin must be less than end.")
        return

    if pCount < 1:
        print("Invalid input. Segment count must be greater than 1.")
        return
    
    h = (end - begin) / pCount
    print("h:", h)

    x = np.linspace(begin, end, pCount+1)
    x1 = np.linspace(begin, end, 2*pCount+1)

    yr = [solvG(begin)]
    gr = [g(begin)]

    yr1 = [solvG(begin)]
    gr1 = [g(begin)]

    k = intInput("Enter k (1, 2 or 4): ")

    if k not in (1, 2, 4):
        print("Invalid input. k must be 1, 2 or 4.")
        return
    
    if k == 1:
        for i in range(1, pCount+1):
            y0 = eqForK1(yr[-1], gr[-1], h)
            yr.append(y0)
            gr.append(g(x[i]))

        for i in range(1, 2*pCount+1):
            y0 = eqForK1(yr1[-1], gr1[-1], h/2)
            yr1.append(y0)
            gr1.append(g(x1[i]))
    elif k == 2:
        y0 = eqForK1(yr[-1], gr[-1], h)
        yr.append(y0)
        gr.append(g(x[1]))

        for i in range(2, pCount+1):
            y0 = eqForK2(yr[-2], gr[-1], h)
            yr.append(y0)
            gr.append(g(x[i]))

        y0 = eqForK1(yr1[-1], gr1[-1], h/2)
        yr1.append(y0)
        gr1.append(g(x1[1]))

        for i in range(2, 2*pCount+1):
            y0 = eqForK2(yr1[-2], gr1[-1], h/2)
            yr1.append(y0)
            gr1.append(g(x1[i]))
    elif k == 4:
        for i in range(1, pCount+1):
            gr.append(g(x[i]))

        y0 = geteqY1(yr[0], gr[0], gr[1], gr[2], h)
        yr.append(y0)

        for i in range(2, pCount+1):
            y0 = eqForK4(gr[i - 2], gr[i - 1], gr[i], yr[i - 2], h)
            yr.append(y0)

        for i in range(1, 2*pCount+1):
            gr1.append(g(x1[i]))

        y0 = geteqY1(yr1[0], gr1[0], gr1[1], gr1[2], h/2)
        yr1.append(y0)

        for i in range(2, 2*pCount+1):
            y0 = eqForK4(gr1[i - 2], gr1[i - 1], gr1[i], yr1[i - 2], h/2)
            yr1.append(y0)

    print("Absolute difference for n points:", np.abs(yr - solvG(x)).max())

    plt.plot(x, yr, 'ro')

    x1 = np.linspace(begin, end, 10*pCount+1)
    
    plt.plot(x1, solvG(x1))
    plt.show()

    iteration = intInput("Enter p tests: ")

    if iteration < 1:
        print("Invalid input. Tests must be greater than 0.")
        return

    dRes1 = yr[-2]
    dRes2 = yr1[-3]

    pCount *= 2
    h /= 2

    id = -2

    for _ in range(iteration):
        pCount *= 2
        h /= 2

        id *= 2

        oldRes = dRes1
        dRes1 = dRes2

        yr = [solvG(begin)]
        gr = [g(begin)]

        x = np.linspace(begin, end, pCount+1)

        if k == 1:
            for i in range(1, pCount):
                y0 = eqForK1(yr[-1], gr[-1], h)
                yr.append(y0)
                gr.append(g(x[i]))

            dRes2 = yr[id]
        elif k == 2:
            y0 = eqForK1(yr[-1], gr[-1], h)
            yr.append(y0)
            gr.append(g(x[1]))

            for i in range(2, pCount):
                y0 = eqForK2(yr[-2], gr[-1], h)
                yr.append(y0)
                gr.append(g(x[i]))

            dRes2 = yr[id]
        elif k == 4:
            for i in range(1, pCount):
                gr.append(g(x[i]))

            y0 = geteqY1(yr[0], gr[0], gr[1], gr[2], h)
            yr.append(y0)

            for i in range(2, pCount):
                y0 = eqForK4(gr[i - 2], gr[i - 1], gr[i], yr[i - 2], h)
                yr.append(y0)

            dRes2 = yr[id]

        print("P:", getP(np.abs(oldRes-dRes1), np.abs(dRes1-dRes2)))


if __name__ == "__main__":
    choose = input("Choose a task (a or b): ")
    
    if choose == "a":
        main()
    elif choose == "b":
        main1()
    else:
        print("Invalid input. Please enter a or b.")
