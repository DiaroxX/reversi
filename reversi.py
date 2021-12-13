class pawn:
    """
    Can be 0 or 1 depend of the color
    0 for black
    1 for white
    """

    def __init__(self, color):
        self.color = color

    def __repr__(self):
        if self.color == None:
            return " "
        elif self.color == 0:
            return "◼"
        elif self.color == 1:
            return "▢"

    def Flip(self):
        self.color = 1-self.color
        return self


class board:
    def __init__(self, size, place_holder=None):
        self.size = size
        self.place_holder = pawn(place_holder)
        self.grid = [[self.place_holder for i in range(size)] for j in range(size)]


    def __getitem__(self, i):
        return self.grid[i]


    def __repr__(self):
        return self.grid


    def Print(self):
        for i in range(self.size):
            str_row = ""
            for j in range(self.size):
                str_row += str(self[i][j]) + " | "
            print(str_row[:-3])


    def Setup(self, game):
        if game == "reversi":
            self.grid[3][3], self.grid[4][4] = pawn(0), pawn(0)
            self.grid[3][4], self.grid[4][3] = pawn(1), pawn(1)
        return self.grid


    def CountFlips(self, x, y, color=None):
        if color == None:
            color = self[x][y].color

        flips = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    temp_flips = []
                    for distance in range(1, round(min((3.5*i) + 3.5 - (x*i), (3.5*j) + 3.5 - (y*j)))): #need to simplify
                        if self[distance*i + x][distance*j + y].color == None:
                            break

                        elif self[distance*i + x][distance*j + y].color == 1-color:
                            temp_flips.append((distance*i + x, distance*j + y))

                        elif self[distance*i + x][distance*j + y].color == color:
                            flips += temp_flips
                            break
        return flips


    def PossibleMove(self, x, y, color):
        return len(self.CountFlips(x, y, color)) != 0 #self dans les arguments


    def FlipPawns(self, x, y):
        for pawn in self.CountFlips(x, y):
            self.grid[pawn[0]][pawn[1]].Flip()


    def PossiblesMoves(self, color):
        all_possibles_moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.PossibleMove(i, j, color):
                    all_possibles_moves.append([i, j])
        return all_possibles_moves


    def Evaluate(self):
        score = [0, 0]
        possible_moves = [0, 0]

        for i in range(self.size):
            for j in range(self.size):
                if type(self.grid[i][j]) == pawn:
                    score[self.grid[i][j]] += 1
                else:
                    for x in range(2):
                        if self.PossibleMove(i, j, x):
                            possible_moves[x] += 1



#main code start here
grid = board(8)
grid.Setup("reversi")
grid.Print()
player = 0
score = [2, 2]



for rounds in range(60):
    move_possible = None
    while move_possible == None:

        row = None
        while row == None:
            row = input("Player n°" + str(player) +", row of the next move: ")
            try:
                row = int(row)
                if 0 > row or row > 7:
                    row = None

            except:
                row = None

        column = None
        while column == None:
            column = input("Player n°" + str(player) +", column of the next move: ")
            try:
                column = int(column)
                if 0 > column or column > 7:
                    column = None

            except:
                column = None

        if grid.grid[column][row] != None and grid.PossibleMove(column, row, player):
            move_possible = True

    grid.grid[row][column] = pawn(player)
    grid.FlipPawns(row, column)
    score[player] = grid.CountFlips(row, column)
    grid.Print()
    print(grid.PossiblesMoves(player))

    rounds += 1
    player = 1-player