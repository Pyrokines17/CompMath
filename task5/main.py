import matplotlib.pyplot as plt1

from dependencies import *
from decimal import *
from solver import *

EPS = 1e-6

def ln_solver(meth):
    first = True
    counter = 0

    print("Enter variable a: ")
    a = checked_input_float()

    print("Enter left border: ")
    tmp = checked_input_float()

    left_border = tmp if tmp > -2 else -2

    print("Enter right border: ")
    right_border = checked_input_float()

    if (left_border > right_border):
        print("Invalid input of border!")
        exit(1)

    print("Want only different roots? (y - agree)")
    diff = str(input())

    results = []
    diff_roots = []

    points = np.linspace(left_border, right_border, int((right_border-left_border)) * 10)
    
    func = lambda x: np.log(1+x) + a - x
    invFunc = lambda x: np.exp(x-a) - x - 1

    if meth == 1:
        fp = lambda x: 1 / (1+x) - 1
        invfp = lambda x: np.exp(x-a) - 1

        name = "newton"

        for point in points:
            results.append(newton_zero(func, fp, point))
            results.append(newton_zero(invFunc, invfp, point))
    else:
        name = "secant"

        for point in points:
            results.append(secant_zero(func, point-1, point))
            results.append(secant_zero(invFunc, point-1, point))

    for i, res in enumerate(results):
        if res is None:
            print(f"No solution found for {i} point")
        else:
            if diff == "y" and check_root(res[-1], diff_roots):
                continue
            else:
                if diff == "y":
                    diff_roots.append(res[-1])

                    if res[-1] > 0 and not np.abs(res[-1]) < EPS:
                        y = []
                        x = []
                        plt1.clf()

                        if not os.path.exists("plots"):
                            os.makedirs("plots")

                        try:
                            for pt in res:
                                if pt != res[-2] and pt != res[-1]:
                                    sub = Decimal(pt)-Decimal(res[-1])
                                    x.append(Decimal.log10(abs(sub)))
                                if pt != res[0] and pt != res[-1]:
                                    sub = Decimal(pt)-Decimal(res[-1])
                                    y.append(Decimal.log10(abs(sub)))

                            plt1.plot(x, y)
                            plt1.savefig(f"plots/{name}{counter}.jpg")
                            counter += 1
                        except Exception as e:
                            print("Error: can't create plot", e)

                create_gif(res, func, i, name, first)

                if first:
                    first = False
                
    if diff == "y":
        print("Diff roots:", diff_roots)

    return

def sin_solver(meth):
    first = True

    print("Enter variable l: ")
    l = checked_input_float()

    print("Enter the border (max:l): ")
    tmp = checked_input_float()

    border = tmp if tmp < l+1 else l+1

    print("Want only different roots? (y - agree)")
    diff = str(input())

    results = []
    diff_roots = []
    
    points = np.linspace(0, border, int(border) * 10)
    
    func = lambda x: l * np.sin(x) - x
    invFunc = lambda x: np.arcsin(x/l) - x

    if meth == 1:
        fp = lambda x: l * np.cos(x) - 1
        invfp = lambda x: np.abs(l) / (l*np.sqrt(l**2 - x**2)) - 1

        name = "newton"

        for point in points:
            results.append(newton_zero(func, fp, point))
            results.append(newton_zero(invFunc, invfp, point))
    else:
        name = "secant"

        for point in points:
            results.append(secant_zero(func, point, point+1))
            results.append(secant_zero(invFunc, point, point+1))

    for i, res in enumerate(results):
        if res is None:
            print(f"No solution found for {i} point")
        else:
            if diff == "y" and check_root(res[-1], diff_roots):
                continue
            else:
                if diff == "y":
                    diff_roots.append(res[-1])
                    
                create_gif(res, func, i, name, first)

                if first:
                    first = False

    for root in diff_roots:
        if np.abs(root) < EPS:
            continue
        if not check_root(-1 * root, diff_roots):
            diff_roots.append(-1 * root)

    if diff == "y":
        print("Diff roots:", diff_roots)
    
    return

def main():
    print("Enter the function you want to solve: ")
    print_functions()

    func = checked_input()
    
    print("Enter the method you want to use: ")
    print_methods()

    meth = checked_input()

    if func == 1:
        ln_solver(meth)
    else:
        sin_solver(meth)

if __name__ == "__main__":
    main()
    