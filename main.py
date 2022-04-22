from matplotlib import pyplot
import matplotlib.image as image
import numpy as np
import calculations as calc
from PIL import Image, ImageOps


def main():
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
    img = Image.open("test_4.bmp")
    gray_img = ImageOps.grayscale(img)
    gray_img_arr = np.asarray(gray_img)

    # przekształcenie zdjęcia do wektora trasy
    X_vect, Y_vect = calc.img_to_path(gray_img_arr)

    # dodanie zakłócen na trasie, dzięki czemu uzyskany zostanie
    noise_lvl = 2
    X_after_1st_ride, Y_after_1st_ride = calc.add_noise(X_vect, Y_vect, noise_lvl)

    # wygładzenie wektora z trasą
    X_vect_smoth, Y_vect_smoth = calc.smooth_path(X_vect, Y_vect, 10)

    # obliczenia lewych i prawych ograniczeń
    Xl, Yl = calc.left_edge(offset, X_vect_smoth, Y_vect_smoth)
    Xr, Yr = calc.right_edge(offset, X_vect_smoth, Y_vect_smoth)

    # wygładzenie ograniczeń prawo i lewo stronnych
    smoothness = 20
    Xr_smoth, Yr_smoth = calc.smooth_path(Xr, Yr, smoothness)
    Xl_smoth, Yl_smoth = calc.smooth_path(Xl, Yl, smoothness)

    print("bez smothingu:", len(Xl), "smothed:", len(Xl_smoth))

    pyplot.figure(1)
    pyplot.plot(X_after_1st_ride, Y_after_1st_ride)
    pyplot.plot(X_vect, Y_vect)
    # pyplot.plot(Xr_smoth, Yr_smoth)
    pyplot.xlim([0, 500])
    pyplot.ylim([300, 0])
    pyplot.legend(["pierwszy przejazd", "trasa odczytana"])
    pyplot.show()

    # pyplot.figure(1)
    # pyplot.plot(X_after_1st_ride, Y_after_1st_ride)
    # pyplot.plot(Xl_smoth, Yl_smoth)
    # pyplot.plot(Xr_smoth, Yr_smoth)
    # pyplot.xlim([0, 500])
    # pyplot.ylim([300, 0])
    # pyplot.legend(["droga", "lewa granica", "prawa granica"])
    # pyplot.show()


if __name__ == "__main__":
    main()