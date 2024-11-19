from solver import *

MATRIX = [
    [1, 1/2, 1/3],
    [1/2, 1/3, 1/4],
    [1/3, 1/4, 1/5]
]

def print_methods():
    print("1. NumPy")
    print("2. PLU")
    print("3. Jacobi")
    print("4. Gauss-Seidel")
    print("5. Thomas")

def main():
    print("Which methods would you like to use?")
    print_methods()

    methods = list(map(int, input().split()))

    if not methods:
        print("No methods selected")
        return
    
    print("Using matrix? (y/n)")

    if input().lower() == "y":
        A = MATRIX
        b = [1, 1, 1]
        n = 3
    else:
        try:
            print("Enter size of matrix A and vector b:")
            n = int(input())
        except ValueError:
            print("Invalid or empty input")
            return

        print("Enter matrix A:")
        A = []
    
        for _ in range(n):
            row = list(map(float, input().split()))
    
            if len(row) != n:
                print("Invalid input")
                return
            
            A.append(row)
    
        print("Enter vector b:")
        b = list(map(float, input().split()))
    
        if len(A) != len(b) or len(A) != n:
            print("Invalid input")
            return

    npA = np.array(A)
    npb = np.array(b)

    if 1 in methods:
        x = np.linalg.solve(npA, npb)
        print("Np solve:", x)

    if 2 in methods:
        x = plu_solve(npA, npb)
        print("PLU solve:", x)

    if 3 in methods:
        x = jacobi(npA, npb)
        print("Jacobi solve:", x)

    if 4 in methods:
        x = gauss_seidel(npA, npb)
        print("Gauss-Seidel solve:", x)

    if 5 in methods:
        x = thomas(npA, npb)
        print("Thomas solve:", x)

    additional_info(npA)

if __name__ == "__main__":
    main()