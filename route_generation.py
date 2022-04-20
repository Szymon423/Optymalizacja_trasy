import matplotlib.pyplot as plt
import numpy as np


def generate_route():
    X = np.array([i for i in range(2000)])
    Y = np.sin(X*2*np.pi/2000)*200 + np.sin(X*2*np.pi/200)*2
    return X, Y