from matplotlib import pyplot
import matplotlib.image as image
import numpy as np
import calculations as calc
from PIL import Image, ImageOps

length = 2000
offset = 50
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

print(gray_img.size)

X_vect = np.array([0])
Y_vect = np.array([], dtype=int)

gray_img_arr = np.asarray(gray_img)
coll_0 = gray_img_arr[:, 0]
a = np.where(coll_0 == 0)
print(a[0][0])
Y_vect = np.append(Y_vect,a[0][0])
print(X_vect)
print(Y_vect)

gray_img_arr_clean = gray_img_arr.copy()

go_on = True

while go_on:




# np.append(X_vect, x)



pyplot.show()
