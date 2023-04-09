import numpy as np

def U(x, m):
    return x / m

def st(x, a, b, m):
    return a + U(x, m) * b

def tr(x, a, b, m):
    y = []
    for i in range(0, len(x)-1, 2):
        y.append(a + b * (U(x[i], m) + U(x[i+1], m) - 1))
    return np.array(y)

def ex(x, a, b, m):
    return a - b * np.log(U(x, m))

def nr(x, a, b, m):
    y = []
    for i in range(0, len(x)-1, 2):
        y.append(a + b * np.sqrt(-2 * np.log(1 - U(x[i], m))) * np.cos(2 * np.pi * U(x[i+1], m)))
        y.append(a + b * np.sqrt(-2 * np.log(1 - U(x[i], m))) * np.sin(2 * np.pi * U(x[i+1], m)))
    return np.array(y)

def ln(x, a, b, m):
    return a + np.exp(b - nr(x, 0, 1, m))

def ls(x, a, b, m):
    u = U(x, m)
    return a + b * np.log(u / (1 - u))

def factor(x):
    y = 1
    for i in range(x):
        y *= (i + 1)
    return y

def bi(x, a, b, m):
    y = []
    u = U(x, m)
    for i in u:
        s = 0
        k = 0
        while(True):
            s += (factor(b) / (factor(k) * factor(b - k)) * (a ** k) * ((1 - a) ** (b - k)))
            if s > i:
                y.append(k)
                break
            if k < b - 1:
                k += 1
                continue
            y.append(b)
    return np.array(y)

def gm(x, a, b, c, m):
    y = []
    u = U(x, m)
    if type(c) == type(1):
        for i in range(0, len(u), c):
            y.append(a - b  * np.log(np.prod(1 - u[i:i+c])))
    else:
        k = int(c - 0.5)
        for i in range(0, len(u), 2 * k + 2):
            z1, z2 = nr([x[i], x[i+1]], 0, 1, m)
            y.append(a + b * (z1 ** 2 / 2 - np.log(np.prod(1 - u[i+2:i+k+2]))))
            y.append(a + b * (z2 ** 2 / 2 - np.log(np.prod(1 - u[i+k+2:i+2*k+2]))))
    return np.array(y)

print(gm(np.array([510, 33, 290, 900, 171, 72, 124, 523]), 0, 0.5, 2, 1000))
print(gm(np.array([99, 59, 56, 59, 42, 86, 51, 94, 3, 92, 56, 69]), 0, 1, 1.5, 100))
print(gm(np.array([80, 79, 50, 9, 69, 67, 65, 30, 7, 68, 56, 60]), 1, 1.5, 0.5, 100))