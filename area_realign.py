from deap import base
from deap import creator
from deap import tools
from deap import algorithms

import random
import array
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

from ga_area_functions import DistrictRealignment

start_time = time.time()

dr = DistrictRealignment()

# Genetic Algorithm constants:
POPULATION_SIZE = 100
P_CROSSOVER = 0.9  # Probability for crossover
P_MUTATION = 0.15   # Probability for mutating an individual
MAX_GENERATIONS = 15000
HALL_OF_FAME_SIZE = 10

toolbox = base.Toolbox()

""" Set fitness strategy - minimize area distance 
and quality difference from ideal.
1) Distance between clubs in an area in sequence
2) Quality score distribution absolute difference from 0.35
- minimize.
"""

creator.create("MultiFit", base.Fitness, weights=(-1.0, ))

# Create the Individual type based on a list of integers
creator.create('Individual', array.array, typecode='i', 
                fitness=creator.MultiFit)

# A tool to create the shuffled district indices
toolbox.register('random_ordering', random.sample,
                    range(len(dr)), len(dr))

# A tool that creates individuals (a district)
toolbox.register('individual_creator', tools.initIterate,
                  creator.Individual, toolbox.random_ordering)

# A tool that creates a population (multiple districts)
toolbox.register('population_creator', tools.initRepeat, 
                  list, toolbox.individual_creator)

# Register evaluation function
toolbox.register('evaluate', dr.evaluate_district)

# Genetic operators:
toolbox.register("select", tools.selTournament, tournsize=2)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1.0/len(dr))
toolbox.register("mate", tools.cxUniformPartialyMatched, indpb=2.0/len(dr))

# Genetic Algorithm flow:
def main():

    population = toolbox.population_creator(n=POPULATION_SIZE)

    stats = tools.Statistics(key=lambda ind: ind.fitness.values)
    stats.register('min', np.min, axis=0)
    stats.register('avg', np.mean, axis=0)

    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    population, logbook = algorithms.eaSimple(
                                population, toolbox, 
                                cxpb=P_CROSSOVER, 
                                mutpb=P_MUTATION, 
                                ngen=MAX_GENERATIONS, 
                                stats=stats, 
                                halloffame=hof, 
                                verbose=True)

    # Print metrics
    execution_time = (time.time() - start_time)
    
    best = hof.items[0]
    print(f'Best district is {best}.')
    print(f'Execution time is {execution_time} seconds.')
    print(f'Best distance score is {best.fitness.values[0]}')

    # Plot stats
    min_val, avg_val = logbook.select('min', 'avg')
    
    plt.figure(1)
    sns.set_style("whitegrid")
    plt.plot(min_val, color='red')
    plt.plot(avg_val, color='green')
    plt.xlabel('Generation')
    plt.ylabel('Min / Average Fitness')
    plt.title('Min and Average fitness over Generations')

    # show both plots:
    plt.show()

    with open('../data/best_areas_index.pkl', 'wb') as f:  
        pickle.dump(best, f)


if __name__ == "__main__":
    main()
