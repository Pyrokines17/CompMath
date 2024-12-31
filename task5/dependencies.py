import matplotlib.animation as animation
import matplotlib.pyplot as plt

import numpy as np

import os

BORDER = 10
PCOUNT = 1000

def print_functions():
    print("1. f(x) = ln(1+x) + a - x")
    print("2. f(x) = l * sin(x) - x")

def print_methods():
    print("1. Newton's method")
    print("2. Secant method")

def checked_input():
    try:
        tmp = int(input())
    except ValueError:
        print("Invalid or empty input")
        exit()
    
    if tmp > 2 or tmp < 1:
        print("Invalid input")
        exit()
    
    return tmp

def checked_input_float():
    try:
        tmp = float(input())
    except ValueError:
        print("Invalid or empty input")
        exit()
    
    return tmp

def check_root(x, roots, eps=1e-6):
    for root in roots:
        if np.abs(x - root) < eps:
            return True
    
    return False

def create_gif(points: list, func, num: int, name: str, first: bool):
    fig, ax = plt.subplots()
    
    end = points[-1]
    begin = points[0]

    diff = np.abs(end - begin) + 1

    ax.set_xlim(end-diff, end+diff)
    x = np.linspace(end-diff, end+diff, 2*int(diff)*10)
    
    scat = ax.scatter(points[0], 0)

    ax.plot(x, [func(i) for i in x])
    
    ax.axhline(0, color='black')
    ax.axvline(0, color='black')
    
    count_temp = "iter = %d"
    coord_temp = "x = %.10f"

    coord_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    count_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)

    def animate(i):
        scat.set_offsets((points[i], 0))
        coord_text.set_text(coord_temp % points[i])
        count_text.set_text(count_temp % i)
        return scat,
    
    if first:
        if not os.path.exists('output'):
            os.mkdir('output')
            os.mkdir(f'output/{name}')
        elif not os.path.exists(f'output/{name}'):
            os.mkdir(f'output/{name}')
        else:
            files = os.listdir(f'output/{name}')
            for file in files:
                os.remove(f'output/{name}/{file}')

    try:
        ani = animation.FuncAnimation(fig, animate, frames=len(points), interval=100)
        ani.save(f'output/{name}/out{num}.gif', writer='imagemagick', fps=1)
    except Exception as e:
        print("Error: can't create gif:", e)
