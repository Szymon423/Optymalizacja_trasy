import numpy as np


# obliczenia dla krawędzi lewostronnej zgodne z wzorami z pracy mgr
def left_edge(length, X, Y):
    alfa = calculate_alfa(X, Y)
    X_l = X[:-2] + length*np.cos(alfa + np.pi/2)
    Y_l = Y[:-2] + length*np.sin(alfa + np.pi/2)
    return X_l, Y_l


# obliczenia dla krawędzi prawostronnej zgodne z wzorami z pracy mgr
def right_edge(length, X, Y):
    alfa = calculate_alfa(X, Y)
    X_r = X[:-2] + length*np.cos(alfa - np.pi/2)
    Y_r = Y[:-2] + length*np.sin(alfa - np.pi/2)
    return X_r, Y_r


# obliczenia alfy zgodnie z wzorami z pracy mgr
def calculate_alfa(x, y):
    dx = np.array([(x[i+1] - x[i-1]) for i in range(1, len(x)-1)])
    dy = np.array([(y[i+1] - y[i-1]) for i in range(1, len(y)-1)])
    alfa = np.arctan2(dy, dx)
    return alfa


# tutaj jest algorytm zamiany zdjęcia na wektory trasy, ale nie będę go opisywał bo jest dość zawiły
def img_to_path(img):
    X_vect = np.array([0], dtype=int)
    Y_vect = np.array([], dtype=int)
    gray_img_arr = img
    coll_0 = gray_img_arr[:, 0]
    a = np.where(coll_0 == 0)
    Y_vect = np.append(Y_vect,a[0][0])

    gray_img_arr_clean = gray_img_arr

    go_on = True
    first_go = True
    last_go = False

    max_coll = gray_img_arr.shape[1]

    row = a[0][0]
    coll = 0
    prew_help_row = 1
    prew_help_coll = 0

    while go_on:
        # print("row:", row, "coll:", coll)
        # print("p_row:", prew_help_row, "p_coll:", prew_help_coll)
        if first_go:
            help_ = gray_img_arr[row-1:row+2, coll:coll+2]
            if help_[0, 1] == 0:
                if help_[1, 1] == 0:
                    gray_img_arr_clean[row-1, coll+1] = 255
                Y_vect = np.append(Y_vect, row-1)
                X_vect = np.append(X_vect, coll+1)
                coll += 1
                row -= 1
                prew_help_coll = 0
                prew_help_row = 2
            elif help_[2, 1] == 0:
                if help_[1, 1] == 0:
                    gray_img_arr_clean[row+1, coll+1] = 255
                Y_vect = np.append(Y_vect, row+1)
                X_vect = np.append(X_vect, coll+1)
                coll += 1
                row += 1
                prew_help_coll = 0
                prew_help_row = 0
            else:
                Y_vect = np.append(Y_vect, row)
                X_vect = np.append(X_vect, coll+1)
                coll += 1
                prew_help_coll = 0
                prew_help_row = 1
            first_go = False

        elif last_go:
            help_ = gray_img_arr[row-1:row+2, coll-1:]
            if help_[0, 1] == 0:
                if help_[1, 1] == 0:
                    gray_img_arr_clean[row-1, coll+1] = 255
                Y_vect = np.append(Y_vect, row-1)
                X_vect = np.append(X_vect, coll+1)
                coll += 1
                row -= 1
                prew_help_coll = 0
                prew_help_row = 2
            elif help_[2, 1] == 0:
                if help_[1, 1] == 0:
                    gray_img_arr_clean[row+1, coll+1] = 255
                Y_vect = np.append(Y_vect, row+1)
                X_vect = np.append(X_vect, coll+1)
                coll += 1
                row += 1
                prew_help_coll = 0
                prew_help_row = 0
            else:
                Y_vect = np.append(Y_vect, row)
                X_vect = np.append(X_vect, coll+1)
                coll += 1
                prew_help_coll = 0
                prew_help_row = 1

            go_on = False

        else:
            help_ = gray_img_arr[row-1:row+2, coll-1:coll+2]
            # ostatnie help_ [0, 0]
            if prew_help_row == 0 and prew_help_coll == 0:
                # w kierunku prawa góra
                if help_[0, 2] == 0:
                    if help_[1, 2] == 0:
                        gray_img_arr_clean[row, coll+1] = 255
                    Y_vect = np.append(Y_vect, row-1)
                    X_vect = np.append(X_vect, coll+1)
                    row -= 1
                    coll += 1
                    prew_help_row = 2
                    prew_help_coll = 0
                # w kierunku prawa dół
                elif help_[2, 2] == 0:
                    if help_[1, 2] == 0:
                        gray_img_arr_clean[row, coll+1] = 255
                    if help_[2, 1] == 0:
                        gray_img_arr_clean[row+1, coll] = 255
                    Y_vect = np.append(Y_vect, row+1)
                    X_vect = np.append(X_vect, coll+1)
                    row += 1
                    coll += 1
                    prew_help_row = 0
                    prew_help_coll = 0
                # w kierunku lewy dół
                elif help_[2, 0] == 0:
                    if help_[2, 1] == 0:
                        gray_img_arr_clean[row+1, coll] = 255
                    Y_vect = np.append(Y_vect, row+1)
                    X_vect = np.append(X_vect, coll-1)
                    row += 1
                    coll -= 1
                    prew_help_row = 0
                    prew_help_coll = 2
                # w kierunku prawa
                elif help_[1, 2] == 0:
                    Y_vect = np.append(Y_vect, row)
                    X_vect = np.append(X_vect, coll+1)
                    coll += 1
                    prew_help_row = 1
                    prew_help_coll = 0
                # w kiedunku dół
                else:
                    Y_vect = np.append(Y_vect, row+1)
                    X_vect = np.append(X_vect, coll)
                    row += 1
                    prew_help_row = 0
                    prew_help_coll = 1

            # ostatnie help_ [0, 1]
            if prew_help_row == 0 and prew_help_coll == 1:
                # w kierunku lewo dół
                if help_[2, 0] == 0:
                    if help_[1, 0] == 0:
                        gray_img_arr_clean[row, coll-1] = 255
                    if help_[2, 1] == 0:
                        gray_img_arr_clean[row+1, coll] = 255
                    Y_vect = np.append(Y_vect, row+1)
                    X_vect = np.append(X_vect, coll-1)
                    row += 1
                    coll -= 1
                    prew_help_row = 0
                    prew_help_coll = 2
                # w kierunku prawa dół
                elif help_[2, 2] == 0:
                    if help_[1, 2] == 0:
                        gray_img_arr_clean[row, coll+1] = 255
                    if help_[2, 1] == 0:
                        gray_img_arr_clean[row+1, coll] = 255
                    Y_vect = np.append(Y_vect, row+1)
                    X_vect = np.append(X_vect, coll+1)
                    row += 1
                    coll += 1
                    prew_help_row = 0
                    prew_help_coll = 0
                # w kierunku lewo
                elif help_[1, 0] == 0:
                    Y_vect = np.append(Y_vect, row)
                    X_vect = np.append(X_vect, coll-1)
                    coll -= 1
                    prew_help_row = 1
                    prew_help_coll = 2
                # w kierunku prawa
                elif help_[1, 2] == 0:
                    Y_vect = np.append(Y_vect, row)
                    X_vect = np.append(X_vect, coll+1)
                    coll += 1
                    prew_help_row = 1
                    prew_help_coll = 0
                # w kiedunku dół
                else:
                    Y_vect = np.append(Y_vect, row+1)
                    X_vect = np.append(X_vect, coll)
                    row += 1
                    prew_help_row = 0
                    prew_help_coll = 1

            # ostatnie help_ [0, 2]
            if prew_help_row == 0 and prew_help_coll == 2:
                # w kierunku lewa góra
                if help_[0, 0] == 0:
                    if help_[1, 0] == 0:
                        gray_img_arr_clean[row, coll-1] = 255
                    Y_vect = np.append(Y_vect, row-1)
                    X_vect = np.append(X_vect, coll-1)
                    row -= 1
                    coll -= 1
                    prew_help_row = 2
                    prew_help_coll = 2
                # w kierunku prawa dół
                elif help_[2, 2] == 0:
                    if help_[2, 1] == 0:
                        gray_img_arr_clean[row+1, coll] = 255
                    Y_vect = np.append(Y_vect, row+1)
                    X_vect = np.append(X_vect, coll+1)
                    row += 1
                    coll += 1
                    prew_help_row = 0
                    prew_help_coll = 0
                # w kierunku lewy dół
                elif help_[2, 0] == 0:
                    if help_[2, 1] == 0:
                        gray_img_arr_clean[row+1, coll] = 255
                    if help_[1, 0] == 0:
                        gray_img_arr_clean[row, coll-1] = 255
                    Y_vect = np.append(Y_vect, row+1)
                    X_vect = np.append(X_vect, coll-1)
                    row += 1
                    coll -= 1
                    prew_help_row = 0
                    prew_help_coll = 2
                # w kierunku lewa
                elif help_[1, 0] == 0:
                    Y_vect = np.append(Y_vect, row)
                    X_vect = np.append(X_vect, coll-1)
                    coll -= 1
                    prew_help_row = 1
                    prew_help_coll = 2
                # w kiedunku dół
                else:
                    Y_vect = np.append(Y_vect, row+1)
                    X_vect = np.append(X_vect, coll)
                    row += 1
                    prew_help_row = 0
                    prew_help_coll = 1

            # ostatnie help_ [1, 2]
            if prew_help_row == 1 and prew_help_coll == 2:
                # w kierunku lewa góra
                if help_[0, 0] == 0:
                    if help_[1, 0] == 0:
                        gray_img_arr_clean[row, coll-1] = 255
                    if help_[0, 1] == 0:
                        gray_img_arr_clean[row-1, coll] = 255
                    Y_vect = np.append(Y_vect, row-1)
                    X_vect = np.append(X_vect, coll-1)
                    row -= 1
                    coll -= 1
                    prew_help_row = 2
                    prew_help_coll = 2
                # w kierunku lewy dół
                elif help_[2, 0] == 0:
                    if help_[1, 0] == 0:
                        gray_img_arr_clean[row, coll-1] = 255
                    if help_[2, 1] == 0:
                        gray_img_arr_clean[row+1, coll] = 255
                    Y_vect = np.append(Y_vect, row+1)
                    X_vect = np.append(X_vect, coll-1)
                    row += 1
                    coll -= 1
                    prew_help_row = 0
                    prew_help_coll = 2
                # w kierunku lewo
                elif help_[1, 0] == 0:
                    Y_vect = np.append(Y_vect, row)
                    X_vect = np.append(X_vect, coll-1)
                    coll -= 1
                    prew_help_row = 1
                    prew_help_coll = 2
                # w kierunku góra
                elif help_[0, 1] == 0:
                    Y_vect = np.append(Y_vect, row-1)
                    X_vect = np.append(X_vect, coll)
                    row -= 1
                    prew_help_row = 2
                    prew_help_coll = 1
                # w kiedunku dół
                else:
                    Y_vect = np.append(Y_vect, row+1)
                    X_vect = np.append(X_vect, coll)
                    row += 1
                    prew_help_row = 0
                    prew_help_coll = 1

            # ostatnie help_ [2, 2]
            if prew_help_row == 2 and prew_help_coll == 2:
                # w kierunku lewa góra
                if help_[0, 0] == 0:
                    if help_[1, 0] == 0:
                        gray_img_arr_clean[row, coll-1] = 255
                    if help_[0, 1] == 0:
                        gray_img_arr_clean[row-1, coll] = 255
                    Y_vect = np.append(Y_vect, row-1)
                    X_vect = np.append(X_vect, coll-1)
                    row -= 1
                    coll -= 1
                    prew_help_row = 2
                    prew_help_coll = 2
                # w kierunku prawa góra
                elif help_[0, 2] == 0:
                    if help_[0, 1] == 0:
                        gray_img_arr_clean[row-1, coll] = 255
                    Y_vect = np.append(Y_vect, row-1)
                    X_vect = np.append(X_vect, coll+1)
                    row -= 1
                    coll += 1
                    prew_help_row = 2
                    prew_help_coll = 0
                # w kierunku lewy dół
                elif help_[2, 0] == 0:
                    if help_[1, 0] == 0:
                        gray_img_arr_clean[row, coll-1] = 255
                    Y_vect = np.append(Y_vect, row+1)
                    X_vect = np.append(X_vect, coll-1)
                    row += 1
                    coll -= 1
                    prew_help_row = 0
                    prew_help_coll = 2
                # w kierunku lewa
                elif help_[1, 0] == 0:
                    Y_vect = np.append(Y_vect, row)
                    X_vect = np.append(X_vect, coll-1)
                    coll -= 1
                    prew_help_row = 1
                    prew_help_coll = 2
                # w kiedunku góra
                else:
                    Y_vect = np.append(Y_vect, row-1)
                    X_vect = np.append(X_vect, coll)
                    row -= 1
                    prew_help_row = 2
                    prew_help_coll = 1

            # ostatnie help_ [2, 1]
            if prew_help_row == 2 and prew_help_coll == 1:
                # w kierunku lewo góra
                if help_[0, 0] == 0:
                    if help_[1, 0] == 0:
                        gray_img_arr_clean[row, coll-1] = 255
                    if help_[0, 1] == 0:
                        gray_img_arr_clean[row-1, coll] = 255
                    Y_vect = np.append(Y_vect, row-1)
                    X_vect = np.append(X_vect, coll-1)
                    row -= 1
                    coll -= 1
                    prew_help_row = 2
                    prew_help_coll = 2
                # w kierunku prawa góra
                elif help_[0, 2] == 0:
                    if help_[1, 2] == 0:
                        gray_img_arr_clean[row, coll+1] = 255
                    if help_[0, 1] == 0:
                        gray_img_arr_clean[row-1, coll] = 255
                    Y_vect = np.append(Y_vect, row-1)
                    X_vect = np.append(X_vect, coll+1)
                    row -= 1
                    coll += 1
                    prew_help_row = 2
                    prew_help_coll = 0
                # w kierunku lewo
                elif help_[1, 0] == 0:
                    Y_vect = np.append(Y_vect, row)
                    X_vect = np.append(X_vect, coll-1)
                    coll -= 1
                    prew_help_row = 1
                    prew_help_coll = 2
                # w kierunku prawa
                elif help_[1, 2] == 0:
                    Y_vect = np.append(Y_vect, row)
                    X_vect = np.append(X_vect, coll+1)
                    coll += 1
                    prew_help_row = 1
                    prew_help_coll = 0
                # w kiedunku góra
                else:
                    Y_vect = np.append(Y_vect, row-1)
                    X_vect = np.append(X_vect, coll)
                    row -= 1
                    prew_help_row = 2
                    prew_help_coll = 1

            # ostatnie help_ [2, 0]
            if prew_help_row == 2 and prew_help_coll == 0:
                # w kierunku lewa góra
                if help_[0, 0] == 0:
                    if help_[0, 1] == 0:
                        gray_img_arr_clean[row-1, coll] = 255
                    Y_vect = np.append(Y_vect, row-1)
                    X_vect = np.append(X_vect, coll-1)
                    row -= 1
                    coll -= 1
                    prew_help_row = 2
                    prew_help_coll = 2
                # w kierunku prawa góra
                elif help_[0, 2] == 0:
                    if help_[0, 1] == 0:
                        gray_img_arr_clean[row-1, coll] = 255
                    if help_[1, 2] == 0:
                        gray_img_arr_clean[row, coll+1] = 255
                    Y_vect = np.append(Y_vect, row-1)
                    X_vect = np.append(X_vect, coll+1)
                    row -= 1
                    coll += 1
                    prew_help_row = 2
                    prew_help_coll = 0
                # w kierunku prawy dół
                elif help_[2, 2] == 0:
                    if help_[1, 2] == 0:
                        gray_img_arr_clean[row, coll+1] = 255
                    Y_vect = np.append(Y_vect, row+1)
                    X_vect = np.append(X_vect, coll+1)
                    row += 1
                    coll += 1
                    prew_help_row = 0
                    prew_help_coll = 0
                # w kierunku prawa
                elif help_[1, 2] == 0:
                    Y_vect = np.append(Y_vect, row)
                    X_vect = np.append(X_vect, coll+1)
                    coll += 1
                    prew_help_row = 1
                    prew_help_coll = 0
                # w kiedunku góra
                else:
                    Y_vect = np.append(Y_vect, row-1)
                    X_vect = np.append(X_vect, coll)
                    row -= 1
                    prew_help_row = 2
                    prew_help_coll = 1

            # ostatnie help_ [1, 0]
            if prew_help_row == 1 and prew_help_coll == 0:
                # w kierunku prawa góra
                if help_[0, 2] == 0:
                    if help_[1, 2] == 0:
                        gray_img_arr_clean[row, coll+1] = 255
                    if help_[0, 1] == 0:
                        gray_img_arr_clean[row-1, coll] = 255
                    Y_vect = np.append(Y_vect, row-1)
                    X_vect = np.append(X_vect, coll+1)
                    row -= 1
                    coll += 1
                    prew_help_row = 2
                    prew_help_coll = 0
                # w kierunku prawy dół
                elif help_[2, 2] == 0:
                    if help_[1, 2] == 0:
                        gray_img_arr_clean[row, coll+1] = 255
                    if help_[2, 1] == 0:
                        gray_img_arr_clean[row+1, coll] = 255
                    Y_vect = np.append(Y_vect, row+1)
                    X_vect = np.append(X_vect, coll+1)
                    row += 1
                    coll += 1
                    prew_help_row = 0
                    prew_help_coll = 0
                # w kierunku prawo
                elif help_[1, 2] == 0:
                    Y_vect = np.append(Y_vect, row)
                    X_vect = np.append(X_vect, coll+1)
                    coll += 1
                    prew_help_row = 1
                    prew_help_coll = 0
                # w kierunku góra
                elif help_[0, 1] == 0:
                    Y_vect = np.append(Y_vect, row-1)
                    X_vect = np.append(X_vect, coll)
                    row -= 1
                    prew_help_row = 2
                    prew_help_coll = 1
                # w kiedunku dół
                else:
                    Y_vect = np.append(Y_vect, row+1)
                    X_vect = np.append(X_vect, coll)
                    row += 1
                    prew_help_row = 0
                    prew_help_coll = 1

        if coll >= max_coll-2:
            last_go = True

        # if row == 37:
        #     go_on = False
    return X_vect, Y_vect


