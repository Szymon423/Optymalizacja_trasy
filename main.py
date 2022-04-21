from matplotlib import pyplot
import matplotlib.image as image
import numpy as np
import calculations as calc
from PIL import Image, ImageOps

length = 2000
offset = 10
X, Y = calc.generate_route(length)


dx = np.array([(X[i] - X[i-1]) for i in range(1, length)])
dy = np.array([(Y[i] - Y[i-1]) for i in range(1, length)])
T = (dx**2 + dy**2)**0.5
alfa = np.arctan2(dy, dx)
dalfa = np.array([(alfa[i] - alfa[i-1]) for i in range(1, length - 1)])

K = dalfa/T[0:-1]
# import zdjęcia
img = Image.open("test_3.bmp")
gray_img = ImageOps.grayscale(img)
gray_img_arr = np.asarray(gray_img)

# przekształcenie zdjęcia do wektora trasy
X_vect, Y_vect = calc.img_to_path(gray_img_arr)

# obliczenia lewych i prawych ograniczeń
Xl, Yl = calc.left_edge(offset, X_vect, Y_vect)
Xr, Yr = calc.right_edge(offset, X_vect, Y_vect)


pyplot.figure(1)
pyplot.plot(X_vect, Y_vect)
pyplot.plot(Xl, Yl)
pyplot.plot(Xr, Yr)
pyplot.xlim([0, 500])
pyplot.ylim([0, 300])
pyplot.show()


