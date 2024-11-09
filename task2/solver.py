def Lagrange(o, x, y):
    sum = 0;
    n = len(x)

    for i in range(n):
        prod = y[i]

        for j in range(n):
            if i != j:
                prod = prod * (o - x[j])/(x[i] - x[j])

        sum = sum + prod

    return sum

def grad(a, b, x, y):
    if a==0: return y[b]
    return (grad(a-1, b, x, y)-grad(a-1, a-1, x, y))/(x[b]-x[a-1])

def Newton(o, x, y):
    yres = 0

    for p in range(len(x)):
        prodres = grad(p, p, x, y)

        for q in range(p):
            prodres *= (o-x[q])
        
        yres += prodres
    
    return yres
