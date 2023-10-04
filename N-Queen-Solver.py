import pygame_widgets
import pygame
import numpy as np
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
import ctypes
from collections import deque
import random
import time
import csv
import platform

class Stats:
    IsStatsSide: bool = False

class GeneticProperties:
    SAMPLE_SIZE: int = 1000
    MAX_GENERATION: int = 10000
    MUTATION_RATE: int = 0.02
    CONSECUTIVE_GENERATIONS_TRESHOLD: int = 15
    BOARD_SIZE: int | None = None 
    GEN_FINISH: int | None = None

class ActiveTextBox:
    CURRENT_INDEX = -1

class ScreenProperties:
    WIDTH_SCREEN = None
    HEIGHT_SCREEN = None

class BoardProperties:
    BOARD_SIZE = None
    X_SIZE_SQUARE = None
    Y_SIZE_SQUARE = None
    BEGIN_ROW = None
    BEGIN_COL = None
    DISPLAYED = False
    QUEEN_LIST = None

class TextBoxesAlgoSide:
    BOARD_SIZE_LABEL = None
    BOARD_SIZE_RECT = None
    BOARD_SIZE_VAL = None
    MAX_GENERATION_LABEL = None
    MAX_GENERATION_RECT = None
    MAX_GEN_VAL = None
    MUTATION_RATE_LABEL = None
    MUTATION_RATE_RECT = None
    MUTATION_RATE_VAL = None
    ERROR_LABEL = None
    TIME_LABEL = None
    SWITCH_SIDE_BUTTON = None
    ALGO_BUTTON = None
class TextBoxesStatsSide:
    BOARD_SIZE_LABEL = None
    BOARD_SIZE_RECT = None
    BOARD_SIZE_VAL = None
    GENERATION_LABEL = None
    GENERATION_RECT = None
    GENERATION_VAL = None
    MUTATION_RATE_LABEL = None
    MUTATION_RATE_RECT = None
    MUTATION_RATE_VAL = None
    ERROR_LABEL = None
    RUN_BUTTON = None
    GEN_AVG = None
    TIME_AVG = None

class CSVRow:
    def __init__(self, size, m_rate, max_gen, time, gen) -> None:
        self.size = size
        self.m_rate = m_rate
        self.max_gen = max_gen
        self.time = time
        self.gen = gen


def calculate_fitness(item):
    conflits = 0

    for i in range(BoardProperties.BOARD_SIZE):
        for j in range(i + 1, BoardProperties.BOARD_SIZE):
            if abs(i - j) == abs(item[i] - item[j]) or item[i] == item[j]:
                conflits += 1
    return conflits

def get_first_conflict_queen(item):
    for i in range(BoardProperties.BOARD_SIZE):
        for j in range(i + 1, BoardProperties.BOARD_SIZE):
            if abs(i - j) == abs(item[i] - item[j]) or item[i] == item[j]:
                return(i)


