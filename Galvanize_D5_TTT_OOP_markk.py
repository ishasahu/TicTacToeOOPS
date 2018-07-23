from os import system, name
from time import sleep
from colorama import Fore, Back, Style

class Cell:
    def __init__(self, coordinate_x, coordinate_y):
        self._coordinate_x = coordinate_x
        self._coordinate_y = coordinate_y
        self._symbol = ''

    def set_symbol(self, symbol):
        self._symbol = symbol

    def symbol(self):
        return self._symbol

    def display_symbol(self):
        if self._symbol == "X":
            return Fore.GREEN + self._symbol + Style.RESET_ALL #Green then reset back to default
        else:
            return Fore.RED + self._symbol + Style.RESET_ALL #Red then reset back to default

    def coordinates(self):
        t = (self._coordinate_x, self._coordinate_y)
        return t

    def __repr__(self):
       return self.coordinates()

class Player:

    def __init__(self, name, symbol):
        self._name = name
        self._symbol = symbol

    def name(self):
        return self._name

    def set_name(self, player_name):
        self._name = player_name

    def display_name(self):
        if self._symbol == "X":
            return Fore.GREEN + self._name + Style.RESET_ALL #Green then reset back to default
        else:
            return Fore.RED + self._name + Style.RESET_ALL #Red then reset back to default

    def symbol(self):
        return self._symbol

    def display_symbol(self):
        if self._symbol == "X":
            return Fore.GREEN + self._symbol + Style.RESET_ALL  #Green then reset back to default
        else:
            return Fore.RED + self._symbol + Style.RESET_ALL #Red then reset back to default

    def __repr__(self):
        return "Player : {}, Symbol : {}".format(self.display_name(), self.display_symbol())


class Board:

    def __init__(self):
        #reset the board
        self._game_board = {}
        self._winning_board = []
        self._reset_board()
        self._setup_winning_board()
        self._display_board = ''

    def __repr__(self):
        return(str(self.display()))

    def _reset_board(self):
        """
        Reset the main game board - a dictionary of cell objects
        :return:
        """
        self._game_board = {}
        for i in range(3):
            for j in range(3):
                c = Cell(i, j)
                self._game_board[c.coordinates()] = c
        self._board_size = len(self._game_board)

    def _setup_winning_board(self):
        """
        Setup the board that contains the winning combinations
        :return:
        """
        self._winning_board = []
        cell_row = []
        #build rows with loop
        for i in range(3):
            for j in range(3):
                cr = Cell(i, j)
                cell_row.append(cr.coordinates())
            self._winning_board.append(cell_row)
            cell_row = []
        #build cols with loop
        cell_col = []
        for i in range(3):
            for j in range(3):
                cc = Cell(j, i)
                cell_col.append(cc.coordinates())
            self._winning_board.append(cell_col)
            cell_col = []
        #hard code diagonals
        c, d, e, f, g = Cell(0, 0), Cell(1, 1), Cell(2, 2), Cell(0, 2), Cell(2, 0)
        cells_d1 = [c.coordinates(), d.coordinates(), e.coordinates()]
        cells_d2 = [f.coordinates(), d.coordinates(), g.coordinates()]
        self._winning_board.append(cells_d1)
        self._winning_board.append(cells_d2)

    def check_boardfull(self, turncount):
        """
        Check if there are any more turns
        :param turncount: how many turns?
        :return:
        """
        # return True or False
        end_of_game = False
        if turncount == self._board_size:
            end_of_game = True

        return end_of_game

    def check_winner(self):
        """
        Check for a winner
        :return: True or False
        """
        winner = False
        for r in self._winning_board:
            if "{}{}{}".format(self._game_board.get(r[0]).symbol(),
                                     self._game_board.get(r[1]).symbol(),
                                     self._game_board.get(r[2]).symbol())in ("XXX", "OOO"):
                print(Fore.YELLOW + "\n\nWe have a winner\n\n" + Style.RESET_ALL)
                winner = True

        return winner

    def update_board(self, coordinates, symbol):
        """
        updates the board an handles the validation
        :param coordinates:
        :param symbol:
        :return:
        """
        try:
            lst_coords = [int(c) for c in coordinates.split(",")]
            c = Cell(lst_coords[0], lst_coords[1])
            c.set_symbol(symbol)
            if self._game_board[c.coordinates()].symbol() in ("X", "O"):
                print(self)
                print('Invalid move, cell {} is already taken'.format(c.coordinates()))
                return False
            else:
                self._game_board[c.coordinates()] = c
                return True
        except:
            print('Invalid move, that is not a valid position on a tic-tac-toe board')
            return False

    def display(self):
        """
        build the board for display purposes
        :return: string (the board)
        """
        s_board = ""
        s_board += '' + "\n\n\n"
        s_board += '      TIC TAC TOE      ' + "\n\n"
        s_board += '       |       |       ' + "\n"
        s_board += ' (0,0) | (0,1) | (0,2) ' + "\n"
        s_board += '       |       |       ' + "\n"
        s_board += '-------+-------+-------' + "\n"
        s_board += '       |       |       ' + "\n"
        s_board += ' (1,0) | (1,1) | (1,2) ' + "\n"  # board template
        s_board += '       |       |       ' + "\n"
        s_board += '-------+-------+-------' + "\n"
        s_board += '       |       |       ' + "\n"
        s_board += ' (2,0) | (2,1) | (2,2) ' + "\n"
        s_board += '       |       |       ' + "\n"
        s_board += '' + "\n\n\n"
        s_board += '       |       |       ' + "\n"
        s_board += '   ' + (self._game_board[(0, 0)].display_symbol() if self._game_board[(0, 0)].symbol() != '' else ' ') + '   |   '
        s_board +=         (self._game_board[(0, 1)].display_symbol() if self._game_board[(0, 1)].symbol() != '' else ' ') + '   |   ' \
                          +(self._game_board[(0, 2)].display_symbol() if self._game_board[(0, 2)].symbol() != '' else ' ') + "\n"
        s_board += '       |       |       ' + "\n"
        s_board += '-------+-------+-------' + "\n"
        s_board += '       |       |       ' + "\n"
        s_board += '   ' + (self._game_board[(1, 0)].display_symbol() if self._game_board[(1, 0)].symbol() != '' else ' ') + '   |   ' + \
                           (self._game_board[(1, 1)].display_symbol() if self._game_board[(1, 1)].symbol() != '' else ' ') + '   |   ' + \
                           (self._game_board[(1, 2)].display_symbol() if self._game_board[(1, 2)].symbol() != '' else ' ') + "\n"
        s_board += '       |       |       ' + "\n"
        s_board += '-------+-------+-------' + "\n"
        s_board += '       |       |       ' + "\n"
        s_board += '   ' + (self._game_board[(2, 0)].display_symbol() if self._game_board[(2, 0)].symbol() != '' else ' ') + '   |   ' + \
                           (self._game_board[(2, 1)].display_symbol() if self._game_board[(2, 1)].symbol() != '' else ' ') + '   |   ' + \
                           (self._game_board[(2, 2)].display_symbol() if self._game_board[(2, 2)].symbol() != '' else ' ') + "\n"
        s_board += '       |       |       ' + "\n"
        s_board += '' + "\n\n"

        return s_board


