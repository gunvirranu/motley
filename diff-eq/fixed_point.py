import matplotlib.pyplot as plt
import numpy as np

scale = 100
data = []

for c in range(int(-2*scale), int(0.25*scale)):
    c = c / scale

    its = [0]

    for i in range(200):
        its.append(its[-1]**2 + c)

    data.append(its[101:])

data = np.array(data)

# Bifurcation
plt.plot(data)
# Other graph from sheet
# plt.imshow(np.rot90(data),interpolation='nearest', aspect='auto')
plt.show()
