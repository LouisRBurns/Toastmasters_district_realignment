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
import pickle

from ga_division_functions import AreaAlignment

start_time = time.time()

aa = AreaAlignment()

# Genetic Algorithm constants:
POPULATION_SIZE = 100
P_CROSSOVER = 0.9  # Probability for crossover
P_MUTATION = 0.15   # Probability for mutating an individual
MAX_GENERATIONS = 10000
HALL_OF_FAME_SIZE = 10

toolbox = base.Toolbox()

creator.create("MinFit", base.Fitness, weights=(-1.0, ))

# Create the Individual type based on a list of integers
creator.create('Individual', array.array, typecode='i', 
                fitness=creator.MinFit)

# A tool to create the shuffled district indices
toolbox.register('random_ordering', random.sample,
                    range(len(aa)), len(aa))

# A tool that creates individuals (a district)
toolbox.register('individual_creator', tools.initIterate,
                  creator.Individual, toolbox.random_ordering)

# A tool that creates a population (multiple districts)
toolbox.register('population_creator', tools.initRepeat, 
                  list, toolbox.individual_creator)

# Register evaluation function
toolbox.register('evaluate', aa.evaluate_district)

# Genetic operators:
toolbox.register("select", tools.selTournament, tournsize=2)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1.0/len(aa))
toolbox.register("mate", tools.cxUniformPartialyMatched, indpb=2.0/len(aa))

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

    with open('../data/best_divisions_index.pkl', 'wb') as f:  
        pickle.dump(best, f)

if __name__ == "__main__":
    main()
