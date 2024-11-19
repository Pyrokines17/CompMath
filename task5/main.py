from dependencies import *
from solver import *

def ln_solver(meth):
    print("Enter variable: a")
    a = checked_input_float()

    print("Enter left border: ")
    tmp = checked_input_float()
    left_border = tmp if tmp > -1 else -1

    print("Enter right border: ")
    right_border = checked_input_float()

    print("Want only different roots? (y/n)")
    diff = str(input())

    results = []
    diff_roots = []

    points = np.linspace(left_border, right_border, int((right_border - left_border)) * 10)
    
    func = lambda x: np.log(1+x) + a - x

    if meth == 1:
        fp = lambda x: 1 / (1 + x) - 1

        for point in points:
            results.append(newton_zero(func, fp, point))
    else:
        for point in points:
            results.append(secant_zero(func, point, point + 1))

    for i, res in enumerate(results):
        if res is None:
            print(f"No solution found for {i} point")
        else:
            if diff == "y" and check_root(res[-1], diff_roots):
                continue
            else:
                if diff == "y":
                    diff_roots.append(res[-1])

                create_gif(res, func, i)

    return
    
def sin_solver(meth):
    print("Enter variable: l")
    l = checked_input_float()

    print("Enter left border: ")
    left_border = checked_input_float()
    
    print("Enter right border: ")
    right_border = checked_input_float()

    print("Want only different roots? (y/n)")
    diff = str(input())

    results = []
    diff_roots = []
    
    points = np.linspace(left_border, right_border, int((right_border - left_border)) * 10)
    
    func = lambda x: l * np.sin(x) - x

    if meth == 1:
        fp = lambda x: l * np.cos(x) - 1

        for point in points:
            results.append(newton_zero(func, fp, point))
    else:
        for point in points:
            results.append(secant_zero(func, point, point + 1))

    for i, res in enumerate(results):
        if res is None:
            print(f"No solution found for {i} point")
        else:
            if diff == "y" and check_root(res[-1], diff_roots):
                continue
            else:
                if diff == "y":
                    diff_roots.append(res[-1])
                    
                create_gif(res, func, i)
    
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
    