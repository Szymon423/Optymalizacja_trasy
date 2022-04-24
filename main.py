from matplotlib import pyplot
import numpy as np
import calculations as calc
from PIL import Image, ImageOps
from genetic_algoritm import genetic_optimization


def main():
    # import zdjęcia
    img = Image.open("test_3.bmp")
    gray_img = ImageOps.grayscale(img)
    gray_img_arr = np.asarray(gray_img)

    # przekształcenie zdjęcia do wektora trasy
    X_vect, Y_vect = calc.img_to_path(gray_img_arr)

    # dodanie zakłócen na trasie, dzięki czemu uzyskana zostanie trasa imitująca drogę jaką odczytał robot przy pierwszym przejeździe
    noise_lvl = 0
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
    # K_before_smoothing = calc.calculate_curvature(X_after_1st_ride, Y_after_1st_ride)
    # K_after_smoothing = calc.calculate_curvature(X_vect_smoth, Y_vect_smoth)

    # wykreślenie krzywizn przed i po wygładzaniu
    # pyplot.figure(1)
    # pyplot.plot(K_before_smoothing)
    # pyplot.plot(K_after_smoothing)
    # pyplot.xlim([0, gray_img_arr.shape[1]])
    # pyplot.ylim([gray_img_arr.shape[0], 0])
    # pyplot.legend(["Krzywizna przed wygładzeniem", "Krzywizna po wygładzeniu"])

    # wyświetlenie trasy pokonanej przez robota oraz obliczonych ograniczń obustronnych
    # pyplot.figure(2)
    # pyplot.plot(X_after_1st_ride, Y_after_1st_ride)
    # pyplot.plot(Xl_smoth, Yl_smoth)
    # pyplot.plot(Xr_smoth, Yr_smoth)
    # pyplot.xlim([0, gray_img_arr.shape[1]])
    # pyplot.ylim([gray_img_arr.shape[0], 0])
    # pyplot.legend(["droga po 1 przejeździe", "lewa granica", "prawa granica"])
    # pyplot.show()


    # print("X_vect_smoth:", len(X_vect_smoth), "Y_vect_smoth:", len(Y_vect_smoth))
    # print("Xl_smoth:", len(Xl_smoth), "Yl_smoth:", len(Yl_smoth))
    # print("Xr_smoth:", len(Xr_smoth), "Yr_smoth:", len(Yr_smoth))

    # obliczenie wskaźnika do minimalizacji
    H = calc.H_matrix(Xl_smoth, Yl_smoth, Xr_smoth, Yr_smoth)
    B = calc.B_matrix(Xl_smoth, Yl_smoth, Xr_smoth, Yr_smoth)
    alfa = np.full(len(B), 0.5)

    # wyznaczenie optymalnej wartości alfa
    population_size = 1000
    epochs = 100
    min_err = 5
    catcher = np.asarray(genetic_optimization(alfa, H, B, population_size, epochs, min_err), dtype=object)
    optim_alfa = np.asarray(catcher[1])

    X_not_opt, Y_not_opt = calc.x_and_y_from_alfa(alfa, Xl_smoth, Yl_smoth, Xr_smoth, Yr_smoth)

    # obliczenie optymalej trasy na podstawie optymalnego alfa
    X_opt, Y_opt = calc.x_and_y_from_alfa(optim_alfa, Xl_smoth, Yl_smoth, Xr_smoth, Yr_smoth)


    # print("Pierwsze 50 elementów macierzy alfa:", optim_alfa[:50])

    # wyświetlenie trasy pokonanej przez robota oraz obliczonych ograniczń obustronnych
    pyplot.figure(3)
    pyplot.plot(X_opt, Y_opt)
    pyplot.plot(X_not_opt, Y_not_opt)
    pyplot.plot(Xl_smoth, Yl_smoth)
    pyplot.plot(Xr_smoth, Yr_smoth)
    pyplot.xlim([0, gray_img_arr.shape[1]])
    pyplot.ylim([gray_img_arr.shape[0], 0])
    pyplot.legend(["najkrótsza trasa", "bez optymalizacji","lewa granica", "prawa granica"])

    # obliczenie długości lewego i prawego ograniczenia
    n = Xr_smoth
    S2_l = 0
    S2_r = 0
    for i in range(1, len(n)):
        S2_l += (Xl_smoth[i] - Xl_smoth[i-1]) ** 2 + (Yl_smoth[i] - Yl_smoth[i-1]) ** 2
        S2_r += (Xr_smoth[i] - Xr_smoth[i-1]) ** 2 + (Yr_smoth[i] - Yr_smoth[i-1]) ** 2
    print("s2_l:", S2_l, "s2_r:", S2_r)

    # dupa = Xl_smoth - Xr_smoth
    # pyplot.figure(4)
    # pyplot.plot(dupa)
    pyplot.show()


if __name__ == "__main__":
    main()