def select_parents(sample):
    parents = random.choices(sample, k=GeneticProperties.SAMPLE_SIZE // 2, weights=[1.0 / (calculate_fitness(each) + 1) for each in sample])
    return parents

def crossover(parent1: list[int], parent2: list[int]) -> list[int]:
    crossover_point = random.randint(1, GeneticProperties.BOARD_SIZE - 1)
    child = [-1] * BoardProperties.BOARD_SIZE
    child[:crossover_point] = parent1[:crossover_point]
    
    available_positions = [x for x in parent2 if x not in child]

    for i in range(BoardProperties.BOARD_SIZE):
        if child[i] == -1:
            if available_positions:
                gene = available_positions.pop()
                child[i] = gene
            else:
                remaining_genes = [x for x in range(BoardProperties.BOARD_SIZE) if x not in child]
                random_gene = random.choice(remaining_genes)
                child[i] = random_gene

    return child

def mutate(child):
    for i in range(BoardProperties.BOARD_SIZE):
        if random.random() < GeneticProperties.MUTATION_RATE:
            j = child[random.randint(0, BoardProperties.BOARD_SIZE - 1)]
            child[i], child[j] = child[j], child[i]
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
                return col

            row_counts[col] += 1
            diag1_counts[row - col] += 1
            diag2_counts[row + col] += 1

    return None

def genetical_algorithm(mutation_Rate = 0.02, max_generation = 10000):
    GeneticProperties.MUTATION_RATE = mutation_Rate
    GeneticProperties.MAX_GENERATION = max_generation
    sample  = [list(np.random.permutation(GeneticProperties.BOARD_SIZE)) for _ in range(GeneticProperties.SAMPLE_SIZE)]
    best_solution_queue = deque(maxlen=GeneticProperties.CONSECUTIVE_GENERATIONS_TRESHOLD) #You can remove first or last element with deque -> double-ended queue
    
    for generation in range(GeneticProperties.MAX_GENERATION):
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
            GeneticProperties.GEN_FINISH = generation + 1
            return best_solution
        if len(best_solution_queue) == GeneticProperties.CONSECUTIVE_GENERATIONS_TRESHOLD and all_equal(best_solution_queue):
            problematic_queen_index = find_problematic_queen(best_solution)
            if problematic_queen_index is not None:
                best_solution[problematic_queen_index] = random.randint(0, GeneticProperties.BOARD_SIZE - 1)
            best_solution_queue.clear();
    return None

def set_TextBoxes():
    TextBoxesAlgoSide.BOARD_SIZE_RECT.show()
    TextBoxesAlgoSide.MAX_GENERATION_RECT.show()
    TextBoxesAlgoSide.MUTATION_RATE_RECT.show()
    TextBoxesAlgoSide.ALGO_BUTTON.show()
    TextBoxesStatsSide.BOARD_SIZE_RECT.hide()
    TextBoxesStatsSide.GENERATION_RECT.hide()
    TextBoxesStatsSide.MUTATION_RATE_RECT.hide()
    TextBoxesStatsSide.RUN_BUTTON.hide()
  

def clear_TextBoxes():
    TextBoxesAlgoSide.BOARD_SIZE_RECT.hide()
    TextBoxesAlgoSide.MAX_GENERATION_RECT.hide()
    TextBoxesAlgoSide.MUTATION_RATE_RECT.hide()
    TextBoxesAlgoSide.ALGO_BUTTON.hide()
    TextBoxesStatsSide.BOARD_SIZE_RECT.show()
    TextBoxesStatsSide.GENERATION_RECT.show()
    TextBoxesStatsSide.MUTATION_RATE_RECT.show()
    TextBoxesStatsSide.RUN_BUTTON.show()


def change_side():
    if Stats.IsStatsSide:
        Stats.IsStatsSide = False
        set_TextBoxes()
        return
    Stats.IsStatsSide =  True
    clear_TextBoxes()

def get_square_size(nb: int):
    BoardProperties.BOARD_SIZE = nb
    BoardProperties.X_SIZE_SQUARE = int(min(150, (ScreenProperties.WIDTH_SCREEN * 0.75) / nb))
    BoardProperties.Y_SIZE_SQUARE = min(150, int((ScreenProperties.HEIGHT_SCREEN * 0.80) / nb))

def get_position_of_first_square():
    BoardProperties.BEGIN_ROW = int(((ScreenProperties.WIDTH_SCREEN * 0.75) - (BoardProperties.X_SIZE_SQUARE * BoardProperties.BOARD_SIZE)) / 2)
    BoardProperties.BEGIN_COL = int(((ScreenProperties.HEIGHT_SCREEN * 0.80) - (BoardProperties.Y_SIZE_SQUARE * BoardProperties.BOARD_SIZE)) / 2) + (ScreenProperties.HEIGHT_SCREEN * 0.20)

def is_numeric(input_str):
    try:
        float(input_str)
        return True
    except ValueError:
        return False


def run_stats(pygame):
    if is_numeric(TextBoxesStatsSide.BOARD_SIZE_RECT.getText()):
        TextBoxesStatsSide.BOARD_SIZE_VAL = float(TextBoxesStatsSide.BOARD_SIZE_RECT.getText())
    if is_numeric(TextBoxesStatsSide.MUTATION_RATE_RECT.getText()):
        TextBoxesStatsSide.MUTATION_RATE_VAL = float(TextBoxesStatsSide.MUTATION_RATE_RECT.getText())
    if is_numeric(TextBoxesStatsSide.GENERATION_RECT.getText()):
        TextBoxesStatsSide.GENERATION_VAL = float(TextBoxesStatsSide.GENERATION_RECT.getText())

    data_list = []
    filtered_items = []
    try:
        with open("stats.csv", newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                if len(row) == 5:
                    data_list.append(CSVRow(row[0], row[1], row[2], row[3], row[4]))
    except FileNotFoundError as e:
        TextBoxesStatsSide.TIME_AVG = None
        TextBoxesStatsSide.GEN_AVG = None
        label_surface = pygame.font.Font(None, 20).render("Non-existing file, no data", True, (255,0,0))
        label_rect = label_surface.get_rect()
        label_rect.topleft = ((ScreenProperties.WIDTH_SCREEN * 0.40), (ScreenProperties.HEIGHT_SCREEN * 0.35))
        TextBoxesStatsSide.ERROR_LABEL = (label_surface, label_rect)
        return
    except Exception as e:
        TextBoxesStatsSide.TIME_AVG = None
        TextBoxesStatsSide.GEN_AVG = None
        label_surface = pygame.font.Font(None, 20).render("Error occured, try again ", True, (255,0,0))
        label_rect = label_surface.get_rect()
        label_rect.topleft = ((ScreenProperties.WIDTH_SCREEN * 0.40), (ScreenProperties.HEIGHT_SCREEN * 0.35))
        TextBoxesStatsSide.ERROR_LABEL = (label_surface, label_rect)
        return

    if TextBoxesStatsSide.BOARD_SIZE_VAL is not None:
        filtered_items = [item for item in data_list if float(item.size) == TextBoxesStatsSide.BOARD_SIZE_VAL]
    if len(filtered_items) == 0:
        TextBoxesStatsSide.TIME_AVG = None
        TextBoxesStatsSide.GEN_AVG = None
        label_surface = pygame.font.Font(None, 20).render("You never done the algorithm with this board size", True, (255,0,0))
        label_rect = label_surface.get_rect()
        label_rect.topleft = ((ScreenProperties.WIDTH_SCREEN * 0.40), (ScreenProperties.HEIGHT_SCREEN * 0.35))
        TextBoxesStatsSide.ERROR_LABEL = (label_surface, label_rect)
        return
    TextBoxesStatsSide.ERROR_LABEL = None
    sum_col4 = 0
    sum_col5 = 0
    for item in filtered_items:
        sum_col4 += float(item.time)
        sum_col5 += float(item.gen)
    average_col4 = sum_col4 / len(filtered_items)
    average_col5 = int(sum_col5 / len(filtered_items))
    label_surface = pygame.font.Font(None, 30).render(f"The mean of the compute time is : {average_col4}", True, (0,0,0))
    label_rect = label_surface.get_rect()
    label_rect.topleft = ((ScreenProperties.WIDTH_SCREEN * 0.20), (ScreenProperties.HEIGHT_SCREEN * 0.50))
    TextBoxesStatsSide.TIME_AVG = (label_surface, label_rect)
    label_surface = pygame.font.Font(None, 36).render(f"The mean of the generation where the solution is found is : {average_col5}", True, (0,0,0))
    label_rect = label_surface.get_rect()
    label_rect.topleft = ((ScreenProperties.WIDTH_SCREEN * 0.20), (ScreenProperties.HEIGHT_SCREEN * 0.70))
    TextBoxesStatsSide.GEN_AVG = (label_surface, label_rect)


def setup_textBoxes(police, window, pygame):
    label_surface = police.render("Board size (Between 4 and 100) :", True, (0,0,0))
    label_rect = label_surface.get_rect()
    label_rect.topleft = ((ScreenProperties.WIDTH_SCREEN * 0.80), (ScreenProperties.HEIGHT_SCREEN * 0.20))
    TextBoxesAlgoSide.BOARD_SIZE_LABEL = (label_surface, label_rect)
    TextBoxesAlgoSide.BOARD_SIZE_RECT = TextBox(window, (ScreenProperties.WIDTH_SCREEN * 0.80), (ScreenProperties.HEIGHT_SCREEN * 0.27),
                    (ScreenProperties.WIDTH_SCREEN * 0.10), (ScreenProperties.HEIGHT_SCREEN * 0.05),
                    fontSize=40,colour=(255,255,255),
                    borderColour=(0, 0, 0), textColour=(0,0,0),
                    radius=0, borderThickness=1)
    label_surface = police.render("Mutation rate (Between 0 and 1):", True, (0,0,0))
    label_rect = label_surface.get_rect()
    label_rect.topleft = ((ScreenProperties.WIDTH_SCREEN * 0.80), (ScreenProperties.HEIGHT_SCREEN * 0.40))
    TextBoxesAlgoSide.MUTATION_RATE_LABEL = (label_surface, label_rect)
    TextBoxesAlgoSide.MUTATION_RATE_RECT = TextBox(window, (ScreenProperties.WIDTH_SCREEN * 0.80), (ScreenProperties.HEIGHT_SCREEN * 0.47),
                    (ScreenProperties.WIDTH_SCREEN * 0.10), (ScreenProperties.HEIGHT_SCREEN * 0.05),
                    fontSize=40,colour=(255,255,255),
                    borderColour=(0, 0, 0), textColour=(0,0,0),
                    radius=0, borderThickness=1)
    label_surface = police.render("Max generation (Between 1 and 100000):", True, (0,0,0))
    label_rect = label_surface.get_rect()
    label_rect.topleft = ((ScreenProperties.WIDTH_SCREEN * 0.80), (ScreenProperties.HEIGHT_SCREEN * 0.60))
    TextBoxesAlgoSide.MAX_GENERATION_LABEL = (label_surface, label_rect)
    TextBoxesAlgoSide.MAX_GENERATION_RECT = TextBox(window, (ScreenProperties.WIDTH_SCREEN * 0.80), (ScreenProperties.HEIGHT_SCREEN * 0.67),
                    (ScreenProperties.WIDTH_SCREEN * 0.10), (ScreenProperties.HEIGHT_SCREEN * 0.05),
                    fontSize=40,colour=(255,255,255),
                    borderColour=(0, 0, 0), textColour=(0,0,0),
                    radius=0, borderThickness=1)
    TextBoxesAlgoSide.ALGO_BUTTON = Button(window, (ScreenProperties.WIDTH_SCREEN * 0.82), (ScreenProperties.HEIGHT_SCREEN * 0.80), (ScreenProperties.WIDTH_SCREEN * 0.05), (ScreenProperties.HEIGHT_SCREEN * 0.05), text="Start algorithm",
                pressedColour=(200, 200, 200), inactiveColour=(155, 155, 155), fontSize=20
                ,onClick=compute, onClickParams=[window, pygame])
    TextBoxesAlgoSide.SWITCH_SIDE_BUTTON = Button(window, (ScreenProperties.WIDTH_SCREEN * 0.82), (ScreenProperties.HEIGHT_SCREEN * 0.95), (ScreenProperties.WIDTH_SCREEN * 0.05), (ScreenProperties.HEIGHT_SCREEN * 0.05), text="Go other Page",
                pressedColour=(200, 200, 200), inactiveColour=(155, 155, 155), fontSize=20
                ,onClick=change_side)
    label_surface = police.render("Board size (Between 4 and 100) :", True, (0,0,0))
    label_rect = label_surface.get_rect()
    label_rect.topleft = ((ScreenProperties.WIDTH_SCREEN * 0.20), (ScreenProperties.HEIGHT_SCREEN * 0.20))
    TextBoxesStatsSide.BOARD_SIZE_LABEL = (label_surface, label_rect)
    TextBoxesStatsSide.BOARD_SIZE_RECT = TextBox(window, (ScreenProperties.WIDTH_SCREEN * 0.20), (ScreenProperties.HEIGHT_SCREEN * 0.27),
                    (ScreenProperties.WIDTH_SCREEN * 0.10), (ScreenProperties.HEIGHT_SCREEN * 0.05),
                    fontSize=40,colour=(255,255,255),
                    borderColour=(0, 0, 0), textColour=(0,0,0),
                    radius=0, borderThickness=1)
    label_surface = police.render("Mutation rate (Between 0 and 1):", True, (0,0,0))
    label_rect = label_surface.get_rect()
    label_rect.topleft = ((ScreenProperties.WIDTH_SCREEN * 0.40), (ScreenProperties.HEIGHT_SCREEN * 0.20))
    TextBoxesStatsSide.MUTATION_RATE_LABEL = (label_surface, label_rect)
    TextBoxesStatsSide.MUTATION_RATE_RECT = TextBox(window, (ScreenProperties.WIDTH_SCREEN * 0.40), (ScreenProperties.HEIGHT_SCREEN * 0.27),
                    (ScreenProperties.WIDTH_SCREEN * 0.10), (ScreenProperties.HEIGHT_SCREEN * 0.05),
                    fontSize=40,colour=(255,255,255),
                    borderColour=(0, 0, 0), textColour=(0,0,0),
                    radius=0, borderThickness=1)
    label_surface = police.render("Max generation (Between 1 and 100000):", True, (0,0,0))
    label_rect = label_surface.get_rect()
    label_rect.topleft = ((ScreenProperties.WIDTH_SCREEN * 0.60), (ScreenProperties.HEIGHT_SCREEN * 0.20))
    TextBoxesStatsSide.GENERATION_LABEL = (label_surface, label_rect)
    TextBoxesStatsSide.GENERATION_RECT = TextBox(window, (ScreenProperties.WIDTH_SCREEN * 0.60), (ScreenProperties.HEIGHT_SCREEN * 0.27),
                    (ScreenProperties.WIDTH_SCREEN * 0.10), (ScreenProperties.HEIGHT_SCREEN * 0.05),
                    fontSize=40,colour=(255,255,255),
                    borderColour=(0, 0, 0), textColour=(0,0,0),
                    radius=0, borderThickness=1)
    TextBoxesStatsSide.RUN_BUTTON = Button(window, (ScreenProperties.WIDTH_SCREEN * 0.90), (ScreenProperties.HEIGHT_SCREEN * 0.20), (ScreenProperties.WIDTH_SCREEN * 0.05), (ScreenProperties.HEIGHT_SCREEN * 0.05), text="Get mean",
                pressedColour=(200, 200, 200), inactiveColour=(155, 155, 155), fontSize=20
                ,onClick=run_stats, onClickParams=[pygame])
    TextBoxesStatsSide.BOARD_SIZE_RECT.hide()
    TextBoxesStatsSide.MUTATION_RATE_RECT.hide()
    TextBoxesStatsSide.GENERATION_RECT.hide()
    TextBoxesStatsSide.RUN_BUTTON.hide()

def setup_screen_properties():
    if (platform.system() == "Windows"):
        ctypes.windll.user32.SetProcessDPIAware()
        ScreenProperties.WIDTH_SCREEN = ctypes.windll.user32.GetSystemMetrics(0)
        ScreenProperties.HEIGHT_SCREEN = ctypes.windll.user32.GetSystemMetrics(1)
    else:
        ScreenProperties.WIDTH_SCREEN = 1500
        ScreenProperties.HEIGHT_SCREEN = 1200


def compute(window, pygame):
    try:
        TextBoxesAlgoSide.BOARD_SIZE_VAL = int(TextBoxesAlgoSide.BOARD_SIZE_RECT.getText())
        if TextBoxesAlgoSide.BOARD_SIZE_VAL < 4 or TextBoxesAlgoSide.BOARD_SIZE_VAL > 100:
            raise Exception("BOARD_SIZE_VAL")
        GeneticProperties.BOARD_SIZE = TextBoxesAlgoSide.BOARD_SIZE_VAL
        TextBoxesAlgoSide.MAX_GEN_VAL = int(TextBoxesAlgoSide.MAX_GENERATION_RECT.getText())
        if TextBoxesAlgoSide.MAX_GEN_VAL < 1 or TextBoxesAlgoSide.MAX_GEN_VAL > 100000:
            raise Exception("MAX_GEN_VAL")
        TextBoxesAlgoSide.MUTATION_RATE_VAL = float(TextBoxesAlgoSide.MUTATION_RATE_RECT.getText())
        if TextBoxesAlgoSide.MUTATION_RATE_VAL < 0.0 or TextBoxesAlgoSide.MUTATION_RATE_VAL > 1.0:
            raise Exception("MUTATION_RATE_VAL")
        get_square_size(TextBoxesAlgoSide.BOARD_SIZE_VAL)
        get_position_of_first_square()
        display_squares(window, pygame)
        begin = time.time()
        BoardProperties.QUEEN_LIST = genetical_algorithm(max_generation=TextBoxesAlgoSide.MAX_GEN_VAL, mutation_Rate=TextBoxesAlgoSide.MUTATION_RATE_VAL)
        end = time.time()
        if BoardProperties.QUEEN_LIST == None:
            label_surface = police.render(f"No correct in solution found in {end - begin}, try again or increase the generation max (actual : {TextBoxesAlgoSide.MAX_GEN_VAL})", True, (0,0,0))
            label_rect = label_surface.get_rect()
            label_rect.topleft = ((ScreenProperties.WIDTH_SCREEN * 0.30), (ScreenProperties.HEIGHT_SCREEN * 0.1))
            TextBoxesAlgoSide.TIME_LABEL = (label_surface, label_rect)
        else:
            label_surface = police.render(f"Solution found in {end - begin}", True, (0,0,0))
            label_rect = label_surface.get_rect()
            label_rect.topleft = ((ScreenProperties.WIDTH_SCREEN * 0.30), (ScreenProperties.HEIGHT_SCREEN * 0.1))
            TextBoxesAlgoSide.TIME_LABEL = (label_surface, label_rect)
        with open('stats.csv', 'a') as file:
            file.write(str(TextBoxesAlgoSide.BOARD_SIZE_VAL) + "," + str(TextBoxesAlgoSide.MUTATION_RATE_VAL) + ',' + str(TextBoxesAlgoSide.MAX_GEN_VAL) + ',' + str(end - begin) + ',' + str(GeneticProperties.GEN_FINISH) + '\n')
        TextBoxesAlgoSide.ERROR_LABEL = None
        pygame.display.update()
    except Exception as e:
        BoardProperties.DISPLAYED = False
        label_surface = pygame.font.Font(None, 20).render("You have to fill all the textboxesAlgoSide and check labels for values", True, (255,0,0))
        label_rect = label_surface.get_rect()
        label_rect.topleft = ((ScreenProperties.WIDTH_SCREEN * 0.80), (ScreenProperties.HEIGHT_SCREEN * 0.90))
        TextBoxesAlgoSide.ERROR_LABEL = (label_surface, label_rect)
        return

def display_squares(window, pygame):
    for x in range(BoardProperties.BOARD_SIZE):
        for y in range(BoardProperties.BOARD_SIZE):
            z = (int(BoardProperties.BEGIN_ROW + (BoardProperties.X_SIZE_SQUARE * y)), int(BoardProperties.BEGIN_COL + (BoardProperties.Y_SIZE_SQUARE * x)))
            if x % 2 == 0:
                if y % 2 == 0:
                    pygame.draw.rect(window, (0,0,0), (z[0], z[1], BoardProperties.X_SIZE_SQUARE, BoardProperties.Y_SIZE_SQUARE))
                else:
                    pygame.draw.rect(window, (255,255,255), (z[0], z[1], BoardProperties.X_SIZE_SQUARE, BoardProperties.Y_SIZE_SQUARE))
            else:
                if y % 2 == 0:
                    pygame.draw.rect(window, (255,255,255),(z[0], z[1], BoardProperties.X_SIZE_SQUARE, BoardProperties.Y_SIZE_SQUARE))
                else:
                    pygame.draw.rect(window, (0,0,0),(z[0], z[1], BoardProperties.X_SIZE_SQUARE, BoardProperties.Y_SIZE_SQUARE))
    if BoardProperties.QUEEN_LIST is not None:
        for x, y in enumerate(BoardProperties.QUEEN_LIST):
            z = (int(BoardProperties.BEGIN_ROW + (BoardProperties.X_SIZE_SQUARE * y)), int(BoardProperties.BEGIN_COL + (BoardProperties.Y_SIZE_SQUARE * x)))
            pygame.draw.rect(window, (255,0,0), (z[0], z[1], BoardProperties.X_SIZE_SQUARE, BoardProperties.Y_SIZE_SQUARE))
    BoardProperties.DISPLAYED = True
        

if __name__ == "__main__":
    pygame.init()
    setup_screen_properties()
    window = pygame.display.set_mode((ScreenProperties.WIDTH_SCREEN, ScreenProperties.HEIGHT_SCREEN))
    pygame.display.set_caption("N-Queens Problem Solver")
    running: bool = True
    police = pygame.font.Font(None, 36)
    setup_textBoxes(police, window, pygame)

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        window.fill((255, 255, 255))
        if Stats.IsStatsSide == False:
            window.blit(TextBoxesAlgoSide.BOARD_SIZE_LABEL[0], TextBoxesAlgoSide.BOARD_SIZE_LABEL[1])
            window.blit(TextBoxesAlgoSide.MUTATION_RATE_LABEL[0], TextBoxesAlgoSide.MUTATION_RATE_LABEL[1])
            window.blit(TextBoxesAlgoSide.MAX_GENERATION_LABEL[0], TextBoxesAlgoSide.MAX_GENERATION_LABEL[1])
            if (TextBoxesAlgoSide.ERROR_LABEL) is not None:
                window.blit(TextBoxesAlgoSide.ERROR_LABEL[0], TextBoxesAlgoSide.ERROR_LABEL[1])
            if (TextBoxesAlgoSide.TIME_LABEL) is not None:
                window.blit(TextBoxesAlgoSide.TIME_LABEL[0], TextBoxesAlgoSide.TIME_LABEL[1])

            if BoardProperties.DISPLAYED == True:
                display_squares(window, pygame)
        else:
            window.blit(TextBoxesStatsSide.BOARD_SIZE_LABEL[0], TextBoxesStatsSide.BOARD_SIZE_LABEL[1])
            window.blit(TextBoxesStatsSide.MUTATION_RATE_LABEL[0], TextBoxesStatsSide.MUTATION_RATE_LABEL[1])
            window.blit(TextBoxesStatsSide.GENERATION_LABEL[0], TextBoxesStatsSide.GENERATION_LABEL[1])

            if (TextBoxesStatsSide.ERROR_LABEL):
                window.blit(TextBoxesStatsSide.ERROR_LABEL[0], TextBoxesStatsSide.ERROR_LABEL[1])
            if (TextBoxesStatsSide.TIME_AVG):
                window.blit(TextBoxesStatsSide.TIME_AVG[0], TextBoxesStatsSide.TIME_AVG[1])
                window.blit(TextBoxesStatsSide.GEN_AVG[0], TextBoxesStatsSide.GEN_AVG[1])
            
        pygame_widgets.update(events)
        pygame.display.update()
        pygame.display.flip()
    pygame.quit()
