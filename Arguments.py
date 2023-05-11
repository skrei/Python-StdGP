from sys import argv

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-StdGP
#
# Copyright ©2019-2022 J. E. Batista
#


# Operators to be used by the models
# Only these operators are available. To add mode, edit m3gp.Node.calculate(self, sample)

#OPERATORS = [("+",2),("-",2),("*",2),("/",2),("log2",1), ("max", 3)] # Example
OPERATORS = [("+",2),("-",2),("*",2),("/",2)] # Default

# Initial Maximum depth
MAX_DEPTH = 6

# Number of models in the population
POPULATION_SIZE = 100

# Maximum number of iterations
MAX_GENERATION = 25

# Fraction of the dataset to be used as training (used by Main_M3GP_standalone.py)
TRAIN_FRACTION = 0.70

# Number of individuals to be used in the tournament
TOURNAMENT_SIZE = 5

# Number of best individuals to be automatically moved to the next generation
ELITISM_SIZE = 1

# Shuffle the dataset (used by Main_M3GP_standalone.py)
SHUFFLE = True

# Dimensions maximum depth
LIMIT_DEPTH=17

# Number of runs (used by Main_M3GP_standalone.py)
RUNS = 30

# Verbose
VERBOSE = True

# Number of CPU Threads to be used
THREADS = 1

# Random state
RANDOM_STATE = 42

# Models wrapped by the StdGP models
MODEL_NAME = ["SimpleThresholdClassifier"][0]

# Fitness used by the M3GP models
FITNESS_TYPE = ["Accuracy", "MSE", "WAF", "2FOLD"][0]



DATASETS_DIR = "datasets/"
OUTPUT_DIR = "results/"

DATASETS = ["heart.csv"]
OUTPUT = "Classification"




if "-dsdir" in argv:
	DATASETS_DIR = argv[argv.index("-dsdir")+1]

if "-odir" in argv:
	OUTPUT_DIR = argv[argv.index("-odir")+1]

if "-d" in argv:
	DATASETS = argv[argv.index("-d")+1].split(";")

if "-runs" in argv:
	RUNS = int(argv[argv.index("-runs")+1])

if "-op" in argv:
	OPERATORS = argv[argv.index("-op")+1].split(";")
	for i in range(len(OPERATORS)):
		OPERATORS[i] = OPERATORS[i].split(",")
		OPERATORS[i][1] = int(OPERATORS[i][1])

if "-md" in argv:
	MAX_DEPTH = int(argv[argv.index("-md")+1])

if "-ps" in argv:
	POPULATION_SIZE = int(argv[argv.index("-ps")+1])

if "-mg" in argv:
	MAX_GENERATION = int(argv[argv.index("-mg")+1])

if "-tf" in argv:
	TRAIN_FRACTION = float(argv[argv.index("-tf")+1])

if "-ts" in argv:
	TOURNAMENT_SIZE = int(argv[argv.index("-ts")+1])

if "-es" in argv:
	ELITISM_SIZE = int(argv[argv.index("-es")+1])

if "-dontshuffle" in argv:
	SHUFFLE = False

if "-s" in argv:
	VERBOSE = False

if "-t" in argv:
	THREADS = int(argv[argv.index("-t")+1])

if "-rs" in argv:
	RANDOM_STATE = int(argv[argv.index("-rs")+1])



