import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


a = 2

top = 30
left = 0
bottom = 90
right = 60

N = 60
M = 60
dx = a / N
dy = a / M
nx = N - 1
ny = M - 1


A = np.zeros((nx*ny, nx*ny))
for i in range(nx*ny):
    # itself
    A[i][i] = -2 * (dx**2 + dy**2)
    # right
    if (i+1) % ny != 0:
        A[i][i + 1] = dy**2
    # left
    if i % ny != 0:
        A[i][i - 1] = dy**2
    # up
    if i < nx*ny - nx:
        A[i][i + nx] = dx**2
    # down
    if i > nx - 1:
        A[i][i - nx] = dx**2

def f(x, y):
    return x+y

b = np.zeros((nx*ny, 1))
for i in range(nx*ny):
    # up
    if i+1 > nx*ny - nx:
        b[i] -= top * dx**2
    # left
    if i % ny == 0:
        b[i] -= left * dy**2
    # down
    if i < nx:
        b[i] -= bottom * dx**2
    # right
    if (i+1) % ny == 0:
        b[i] -= right * dy**2


u = np.linalg.solve(A, b)
u = np.flipud(u.reshape((ny, nx)))

u = np.insert(u, 0, top, axis=0)
u = np.insert(u, 0, left, axis=1)
u = np.insert(u, M, bottom, axis=0)
u = np.insert(u, N, right, axis=1)
u[0, 0] = (top + left) / 2
u[M, 0] = (left + bottom) / 2
u[M, N] = (bottom + right) / 2
u[0, N] = (right + top) / 2

print(u.size)

fig = plt.figure()
ax = fig.gca(projection='3d')

X = np.linspace(0, a, N+1)
Y = np.linspace(0, a, M+1)
X, Y = np.meshgrid(X, Y)

surf = ax.plot_surface(X, Y, u, cmap=cm.coolwarm, antialiased=False)
fig.colorbar(surf)
plt.show()
