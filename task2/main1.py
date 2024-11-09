from solver import Lagrange as polyInter

import matplotlib.pyplot as plt
import numpy as np

def getPoints(count, coef):
    x = np.linspace(0, count, count//coef+1).tolist()
    y = f(x)

    return x, y

def getDiffPoints(prange, x1, x2):
    ch = np.random.choice(prange)

    while (ch in x1 or ch in x2):
        ch = np.random.choice(prange)

    return ch
    
def f(x):
    return np.sqrt(x) + np.cos(x)

count = int(input("Enter the number for border: "))
prange = np.linspace(0, count, count * 10)

coef1 = int(input("Enter the number coeficient for first less then border: "))

while coef1 > count:
    coef1 = int(input("Enter the number coeficient for first less then border: "))

x1, y1 = getPoints(count, coef1)
plt.plot(x1,y1,marker='o', color='r', ls='', markersize=10)

coef2 = int(input("Enter the number coeficient for second less then border: "))

while coef2 > count:
    coef2 = int(input("Enter the number coeficient for second less then border: "))

x2, y2 = getPoints(count, coef2)
plt.plot(x2,y2,marker='o', color='b', ls='', markersize=10)

res = f(prange)
plt.plot(prange, res, color='g')

res1 = polyInter(prange, x1, y1)
plt.plot(prange, res1, color='r')

res2 = polyInter(prange, x2, y2)
plt.plot(prange, res2, color='b')

print("Max of error for first: ", np.max(np.abs(res-res1)))
print("Max of error for second: ", np.max(np.abs(res-res2)))

ch = getDiffPoints(prange, x1, x2)

print("X point for comparison: ", ch)
print("Diff between original and first: ", np.abs(f(ch)-polyInter(ch, x1, y1)))
print("Diff between original and second: ", np.abs(f(ch)-polyInter(ch, x2, y2)))

plt.show()
