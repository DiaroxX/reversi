"""Reversi Game
Authors : DiaroxX : https://github.com/DiaroxX
          Colnup : https://github.com/Colnp
          Prof-redstone (le BG de la street) : https://github.com/prof-redstone"""


class Pawn():
    """
    Can be 0 or 1 depend of the color
    0 for black
    1 for white
    """

    def __init__(self, color):
        self.color = color

    def __repr__(self):
        if self.color is None:
            return " "
        if self.color == 0:
            return "◼"
        if self.color == 1:
            return "▢"

    def flip(self):
        """Change the pawn color"""
        self.color = 1-self.color
        return self


class Board():
    """Class wrapping the board"""

    def __init__(self, size, place_holder=None):
        self.size = size
        self.place_holder = Pawn(place_holder)
        self.grid = [
            [self.place_holder for i in range(size)] for j in range(size)]

    def __getitem__(self, i):
        return self.grid[i]

    def __repr__(self):
        return self.grid

    def show(self):
        """Print the board in a nice way"""
        for i in range(self.size):
            str_row = ""
            for j in range(self.size):
                str_row += str(self[i][j]) + " | "
            print(str_row[:-3])

    def setup(self, game):
        """Setup the board"""
        if game == "reversi":
            self.grid[3][3], self.grid[4][4] = Pawn(0), Pawn(0)
            self.grid[3][4], self.grid[4][3] = Pawn(1), Pawn(1)
        return self.grid

    def count_flips(self, x, y, color=None):
        """Count the number of flips for the move x,y"""
        if color is None:
            color = self[x][y].color

        flips = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    temp_flips = []
                    # need to simplify
                    for distance in range(1, round(min((3.5*i) + 3.5 - (x*i), (3.5*j) + 3.5 - (y*j)))):
                        if self[distance*i + x][distance*j + y].color is None:
                            break

                        if self[distance*i + x][distance*j + y].color == 1-color:
                            temp_flips.append((distance*i + x, distance*j + y))

                        elif self[distance*i + x][distance*j + y].color == color:
                            flips += temp_flips
                            break
        return flips

    def is_move_possible(self, x, y, color):
        """Return True if the move is possible"""
        return len(self.count_flips(x, y, color)) != 0

    def flip_pawns(self, x, y):
        """Flip all pawns for the move x,y"""
        for pawn in self.count_flips(x, y):
            self.grid[pawn[0]][pawn[1]].flip()

    def possible_move_list(self, color):
        """Return a list of possible moves"""
        all_possibles_moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.is_move_possible(i, j, color):
                    all_possibles_moves.append([i, j])
        return all_possibles_moves

    def evaluate(self):
        """Evaluate the board"""
        # TODO : implement the evaluation function
        score = [0, 0]
        possible_moves = [0, 0]

        for i in range(self.size):
            for j in range(self.size):
                if isinstance(self.grid[i][j], Pawn):
                    score[self.grid[i][j]] += 1
                else:
                    for x in range(2):
                        if self.is_move_possible(i, j, x):
                            possible_moves[x] += 1



# Valid inputs are numbers between 0 and board size
def enforce_valid_input(prompt: str, board: Board) -> int:
    """Ask user for input and check if it is valid"""
    # REVIEW Maybe implement it in the Board class ?
    while True:
        try:
            choice = int(input(prompt))
            if not 0 <= choice < board.size:
                raise ValueError
            return choice
        except ValueError:
            print("Please enter a valid number")


def main():
    """Main game function"""
    grid = Board(8)

    grid.setup("reversi")
    grid.show()
    curren_player = 0
    score = [2, 2]

    for rounds in range(60):
        move_possible = False
        while not move_possible:

            # Check if player can move, if not, switch player
            if grid.possible_move_list(curren_player) == []:
                print("No possible move for player", curren_player)
                curren_player = 1 - curren_player
                continue
            
            print(f"Possible moves : {grid.possible_move_list(curren_player)}")

            row = enforce_valid_input(
                "Player " + str(curren_player+1) + "(ligne): ", grid)
            column = enforce_valid_input(
                "Player " + str(curren_player+1) + "(colone): ", grid)

            move_possible = grid.is_move_possible(row, column, curren_player)

        grid.grid[row][column] = Pawn(curren_player)
        grid.flip_pawns(row, column)
        score[curren_player] = grid.count_flips(row, column)
        grid.show()

        rounds += 1
        curren_player = 1-curren_player



if __name__ == '__main__':
    main()
