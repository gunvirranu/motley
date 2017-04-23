import matplotlib.pyplot as plt
import numpy as np
from math import *

w = None

def f(t, y, z):
    return z

def g(t, y, z):
    # return -y
    return -sin(y)
    # return -sin(y) - 0.25*z
    # return -sin(y) - 7*z
    # return -sin(y) - 1.7*z
    # return -sin(y) + 0.25*cos(w*t) - 0.0*z
    # return -y + cos(t * 0.9)


trange = 50
dt = 0.05
N = int(trange / dt)

y_init = 3.14
# y_init = 1
z_init = 0

y = [0] * N
z = [0] * N
y[0] = y_init
z[0] = z_init

for i in range(1, N):
    t = i * dt

    k1 = dt * f(t, y[i-1], z[i-1])
    l1 = dt * g(t, y[i-1], z[i-1])
    k2 = dt * f(t + dt/2, y[i-1] + k1/2, z[i-1] + l1/2)
    l2 = dt * g(t + dt/2, y[i-1] + k1/2, z[i-1] + l1/2)
    k3 = dt * f(t + dt/2, y[i-1] + k2/2, z[i-1] + l2/2)
    l3 = dt * g(t + dt/2, y[i-1] + k2/2, z[i-1] + l2/2)
    k4 = dt * f(t + dt, y[i-1] + k3, z[i-1] + l3)
    l4 = dt * g(t + dt, y[i-1] + k3, z[i-1] + l3)

    y[i] = y[i-1] + 1/6 * (k1 + 2*k2 + 2*k3 + k4)
    z[i] = z[i-1] + 1/6 * (l1 + 2*l2 + 2*l3 + l4)

plt.plot(np.arange(0, trange, dt), y, label='Coupled RK')
plt.plot(np.arange(0, trange, dt), z, label='Velocity')
# plt.plot(y, z, label='Phase Plot')
plt.legend()
plt.show()

import tkinter

root = tkinter.Tk()
canvas = tkinter.Canvas(root, width=600, height=600)
canvas.pack()

angle = y
i = 0

canvas.create_oval(295, 295, 305, 305, fill='black')
line = canvas.create_line(300, 300, 300, 300, width=3)
ball = canvas.create_oval(300, 300, 300, 300, fill='black')
if w is not None: driver = canvas.create_line(300, 300, 300, 300)
else: driver = None

def update():

    global i
    global angle
    global line
    global circle
    global driver

    x = 300 + 200 * sin(angle[i])
    y = 300 + 200 * cos(angle[i])

    canvas.coords(line, 300, 300, x, y)
    rad = 14
    canvas.coords(ball, x-rad, y-rad, x+rad, y+rad)
    if driver:
        canvas.coords(driver, 300, 300, 300 + 200*cos(w*i*dt), 300)

    if i < N-1:
        i += 1
    else:
        i = 0

    root.after(20, update)

root.after(100, update)
root.mainloop()
