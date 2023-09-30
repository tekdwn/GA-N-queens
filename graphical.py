import tkinter as tk
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







# Fonction pour résoudre le problème des N-Queens (vous devez implémenter votre propre algorithme ici)
def solve_nqueens(board_size, mutation_rate, generation_max):
    # Implémentez votre algorithme N-Queens ici
    pass

# Fonction pour afficher le plateau
def display_board(board, canvas):
    canvas.delete("all")
    board_size = len(board)
    
    # Calcul de la taille des cases pour que la dernière case des lignes atteigne 75% de la largeur de la partie gauche
    left_width = board_frame.winfo_width()
    long = left_width // board_size
    larg = board_frame.winfo_height() // board_size

    long2 = (board_frame.winfo_width() - long * board_size) / board_size
    larg2 = (board_frame.winfo_height() - larg * board_size) / board_size
    print(long2, larg2)
    rect_longueur = long2 + long
    rect_largeur = larg2 + larg

    
    print(board_frame.winfo_height(), rect_largeur)
    for row in range(board_size):
        for col in range(board_size):
            if (row + col) % 2 == 0:
                canvas.create_rectangle(col * rect_longueur, row * rect_largeur,
                                        (col + 1) * rect_longueur, (row + 1) * rect_largeur,
                                        fill="white")
            else:
                canvas.create_rectangle(col * rect_longueur, row * rect_largeur,
                                        (col + 1) * rect_longueur, (row + 1) * rect_largeur,
                                        fill="red")

    for col, row in enumerate(board):
        canvas.create_text(int(col * rect_longueur + rect_longueur // 2),
                           int(row * rect_largeur + rect_largeur // 2),
                           text="Q", font=("Arial", int(rect_longueur // 2)), fill="black")

# Fonction appelée lorsque le bouton "Go" est cliqué
def start_algorithm():
    Properties.BOARD_SIZE = int(board_size_entry.get())
    Properties.MUTATION_RATE = float(mutation_rate_entry.get())
    Properties.MAX_GENERATION = int(generation_max_entry.get())


    board = [random.randint(0, Properties.BOARD_SIZE - 1) for _ in range(Properties.BOARD_SIZE)]

    display_board(genetical_algorithm(), board_canvas)

# Création de la fenêtre principale
root = tk.Tk()
root.attributes('-fullscreen', True)
root.title("N-Queens Solver")

# Définir la taille de la fenêtre principale pour qu'elle occupe tout l'écran
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}")

# Crée un cadre à gauche pour afficher le tableau
board_frame = tk.Frame(root, height=screen_height)
board_frame.grid(row=0, column=0, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=3)

# Crée un canevas pour afficher le tableau
board_canvas = tk.Canvas(board_frame, bg="white")
board_canvas.pack(fill="both", expand=True)

# Crée un cadre à droite pour les entrées utilisateur et le bouton
input_frame = tk.Frame(root, width=screen_width * 0.25, height=screen_height)
input_frame.grid(row=0, column=1, sticky="nsew")
root.grid_columnconfigure(1, weight=1)

# Crée un cadre à l'intérieur du cadre de droite pour les widgets que vous souhaitez organiser avec grid
grid_frame = tk.Frame(input_frame, padx=20, pady=screen_height // 4)  # Ajoutez de l'espacement
grid_frame.grid(row=0, column=0, sticky="nsew")

# Crée des étiquettes et des entrées pour les paramètres
label_board_size = tk.Label(grid_frame, text="Board size?", font=("Arial", 14))  # Augmente la taille de la police
label_board_size.grid(row=0, column=0, sticky="w")
board_size_entry = tk.Entry(grid_frame)
board_size_entry.grid(row=1, column=0, padx=(0, 20))  # Ajoutez un espacement à droite

label_mutation_rate = tk.Label(grid_frame, text="Mutation rate? (between 0 and 1)", font=("Arial", 14))
label_mutation_rate.grid(row=2, column=0, sticky="w")
mutation_rate_entry = tk.Entry(grid_frame)
mutation_rate_entry.grid(row=3, column=0, padx=(0, 20))

label_generation_max = tk.Label(grid_frame, text="Generation Max", font=("Arial", 14))
label_generation_max.grid(row=4, column=0, sticky="w")
generation_max_entry = tk.Entry(grid_frame)
generation_max_entry.grid(row=5, column=0, padx=(0, 20))

# Crée un bouton "Go" pour lancer l'algorithme dans le cadre à droite
go_button = tk.Button(grid_frame, text="Go", command=start_algorithm)
go_button.grid(row=6, column=0, pady=10)

# Crée un bouton "Fermer" pour quitter l'application dans le cadre à droite
bouton_fermer = tk.Button(input_frame, text="Fermer", command=root.quit)
bouton_fermer.grid(row=1, column=1, pady=(screen_height // 10, 0), padx=(0, 0), sticky="s")

# Configuration de la grille pour pousser les widgets vers le haut et la droite
input_frame.grid_rowconfigure(0, weight=1)
input_frame.grid_columnconfigure(0, weight=1)

# Assurez-vous que la partie de droite occupe 25% de la largeur
root.grid_columnconfigure(1, weight=1)



# Exécute la boucle principale de l'interface graphique
root.mainloop()
