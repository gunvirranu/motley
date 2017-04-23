import matplotlib.pyplot as plt
import numpy as np
from math import *

"""
    For first-order differential equations in the form:
    y' = f(t, y)
"""

def f(t, y):
    return 2*sin(3*t) + y/2


init = 1

r = 6
dt = 0.1

x = [init]
for i in range(int(r / dt)):
    t = dt * i
    x.append(x[-1] + dt*f(t, x[-1]))
plt.plot(x, label='Forward Euler')

x = [init]
for i in range(int(r / dt)):
    t = dt * i
    x.append(x[-1] + dt/2 * (f(t, x[-1]) + f(t+dt, (x[-1] + dt*f(t, x[-1])))))
plt.plot(x, label='Improved Euler')

x = [init]
for i in range(int(r / dt)):
    t = dt * i
    k1 = f(t, x[-1])
    k2 = f(t + dt/2, x[-1] + dt/2 * k1)
    k3 = f(t + dt/2, x[-1] + dt/2 * k2)
    k4 = f(t + dt, x[-1] + dt*k3)
    x.append(x[-1] + dt/6 * (k1 + 2*k2 + 2*k3 + k4))
plt.plot(x, label='RK4')

plt.legend()
plt.show()