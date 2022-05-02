from matplotlib import pyplot
import random
import numpy as np
import calculations as calc


# wskaźnik jakości
def quality(alfa, Xl, Yl, Xr, Yr):
    X, Y = calc.x_and_y_from_alfa(alfa, Xl, Yl, Xr, Yr)
    to_return = calc.length_of_route(X, Y)
    return to_return

# funkcja dopasowywująca - im większa wartość pochodząca z foo, tym mniejsza wartość jest zwracana
def fitness(alfa, xl, yl, xr, yr):
    res = quality(alfa, xl, yl, xr, yr)
    if res == 0:
        return 99999
    else:
        return abs(1/res)


# funkcja odpowiedizalna za generowanie populacji - do MODYFIKACJI
def generate_population(edg, sol_num, n):
    population = np.full((sol_num, n), 0.5)

    for ii in range(sol_num):
        sample = np.full(n, 0.5)
        for o in range(n):
            if edg[o] == 1:
                sample[o] = 1
            elif edg[o] == 0:
                sample[o] = 0
            else:
                a = 0.5 * random.uniform(0.1, 2.5)
                if a > 1:
                    sample[o] = 1
                elif a < 0:
                    sample[o] = 0
                else:
                    sample[o] = a

        population[ii, :] = sample

    return population


# funkcja odpowiedzialna za mutację
def mutate(to_change, edg):
    size = len(to_change)
    to_return = np.full(size, 0.5)
    for o in range(size):
        if edg[o] == 1:
            to_return[o] = 1
        elif edg[o] == 0:
            to_return[o] = 0
        else:
            a = to_change[o]*random.uniform(0.95, 1.05)
            if a > 1:
                to_return[o] = 1
            elif a < 0:
                to_return[o] = 0
            else:
                to_return[o] = a

    return to_return


# algorytm sam w sobie
def genetic_optimization(alfa, xl, yl, xr, yr, solutions_number, epochs, min_fit, edges):
    # długość wektora do minimalizacji
    n = len(alfa)

    # wektor z populacją - macierz gdzie każdy wiersz zawiera pełen wektor z rozwiązaniami - alfa
    my_population = np.zeros((solutions_number, n))

    # generacja wektora, którego elementami są poszczególne rozwiązania
    # oraz wartości z funkcji fitness
    population_with_qual = np.zeros((solutions_number, n + 1))

    # generowanie pierwszej grupy rozwiązań - populacja początkowa
    my_population = generate_population(edges, solutions_number, n)

    # algorytm genetyczny sam w sobie
    for i in range(epochs):
        # zapisanie talbicy z populacją do tablicy z populacją powiększonej o wskaźnik jakości
        population_with_qual[:, 1:n+1] = my_population

        # obliczenie wskaźnika jakości dla każdego osobnika
        for k in range(solutions_number):
            subject = my_population[k, :]
            population_with_qual[k, 0] = quality(subject, xl, yl, xr, yr)

        # sortowanie tablicy względem malejącego wskaźnika jakości
        sorted_population_with_qual = population_with_qual[population_with_qual[:, 0].argsort()]
        best_resoult = sorted_population_with_qual[0, 1:n+1]
        best_resoult_fit = sorted_population_with_qual[0, 0]

        # najlepsze 10%
        best_solutions = sorted_population_with_qual[0:solutions_number//10, 1:n+1]

        print("iteration number:", i + 1, "vall:", best_resoult_fit)

        if best_resoult_fit < min_fit:
            break


        # generacja nowej populacji - mutajcje
        new_population = np.zeros_like(my_population)
        new_population[0:solutions_number//10, :] = best_solutions
        for j in range(solutions_number//10, solutions_number):
            to_pass = best_solutions[random.randint(0, solutions_number//10 - 1), :]
            new_population[j, :] = mutate(to_pass, edges)

        # zapisanie nowej populacji do zmiennej aktualną populacją
        my_population = new_population

    return  best_resoult








