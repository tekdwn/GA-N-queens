import random
import numpy as np
from collections import deque
import time
import sys

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
    child = parent1[:crossover_point] + parent2[crossover_point:]

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
                return col  # Retourne la colonne de la première reine avec des conflits

            row_counts[col] += 1
            diag1_counts[row - col] += 1
            diag2_counts[row + col] += 1

    return None  # S'il n'y a pas de reine problématique, retourne None
def genetic_algorithm(board_size, population_size, num_generations, mutation_rate, max_consecutive_conflicts, consecutive_generations_threshold):
    population = initialize_population(board_size, population_size)
    consecutive_conflicts = 0
    best_solution_queue = deque(maxlen=consecutive_generations_threshold)  # File pour stocker les meilleures solutions des générations précédentes

    for generation in range(num_generations):
        parents = select_parents(population, population_size // 2)
        children = []

        for i in range(0, len(parents), 2):
            child = crossover(parents[i], parents[i + 1])
            mutate(child, mutation_rate)
            children.append(child)

        population = parents + children

        best_solution = min(population, key=calculate_fitness)
        best_fitness = calculate_fitness(best_solution)
        best_solution_queue.append(best_solution)  # Ajoute la meilleure solution actuelle à la file

        if len(best_solution_queue) == consecutive_generations_threshold and all(np.array_equal(best_solution, sol) for sol in best_solution_queue):
            problematic_queen_col = find_problematic_queen(best_solution)
            if problematic_queen_col is not None:
                new_col = random.randint(0, board_size - 1)
                best_solution[problematic_queen_col] = new_col
            best_solution_queue.clear()  # Efface la file pour éviter des mutations excessives

        print(f"Generation {generation + 1}: Best Fitness = {best_fitness}")

        if best_fitness == 0:
            print(len(best_solution))
            print("Solution trouvée :", best_solution)
            break

    return best_solution

if __name__ == "__main__":
    start_time = time.time()
    board_size = int(sys.argv[1])
    population_size = 1000
    num_generations = 100000
    mutation_rate = 0.02
    max_consecutive_conflicts = 50
    consecutive_generations_threshold = 15
    solution = genetic_algorithm(board_size, population_size, num_generations, mutation_rate, max_consecutive_conflicts, consecutive_generations_threshold)
    current_time = time.time()
    elapsed_time = current_time - start_time
    print(f"Temps total d'exécution : {elapsed_time} secondes")
