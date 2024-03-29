
import random
from math import sqrt
from itertools import count, islice

#
# Global variables
#

GENERATIONS = 20
POP_SIZE = 20

def custom_sort(t):
  return t[1]

def isPrime(n):
  if n < 2:
    return False

  for number in islice(count(2), int(sqrt(n) - 1)):
    if n % number == 0:
      return False
  return True

def random_population():
  pop = []
  for i in xrange(POP_SIZE):
    pop.append(random.randint(1, 1000))
  return pop

#
# GA Functions
#

def fitness(num):
  fitness = 0
  if isPrime(num):
    fitness = 1 
  return fitness

def mutate(num):
  return num + random.randint(-10, 10)


#
# Main 
# 

if __name__ == "__main__":
  #Generate our inital population! 
  population = random_population()

  # Time to generate our simulation!
  print("\n\n")
  for generation in xrange(GENERATIONS):
    print "Gen %s - '%s'" % (generation, population)
    weighted_population = []

    # Add individuals and their respective fitness levels to the weighted
    # population list. This will be used to pull out individuals via certain
    # probabilities during the selection phase. Then, reset the population list
    # so we can repopulate it after selection.   
    for individual in population:
      fitness_val = fitness(individual)
      if fitness_val == 0:
        pair = (individual, 0.0)
      else: 
        pair = (individual, 1.0)
      weighted_population.append(pair)
      # print weighted_population

    weighted_population.sort(key = custom_sort)
    population = []
    # print weighted_population

    for individual, prime in weighted_population: 
      if prime == 0:
        population.append(mutate(individual))
      else: 
        population.append(individual)

  print("\n\n")
