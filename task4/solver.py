import numpy as np

def plu_decomposition(A):
    n = A.shape[0]

    P = np.eye(n, dtype=np.double)
    L = np.eye(n, dtype=np.double)
    U = A.copy()

    for i in range(n):
        for j in range(i, n):
            if ~np.isclose(U[i, i], 0):
                break
            
            U[[j, j+1]] = U[[j+1, j]]
            P[[j, j+1]] = P[[j+1, j]]

        factor = U[i+1:, i] / U[i, i]

        L[i+1:, i] = factor
        U[i+1:] -= factor[:, np.newaxis] * U[i]

    return P, L, U

def forward_substitution(L, b):
    n = L.shape[0]

    y = np.zeros_like(b, dtype=np.double)

    y[0] = b[0] / L[0, 0]

    for i in range(1, n):
        y[i] = (b[i] - np.dot(L[i, :i], y[:i])) / L[i, i]

    return y

def backward_substitution(U, y):
    n = U.shape[0]

    x = np.zeros_like(y, dtype=np.double)

    x[-1] = y[-1] / U[-1, -1]

    for i in range(n-2, -1, -1):
        x[i] = (y[i] - np.dot(U[i, i:], x[i:])) / U[i, i]

    return x

def plu_solve(A, b):
    P, L, U = plu_decomposition(A)

    y = forward_substitution(L, np.dot(P, b))
    x = backward_substitution(U, y)

    return x

def jacobi(A, b, tol=1e-10, max_iter=10000):
    x = np.zeros_like(b, dtype=np.double)

    T = A - np.diag(np.diagonal(A))

    for i in range(max_iter):
        x_old = x.copy()

        x[:] = (b - np.dot(T, x)) / np.diagonal(A)

        if np.linalg.norm(x - x_old, ord=np.inf) / np.linalg.norm(x, ord=np.inf) < tol:
            break

    return x

def gauss_seidel(A, b, tol=1e-10, max_iter=10000):
    x = np.zeros_like(b, dtype=np.double)

    for i in range(max_iter):
        x_old = x.copy()

        for j in range(A.shape[0]):
            x[j] = (b[j] - np.dot(A[j, :j], x[:j]) - np.dot(A[j, (j+1):], x_old[(j+1):])) / A[j, j]

        if np.linalg.norm(x - x_old, ord=np.inf) / np.linalg.norm(x, ord=np.inf) < tol:
            break

    return x

def thomas(A, d):
    n = len(d)

    a = np.diag(A, k=-1)
    a = np.insert(a, 0, 0)

    b = np.diag(A)

    c = np.diag(A, k=1)
    c = np.append(c, 0)

    cp = np.zeros(n, dtype='float64')
    dp = np.zeros(n, dtype='float64')
    x = np.zeros(n, dtype='float64')

    cp[0] = c[0] / b[0]
    dp[0] = d[0] / b[0]

    for i in np.arange(1, (n), 1):
        dnum = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / dnum
        dp[i] = (d[i] - a[i] * dp[i - 1]) / dnum

    x[(n-1)] = dp[(n-1)]

    for i in np.arange((n - 2), -1, -1):
        x[i] = (dp[i]) - (cp[i]) * (x[i+1])

    return (x)

def additional_info(A):
    eigenvalues = np.linalg.eigvals(A)
    print("Eigenvalues:", eigenvalues)

    norm = np.linalg.norm(A)
    print("Norm:", norm)

    cond = np.linalg.cond(A)
    print("Condition number:", cond)
