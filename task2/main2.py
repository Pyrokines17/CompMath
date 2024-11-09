from solver import Lagrange as polyInter

import matplotlib.pyplot as plt
import numpy as np

def getPoints(base, temp):
    x = np.linspace(-2, 2, base).tolist()
    border = int(temp)
    counter = 0

    while (counter < border):
        x.insert(-1, (x[-2]+x[-1])/2)
        x.insert(1, (x[0]+x[1])/2)
        counter += 1

    return x, f(x)

def f(x):
    return np.abs(x);

count = int(input("Enter the number more then 2 of base points: "))

while count < 3:
    count = int(input("Enter the number more then 2 of base points: "))

temp = input("Enter the number of iterations for points: ")

x, y = getPoints(count, temp)
prange = np.linspace(-2, 2, 500)

res1 = f(prange)
res2 = polyInter(prange, x, y)

plt.plot(x,y,marker='o', color='r', ls='', markersize=10)
plt.fill_between(prange, 0, np.abs(res1-res2), color='gray')

plt.plot(prange, res1)
plt.plot(prange, res2)

plt.show()
