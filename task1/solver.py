from dataclasses import dataclass

EPSILON = 1e-6
DELTA = 5

glo_coefficients = (0, 0, 0, 0)

@dataclass
class QuadraticSolutions:
    D: float
    x1: float
    x2: float
    sol_count: int

@dataclass
class Segment:
    x1: float
    x2: float

@dataclass
class Ray:
    x: float
    go_right: bool

def y(x):
    a, b, c, d = glo_coefficients
    return a*x**3 + b*x**2 + c*x + d

def is_sol(x):
    return abs(y(x)) < EPSILON

def finding_on_segment(segment):
    if is_sol(segment.x1):
        return segment.x1
    if is_sol(segment.x2):
        return segment.x2
    
    l = segment.x1
    r = segment.x2
    c = (l + r) / 2
    
    while True:
        if is_sol(c):
            return c
        elif y(r) * y(c) < 0:
            l = c
        else:
            r = c
        
        c = (l + r) / 2

def finding_on_ray(ray):
    x1 = ray.x
    go_right = ray.go_right
    step = 0
    
    if go_right:
        step = DELTA
    else:
        step = -DELTA

    x2 = x1 + step
    segment = Segment(0, 0)

    while True:
        if is_sol(x1):
            return x1
        if is_sol(x2):
            return x2
        if y(x1) * y(x2) > 0:
            x1 = x2
            x2 += step
        else:
            if go_right:
                segment = Segment(x1, x2)
            else:
                segment = Segment(x2, x1)
            
            break

    return finding_on_segment(segment)

def solveDif():
    a, b, c, d = glo_coefficients

    D = b**2 - 3*a*c

    if D < 0:
        return QuadraticSolutions(D, 0, 0, 0)
    elif D == 0:
        x = (-b)/(3*a)
        return QuadraticSolutions(D, x, 0, 1)
    else:
        x1 = (-b - D**0.5)/(3*a)
        x2 = (-b + D**0.5)/(3*a)
        return QuadraticSolutions(D, x1, x2, 2)

def get_solutions(coefficients):
    global glo_coefficients
    glo_coefficients = coefficients

    diff_solutions = solveDif()

    if diff_solutions.sol_count == 0 or diff_solutions.sol_count == 1:
        cond = diff_solutions.x1
        solution = 0

        if is_sol(cond):
            solution = cond
        elif y(cond) > 0:
            solution = finding_on_ray(Ray(cond, False))
        else:
            solution = finding_on_ray(Ray(cond, True))

        return 3, (solution, solution, solution)
    else:
        x1 = diff_solutions.x1
        x2 = diff_solutions.x2

        if is_sol(x1):
            solution1 = finding_on_ray(Ray(x2, True))
            return 3, (x1, x1, solution1)
        if is_sol(x2):
            solution1 = finding_on_ray(Ray(x1, False))
            return 3, (x2, x2, solution1)
        if y(x1) < -EPSILON:
            solution1 = finding_on_ray(Ray(x2, True))
            return 3, (solution1, solution1, solution1)
        if y(x2) > EPSILON:
            solution1 = finding_on_ray(Ray(x1, False))
            return 3, (solution1, solution1, solution1)
        
        solution1 = finding_on_ray(Ray(x1, False))
        solution2 = finding_on_ray(Ray(x2, True))
        solution3 = finding_on_segment(Segment(x1, x2))

        return 3, (solution1, solution2, solution3)
