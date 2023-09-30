import sys
import numpy as np
from collections import deque
import random
import time

class Properties:
    SAMPLE_SIZE: int = 1000
    MAX_GENERATION: int = 10000
    MUTATION_RATE: int = 0.02
    CONSECUTIVE_GENERATIONS_TRESHOLD: int = 15
    BOARD_SIZE: int | None = None 

def test_arg(arg_length: int, args: []) -> None:
    if arg_length != 2:
        raise Exception("Incorrect number of arguments")
    try:
        int(args[1])
    except:
        raise Exception("Argument not well formated")
    if int(args[1]) < 4:
        raise Exception("Argument must be over 3")

def calculate_fitness(item):
    
    row_counts = [0] * Properties.BOARD_SIZE
    diag1_counts = [0] * (2 * Properties.BOARD_SIZE - 1)
    diag2_counts = [0] * (2 * Properties.BOARD_SIZE - 1)
    
    conflicts = 0

    for col, row in enumerate(item):
        if col < Properties.BOARD_SIZE and row < Properties.BOARD_SIZE:
            conflicts += row_counts[col] + diag1_counts[row - col] + diag2_counts[row + col]
            row_counts[col] += 1
            diag1_counts[row - col] += 1
            diag2_counts[row + col] += 1
    return conflicts

def select_parents(sample):
    parents = random.choices(sample, k=Properties.SAMPLE_SIZE // 2, weights=[1.0 / (calculate_fitness(each) + 1) for each in sample])
    return parents

def crossover(parent1: list[int], parent2: list[int]) -> list[int]:
    crossover_point = random.randint(1, Properties.BOARD_SIZE - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def mutate(child):
    if random.random() < Properties.MUTATION_RATE:
        child[random.randint(0, Properties.BOARD_SIZE - 1)] = random.randint(0, Properties.BOARD_SIZE - 1)
    return child
    
def all_equal(best_solution_queue):

    nb = best_solution_queue[0]

    for i in range(len(best_solution_queue)):
        if best_solution_queue[i] != nb:
            return False
    return True

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

    return None

def genetical_algorithm():
    sample  = [list(np.random.permutation(Properties.BOARD_SIZE)) for _ in range(Properties.SAMPLE_SIZE)]
    best_solution_queue = deque(maxlen=Properties.CONSECUTIVE_GENERATIONS_TRESHOLD) #You can remove first or last element with deque -> double-ended queue
    
    for generation in range(Properties.MAX_GENERATION):
        parents = select_parents(sample)
        children = []

        for i in range(0, len(parents) - 1, 1):
            child = crossover(parents[i], parents[i + 1])
            child = mutate(child)
            children.append(child)

        sample = parents + children
        best_solution = min(sample, key=calculate_fitness)
        best_solution_fitness = calculate_fitness(best_solution)
        best_solution_queue.append(best_solution)

        if best_solution_fitness == 0:
            print("Solution trouvée à la génération " + str((generation + 1)) + ":", best_solution)
            break

        if len(best_solution_queue) == 15 and all_equal(best_solution_queue):
            problematic_queen_index = find_problematic_queen(best_solution)
            if problematic_queen_index is not None:
                best_solution[problematic_queen_index] = random.randint(0, Properties.BOARD_SIZE - 1)
            best_solution_queue.clear();

        print(f"Generation {generation + 1}: Best Fitness = {best_solution_fitness}")
    return best_solution

if __name__ == "__main__":
    start_time = time.time()
    try:
        test_arg(len(sys.argv), sys.argv);
        Properties.BOARD_SIZE = int(sys.argv[1]) 
        genetical_algorithm()
    except Exception as e:
        print(str(e))
        sys.exit(1);
    print(f"Temps total d'exécution : {time.time() - start_time} secondes")

