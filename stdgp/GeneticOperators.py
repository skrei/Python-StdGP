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
    # Check the value of the switch variable
    if Switch == False:
        # Perform Sf tournaments and select the fittest individual from each tournament
        fittest = [fitness_tournament(rng, population, n) for _ in range(Sf)]
        # Select the fittest individual from all tournaments
        best = max(fittest, key=lambda x: x.fitness)
    else:
        # Perform Sp tournaments and get the fittest individuals
        fittest = [fitness_tournament(rng, population, n) for _ in range(Sp)]
    
    # Select the candidates from population that were part of fittest
    candidates = [individual for individual in population if individual in fittest]
    # Select the fittest individual from the candidates based on fitness
    fittest_individual = min(candidates, key=lambda x: x.fitness)
    # Set the best individual to be the fittest individual
    best = fittest_individual
    
    # Return the best individual
    return best




def getElite(population,n):
	'''
	Returns the "n" best Individuals in the population.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	return population[:n]

def parsimony_tournament(rng, population, n):
    # Select `tournament_size` random individuals from the population
    tournament = [rng.choice(population) for _ in range(n)]
    
    # Find the fittest individual in the tournament based on size and fitness
    fittest_individual = min(tournament, key=lambda ind: (ind.fitness, ind.size))
    
    # Return the fittest individual
    return fittest_individual

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
	ind1 = fitness_tournament(rng, population, tournament_size, Sf, Sp, Switch)
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
