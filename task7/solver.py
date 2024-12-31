import numpy as np

#u0(n,j-1), u1(n-1,j), u2(n+1,j)
def cross(h, a, t, u0, u1, u2):
    return u0 - (a*t) / h * (u2 - u1)

#u0(n,j), u1(n,j-1)
def rCorner(h, a, t, u0, u1):
    return u0 - a*t/h * (u0 - u1)

#u0(n,j), u1(n,j+1)
def lCorner(h, a, t, u0, u1):
    return u0 - a*t/h * (u1 - u0)

def ufun(x, t):
    x = x - t
    if x < 0:
        return 1
    elif x >= 0:
        return 0
    else:
        return 0

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

def resCross(h, a, t, u, n, end = -1):
    res = []
    tempRes = []

    print("h: ", h, "a: ", a, "t: ", t);
    cfl = a*t/h
    print("cfl: ", cfl)

    res.append(u)
    tempRes.append(lCorner(h, a, t, u[0], u[1]))

    for i in range(1, len(u)):
        tempRes.append(rCorner(h, a, t, u[i-1], u[i]))

    res.append(tempRes)

    if end == -1:
        border = n
    else:
        border = end+1

    while len(res) < border:
        tempRes = []
        
        tempRes.append(res[-1][0])
        #tempRes.append(lCorner(h, a, t, res[-1][0], res[-1][1]))

        for i in range(1, len(res[-1])-1):
            tempRes.append(cross(h, a, t, res[-2][i], res[-1][i-1], res[-1][i+1]))

        #tempRes.append(res[-1][-1])
        tempRes.append(rCorner(h, a, t, res[-1][-2], res[-1][-1]))

        res.append(tempRes)

    return res

def implicit(h, a, t, u, n, end = -1, xend = -1):
    res = []
    tempRes = []

    print("h: ", h, "a: ", a, "t: ", t);
    cfl = a*t/h
    print("cfl: ", cfl)

    matrix = []
    m_part = []
    vector = []

    res.append(u)

    count = len(u)
    
    if end == -1:
        border = n
    else:
        border = end+1

    m_part.append(1)
    m_part.append(a*t/(2*h))
    for i in range(2, count-2):
        m_part.append(0)
    matrix.append(m_part)
    m_part = []

    for i in range(1, count-3):
        for _ in range(0, i-1):
            m_part.append(0)
        m_part.append(-a*t/(2*h))
        m_part.append(1)
        m_part.append(a*t/(2*h))
        for _ in range(i+2, count-2):
            m_part.append(0)
        matrix.append(m_part)
        m_part = []

    for i in range(0, count-4):
        m_part.append(0)
    m_part.append(-a*t/(2*h))
    m_part.append(1)
    matrix.append(m_part)
    m_part = []

    while len(res) < border:
        for i in range(1, count-1):
            vector.append(res[-1][i])

        vector[0] = vector[0] + t/(2*h)
        
        #tempRes = thomas(matrix, vector)
        tempRes = np.linalg.solve(matrix, vector)

        tempRes = np.insert(tempRes, 0, ufun(0, t))
        #tempRes[-1] = rCorner(h, a, t, res[-1][-2], res[-1][-1])
        #tempRes[-1] = res[-1][-1]
        #tempRes[0] = res[-1][0]
        tempRes = np.append(tempRes, 0)
        
        res.append(tempRes)
        
        vector = []

    return res

def error(res, oldRes1, oldRes2):
    return np.log2(np.abs(res - oldRes1) / np.abs(res - oldRes2))