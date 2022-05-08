from matplotlib import pyplot
import random
import numpy as np
import calculations as calc

#########################################################################
#########################################################################
#                                                                       #
#       Algorytm genetyczny dla znajdywania najkrótszej ścieżki         #
#                                                                       #
#########################################################################
#########################################################################

# wskaźnik jakości
def quality(alfa, Xl, Yl, Xr, Yr):
    X, Y = calc.x_and_y_from_alfa(alfa, Xl, Yl, Xr, Yr)
    to_return = calc.length_of_route(X, Y)
    return to_return


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

        # filtrowanie
        smothed_best_resoult = np.zeros_like(best_resoult)
        prev = 0
        prev_2 = 0
        ratio = 0.05
        if (i+1) % 5 == 0 or i == 0:
            for s in range(n):
                smothed_best_resoult[s] = best_resoult[s] * ratio + prev * 0.5 * (1 - ratio) + prev_2 * 0.5 * (1 - ratio)
                prev_2 = prev
                prev = smothed_best_resoult[s]
            if i != epochs-1:
                for o in range(n):
                    if edges[o] == 1:
                        smothed_best_resoult[o] = 1
                    if edges[o] == 0:
                        smothed_best_resoult[o] = 0
            best_solutions[0, :] = smothed_best_resoult

        # generacja nowej populacji - mutajcje
        new_population = np.zeros_like(my_population)
        new_population[0:solutions_number//10, :] = best_solutions
        for j in range(solutions_number//10, solutions_number):
            to_pass = best_solutions[random.randint(0, solutions_number//10 - 1), :]
            new_population[j, :] = mutate(to_pass, edges)

        # zapisanie nowej populacji do zmiennej aktualną populacją
        my_population = new_population

    return best_resoult


#########################################################################
#########################################################################
#                                                                       #
#       Algorytm genetyczny dla znajdywania najkrótszej ścieżki         #
#               Z interpolacją liniową pomiędzy punktami                #
#                                                                       #
#########################################################################
#########################################################################

# funkcja odpowiedizalna za generowanie populacji - z wstępną linearyzacją
def generate_population_linearized(edg, sol_num, n):
    population = np.full((sol_num, n), 0.5)

    # Pierwszy wierwsz to indeksy startowych wartości, a drugi to indeksy końcowych wartości
    start = np.array([0], dtype=int)
    end = np.array([], dtype=int)
    prev = edg[0]
    counter = 0
    for i in range(len(edg)):
        if edg[i] != prev:
            counter += 1
            prev = edg[i]
            if counter % 2 == 0:
                start = np.append(start, i)
            if counter % 2 == 1:
                end = np.append(end, i)
    end = np.append(end, n)
    section_count = len(start)

    subject = edg
    for j in range(sol_num):

        for x in range(section_count):
            rising = True if edg[end[x]-1] > edg[start[x]-1] else False

            if x == 0:
                beginning = start[x]
                ending = random.randint(end[x], end[x] + int((start[x+1] - end[x]) / 2))
                print(beginning, ending)
                subject[beginning: ending] = linear_connection(beginning, ending, 1, rising)

            elif x == (section_count - 1):
                beginning = random.randint(ending, start[x])
                ending = end[x]
                print(beginning, ending)
                subject[beginning: ending] = linear_connection(beginning, ending, 3, rising)

            else:
                beginning = random.randint(ending, start[x])
                ending = random.randint(end[x], end[x] + int((start[x+1] - end[x]) / 2))
                print(beginning, ending)
                subject[beginning: ending] = linear_connection(beginning, ending, 2, rising)

    return subject


# interpolacja liniowa pomiędzy dwoma punktami
def linear_connection(start, end, pos, rising):
    len_ = end - start
    line = np.zeros(len_)
    if pos == 1:
        start_val = 0.5
        stop_val = int(rising)

    elif pos == 2:
        start_val = int(not rising)
        stop_val = int(rising)

    else:
        start_val = int(not rising)
        stop_val = 0.5


    for i in range(len_):
        line[i] = start_val + (stop_val - start_val) / len_ * (i + 1)
        # print(line[i])

    return line


# sam w sobie alg gen
def genetic_optimization_with_linearization(alfa, xl, yl, xr, yr, solutions_number, epochs, min_fit, edges):
    # długość wektora do minimalizacji
    n = len(alfa)

    # wektor z populacją - macierz gdzie każdy wiersz zawiera pełen wektor z rozwiązaniami - alfa
    my_population = np.zeros((solutions_number, n))

    # generacja wektora, którego elementami są poszczególne rozwiązania oraz wartości z funkcji fitness
    population_with_qual = np.zeros((solutions_number, n + 1))

    # generowanie pierwszej grupy rozwiązań - populacja początkowa
    my_population = generate_population_linearized(edges, solutions_number, n)
    # print(my_population[0:24])
    # my_population = np.full_like(my_population, 0.8)
    X_l, Y_l = calc.x_and_y_from_alfa(my_population, xl, yl, xr, yr)
    pyplot.figure(41)
    pyplot.plot(xl, yl)
    pyplot.plot(xr, yr)
    pyplot.plot(X_l, Y_l)
    pyplot.show()


    # # algorytm genetyczny sam w sobie
    # for i in range(epochs):
    #     # zapisanie talbicy z populacją do tablicy z populacją powiększonej o wskaźnik jakości
    #     population_with_qual[:, 1:n+1] = my_population
    #
    #     # obliczenie wskaźnika jakości dla każdego osobnika
    #     for k in range(solutions_number):
    #         subject = my_population[k, :]
    #         population_with_qual[k, 0] = quality(subject, xl, yl, xr, yr)
    #
    #     # sortowanie tablicy względem malejącego wskaźnika jakości
    #     sorted_population_with_qual = population_with_qual[population_with_qual[:, 0].argsort()]
    #     best_resoult = sorted_population_with_qual[0, 1:n+1]
    #     best_resoult_fit = sorted_population_with_qual[0, 0]
    #
    #     # najlepsze 10%
    #     best_solutions = sorted_population_with_qual[0:solutions_number//10, 1:n+1]
    #
    #     print("iteration number:", i + 1, "vall:", best_resoult_fit)
    #
    #     if best_resoult_fit < min_fit:
    #         break
    #
    #     # filtrowanie
    #     smothed_best_resoult = np.zeros_like(best_resoult)
    #     prev = 0
    #     prev_2 = 0
    #     ratio = 0.05
    #     if (i+1) % 5 == 0 or i == 0:
    #         for s in range(n):
    #             smothed_best_resoult[s] = best_resoult[s] * ratio + prev * 0.5 * (1 - ratio) + prev_2 * 0.5 * (1 - ratio)
    #             prev_2 = prev
    #             prev = smothed_best_resoult[s]
    #         if i != epochs-1:
    #             for o in range(n):
    #                 if edges[o] == 1:
    #                     smothed_best_resoult[o] = 1
    #                 if edges[o] == 0:
    #                     smothed_best_resoult[o] = 0
    #         best_solutions[0, :] = smothed_best_resoult
    #
    #     # generacja nowej populacji - mutajcje
    #     new_population = np.zeros_like(my_population)
    #     new_population[0:solutions_number//10, :] = best_solutions
    #     for j in range(solutions_number//10, solutions_number):
    #         to_pass = best_solutions[random.randint(0, solutions_number//10 - 1), :]
    #         new_population[j, :] = mutate(to_pass, edges)
    #
    #     # zapisanie nowej populacji do zmiennej aktualną populacją
    #     my_population = new_population

    # return best_resoult