# wygładzanie jest realizaowane przez uśrednianie N poprzednich próbek
def smooth_path(x, y, smothness):
    X = np.zeros(len(x) + smothness)
    Y = np.zeros(len(y) + smothness)
    for i in range(len(x)+smothness):
        if i < smothness:
            sum_ = np.average(x[:i+1])
        elif i >= len(x):
            sum_ = np.average(x[i-smothness:])
        else:
            sum_ = np.average(x[i-smothness:i])
        X[i] = sum_
    for i in range(len(y)+smothness):
        if i < smothness:
            sum_ = np.average(y[:i+1])
        elif i >= len(y):
            sum_ = np.average(y[i-smothness:])
        else:
            sum_ = np.average(y[i-smothness:i])
        Y[i] = sum_

    return X, Y


# dodanie szumów jest realizowane za pomocą dodania wartości sinusa oraz małej randomowej wartości w osi prostopadłej do przebiegu
def add_noise(x, y, noise_lvl):
    alfa = calculate_alfa(x, y)
    # x_noise = x[:-2] + noise_lvl * np.cos(alfa + np.pi / 2) * (np.random.rand(len(x[:-2])) * 2 - 1)
    # y_noise = y[:-2] + noise_lvl * np.sin(alfa + np.pi / 2) * (np.random.rand(len(y[:-2])) * 2 - 1)
    x_noise = x[:-2] + noise_lvl * np.cos(alfa + np.pi / 2) * (np.sin(np.arange(len(x[:-2]))*2*np.pi/20) + (np.random.rand(len(x[:-2])) * 2 - 1) * 0.1)
    y_noise = y[:-2] + noise_lvl * np.sin(alfa + np.pi / 2) * (np.sin(np.arange(len(y[:-2]))*2*np.pi/20) + (np.random.rand(len(y[:-2])) * 2 - 1) * 0.1)
    return x_noise, y_noise


