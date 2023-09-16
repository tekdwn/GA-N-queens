#Lucas Marteau & Max Cekanowski

import sys;
import random;


def round(nb):
    decimal = nb - int(nb)
    if decimal >= 0.5:
        return int(nb) + 1  
    else:
        return int(nb)  

class GridClass:
    
    def __init__(self, board_length: int, myQueensList = None):
        self.BoardLength = board_length
        self.Grid = []
        self.Conflicts = 0;
    
        if myQueensList is None:
            self.GridRandomQueens = []
        else:
            self.GridQueens = myQueensList
    
    
    def FillUpGrid(self) -> None:
        self.Grid = [[False for col in range(self.BoardLength)] for row in range(self.BoardLength)]

    def PlaceQueens(self) -> None:
        i = 0

        while i < self.BoardLength:
            x = random.randint(0, self.BoardLength - 1)
            y = random.randint(0, self.BoardLength - 1)
            if [x, y] in self.GridRandomQueens:
                i = i - 1
            else:
                self.GridRandomQueens.append([x, y])
            i = i + 1
        for coordinates in self.GridRandomQueens:
            self.Grid[coordinates[0]][coordinates[1]] = True;

    def CheckConflicts(self) -> None:

        for i in range(len(self.GridRandomQueens)):
            for j in range(i + 1, len(self.GridRandomQueens)):

                queen1 = self.GridRandomQueens[i]
                queen2 = self.GridRandomQueens[j]

                if (abs(queen1[0] - abs(queen2[0])) == abs(queen1[1] - abs(queen2[1]))):
                    self.Conflicts += 1
                if ((queen1[0] == queen2[0]) or (queen1[1] == queen2[1])):
                    self.Conflicts += 1
    def __str__(self) -> str:
        return str(self.Conflicts)

class IA:
    def __init__(self, Parent1: GridClass, Parent2: GridClass, board_length: int):
        self.Parent1 = Parent1
        self.Parent2 = Parent2
        self.Child1Queens = []
        self.Child2Queens = []
        self.boardLength = board_length

    def crossOver(self) -> tuple:
        size = len(self.Parent1.GridRandomQueens)
        firsthalf = round(size * 0.40)

        self.Child1Queens.extend(self.Parent1.GridRandomQueens[:firsthalf])
        self.Child1Queens.extend(self.Parent2.GridRandomQueens[firsthalf:])
        self.Child2Queens.extend(self.Parent2.GridRandomQueens[:firsthalf])
        self.Child2Queens.extend(self.Parent1.GridRandomQueens[firsthalf:])

        print(self.Child1Queens)
        print(self.Child2Queens)
        print("--------------------------------------------------------")
        randomize = random.randint(1, 100)
        if (randomize < 80):
            self.mutagen(True)

        randomize = random.randint(1, 100)
        if (randomize < 80):
            self.mutagen(False)

    
    def mutagen(self, boolean : bool) -> list:

        element_to_change = round(len(self.Child1Queens) * 0.50)
        # On vérifiera ce qu'on doit mettre entre element_to_change et randomize le quel est le mieux et dans quel cas.
        # randomize = random.randint(0, self.boardLength - 1)
        if boolean:
            while True:
                random_x = random.randint(0, self.boardLength - 1)
                random_y = random.randint(0, self.boardLength - 1)
                if [random_x, random_y] not in self.Child1Queens:
                    break
            self.Child1Queens[element_to_change] = [random_x, random_y]
            print("Mutation on Child 1 :", self.Child1Queens)
            print("---------------------new one / mutation child 2---------------------------")
            return
        
        while True:
            random_x = random.randint(0, self.boardLength - 1)
            random_y = random.randint(0, self.boardLength - 1)
            if [random_x, random_y] not in self.Child2Queens:
                break
        self.Child2Queens[element_to_change] = [random_x, random_y]
        print("Mutation on Child 2 :", self.Child2Queens)
        print("---------------------new one---------------------------")


        

    # Regarde comment l'autre classe est faite, les -> None sur les méthodes 
    # forcent le type de return (None = void), et les ":" dans les paramètres forcent le typage 
    # du paramètre genre Parent1 : GridClass, si il reçoit autre chose qu'une gridclass, ça va péter

            
def test_arg(arg_length: int, args: []) -> None:
    if arg_length != 2:
        raise Exception("Incorrect number of arguments")
    try:
        int(args[1])
    except:
        raise Exception("Argument not well formated")
    if int(args[1]) < 4:
        raise Exception("Argument must be over 3")

def main(board_length: int) -> None:
    
    grid_list = []
    IA_list = []
    for _ in range(100):
        Grid = GridClass(board_length)
        Grid.FillUpGrid();
        Grid.PlaceQueens();
        Grid.CheckConflicts();
        grid_list.append(Grid)
    
    grid_list.sort(key=lambda x: x.Conflicts)
    grid_list = grid_list[0:5:1]
    for i in range(4):
        Ia = IA(grid_list[i], grid_list[i + 1], board_length)
        Ia.crossOver();
        IA_list.append(Ia)


        
    # Dégager tous les autres objets autres que les 10 premiers, en gros un slice
    # Créer un objet "IA" et tu mets deux objets genre 0 et 1, 2 et 3, 4 et 5, 6 et 7, 8 et 9 dans l'objet avec un constructeur qui prend deux objets GRID
    # et tu fais le cross-over + la mutation.
    # Voir plus tard mais pas tout de suite, une fois qu'on a fait la premiere generation, comment boucler pour faire les autres et arriver à 0.



if __name__ == '__main__':
    try:
        test_arg(len(sys.argv), sys.argv);
        main(int(sys.argv[1]));
    except Exception as e:
        print(str(e))
        sys.exit(1);

