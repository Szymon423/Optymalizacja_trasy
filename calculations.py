from matplotlib import pyplot
import numpy as np


def generate_route(end):
    X = np.linspace(0, end + 1, end)
    Y = np.sin(X*2*np.pi/2000)*200# + np.sin(X*2*np.pi/200)*2 + (np.random.rand(2000)*10 - 1) * 2
    return X, Y


def left_edge(length, X, Y):
    alfa = calculate_alfa(X, Y)
    X_l = X[:-2] + length*np.cos(alfa + np.pi/2)
    Y_l = Y[:-2] + length*np.sin(alfa + np.pi/2)
    return X_l, Y_l


def right_edge(length, X, Y):
    alfa = calculate_alfa(X, Y)
    X_r = X[:-2] + length*np.cos(alfa - np.pi/2)
    Y_r = Y[:-2] + length*np.sin(alfa - np.pi/2)
    return X_r, Y_r


def calculate_alfa(x, y):
    dx = np.array([(x[i+1] - x[i-1]) for i in range(1, len(x)-1)])
    dy = np.array([(y[i+1] - y[i-1]) for i in range(1, len(y)-1)])
    alfa = np.arctan2(dy, dx)
    return alfa


def img_to_path(img):
    X_vect = np.array([0], dtype=int)
    Y_vect = np.array([], dtype=int)
    gray_img_arr = img
    coll_0 = gray_img_arr[:, 0]
    a = np.where(coll_0 == 0)
    print(a[0][0])
    Y_vect = np.append(Y_vect,a[0][0])
    print("X:", X_vect)
    print("Y:", Y_vect)

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
        if first_go:
            help_ = gray_img_arr[row-1:row+2, coll:coll+2]
            print(help_)
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
            print(help_)
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
            print("row:", row, "coll:", coll)
            print("p_row:", prew_help_row, "p_coll:", prew_help_coll)
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
                print("i am here0")
                # w kierunku lewa góra
                if help_[0, 0] == 0:
                    print("i am here1")
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
                    print("i am here2")
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
                    print("i am here3")
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
                    print("i am here4")
                    Y_vect = np.append(Y_vect, row)
                    X_vect = np.append(X_vect, coll+1)
                    coll += 1
                    prew_help_row = 1
                    prew_help_coll = 0
                # w kiedunku góra
                else:
                    print("i am here5")
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

        if coll == 499:
            last_go = True

    return X_vect, Y_vect