# obliczenia krzywizny zgodnie z pracą mgr
def calculate_curvature(X, Y):
    dx = np.array([(X[i] - X[i - 1]) for i in range(1, len(X))])
    dy = np.array([(Y[i] - Y[i - 1]) for i in range(1, len(X))])
    T = (dx ** 2 + dy ** 2) ** 0.5
    alfa = np.arctan2(dy, dx)
    dalfa = np.array([(alfa[i] - alfa[i - 1]) for i in range(1, len(X) - 1)])
    # żeby nie dzielić przez 0
    K = np.zeros_like(dalfa)
    for i in range(len(K)):
        K[i] = 0 if T[i] == 0 else dalfa[i] / T[i]
    return K


# obliczenie macierzy H do optymalizacji z najkrótkszą ścieżką
def H_matrix(xl, yl, xr, yr):
    n = len(xl)
    H = np.zeros([n, n])
    for i in range(1, n-1):
        H[i-1, i] = - calc_delta(xl, xr, i-1) * calc_delta(xl, xr, i) - calc_delta(yl, yr, i-1) * calc_delta(yl, yr, i)
        H[i, i+1] = - calc_delta(xl, xr, i) * calc_delta(xl, xr, i+1) - calc_delta(yl, yr, i) * calc_delta(yl, yr, i+1)
        if i == 1 or i == n:
            H[i, i] = calc_delta(xl, xr, i) ** 2 + calc_delta(yl, yr, i) ** 2
        if i != 1 or i != n:
            H[i, i] = 2 * (calc_delta(xl, xr, i) ** 2 + calc_delta(yl, yr, i) ** 2)
    return H



