class Player:
    def __init__(self,name,symbol_choice):
        self._name = name
        self._symbol_x = ' X  '
        self._symbol_o = ' O  '
        self.symbol = self._set_player_symbol(symbol_choice)
        
    def _set_player_symbol(self,symbol_choice):
        if symbol_choice.lstrip().rstrip().lower() == 'x':
            return self._symbol_x
        else:
            return self._symbol_o
    
    def take_turn(self,game_board):
        self._success = False
        #while self._success == False:
        self._success = game_board.place_symbol(self)
        
        
class Board:
    def __init__(self,size=3):
        self._size = size
        self._tic_tac_toe_list=[]
        self._coordinate = ''
        self._initialize_board()
        self._display_board()
        self.game_over = False
        self.tie_game = False
        self.we_have_a_winner = False
        
    def _initialize_board(self):
        for y in range(self._size):
            self._tic_tac_toe_list.append([(y,x) for x in range(self._size)])
            
    def _display_board(self):
        for rowList in self._tic_tac_toe_list:
            print(rowList)
            
    def _check_coordinate_status(self,player):
        coordinatesList=[int(i) for i in self._coordinate.split(',')]
        #print(tuple(coordinatesList))
        #print(self._tic_tac_toe_list)
        
        for i in range(3):
            if tuple(coordinatesList) not in self._tic_tac_toe_list[i]:
                #print('Coordinate {} does not exist.'.format(tuple(coordinatesList)))
                return False
        else:
            return self._tic_tac_toe_list[coordinatesList[0]][coordinatesList[1]]!=player._symbol_x \
                and self._tic_tac_toe_list[coordinatesList[0]][coordinatesList[1]]!=player._symbol_o
            
    def _fill_location(self,player):
        coordinatesList=[int(i) for i in self._coordinate.split(',')]
        coordinateTuple=(coordinatesList[0],coordinatesList[1])
        for rowIdx,rowList in enumerate(self._tic_tac_toe_list):
           for idx,cell in enumerate(rowList):
               if cell==coordinateTuple:
                   #if(self._tic_tac_toe_list[rowIdx][idx] != player._symbol_x and  self._tic_tac_toe_list[rowIdx][idx] != player._symbol_o):
                   self._tic_tac_toe_list[rowIdx][idx]=player.symbol
        #return self.tic_tac_toe_list
        
    def place_symbol(self,player):
        self._coordinate = input('{}, please choose a coordinate (x,y) to mark with an {}:  '.format(player._name,player.symbol.lstrip().rstrip()))
        if self._check_coordinate_status(player):
            self._fill_location(player)
            self._display_board()
            self.game_over = self._is_game_over(player)
            return True
        else:
            #raise Exception('Location not available. Game Over!!! {} loses!!!'.format(player._name))
            #print('{}, that coordinate does not exist.  Please choose an existing coordinate!'.format(player._name))
            return False #return that the game is over
    
    def _is_game_over(self,player):
        #print(self._is_game_tied(), self._is_game_won())
        return (self._is_game_tied() or self._is_game_won(player))
        
        #if self.tie_game or self.we_have_a_winner:
        #    self.game_over = True
        #else:
        #    return False
            
    
    def _is_game_tied(self):
        self.tie_game = True
        for rowList in self._tic_tac_toe_list:
            if not all( type(i) is str for i in rowList):
                self.tie_game = False
        return self.tie_game
    
    def _is_game_won(self,player):
        self.we_have_a_winner = False
        winMatrix=[[(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]]
        for winningrowList in winMatrix:
            tictacrow=[self._tic_tac_toe_list[x][y] for x,y in winningrowList]
            #print(tictacrow)
            #print('tictacrow = {}'.format(tictacrow))
            #print('player symbol row = {}'.format([player.symbol,player.symbol,player.symbol]))
            if tictacrow == [player.symbol,player.symbol,player.symbol]:
                #self._display_board()
                self.we_have_a_winner = True

        #print('we have a winner equals {}'.format(self.we_have_a_winner))
        return self.we_have_a_winner
class Game:
    def __init__(self):
        self._p1 = self._create_player()
        self._p2 = self._create_player()
        self._board = self._create_board()
        self._current_player = self._p2
        
    def _create_player(self):
        player_info_list = input("Please enter your name and symbol like 'name,symbol(X or O)':  ").split(',')
        return(Player(player_info_list[0],player_info_list[1]))
        
    def _create_board(self):
        return Board()
    
    def _change_player(self):
        if self._current_player == self._p1:
            self._current_player = self._p2
        else:
            self._current_player = self._p1
    
    def play_game(self):
        #print('Game over = {}'.format(self._board.game_over))
        while not self._board.game_over:
            self._change_player()
            #print('After change player.  Player name is {}.'.format(self._current_player._name))
            self._current_player.take_turn(self._board)
            
        if self._board.tie_game:
            print('NO WINNER!  Game ends in a tie!')
        else:
            print('We have a winner!!  {} is the Tic Tac Toe Champion!!!!'.format(self._current_player._name))
            
        
if __name__ == "__main__":
    Game().play_game()