import random
import numpy as np
from multiprocessing import Pool, Value, Manager, Lock
import time
import sys
from collections import deque
import os

def initialize_population(board_size, population_size):
    population = []
    for _ in range(population_size):
        solution = list(np.random.permutation(board_size))
        population.append(solution)
    return population

def calculate_fitness(solution):
    board_size = len(solution)
    conflicts = 0
    row_counts = [0] * board_size
    diag1_counts = [0] * (2 * board_size - 1)
    diag2_counts = [0] * (2 * board_size - 1)

    for col, row in enumerate(solution):
        if col < board_size and row < board_size:
            conflicts += row_counts[col] + diag1_counts[row - col] + diag2_counts[row + col]
            row_counts[col] += 1
            diag1_counts[row - col] += 1
            diag2_counts[row + col] += 1

    return conflicts

def select_parents(population, num_parents):
    parents = random.choices(population, k=num_parents, weights=[1.0 / (calculate_fitness(solution) + 1) for solution in population])
    return parents

def crossover(parent1, parent2):
    board_size = len(parent1)
    crossover_point = random.randint(1, board_size - 1)
    child = parent1[:crossover_point] + [gene for gene in parent2 if gene not in parent1[:crossover_point]]
    return child

def mutate(solution, mutation_rate):
    if random.random() < mutation_rate:
        board_size = len(solution)
        col = random.randint(0, board_size - 1)
        new_row = random.randint(0, board_size - 1)
        solution[col] = new_row

def find_problematic_queen(solution):
    board_size = len(solution)
    row_counts = [0] * board_size
    diag1_counts = [0] * (2 * board_size - 1)
    diag2_counts = [0] * (2 * board_size - 1)

    for col, row in enumerate(solution):
        if col < board_size and row < board_size:
            if row_counts[col] > 1 or diag1_counts[row - col] > 1 or diag2_counts[row + col] > 1:
                return col

            row_counts[col] += 1
            diag1_counts[row - col] += 1
            diag2_counts[row + col] += 1

    return None

def worker(board_size, population_size, num_generations, mutation_rate, max_consecutive_conflicts, consecutive_generations_threshold):
    seed = os.getpid()  # Utilisez l'identifiant unique du processus comme graine
    random.seed(seed)
    population = initialize_population(board_size, population_size)
    consecutive_conflicts = 0
    best_solution_queue = deque(maxlen=consecutive_generations_threshold)
    
    for generation in range(num_generations):
        if result_found.value == 1:
            break
        
        parents = select_parents(population, population_size // 2)
        children = []

        for i in range(0, len(parents), 2):
            child = crossover(parents[i], parents[i + 1])
            mutate(child, mutation_rate)

            if calculate_fitness(child) == calculate_fitness(parents[i]):
                consecutive_conflicts += 1
            else:
                consecutive_conflicts = 0

            if consecutive_conflicts >= max_consecutive_conflicts:
                problematic_queen_col = find_problematic_queen(child)
                if problematic_queen_col is not None:
                    new_col = random.randint(0, board_size - 1)
                    child[problematic_queen_col] = new_col
                consecutive_conflicts = 0

            children.append(child)

        population = parents + children

        best_solution = min(population, key=calculate_fitness)
        best_fitness = calculate_fitness(best_solution)
        best_solution_queue.append(best_solution)

        if len(best_solution_queue) == consecutive_generations_threshold and all(np.array_equal(best_solution, sol) for sol in best_solution_queue):
            problematic_queen_col = find_problematic_queen(best_solution)
            if problematic_queen_col is not None:
                new_col = random.randint(0, board_size - 1)
                best_solution[problematic_queen_col] = new_col
            best_solution_queue.clear()

        print(f"Process-{seed}: Generation {generation + 1}: Best Fitness = {best_fitness}")

        if best_fitness == 0:
            print(f"Process-{seed}: Solution trouvée :", best_solution)
            with result_lock:
                if result_found.value == 0:
                    result_found.value = 1
                    result.append(best_solution)

def genetic_algorithm_multithread(board_size, population_size, num_generations, mutation_rate, max_consecutive_conflicts, consecutive_generations_threshold, num_processes):
    result_lock = Lock()
    result_found = Value('i', 0)
    result = []
    
    with Pool(processes=num_processes) as pool:
        pool.starmap(worker, [(board_size, population_size, num_generations, mutation_rate, max_consecutive_conflicts, consecutive_generations_threshold, i, result_lock, result_found) for i in range(num_processes)])
    
    return result



# ...

if __name__ == "__main__":
    start_time = time.time()
    board_size = int(sys.argv[1])
    population_size = 1000
    num_generations = 100000
    mutation_rate = 0.02
    max_consecutive_conflicts = 50
    consecutive_generations_threshold = 15
    num_processes = 4
    
    manager = Manager()
    result_lock = manager.Lock()
    result_found = manager.Value('i', 0)
    result = manager.list()
    
    with Pool(processes=num_processes) as pool:
        pool.starmap(worker, [(board_size, population_size, num_generations, mutation_rate, max_consecutive_conflicts, consecutive_generations_threshold) for _ in range(num_processes)])
    
    current_time = time.time()
    elapsed_time = current_time - start_time
    print(f"Temps total d'exécution : {elapsed_time} secondes")
