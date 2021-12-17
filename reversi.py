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


    def Play(self, player, player_nbr, score):
        match player:
            case "human":
                move_possible = None
                while move_possible == None:

                    row = None
                    while row == None:
                        row = input("Player n°" + str(player_nbr) +", row of the next move: ")
                        try:
                            row = int(row)
                            if 0 > row or row > 7:
                                row = None

                        except:
                            row = None

                    column = None
                    while column == None:
                        column = input("Player n°" + str(player_nbr) +", column of the next move: ")
                        try:
                            column = int(column)
                            if 0 > column or column > 7:
                                column = None

                        except:
                            column = None

                    if self.grid[column][row] != None and self.PossibleMove(row, column, player_nbr):
                        move_possible = True

                self.Print()

            case "discord":
                pass
            case "bot":
                pass

        self.grid[row][column] = pawn(player_nbr)
        self.FlipPawns(row, column)
        score[player_nbr] = self.CountFlips(row, column)

        return self

class player:
    def __init__(self, player_type):
        self.type = player_type

    def __repr__(self):
        return self.type

class game:
    def __init__(self, game_name, player_a, player_b):
        match game_name:
            case "reversi":
                self.grid = board(8)
                self.grid.Setup("reversi")

                if player_a == "human" or player_b == "human":
                    self.grid.Print()

                self.player_nbr = 0
                self.players = (player_a, player_b)
                self.score = [2, 2]


    def Finish(self):
        for rounds in range(60):
            self.grid = self.grid.Play(self.players[self.player_nbr], self.player_nbr, self.score)
            rounds += 1
            self.player_nbr = 1-self.player_nbr
            print(self.grid.PossiblesMoves(self.player_nbr))

        return self.score

test = game("reversi", "human", "human")
test.Finish()