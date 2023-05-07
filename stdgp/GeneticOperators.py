from .Individual import Individual
from .Node import Node

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-StdGP
#
# Copyright ©2019-2022 J. E. Batista
#


def double_tournament(rng, population, n, Sf, Sp, Switch):
    # Initialize variables for the best individual, fittest individuals, and smallest individuals
    best = None
    fittest = []
    smallest = []
    
    # Define fitness function that returns the fitness of an individual
    def fitness(individual):
        size = individual.size
        return 1 / (1 + size)
    
    # Determine the list of individuals to use in the tournament
    if Switch:
        # If Switch is True, select fittest individuals from the entire population using the fitness_tournament function
        fittest = [fitness_tournament(rng, population, n) for _ in range(Sp)]
    else:
        # If Switch is False, select fittest individuals from a subset of the population using the fitness_tournament function
        fittest = [fitness_tournament(rng, population, n) for _ in range(Sf)]
    
    # Run the tournament and select the winner
    if Switch:
        # If Switch is True, select the individual from population that is both in fittest and has the lowest fitness
        fittest_idx = min(range(len(population)), key=lambda idx: fitness(population[idx]) if population[idx] in fittest else float('inf'))
        return population[fittest_idx]
    else:
        # If Switch is False, run a tournament among the fittest individuals and return the winner
        for _ in range(Sp):
            # Select a competitor from the fittest individuals at random
            competitor = rng.choice(fittest)
            # Calculate the size and fitness of the competitor
            competitor_size = competitor.size
            competitor_fitness = 1 / (1 + competitor_size)
            # If the competitor is the best so far, update the best individual
            if best is None or competitor_fitness > best[1]:
                best = (competitor, competitor_fitness)
        return best[0]




def getElite(population,n):
	'''
	Returns the "n" best Individuals in the population.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	return population[:n]

def parsimony_tournament(rng, population, n):
    # Define fitness function that returns the fitness of an individual
    def fitness(individual):
        size = individual.size
        return 1 / (1 + size)
    
    # Select n competitors from the population at random
    competitors = rng.choice(population, size=n, replace=False)
    
    # Evaluate the fitness of each competitor
    competitor_fitnesses = [fitness(competitor) for competitor in competitors]
    
    # Select the competitor with the highest fitness
    best_idx = max(range(n), key=lambda idx: competitor_fitnesses[idx])
    best = competitors[best_idx]
    
    return best


def fitness_tournament(rng, population,n):
	'''
	Selects "n" Individuals from the population and return a 
	single Individual.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''

	candidates = [rng.randint(0,len(population)-1) for i in range(n)]
	return population[min(candidates)]

def getOffspring(rng, population, tournament_size, Sf, Sp, Switch):
	'''
	Genetic Operator: Selects a genetic operator and returns a list with the 
	offspring Individuals. The crossover GOs return two Individuals and the
	mutation GO returns one individual. Individuals over the LIMIT_DEPTH are 
	then excluded, making it possible for this method to return an empty list.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	isCross = rng.random()<0.5

	desc = None

	if isCross:
		desc = STXO(rng, population, tournament_size, Sf, Sp, Switch)
	else:
		desc = STMUT(rng, population, tournament_size, Sf, Sp, Switch)

	return desc


def discardDeep(population, limit):
	ret = []
	for ind in population:
		if ind.getDepth() <= limit:
			ret.append(ind)
	return ret


def STXO(rng, population, tournament_size, Sf, Sp, Switch):
	'''
	Randomly selects one node from each of two individuals; swaps the node and
	sub-nodes; and returns the two new Individuals as the offspring.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	ind1 = double_tournament(rng, population, tournament_size, Sf, Sp, Switch)
	ind2 = double_tournament(rng, population, tournament_size, Sf, Sp, Switch)

	h1 = ind1.getHead()
	h2 = ind2.getHead()

	n1 = h1.getRandomNode(rng)
	n2 = h2.getRandomNode(rng)

	n1.swap(n2)

	ret = []
	for h in [h1,h2]:
		i = Individual(ind1.operators, ind1.terminals, ind1.max_depth, ind1.model_name, ind1.fitnessType)
		i.copy(h)
		ret.append(i)
	return ret


def STMUT(rng, population, tournament_size, Sf, Sp, Switch):
	'''
	Randomly selects one node from a single individual; swaps the node with a 
	new, node generated using Grow; and returns the new Individual as the offspring.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	ind1 = double_tournament(rng, population, tournament_size, Sf, Sp, Switch)
	h1 = ind1.getHead()
	n1 = h1.getRandomNode(rng)
	n = Node()
	n.create(rng, ind1.operators, ind1.terminals, ind1.max_depth)
	n1.swap(n)


	ret = []
	i = Individual(ind1.operators, ind1.terminals, ind1.max_depth, ind1.model_name, ind1.fitnessType)
	i.copy(h1)
	ret.append(i)
	return ret
