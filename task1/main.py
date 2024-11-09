from solver import get_solutions

def print_result(count_solutions, solutions):
    if count_solutions == 1:
        print("One solution: ", solutions[0])
    elif count_solutions == 2:
        print("Two solutions: ", solutions[0], solutions[1])
    elif count_solutions == 3:
        print("Three solutions: ", solutions[0], solutions[1], solutions[2])

def main():
    print("Give me a value of: a, b, c, d -- from ax^3+bx^2+cx+d, separated by spaces")
    a, b, c, d = map(float, input().split())
    count_solutions, solutions = get_solutions((a, b, c, d))
    print_result(count_solutions, solutions)

if __name__ == "__main__":
    main()