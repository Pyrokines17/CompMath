import numpy as np

def newton_zero(f, fp, x0, max_iter=10000, tol=1e-10):
    results = []
    x = x0

    for _ in range(max_iter):
        x1 = x

        x = x - f(x) / fp(x)
        results.append(x)

        if np.abs(x - x1) < tol:
            return results
        
    return None

def secant_zero(f, p0, p1, max_iter=10000, tol=1e-10):
    results = []
    q0 = f(p0)
    q1 = f(p1)

    for _ in range(max_iter):
        p = p1 - q1 * (p1 - p0) / (q1 - q0)
        results.append(p)

        if np.abs(p - p1) < tol:
            return results

        p0 = p1
        q0 = q1
        p1 = p
        q1 = f(p)

    return None
