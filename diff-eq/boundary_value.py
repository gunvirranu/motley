
"""
Non-Linear Second-Order Boundary Value Problem Solver

By: Gunvir Ranu

- Solves `y'' = f(x, y, y')`, with y' being z
- Works on some closed interval, `[a, b]`
- Accepts Dirichlet boundry conditions such that
  `y(a) = alpha` and `y(b) = beta`
- Uses the secant method to refine the first derivative
  of y(x) at `a`
- Uses the more efficient scipy initial value problem
  ODE solver, `odeint` to make computation faster

"""

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt


def f(x, y, z):
    # return -y
    return 0.1*np.sqrt(1 + z**2)

# makes f useable with odeint
def g(w, t):
    return [w[1], f(t, w[0], w[1])]

a = 0
b = 10
alpha = 0
beta = 0

M = 100     # max number of iterations
N = 1000     # number of subintervals
t = np.linspace(a, b, N)  # x-axis values
tol = 1e-8   # tolerance

# guesses for first derivative at a
v1 = (beta - alpha) / (b - a)
v2 = 0
# values for estimated solutions at b
# first guess is solved for
b1 = odeint(g, [alpha, v2], t)[-1, 0]
b2 = 0

for k in range(M):

    if abs(b1 - beta) < tol:
        break

    w0 = [alpha, v1]
    sol = odeint(g, w0, t)

    b2 = b1
    b1 = sol[-1, 0]


    tmp = v1
    # Uses secant method to refine first derivative at a
    v1 = v1 - ((b1 - beta) * (v1 - v2)) / (b1 - b2)
    v2 = tmp


# v1 is final estimate for first derivative of y(x) at a
print(v1)
plt.plot(t, sol[:, 0])
plt.show()
