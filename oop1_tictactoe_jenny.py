class Board:
    def __init__(self, size):
        self.size = size
        self.board = [[(i, j) for i in range(self.size)]
              for j in range(self.size)]

    def validate_move(self,x,y):
        #check if the input within board size
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            print("Your move is outside of the board. Please try again.")
            return False
        #check if the position has been taken
        elif type(self.board[y][x]) != tuple:
            print("The spot has been taken. Please try again.")
            return False
        return True

    def update_board(self,x,y,symbol):
        self.board[y][x] = symbol
        repr(self)

    def determine_winner(self, name, symbol):
        winner_list = self.board.copy()
        #add all the columns to the list
        for i in range(self.size):
            winner_list.append([self.board[j][i] for j in range(self.size)])
        #add two diagnal to the list
        winner_list.append([self.board[i][i] for i in range(self.size)])
        winner_list.append([self.board[i][self.size-1-i] for i in range(self.size)])
        for i in winner_list:
            if i.count(symbol) == self.size:
                print("Game end. {} wins!".format(name))
                return True
        return False

    def __repr__(self):
        print('  '+'    '.join(str(i) for i in range(self.size)))
        for i in range(self.size):
            row = str(i)
            for j in range(self.size):
                elem = self.board[i][j]
                if type(elem) != str:
                    elem = "   "
                else:
                    elem = " "+str(self.board[i][j]+" ")
                row = row + elem
                if j < self.size - 1:
                    row = row + " |"
            print(row)
            if i < self.size - 1:
                print('  '+'-'* self.size * 4)
        return ''

class Player:
    def __init__(self,name,symbol):
        self.name = name
        self.symbol = symbol
        self.win_num = 0

    def __repr__(self):
        return ("Player {}, symbol {}".format(self.name, self.symbol))

class Game:
    def __init__(self):
        self._initialize_players()
        self._initialize_board()
        self.play_game()

    def _initialize_players(self):
        while True:
            try:
                name, symbol = input("Player 1, please enter your name and symbol separated by comma and space: ").split(', ')
                self.p1 = Player(name,symbol)
                print(repr(self.p1))
                name, symbol = input("Player 2, please enter your name and symbol separated by comma and space: ").split(', ')
                self.p2 = Player(name,symbol)
                print(repr(self.p2))
                break
            except ValueError:
                print("You must enter your name and symbol separated by comma and space: ")

    def _initialize_board(self):
        self.play_flag = 'Y'
        self.found_winner = 'N'
        while True:
            try:
                size = int(input("Please enter board size: "))
                self.b = Board(size)
                repr(self.b)
                break
            except ValueError:
                print("Please enter an integer for the board size: ")

    def play_game(self):
        turn = 0
        while turn < self.b.size ** 2 and self.play_flag == 'Y':
            if turn%2 == 0:
                self.player_move(self.p1)
            else:
                self.player_move(self.p2)
            turn += 1
            if turn == self.b.size ** 2:
                print("Game resulted in a tie...like usual.")
                break
            if self.found_winner == 'Y':
                self.play_flag = input("Do you want to play again? Enter Y/N: ")
                if self.play_flag == 'N':
                    print("{} won {} times. {} won {} times".format(self.p1.name, self.p1.win_num, self.p2.name, self.p2.win_num))
                    break
                else:
                    self._initialize_board()
                    self.play_game()

    def player_move(self, player):
        while True:
            try:
                x,y = input(("Player {}, where would you play? ").format(player.name)).split(', ')
                x = int(x)
                y = int(y)
                if self.b.validate_move(x,y):
                    self.b.update_board(x,y,player.symbol)
                    break
            except ValueError:
                print("You must enter two integers separated by comma and space.")
        if self.b.determine_winner(player.name, player.symbol):
            player.win_num += 1
            self.found_winner = 'Y'


if __name__ == '__main__':
    Game()
