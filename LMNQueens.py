import sys
import random

MAX_GENERATIONS = 1000
MUTATION_RATE = 3
INITIAL_POPULATION_SIZE = 10000
MAX_BOARD_SIZE = 50
LITTLE_BOARD_PERCENTAGE = 0.6
LITTLE_BOARD_BIG_BOARD_DIFF = 14
CROSSOVER_PERCENTAGE = 0.4

class Sample:
    def __init__(self, queens:list):
        self.queens = queens
        self.conflictList = [0 for _ in queens]
        self.conflicts = 0
        self.compute_conflicts()
    
    def compute_conflicts(self):
        for i, queen in enumerate(self.queens):
            for j, other_queen in enumerate(self.queens):
                if i == j:
                    continue
                if queen == other_queen: # horizontal
                    self.conflictList[i] += 1
                if queen + (j - i) == other_queen or queen + (i - j) == other_queen: # diagonal (les deux)
                    self.conflictList[i] += 1
        self.conflicts = sum(self.conflictList)

class Generation:
    def __init__(self ,parent1: list, parent2: list):
        self.first_parent = parent1
        self.second_parent = parent2
        self.child1: Sample = None
        self.child2: Sample = None
        self.cross_over()
    
    def cross_over(self):
        size: int = round(len(self.first_parent) * CROSSOVER_PERCENTAGE)
        child1: list = []
        child2: list = []

        child1.extend(self.first_parent[:size])
        child1.extend(self.first_parent[size:])
        child2.extend(self.second_parent[:size])
        child2.extend(self.second_parent[size:])

        isMutation : int = random.randint(1, 100)

        if isMutation <= MUTATION_RATE:
            self.child1 = self.mutate(child1)
            self.child2 = self.mutate(child2)
        else:
            self.child1 = Sample(child1)
            self.child2 = Sample(child2)

    def mutate(self, new_sample: list) -> Sample:
        new_sample[random.randint(0, len(new_sample) - 1)] = random.randint(0, len(new_sample) - 1)
        return (Sample(new_sample))
        

def round(nb: float) -> int:
    decimal: float  = nb - int(nb)
    
    if decimal >= 0.5:
        return int(nb) + 1  
    return int(nb)  


def main(arg: int) -> None:
    first_sample: list = [random.sample(range(arg), arg) for _ in range(INITIAL_POPULATION_SIZE)]
    initial_population: list = sorted([Sample(each) for each in first_sample], key=lambda x: x.conflicts)

    if (arg <= LITTLE_BOARD_BIG_BOARD_DIFF):
        initial_population = initial_population[0:round(len(initial_population) * LITTLE_BOARD_PERCENTAGE):1]
    else:
        print()

    for i in range(MAX_GENERATIONS):
        print(i)
        gen_population = [Generation(initial_population[i].queens, initial_population[i + 1].queens) for i in range(len(initial_population) - 1)]
        initial_population.clear()
        for each in gen_population:
            initial_population.append(each.child1)
            initial_population.append(each.child2)
        initial_population.sort(key= lambda x: x.conflicts)
        initial_population = initial_population[0:300:1]
        print(initial_population[0].conflicts)
        if (initial_population[0].conflicts == 0):
            print([[i, queen] for i, queen in enumerate(initial_population[0].queens)])
            break

def test_args(argv: list) -> None:
    try:
        if (len(argv) != 2 or int(argv[1]) <= 3 or int(argv[1]) > MAX_BOARD_SIZE):
            raise Exception("Arguments must be an int over 3 and under " + str(MAX_BOARD_SIZE) + ".")
    except ValueError:
        raise Exception("First and only argument should be an int")
    except Exception as e:
            raise e


if __name__ == "__main__":
    # try:
        # test_args(sys.argv)
    main(int(sys.argv[1]))
    # except Exception as e:
        # print(e)
        # exit(84)