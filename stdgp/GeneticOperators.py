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

    best = None    # The best individual found so far.
    fittest = []   # The list of fittest individuals.
    smallest = []  # The list of smallest individuals.

    if Switch == False and Sf >= Sp:
        # If `Switch` is `False`, run a fitness tournament first followed by a parsimony tournament.

        # Run `Sf` fitness tournaments and save the best individual from each tournament to `fittest`.
        for _ in range(Sf):
            fittest.append(fitness_tournament(rng, population, n))

        # Run `Sp` parsimony tournaments, where each competitor is selected from `fittest`.
        for _ in range(Sp):
      
            competitor = rng.choice(fittest)
            competitor_size = competitor.size
            competitor_fitness = 1 / (1 + competitor_size)
            # Update `best` if the competitor has a higher parsimony measure than the current best individual.
            if best is None or competitor_fitness > best[1]:
                best = (competitor, competitor_fitness)
            # If the competitor has the same parsimony measure as the current best individual, randomly choose between them.
            elif competitor_fitness == best[1]:
                if rng.random() < 0.5:
                    best = (competitor, competitor_fitness)

        return best[0]

    elif Switch == True and Sf <= Sp:
        # If `Switch` is `True`, run a parsimony tournament first followed by a fitness tournament.

        # Run `Sp` parsimony tournaments and save the best individual from each tournament to `smallest`.
        for _ in range(Sp):
            smallest.append(parsimony_tournament(rng, population, n))

        # Run `Sf` fitness tournaments, where each competitor is selected from `smallest`.
        for _ in range(Sf):

            competitor = rng.choice(smallest)
            competitor_fitness = competitor.fitness
            # Update `best` if the competitor has a higher fitness measure than the current best individual.
            if best is None or competitor_fitness > best[1]:
                best = (competitor, competitor_fitness)
            # If the competitor has the same fitness measure as the current best individual, randomly choose between them.
            elif competitor_fitness == best[1]:
                if rng.random() < 0.5:
                    best = (competitor, competitor_fitness)

        return best[0]

    else:
        # If the values of `Sf` and `Sp` are incompatible with the value of `Switch`, raise an exception.
        raise Exception('Incompatible values of Sf and Sp')




def parsimony_tournament(rng, population, n):
	
	#Selects "n" Individuals from the population and return a 
	#single Individual - selecting the shortest one..
	
	best = None
	for _ in range(n):
		competitor = rng.choice(population)
		competitor_size = competitor.size
		competitor_fitness = 1 / (1 + competitor_size)
		if best is None or competitor_fitness > best[1]:
			best = (competitor, competitor_fitness)
	return best[0]


def fitness_tournament(rng, population,n):
	
	#Selects "n" Individuals from the population and return a 
	#single Individual.

	#Parameters:
	#population (list): A list of Individuals, sorted from best to worse.
	

	candidates = [rng.randint(0,len(population)-1) for i in range(n)]
	return population[min(candidates)]


def getElite(population,n):
	
	#Returns the "n" best Individuals in the population.

	#Parameters:
	#population (list): A list of Individuals, sorted from best to worse.
	
	return population[:n]


def getOffspring(rng, population, tournament_size, Sf, Sp, Switch):
	
	#Genetic Operator: Selects a genetic operator and returns a list with the 
	#offspring Individuals. The crossover GOs return two Individuals and the
	#mutation GO returns one individual. Individuals over the LIMIT_DEPTH are 
	#then excluded, making it possible for this method to return an empty list.

	#Parameters:
	#population (list): A list of Individuals, sorted from best to worse.
	
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
	
	#Randomly selects one node from each of two individuals; swaps the node and
	#sub-nodes; and returns the two new Individuals as the offspring.

	#Parameters:
	#population (list): A list of Individuals, sorted from best to worse.
	
	ind1 = double_tournament(rng, population, tournament_size, Sf=Sf, Sp=Sp, Switch=Switch)
	ind2 = double_tournament(rng, population, tournament_size, Sf=Sf, Sp=Sp, Switch=Switch)

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
	
	#Randomly selects one node from a single individual; swaps the node with a 
	#new, node generated using Grow; and returns the new Individual as the offspring.

	#Parameters:
	#population (list): A list of Individuals, sorted from best to worse.
	
	ind1 = double_tournament(rng, population, tournament_size, Sf=Sf, Sp=Sp, Switch=Switch)
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
