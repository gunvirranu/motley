import matplotlib.pyplot as plt
import numpy as np


rsteps = 100000
r, step = np.linspace(1, 4, rsteps, retstep=True)
# r, step = np.linspace(3.55, 4, rsteps, retstep=True)

b = np.zeros((rsteps, 499))

b[:, 0] = 0.5
for i in range(1, 499):
    b[:, i] = r * b[:, i-1] * (1 - b[:, i-1])


# db = np.gradient(b, step)[0]
# plt.plot(r, db, ',', color='0.3')

plt.plot(r, b, ',', color='0.3')
plt.show()