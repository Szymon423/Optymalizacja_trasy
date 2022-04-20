from matplotlib import pyplot
import matplotlib.image as image
import numpy as np
import calculations as calc
from PIL import Image, ImageOps

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


pyplot.figure(1)
pyplot.plot(X, Y)
pyplot.plot(Xl, Yl)
pyplot.plot(Xr, Yr)
pyplot.xlim([0, length])
pyplot.ylim([-500, 500])

img = Image.open("test_1.jpg")

gray_img = ImageOps.grayscale(img)

d = np.asarray(gray_img)


X_vect = np.array([])
Y_vect = np.array([])

for x,y in d:
    if d[y, x] == 0:
        np.append(X_vect, x)
        np.append(Y_vect, y)

print(d.shape[1])

pyplot.show()
