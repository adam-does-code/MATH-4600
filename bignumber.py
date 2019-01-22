
import random
from math import sqrt
from itertools import count, islice

#
# Global variables
#

GENERATIONS = 30
POP_SIZE = 20

def custom_sort(t):
  return t[1]

def random_population():
  pop = []
  for i in xrange(POP_SIZE):
    pop.append(random.randint(1, 100))
  return pop

# def weighted_choice(items):
#   """
#   Chooses a random element from items, where items is a list of tuples in
#   the form (item, weight). weight determines the probability of choosing its
#   respective item. Note: this function is borrowed from ActiveState Recipes.
#   """
#   weight_total = sum((item[1] for item in items))
#   n = random.uniform(0, weight_total)
#   for item, weight in items:
#     if n < weight:
#       return item
#     n = n - weight
#   return item

#
# GA Functions
#

def fitness(num):
  """
  For each number in our population we want to check 
  if any of the numbers are prime and sum up all the counts
  of the prime numbers and return it! 
  """
  fitness = 0
  if num > 100: 
    fitness = 1
  elif num > 1000:
    fitness = 2
  elif num > 10000:
    fitness = 3
  return fitness

def mutate(num):
  return num + random.randint(0, 10)

def crossover(dna1, dna2): 
  bin1 = str(bin(dna1))[2:]
  bin2 = str(bin(dna2))[2:]
  length = len(bin1)
  if length < len(bin2):
    length = len(bin2)
  pos = int(random.random() * length)
  crossover1 = bin1[:pos]+bin2[pos:]
  crossover2 = bin2[:pos]+bin1[pos:]

  return int(crossover1, 2), int(crossover2, 2)
#
# Main 
# 

if __name__ == "__main__":
  #Generate our inital population! 
  population = random_population()

  # Time to generate our simulation!
  for generation in xrange(GENERATIONS):
    print "Generation %s ... Random sample: '%s'" % (generation, population)
    weighted_population = []

    # Add individuals and their respective fitness levels to the weighted
    # population list. This will be used to pull out individuals via certain
    # probabilities during the selection phase. Then, reset the population list
    # so we can repopulate it after selection.   
    for individual in population:
      fitness_val = fitness(individual)
      if fitness_val == 0:
        pair = (individual, 0.0)
      elif fitness_val == 1: 
        pair = (individual, 1.0)
      elif fitness_val == 2:
        pair = (individual, 2.0)
      elif fitness_val == 3: 
        pair = (individual, 3.0)
      weighted_population.append(pair)
      # print weighted_population

    weighted_population.sort(key = custom_sort)
    weighted_population.reverse
    weighted_population = weighted_population[:POP_SIZE/2]
    population = []
    # print len/(weighted_population)

    for individual, bigness in weighted_population:
      #Select
      ind1 = individual
      ind2 = individual

      #Crossover
      ind1, ind2 = crossover(ind1, ind2)
      population.append(mutate(ind1))
      population.append(mutate(ind2))