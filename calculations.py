import matplotlib.pyplot as plt
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