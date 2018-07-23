class Player:
  def __init__(self, number, symbol):
    self._number = number
    symbol_fixed = symbol.upper().strip()
    if symbol_fixed not in ['X','O']:
      raise ValueError("Player symbol must be either 'X' or 'O'!")
    self._symbol = symbol_fixed

  '''Accessor Methods'''
  def get_number(self):
    return self._number

  def get_symbol(self):
    return self._symbol

  '''Behavior'''
  @classmethod
  def choose_sides(cls):
    # Player 1 chooses a side
    sides = ["X", "O"]
    side_val = "a"
    while side_val not in sides:
      side_val = str(input("Player 1, please choose a side: "))
      side_val = side_val.upper().strip()
      if side_val not in sides:
        print("Error! Please choose 'X' or 'O'.")

    player1_side = side_val.upper().strip()
    player2_side = list(set(sides) - set(player1_side))[0]

    print("Player 2 you are {0}.".format(player2_side))

    return [Player(1, player1_side), Player(2, player2_side)]
  
  def make_a_move(self, board_size):
    return self.__parse_move(input("Player {0} ({1}), please make your move: ".format(self._number, self._symbol)), board_size)

  def __parse_move(self, move_str, board_size):
    move_str_arr = move_str.split(",")
    if len(move_str_arr) == 2:
      if int(move_str_arr[0]) >= board_size or int(move_str_arr[0]) < 0:
        print("The selected row is out of range! Try again.")
        return -1
      if int(move_str_arr[1]) >= board_size or int(move_str_arr[0]) < 0:
        print("The selected column is out of range! Try again.")
        return -1
      return [int(move_str_arr[0]), int(move_str_arr[1])]
    else:
      print("Improper move format! Please type your move coordinates, like '0,1'.")
      return -1

class Board:
  def __init__(self, size=3):
    self._size = size
    self._move_count = 0
    self._spaces = []
    for x in range(size):
      self._spaces.append([0 for i in range(size)])

    self._win_list = [] 
    # Win Rows
    for x in range(size):
      self._win_list.append([ (x,y) for y in range(size)])
    # Win Columns
    for y in range(size):
      self._win_list.append([ (x,y) for x in range(size)])
    # Win Diagonal1
    self._win_list.append([(x,x) for x in range(size)])
    # Win Diagonal2
    self._win_list.append([(x,size-x-1) for x in range(size)])

    print(self._win_list)

    print(self._spaces)

  def get_spaces(self):
    return self._spaces

  def set_space(self, x, y, symbol):
    self._spaces[x][y] = symbol
    return symbol

  def get_space(self, x, y):
    return self._spaces[x][y]

  def display_board(self):
    dash_count = (8*self._size - 1) # - 3 + (self._size % 2))
    # Top Border
    output = "+-"+ "-"*dash_count + "-+" + "\r\n"
    for i in range(len(self._spaces)):
      # Board Cells
      output += "| "
      for j in range(len(self._spaces[i])):
        if self._spaces[i][j] != 0:
          output += "   {0}   ".format(self._spaces[i][j])
        else:
          output += " ({0},{1}) ".format(i,j)
        if j < len(self._spaces[i]) -1:
          output += "|"
      output += " |"
      # If not last row, print line between rows
      if i < len(self._spaces) -1:
        output += "\r\n|-"
        for j in range(len(self._spaces[i])):
          #if (self._size % 2 == 1 and j != self._size//2) or \
          #  (self._size % 2 == 0 and j not in [self._size//2, self._size//2-1]):
          #  output += "-"*8
          #else:
          #  output += "-"*7
          output += "-"*7
          if j < len(self._spaces[i]) - 1:
            output += "+"
        output += "-|\r\n"
    # Bottom Border
    output += "\r\n" + "+-"+ "-"*dash_count + "-+"
    print(output)

  def is_game_over(self, players):
    ''' Detect when the game has been won or tied. '''
    i = 1
    open_space = False
    winner = -1
    cant_win_count = 0
    for win_alg in self._win_list:
      alg_value = ""
      for win_position in win_alg:
        alg_value += str(self._spaces[win_position[0]][win_position[1]])
      print("Check value number {0} is '{1}'.".format(i, alg_value))

      # Check for winners
      if alg_value == players[0].get_symbol() * self._size:
        number = players[0].get_number()
        print("Player {0} wins!".format(number))
        winner = 1
      elif alg_value == players[1].get_symbol() * self._size:
        number = players[1].get_number()
        print("Player {0} wins!".format(number))
        winner = 2
      else:
        if "0" in alg_value:
          open_space = True
        if alg_value.count("X") > 0 and alg_value.count("O"):
          cant_win_count += 1
      
      # Increment counter
      i += 1

    if (not open_space and winner == -1) or (cant_win_count == len(self._win_list)):
      winner = 0
      print("Tie game ¯\_(ツ)_/¯")
    
    self._move_count += 1
    #return self.move_count > 3
    return winner

class TicTacToe:

  def __init__(self, size=3):
    self._size = size
    self._board = Board(size)
    
    
    self._players = []
    self._turn = 0
    self._move_count = 0
    self._winner = -1

  def get_active_player(self):
    return self._players[self._turn]

  def __swap_turn(self):
    if self._turn == 0:
      self._turn = 1
    else:
      self._turn = 0
    #print("Turn: {0}.".format(self.turn))

  def get_next_move(self):
    move = -1
    move_valid = False
    active_player = self.get_active_player()

    while not move_valid:
      move = active_player.make_a_move(self._size)
      move_valid = self.check_move(move)
    
    self._board.set_space(move[0], move[1], active_player.get_symbol())


  def check_move(self, move):
    '''Is the move valid with the current game state?'''
    if move == -1:
      #print("Invalid move format! Please type your move coordinates, like '0,1'.")
      return False
    if self._board.get_space(move[0], move[1]) == 0:
      return True
    else:
      print("Invalid move! Try again.")
      return False

  def play(self):
    self._players = Player.choose_sides()
    while self._board.is_game_over(self._players) == -1:
      self._board.display_board()
      self.get_next_move()
      self.__swap_turn()
    # Show the game board one last time
    print("Final Game Board:")
    self._board.display_board()


if __name__ == "__main__":
  board_size = int(input("What size game board would you like: "))
  ttt = TicTacToe(board_size)
  ttt.play()