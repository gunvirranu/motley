import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

#parameters
# R_born = 0.005
# PD_born = 0.005
# PRPD = 5e-6
# PDPR = 1

R_born = 0.005
PD_born = 0.01
prey_die = 5e-6
eff = 0.6

time = 2500
prey = [4000]
pred = [2000]

for i in range(time - 1):
    prey.append(prey[-1] + R_born*prey[-1] - prey_die*prey[-1]*pred[-1])
    pred.append(pred[-1] - PD_born*pred[-1] + eff*prey_die*prey[-2]*pred[-1])


# def f(w, t):
#     pr = R_born*w[0] - PRPD*w[0]*w[1]
#     pd = -PD_born*w[1] + PDPR*PRPD*w[0]*w[1]
#     return [pr, pd]


# t = np.linspace(0, time, 2500)
# w0 = [prey[0], pred[0]]

# x = odeint(f, w0, t)

# prey = x[:, 0]
# pred = x[:, 1]

plt.plot(prey, linewidth=3, label='prey')
plt.plot(pred, '--', linewidth=3, label='predator')
plt.legend()
plt.show()
