from matplotlib import pyplot
import numpy as np
import calculations as calc
from PIL import Image, ImageOps, ImageTk
import algorithms as mGA
from gui import GUI
import tkinter as tk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


def main():

    dupa = GUI()

    # import zdjęcia
    img = Image.open("Images/test_3.bmp")
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

    # obliczenie wskaźnika do minimalizacji
    H = calc.H_matrix(Xl_smoth, Yl_smoth, Xr_smoth, Yr_smoth)
    B = calc.B_matrix(Xl_smoth, Yl_smoth, Xr_smoth, Yr_smoth)
    alfa = np.full(len(B), 0.5)

    # obliczenie NIEoptymalej trasy na podstawie ustalonego alfa
    X_not_opt, Y_not_opt = calc.x_and_y_from_alfa(alfa, Xl_smoth, Yl_smoth, Xr_smoth, Yr_smoth)

    # obliczenia dla znaleznienia alfa określającego krótsze krawędzie
    strength = 0.4
    alfa_whats_shorter = calc.find_shortest_edges(Xl_smoth, Yl_smoth, Xr_smoth, Yr_smoth, strength)

    X_maybe_, Y_maybe_ = calc.x_and_y_from_alfa(alfa_whats_shorter, Xl_smoth, Yl_smoth, Xr_smoth, Yr_smoth)

    # # wyświetlenie podziału na dłuższe i krótsze krawędzie
    # pyplot.figure(9)
    # pyplot.plot(X_maybe_, Y_maybe_)
    # pyplot.plot(Xl_smoth, Yl_smoth)
    # pyplot.plot(Xr_smoth, Yr_smoth)
    # pyplot.xlim([0, gray_img_arr.shape[1]])
    # pyplot.ylim([gray_img_arr.shape[0], 0])
    # pyplot.show()

    # realizacja algorytmyu genetycznego

    population_size = 100
    epochs = 1
    min_fit = 1500
    optim_alfa = mGA.genetic_optimization(alfa,
                                          Xl_smoth, Yl_smoth,
                                          Xr_smoth, Yr_smoth,
                                          population_size,
                                          epochs,
                                          min_fit,
                                          alfa_whats_shorter)

    # obliczenie optymalej trasy na podstawie optymalnego alfa
    X_opt, Y_opt = calc.x_and_y_from_alfa(optim_alfa, Xl_smoth, Yl_smoth, Xr_smoth, Yr_smoth)
    # optim_alfa
    # wyświetlenie trasy pokonanej przez robota oraz obliczonych ograniczń obustronnych
    # pyplot.figure(4)

    # pyplot.plot(X_not_opt, Y_not_opt)
    # pyplot.plot(Xl_smoth, Yl_smoth)
    # pyplot.plot(Xr_smoth, Yr_smoth)
    # pyplot.plot(X_opt, Y_opt)
    # pyplot.xlim([0, gray_img_arr.shape[1]])
    # pyplot.ylim([gray_img_arr.shape[0], 0])
    # # pyplot.legend(["najkrótsza trasa", "bez optymalizacji","lewa granica", "prawa granica"])

    # obliczenie długości lewego i prawego ograniczenia oraz optymalnej trasy
    alfa_all_left = np.full_like(Xl_smoth, 1)
    alfa_all_right = np.full_like(Xl_smoth, 0)

    X_l, Y_l = calc.x_and_y_from_alfa(alfa_all_left, Xl_smoth, Yl_smoth, Xr_smoth, Yr_smoth)
    S2_l = calc.length_of_route(X_l, Y_l)

    X_r, Y_r = calc.x_and_y_from_alfa(alfa_all_right, Xl_smoth, Yl_smoth, Xr_smoth, Yr_smoth)
    S2_r = calc.length_of_route(X_r, Y_r)

    S2_opt = calc.length_of_route(X_opt, Y_opt)

    print("s2_l:", S2_l, "s2_r:", S2_r,  "s2_opt:", S2_opt)


    # realizacja algorytmyu genetycznego
    population_size = 2000
    epochs = 100
    min_fit = 1200
    linear_alfa = mGA.genetic_optimization_with_linearization(alfa,
                                                            Xl_smoth, Yl_smoth,
                                                            Xr_smoth, Yr_smoth,
                                                            population_size,
                                                            epochs,
                                                            min_fit,
                                                            alfa_whats_shorter)

    X_linear, Y_linear = calc.x_and_y_from_alfa(linear_alfa, Xl_smoth, Yl_smoth, Xr_smoth, Yr_smoth)
    S2_opt_linear = calc.length_of_route(X_linear, Y_linear)
    print("s2_l:", S2_l, "s2_r:", S2_r,  "s2_opt:", S2_opt_linear)

    pyplot.plot(Xl_smoth, Yl_smoth)
    pyplot.plot(Xr_smoth, Yr_smoth)
    pyplot.plot(X_linear, Y_linear)
    pyplot.xlim([0, gray_img_arr.shape[1]])
    pyplot.ylim([gray_img_arr.shape[0], 0])
    pyplot.legend(["prawa granica", "lewa granica", "najkrótsza trasa"])
    pyplot.show()




if __name__ == "__main__":
    main()