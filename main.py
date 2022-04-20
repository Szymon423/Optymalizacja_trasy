import matplotlib.pyplot as plt
import numpy as np
import calculations as calc
import photo_import as phi

length = 2000
offset = 250
X, Y = calc.generate_route(length)


dx = np.array([(X[i] - X[i-1]) for i in range(1, length)])
dy = np.array([(Y[i] - Y[i-1]) for i in range(1, length)])
T = (dx**2 + dy**2)**0.5
alfa = np.arctan2(dy, dx)
dalfa = np.array([(alfa[i] - alfa[i-1]) for i in range(1, length - 1)])

K = dalfa/T[0:-1]


Xl, Yl = calc.left_edge(offset, X, Y)
Xr, Yr = calc.right_edge(offset, X, Y)


plt.figure(1)
plt.plot(X, Y)
plt.plot(Xl, Yl)
plt.plot(Xr, Yr)
plt.xlim([0, length])
plt.ylim([-500, 500])

img = phi.get_img()




# plt.figure(2)
#
# plt.plot(K)
plt.show()