class Game:
    # Turn 0 for Player 1, Turn 1 for Player 2
    def __init__(self):
        self.clear_display()
        self._initialize_board()
        self._initialize_players()
        self._turn = 1
        self._gameover = False
        self._gamecounter = 0

    def play(self):
        self.clear_display()
        # play the game in
        while not self._gameover:
            # Player Input
            self.clear_display()
            print(self._board)
            while not(self._player_input_option()):
                pass
            self._gameover = self._board.check_winner()
            self._gamecounter += 1
            if self ._board.check_boardfull(self._gamecounter):
                print(Fore.YELLOW + "\n\nThere are no more moves, there was no winner!" + Style.RESET_ALL)
                self._gameover = True

        print(self._board)

    def _initialize_board(self):
        self._board = Board()
        pass

    def _initialize_players(self):
        self._p1 = Player('', 'X')
        self._p2 = Player('', 'O')
        str_name = input("Player 1, your symbol is {}, please enter your name : ".format(self._p1.display_symbol()))
        self._p1.set_name(str_name)
        str_name = input("Player 2, your symbol is {}, please enter your name : ".format(self._p2.display_symbol()))
        self._p2.set_name(str_name)

    def _player_input_option(self):
        p = self._p1
        if self._turn == -1:
            p = self._p2

        # validate input before updating board - user stupidity check
        is_valid_input = False
        while not is_valid_input:
            p_input = input("{} , please enter your move in the format X,Y ? : ".format(p))
            is_valid_input = self.valid_input(p_input)

        if not(self._board.update_board(p_input, p.symbol())):
            self._turn *= 1
            return False
        else:
            self._turn *=-1
            return True

    def valid_input(self, player_input):
        not_valid = False
        if ',' not in player_input:
            print('Invalid move, that is not a valid position on a tic-tac-toe board')
            not_valid = False
        else:
            try:
                lst_coords = [int(c) for c in player_input.split(",")]
                not_valid = True
            except:
                print('Invalid move, that is not a valid position on a tic-tac-toe board')
                not_valid = False

        return not_valid

    @staticmethod
    def clear_display():
        """
        Clears the screen
        :return:
        """
        _ = system("cls")
        _ = system("clear")


if __name__ == '__main__':
    quit_game = False
    str_play = ""
    while not quit_game:
        g = Game()
        g.play()
        str_play = input("Would you like to play again? (Q to quit) : ")
        if str_play.upper() == "Q":
            quit_game = True
