#Lucas Marteau & Max Cekanowski

import sys;
import random;
import time;
class GridClass:
    
    def __init__(self, board_length: int):
        self.BoardLength = board_length
        self.Grid = []
        self.GridRandomQueens = []
        self.Conflicts = 0;
    
    def FillUpGrid(self) -> None:
        self.Grid = [[[row, col, False] for col in range(self.BoardLength)] for row in range(self.BoardLength)]

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
            self.Grid[coordinates[0]][coordinates[1]][2] = True;

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

    for _ in range(1000):
        Grid = GridClass(board_length)
        Grid.FillUpGrid();
        Grid.PlaceQueens();
        Grid.CheckConflicts();
        grid_list.append(Grid)
    
    grid_list.sort(key=lambda x: x.Conflicts)   
    for item in range(1, 10):
        print(grid_list[item].GridRandomQueens)



if __name__ == '__main__':
    try:
        test_arg(len(sys.argv), sys.argv);
        main(int(sys.argv[1]));
    except Exception as e:
        print(str(e))
        sys.exit(1);
