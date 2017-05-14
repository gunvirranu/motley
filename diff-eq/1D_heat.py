import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

left = 10
right = 50

N = 200
frames = 5000

dx = 10 / N
dt = 5 / frames
c = dt / dx**2

x = np.linspace(0, 10, N)
u = np.zeros((frames, N))

# Initial distribution
u[0] = 100 * np.random.rand(N)
# u[0] = 25*np.sin(x) + 10*np.sin(8*x)+ 40
u[:, 0] = left
u[:, -1] = right

for i in range(1, frames):
    for n in range(1, N-1):
        u[i, n] = u[i-1, n] + c * (u[i-1, n-1] - 2*u[i-1, n] + u[i-1, n+1])

fig = plt.figure()
ax = plt.axes(xlim=(0, 10), ylim=(0, 100))
line, = ax.plot([], [], lw=2)

def init():
    line.set_data([], [])
    return line,

def animate(i):
    line.set_data(x, u[i])
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=frames, interval=40)
plt.show()
