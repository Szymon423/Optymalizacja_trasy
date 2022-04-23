from matplotlib import pyplot
import random
import numpy as np


def foo(alfa, b, h):
    # funkjcja zwracająca wartość wskaźnika jakości
    return np.matmul(np.matmul(np.transpose(alfa), h), alfa) + np.matmul(b, alfa)


def fitness(alfa, b, h):
    res = foo(alfa, b, h)
    if res == 0:
        return 99999
    else:
        return abs(1/res)


def genetic_optimization(alfa, h, b, solutions_number, epochs, min_err):
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
            ranked_solutions.append((fitness(s, b, h), s))
        ranked_solutions.sort()
        ranked_solutions.reverse()
        print("iteration number:", i+1, "vall:", ranked_solutions[0][0])

        if ranked_solutions[0][0] > min_err:
            break

        best_solutions = ranked_solutions[:solutions_number//10]

        elements = np.array([])
        for s in best_solutions:
            elements = np.append(elements, s[1])

        new_gen = []
        for _ in range(solutions_number):
            to_append2 = []
            for xx in range(n):
                num = random.choice(elements)
                this = (num * random.uniform(0.99, 1.01) * (num > 0) * (num < 1) +
                        1 * (num > 1) +
                        0 * (num < 0)) if xx > 0 else 0.5
                to_append2.append(this)
            new_gen.append(tuple(to_append2))
        solutions = new_gen

    return ranked_solutions[0]

