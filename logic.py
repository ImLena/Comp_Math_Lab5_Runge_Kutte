import math
import numpy as np
import matplotlib.pyplot as plt

def Runge_Kutte(x0, y0, x1, h, t):
    k1 = k2 = k3 = k4 = 0
    y_vals = []
    while x0 <= x1:
        y0 += h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        k1 = get_function(x0, y0, t)
        k2 = get_function(x0 + h/2, y0 + h * k1 / 2, t)
        k3 = get_function(x0 + h/2, y0 + h * k2 / 2, t)
        k4 = get_function(x0 + h, y0 + h * k3, t)
        x0 += h
        y_vals.append(y0)
    return y0, y_vals


def get_function(x, y, t):
    try:
        if t == 1:
            return math.pow(x, 2) - 2 * y
        if t == 2:
            return -5 * math.log(x, math.e)
        if t == 3:
            return -2 * x * y
    except ValueError:
        return 0


def get_graph(x0, x1, y_vals):
    x = np.linspace(int(x0), int(x1), len(y_vals))
    plt.scatter(x, y_vals)
    x_new = np.linspace(int(x0), int(x1), 200)
    index = x.searchsorted(x_new)
    plt.plot(x_new, cubic_spline(index, x_new, x, y_vals), color="g")
    #y_vals = list(get_function_by_x(x00, t) for x00 in x_new)

    # f1 = np.linspace(x0, x1, int((x1-x0)/h))
    # f2 = list(np.sqrt(2 * i) for i in f1)
    # xx, yy = f1, f2
    # f1 = np.linspace(x0, x1, int((x1-x0)/h))
    # f2 = list(np.power(i, 2) / 2 for i in f1)
    # xxx, yyy = f1, f2
    # plt.plot(xx, yy, color="r", linewidth=2)
    # plt.plot(xxx, yyy, color="y", linewidth=2)


    #plt.plot(x_new, y_vals)
    plt.show()


def cubic_spline(index, x0, x, y):
    x = np.asfarray(x)
    y = np.asfarray(y)

    if np.any(np.diff(x) < 0):
        indexes = np.argsort(x)
        x = x[indexes]
        y = y[indexes]

    size = len(x)

    xdiff = np.diff(x)
    ydiff = np.diff(y)

    A = np.empty(size)
    A_1 = np.empty(size-1)
    s = np.empty(size)

    A[0] = math.sqrt(2*xdiff[0])
    A_1[0] = 0.0
    B0 = 0.0
    s[0] = B0 / A[0]

    for i in range(1, size-1):
        A_1[i] = xdiff[i-1] / A[i-1]
        A[i] = math.sqrt(2*(xdiff[i-1]+xdiff[i]) - A_1[i-1] * A_1[i-1])
        Bi = 6*(ydiff[i]/xdiff[i] - ydiff[i-1]/xdiff[i-1])
        s[i] = (Bi - A_1[i-1]*s[i-1])/A[i]

    i = size - 1
    A_1[i-1] = xdiff[-1] / A[i-1]
    A[i] = math.sqrt(2*xdiff[-1] - A_1[i-1] * A_1[i-1])
    Bi = 0.0
    s[i] = (Bi - A_1[i-1]*s[i-1])/A[i]

    i = size-1
    s[i] = s[i] / A[i]
    for i in range(size-2, -1, -1):
        s[i] = (s[i] - A_1[i-1]*s[i+1])/A[i]

    np.clip(index, 1, size-1, index)

    xi1, xi0 = x[index], x[index-1]
    yi1, yi0 = y[index], y[index-1]
    si1, si0 = s[index], s[index-1]
    hi1 = xi1 - xi0

    f0 = si0/(6*hi1)*(xi1-x0)**3 + \
         si1/(6*hi1)*(x0-xi0)**3 + \
         (yi1/hi1 - si1*hi1/6)*(x0-xi0) + \
         (yi0/hi1 - si0*hi1/6)*(xi1-x0)
    return f0
