from matplotlib import pyplot
import random
import numpy as np
import calculations as calc


def foo(alfa, Xl, Yl, Xr, Yr):
    X, Y = calc.x_and_y_from_alfa(alfa, Xl, Yl, Xr, Yr)
    to_return = calc.length_of_route(X, Y)
    return to_return


def fitness(alfa, xl, yl, xr, yr):
    res = foo(alfa, xl, yl, xr, yr)
    if res == 0:
        return 99999
    else:
        return abs(1/res)


def genetic_optimization(alfa, xl, yl, xr, yr, solutions_number, epochs, min_err):
    n = len(alfa)

    # generowanie wstępnych rozwiązań
    solutions = []
    for s in range(solutions_number):
        to_append = np.random.rand(n)
        solutions.append(tuple(to_append))


    # szukanie optimum
    for i in range(epochs):
        ranked_solutions = []
        for s in solutions:
            ranked_solutions.append((fitness(s, xl, yl, xr, yr), s))
        ranked_solutions.sort()
        ranked_solutions.reverse()
        print("iteration number:", i+1, "vall:", ranked_solutions[0][0])

        if ranked_solutions[0][0] > min_err:
            break
        # wybór 10 procent najlepszych rozwiązń
        best_solutions = ranked_solutions[:solutions_number//10]

        elements = np.array([])
        for s in best_solutions:
            elements = np.append(elements, s[1])
        print(elements.shape)
        new_gen = []
        for j in range(solutions_number):
            to_append2 = []
            for xx in range(n):
                num = random.choice(elements)
                # print("num", num)
                this = (num * random.uniform(0.95, 1.05) * (num > 0) * (num < 1) +
                        1 * (num > 1) +
                        0 * (num < 0)) if xx > 0 else 0.5
                to_append2.append(this)
            new_gen.append(tuple(to_append2))
        solutions = new_gen
    return ranked_solutions[0]