# ga-nqueens Max Cekanowski, Lucas Marteau

import random

#initialisation of the first population genom
def init_board(size, n):
    pop = []
    for i in range(size):
        geno = list(range(n))
        random.shuffle(geno)
        pop.append(geno)
    return (pop)

def check_fit(board):
    conflicts = 0
    n = len(board)

    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board [j] or abs(i - j) == abs(board[i] - board[j]):
                conflicts += 1
            
    return conflicts


def turbo_mutation(genom, mutrate):
    if random.random() < mutrate:
        i, j = random.sample(range(len(genom)), 2)
        genom[i], genom[j] = genom[j], genom[i]


def parents_getter(pop, numberOfParents):
    return sorted(pop, key=check_fit)[:numberOfParents]


def crossover(p1, p2):
    n = len(p1)
    crossover_point = random.randint(1, n - 1)

    child = [-1] * n 

    child[:crossover_point] = p1[:crossover_point]

    for gene in p2:
        if gene not in child:
            for i in range(n):
                if child[i] == -1:
                    child[i] = gene
                    break

    return child

def genetic_algorithm(n, pop_size, num_gen, mutrate):
    pop = init_board(pop_size, n)
    for gen in range(num_gen):
        parents = parents_getter(pop, pop_size // 2)
        new_pop = []
        while len(new_pop) < pop_size:
            p1, p2 = random.sample(parents, 2)
            child = crossover(p1, p2)
            turbo_mutation(child, mutrate)
            new_pop.append(child)
        pop = new_pop
        best_genome = min(pop, key=check_fit)
        best_fitness = check_fit(best_genome)
        print(f"Generation {gen+1}: Best Fitness = {best_fitness}")
        if best_fitness == 0:
            print("Solution found:", best_genome)
            break

if __name__ == "__main__":
    n_queens = 8
    population_size = 100
    num_generations = 100000
    mutation_rate = 0.1
    genetic_algorithm(n_queens, population_size, num_generations, mutation_rate)