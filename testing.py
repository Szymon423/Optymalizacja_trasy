from matplotlib import pyplot
import random
import numpy as np
import calculations as calc

array1 = np.array([1, 2, 3])
array2 = np.array([4, 5, 6])
array3 = np.array([7, 8, 9])

# print(arrayOfArrays)


population = np.zeros((3, 3))
population_with_qual = np.zeros((3, 3+1))

a = np.array([21, 2, 52])
b = np.array([29, 23, 2])
c = np.array([43, 2, 12])
n = 3
a1 = 2
b1 = 1
c1 = 3

population[0, :] = a
population[1, :] = b
population[2, :] = c

population_with_qual[:, 1:n+1] = population

population_with_qual[0, 0] = a1
population_with_qual[1, 0] = b1
population_with_qual[2, 0] = c1

sorted = np.flip(population_with_qual[population_with_qual[:, 0].argsort()], axis=0)





print(random.randint(0, 9))

# population_with_qual = np.sort(population_with_qual)


BBB = np.full(5, True)

print(BBB)
