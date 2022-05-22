from PIL import Image, ImageOps, ImageTk
import numpy as np


class Data:
    """klasa odpowiedzialana za realizcję obsługę optymalizacji"""

    def __init__(self):
        """inicjalizacja obiektu klasy"""
        # plik BMP
        self.bmpfile = Image.open("Images/test_3.bmp")

        # RGB -> gray scale
        self.gray_img = ImageOps.grayscale(self.bmpfile)

        # docelowa macierz liczbowa
        self.gray_img_arr = np.asarray(self.gray_img)

        # zmienna przechowująca najlepszą alfę
        self.alfa = np.zeros(10)

    def convert_bmp_to_arr(self):
        """zamniana zdjęcia na macierz"""
        self.gray_img = ImageOps.grayscale(self.bmpfile)
        self.gray_img_arr = np.asarray(self.gray_img)