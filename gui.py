import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from data import Data
from PIL import Image, ImageOps, ImageTk
from route_optimisation import RouteOptimisation
import algorithms as mGA
import calculations as calc
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


class GUI:
    """klasa odpowiedzialana za obsługę GUI"""

    def __init__(self):
        """inicjalizacja obiektu klasy GUI"""
        self.dane = Data()
        self.start_algorithm = False
        # generacja przestrzeni GUI
        self.root = tk.Tk()
        self.root.title("Optymalizacja trasy robota typu linefollower")
        self.root.geometry("1200x800")
        self.root.configure(bg='white')

        self.RO = RouteOptimisation()

        self.Xl = np.zeros(10)
        self.Xr = np.zeros(10)
        self.Yl = np.zeros(10)
        self.Yr = np.zeros(10)
        self.Xopt = np.zeros(10)
        self.alfa = np.zeros(10)
        self.X = np.zeros(10)
        self.Y = np.zeros(10)

        # generacja przycisku do wyboru zdjęcia/trasy
        b_choice_route = tk.Button(self.root, text="load route",
                                   height=2, width=20, command=lambda: self._get_file_loc())
        b_choice_route.grid(row=0, column=0, padx=10, pady=10)

        # generacja przycisku do STARTU
        b_start = tk.Button(self.root, text="START",
                                   height=2, width=20, command=lambda: self._start_algorith())
        b_start.grid(row=2, column=0, padx=10, pady=10)

        combobo_options = ["random mutation", "linearization"]

        self.choice = ttk.Combobox(self.root, value=combobo_options, height=5, width=20)
        self.choice.grid(row=1, column=0, padx=10, pady=10)
        # self.choice.current(0)
        # self.choice.bind("<<ComboboxSelected>>", self._comboclick())

        self.root.mainloop()

    def _comboclick(self):
        """obsługa comboboxa"""
        self.choice = tk.Label(self.root, text=self.choice.get()).grid(row=0, column=1, padx=10, pady=10)

    def _get_file_loc(self):
        """obsługa przycisku z wyborem zdjęcia/trasy"""
        # wywołaniebsług iokna wczytwania plikó graficznych
        self.root.filename = filedialog.askopenfilename(
            initialdir=r"D:\Szymon\Projekty\Optymalizacja_trasy\Images",
            title="Select photo with route",
            filetypes=[("BMP files", "*.bmp")])
        # wyświetlenie ścieżki dotępu do pliku
        my_label1 = tk.Label(self.root, text=self.root.filename)
        my_label1.grid(row=1, column=1, padx=10, pady=10)

        # otworzenie pliku jako zdjęcie i pokazanie jako windows IMG
        self.dane.bmpfile = Image.open(self.root.filename)
        self.dane.convert_bmp_to_arr()
        # self.dane.bmpfile.show()

    def _start_algorith(self):
        """rozpoczęcie algorytmu"""
        self.start_algorithm = True
        print("START")
        self.run_algorithm()

    def run_algorithm(self):
        # obsługa algorytmu genetycznego
        if self.start_algorithm:
            # przekształcenie zdjęcia do wektora trasy
            X_vect, Y_vect = calc.img_to_path(self.dane.gray_img_arr)

            # dodanie zakłócen na trasie, dzięki czemu uzyskana zostanie trasa imitująca drogę jaką odczytał robot przy pierwszym przejeździe
            noise_lvl = 0
            X_after_1st_ride, Y_after_1st_ride = calc.add_noise(X_vect, Y_vect, noise_lvl)

            # wygładzenie wektora z trasą
            X_vect_smoth, Y_vect_smoth = calc.smooth_path(X_after_1st_ride, Y_after_1st_ride, 10)

            # obliczenia lewych i prawych ograniczeń
            offset = 10
            Xl, Yl = calc.left_edge(offset, X_vect_smoth, Y_vect_smoth)
            Xr, Yr = calc.right_edge(offset, X_vect_smoth, Y_vect_smoth)

            # self.Xl, self.Yl = Xl, Yl
            # self.Xr, self.Yr = Xr, Yr

            # wygładzenie ograniczeń prawo i lewo stronnych
            smoothness = 20
            Xr_smoth, Yr_smoth = calc.smooth_path(Xr, Yr, smoothness)
            Xl_smoth, Yl_smoth = calc.smooth_path(Xl, Yl, smoothness)

            self.Xl, self.Yl = Xl_smoth, Yl_smoth
            self.Xr, self.Yr = Xr_smoth, Yr_smoth

            B = calc.B_matrix(Xl_smoth, Yl_smoth, Xr_smoth, Yr_smoth)
            alfa = np.full(len(B), 0.5)

            # obliczenia dla znaleznienia alfa określającego krótsze krawędzie
            strength = 0.4
            alfa_whats_shorter = calc.find_shortest_edges(Xl_smoth, Yl_smoth, Xr_smoth, Yr_smoth, strength)

            if self.choice.get() == "random mutation":
                # realizacja algorytmyu genetycznego
                population_size = 100
                epochs = 100
                min_fit = 1500
                optim_alfa = mGA.genetic_optimization(self,
                                                      alfa,
                                                      Xl_smoth, Yl_smoth,
                                                      Xr_smoth, Yr_smoth,
                                                      population_size,
                                                      epochs,
                                                      min_fit,
                                                      alfa_whats_shorter)
            elif self.choice.get() == "linearization":
                # realizacja algorytmyu genetycznego z linearyzacją
                population_size = 500
                epochs = 25
                min_fit = 120
                linear_alfa = mGA.genetic_optimization_with_linearization(self,
                                                                          alfa,
                                                                          Xl_smoth, Yl_smoth,
                                                                          Xr_smoth, Yr_smoth,
                                                                          population_size,
                                                                          epochs,
                                                                          min_fit,
                                                                          alfa_whats_shorter)

    def _plot(self):
        # the figure that will contain the plot
        fig = Figure(figsize=(10, 6), dpi=100)

        # dane do wykresu
        self.X, self.Y = calc.x_and_y_from_alfa(self.alfa, self.Xl, self.Yl, self.Xr, self.Yr)

        # adding the subplot
        plot1 = fig.add_subplot(111)

        # plotting the graph
        plot1.plot(self.X, self.Y)
        plot1.plot(self.Xl, self.Yl)
        plot1.plot(self.Xr, self.Yr)
        plot1.set_xlim([0, self.dane.gray_img_arr.shape[1]])
        plot1.set_ylim([self.dane.gray_img_arr.shape[0], 0])

        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().grid(row=3, column=1, columnspan=2, padx=10, pady=10)





