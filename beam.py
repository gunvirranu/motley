import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_bvp

def load(x):
    return 0*x
    return 2**(-100*(x-0.5)**2)

def f(x, w):
    a, s, d, f = w
    return np.vstack((s, d, f, load(x)))

def bc(xa, xb):
    w0, e0, r0, t0 = xa
    w1, e1, r1, t1 = xb

    # simply supported
    # return [w0, w1, r0, r1]
    # cantilever
    # return [w0, e0, r1, t1]
    # left fixed, right pin
    # return [w0, e0, w1, r1]
    #
    return [w0, w1, r0, r1 - 3]

x = np.linspace(0, 1, 50)
w0 = np.zeros((4, x.size))
sol = solve_bvp(f, bc, x, w0)

plt.plot(x, load(x), label="Load")
plt.plot(x, sol.y[0], label="Deflection")
plt.plot(x, sol.y[1], label="Angle")
plt.plot(x, sol.y[2], label="Moment")
plt.plot(x, sol.y[3], label="Shear")
plt.legend(loc="best")
plt.show()

"""
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(x, load(x), 'r')
ax2.plot(x, -sol.y[0], 'g')
ax1.set_ylabel('Load [N]', color='r')
ax2.set_ylabel('Deflection [mm]', color='g')
ax2.set_xlabel('Beam [m]')
ax1.set_title('Beam Deflection lol')
plt.show()
"""
