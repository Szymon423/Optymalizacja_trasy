from matplotlib import pyplot
import matplotlib.image as image
import numpy as np
import calculations as calc
from PIL import Image, ImageOps


def main():
    # import zdjęcia
    img = Image.open("test_4.bmp")
    gray_img = ImageOps.grayscale(img)
    gray_img_arr = np.asarray(gray_img)

    # przekształcenie zdjęcia do wektora trasy
    X_vect, Y_vect = calc.img_to_path(gray_img_arr)

    # dodanie zakłócen na trasie, dzięki czemu uzyskana zostanie trasa imitująca drogę jaką odczytał robot przy pierwszym przejeździe
    noise_lvl = 2
    X_after_1st_ride, Y_after_1st_ride = calc.add_noise(X_vect, Y_vect, noise_lvl)

    # wygładzenie wektora z trasą
    X_vect_smoth, Y_vect_smoth = calc.smooth_path(X_after_1st_ride, Y_after_1st_ride, 10)

    # obliczenia lewych i prawych ograniczeń
    offset = 10
    Xl, Yl = calc.left_edge(offset, X_vect_smoth, Y_vect_smoth)
    Xr, Yr = calc.right_edge(offset, X_vect_smoth, Y_vect_smoth)

    # wygładzenie ograniczeń prawo i lewo stronnych
    smoothness = 20
    Xr_smoth, Yr_smoth = calc.smooth_path(Xr, Yr, smoothness)
    Xl_smoth, Yl_smoth = calc.smooth_path(Xl, Yl, smoothness)

    # obliczenia krzywizny trasy przez wygładzaniem oraz po wygładzeniu
    K_before_smoothing = calc.calculate_curvature(X_after_1st_ride, Y_after_1st_ride)
    K_after_smoothing = calc.calculate_curvature(X_vect_smoth, Y_vect_smoth)

    # wykreślenie krzywizn przed i po wygładzaniu
    pyplot.figure(1)
    pyplot.plot(K_before_smoothing)
    pyplot.plot(K_after_smoothing)
    # pyplot.xlim([0, 500])
    # pyplot.ylim([300, 0])
    pyplot.legend(["Krzywizna przed wygładzeniem", "Krzywizna po wygładzeniu"])

    # wyświetlenie trasy pokonanej przez robota oraz obliczonych ograniczń obustronnych
    pyplot.figure(2)
    pyplot.plot(X_after_1st_ride, Y_after_1st_ride)
    pyplot.plot(Xl_smoth, Yl_smoth)
    pyplot.plot(Xr_smoth, Yr_smoth)
    pyplot.xlim([0, 500])
    pyplot.ylim([300, 0])
    pyplot.legend(["droga po 1 przejeździe", "lewa granica", "prawa granica"])
    pyplot.show()


if __name__ == "__main__":
    main()