def B_matrix(xl, yl, xr, yr):
    n = len(xl)
    B = np.zeros(n)
    for i in range(1, n-2):
        if i == 1:
            B[i] = (xr[i] - xr[i+1]) * calc_delta(xl, xr, i) + (yr[i] - yr[i+1]) * calc_delta(yl, yr, i)
        else:
            B[i] = (2 * xr[i] - xr[i-1] - xr[i+1]) * calc_delta(xl, xr, i) + (2 * yr[i] - yr[i-1] - yr[i+1]) * calc_delta(yl, yr, i)
    n -= 1
    B[n] = (xr[n] - xr[n-1]) * calc_delta(xl, xr, n) + (yr[n] - yr[n-1]) * calc_delta(yl, yr, n)
    return B


def calc_delta(l, r, i):
    return l[i] - r[i]

def x_and_y_from_alfa(alfa, xl, yl, xr, yr):
    x = xr + alfa * (xl - xr)
    y = yr + alfa * (yl - yr)
    return x, y


def length_of_route(x, y):
    len_ = 0
    for i in range(1, len(x)):
        len_ += (x[i] - x[i-1]) ** 2 + (y[i] - y[i-1]) ** 2
    return len_


def length_of(xl, yl, xr, yr):
    n = len(xl)
    len_l = 0
    len_r = 0

    for i in range(1, n):
        len_l += (xl[i] - xl[i-1]) ** 2 + (yl[i] - yl[i-1]) ** 2
        len_r += (xr[i] - xr[i-1]) ** 2 + (yr[i] - yr[i-1]) ** 2
    return len_l, len_r


