# part 2
import random

class Board:
    def __init__(self, size=3):
        self._board_size = size
        self._initialize_board()

    def _initialize_board(self):

        self._board = [[(x,y) for x in range(self._board_size)] for y in range(self._board_size)]

        #-------------------------------------------------------
        # create win_list
        self._win_list = []

        # Win Rows & Columns
        self._win_list = [[(x,y) for x in range(self._board_size)] for y in range(self._board_size)] +\
        [[(y,x) for x in range(self._board_size)] for y in range(self._board_size)]

        # Win Diagonal1
        self._win_list.append([(x,x) for x in range(self._board_size)])
        # Win Diagonal2
        self._win_list.append([(x,self._board_size-x-1) for x in range(self._board_size)])
        ''' other way to find win and column rows
        # Win Rows
        for x in range(self._board_size):
            self._win_list.append([ (x,y) for y in range(self._board_size)])
        # Win Columns
        for y in range(self._board_size):
            self._win_list.append([ (x,y) for x in range(self._board_size)])
        '''
    def get_board_size(self):
        return self._board_size

    def _check_coordinate(self, coord):
        if len(coord[0]) > 1:
            print('Bad coordinate. Try again...')
            return(False,0,0)
        else:
            x, y = int(coord[0]), int(coord[1])
            if x > self._board_size -1 or x < 0  or y > self._board_size - 1 or y < 0:
                print('Bad coordinate. Try again')
                return (False, x, y)
            if self._board[y][x] in ['X', 'O']:
                print('That spot has already been played in. Try again...')
                return (False, x, y)
            return (True, x, y)

    def fill_coordinate(self, coord, symbol):
        ck = self._check_coordinate(coord)
        if ck[0]:
            self._board[ck[2]][ck[1]] = symbol
            return True
        else:
            return False

    def has_winner(self, name, symbol):
        # determine winner: sum of symbol count in any of win list = board_size
        for l in self._win_list:
            if sum(1 for t in l if self._board[t[0]][t[1]] == symbol) == self._board_size:
                print('')
                print('****************************************')
                print('** Bravo! {}, You won!!! ' .format(name))
                print('****************************************')
                print('')
                self.disply_board()
                print('')
                return True
        return False

    def display_win_list(self):
        print ('win coordinate list:')
        for w in self._win_list:
            print (w)

    def disply_board(self):
        s = '       '
        for i in range(self._board_size):
            s += str(i) + '        '
        print(s)
        print('    ' + '---------' * self._board_size)
        for i in range(self._board_size):
            s = ' ' + str(i) + ' |'
            for j in range(self._board_size ):
                if self._board[i][j] == 'X' or self._board[i][j] == 'O':
                    s += '   ' + self._board[i][j].strip() + '    |'
                else:
                    s += ' ' + str(self._board[i][j]).strip() + ' |'
            print(s)
        print('    ' + '---------' * self._board_size)

class Player:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
        self.won_count = 0

    def add_won_count(self):
        self.won_count += 1

class Game:
    def __init__(self):
        self._initiate_board()
        self._initiate_player()
        self._boad_is_full = False
        self._turn = 0

    def _initiate_board(self):
        size = int(input("What size of board do you like to play with: "))
        self._board = Board(size)

    def _reinitiate_board(self, size):
        self._board = Board(size)

    def _initiate_player(self):
        self._players = []
        for i in range(2):
            name = input('Player {} please enter your name: ' .format(i+1))
            if i == 0:
                #symbol = input('Player {} please enter a symbol (X or O): ' .format(i+1))
                self._players.append(Player(name, 'X'))
            else:
                self._players.append(Player(name, 'O'))

    def display_final(self):
       print('')
       print('***************** FINAL ****************')
       for i in range(2):
           if self._players[i].won_count > 1:
               print('Player {} won {} games!' .format(self._players[i].name, self._players[i].won_count))
           else:
               print('Player {} won {} game!' .format(self._players[i].name, self._players[i].won_count))
       print('****************************************')

    def want_play_again(self):
        if input('Do you want to play again Y/N? ').upper() == 'Y':
            self._reinitiate_board(self._board.get_board_size())
            return True
        else:
            self.display_final()
        return False

    def play_game(self):
        turn = 0
        ask_play_again = False
        while True:
            player_idx = turn % 2
            player = self._players[player_idx]

            # Repeat until a valid coordinate is entered
            self._board.disply_board()
            while True:
                cord = tuple(input('Player {}: where will you play ({})? ' .format(player.name, player.symbol)).split(','))
                if len(cord[0]) == 0:
                    print('Game stops!')
                    return

                if self._board.fill_coordinate(cord, player.symbol):
                    break

            if self._board.has_winner(player.name, player.symbol):
                self._players[player_idx].add_won_count()
                ask_play_again = True
            elif turn >= self._board.get_board_size() * self._board.get_board_size() -1:
                print("Tie game!")
                ask_play_again = True

            if ask_play_again == True:
                if self.want_play_again():
                    turn = 0
                    ask_play_again = False
                else:
                    break
            else:
                turn += 1
        return

if __name__ == '__main__':
    g = Game()
    g.play_game()
