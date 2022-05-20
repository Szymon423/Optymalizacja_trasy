import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from settings import Settings
from PIL import Image, ImageOps, ImageTk
from route_optimisation import RouteOptimisation


class GUI:
    """klasa odpowiedzialana za obsługę GUI"""

    def __init__(self):
        """inicjalizacja obiektu klasy GUI"""
        self.settings = Settings()

        # generacja przestrzeni GUI
        self.root = tk.Tk()
        self.root.title("Optymalizacja trasy robota typu linefollower")
        self.root.geometry("1000x600")

        self.RO = RouteOptimisation()

        # generacja przycisku do wyboru zdjęcia/trasy
        b_choice_route = tk.Button(self.root, text="load route",
                                   height=2, width=15, command=lambda: self._get_file_loc())
        b_choice_route.grid(row=0, column=0, padx=10, pady=10)

        combobo_options = ["GA with random mutation",
                                 "GA with linearization"]

        self.choice = ttk.Combobox(self.root, value=combobo_options)
        self.choice.current(0)
        self.choice.bind("<<ComboboxSelected>>", self._comboclick())


        self.root.mainloop()

    def _comboclick(self):
        """obsługa comboboxa"""
        self.choice = tk.Label(self.root, text=self.choice.get()).grid(row=0,
                                                                       column=1,
                                                                       padx=10,
                                                                       pady=10)


    def _get_file_loc(self):
        """obsługa przycisku z wyborem zdjęcia/trasy"""
        # wywołaniebsług iokna wczytwania plikó graficznych
        self.root.filename = filedialog.askopenfilename(
            initialdir=r"D:\Szymon\Projekty\Optymalizacja_trasy\Images",
            title="Select photo with route",
            filetypes=[("BMP files", "*.bmp")])
        # wyświetlenie ścieżki dotępu do pliku
        my_label1 = tk.Label(self.root, text=self.root.filename)
        my_label1.grid(row=2, column=1, padx=10, pady=10)

        # otworzenie pliku jako zdjęcie i pokazanie jako windows IMG
        self.settings.bmpfile = Image.open(self.root.filename)
        self.settings.bmpfile.show()