def find_shortest_edges(xl, yl, xr, yr, strength):
    # obliczanie długości fragmentów trasy
    len_l = np.zeros_like(xl)
    len_r = np.zeros_like(xl)
    count = 10
    alfa_whats_longer = np.full_like(xl, 0.5)

    # odcinkowe sprawdzanie która strona jest dłuższa
    for j in range(len(len_l)-count):
        Xl_smoth_short = xl[j:j+count]
        Yl_smoth_short = yl[j:j+count]
        Xr_smoth_short = xr[j:j+count]
        Yr_smoth_short = yr[j:j+count]
        len_l[j], len_r[j] = length_of(Xl_smoth_short, Yl_smoth_short, Xr_smoth_short, Yr_smoth_short)
        if strength*len_l[j] > len_r[j]:
            alfa_whats_longer[j] = 0
        elif strength*len_r[j] > len_l[j]:
            alfa_whats_longer[j] = 1
        else:
            alfa_whats_longer[j] = 0.5

    # filtrowanie niepotrzebnych zmian np. 0 0 0.5 0 -> 0 0 0 0
    alfa_whats_longer_new = alfa_whats_longer.copy()
    prev = 0
    curr = 0
    start = False
    go_again = True
    alfa_whats_longer_newer = alfa_whats_longer_new.copy()
    for i in range(len(alfa_whats_longer_newer)):
        if (alfa_whats_longer_new[i] == 1 or alfa_whats_longer_new[i] == 0) and go_again:
            prev = i
            start = True
            go_again = False
        if start:
            curr = i
            if alfa_whats_longer_new[curr] == alfa_whats_longer_new[prev]:
                alfa_whats_longer_newer[prev:curr+1] = alfa_whats_longer_new[curr]
                prev = curr
            if alfa_whats_longer_new[curr] != alfa_whats_longer_new[prev] and alfa_whats_longer_new[curr] != 0.5:
                prev = curr

    return alfa_whats_longer_newer