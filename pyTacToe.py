from random import randint

class Game(object):
  def __init__(self):
    self.board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    self.is_game_over = False
    self.winner = 0
    self.current_player = 1
    self.move_number = 0

  def make_move(self, player, index):
    """
    Make a move in the game
    :param player: 1 for X, -1 for O
    :param index: 0-8
    """
    # update the board
    self.board[index] = player
    self.move_number += 1

    # check if player just won, or if it was a cats game
    if self.did_player_win(player):
      self.display_game_board()
      self.winner = player
      print "Looks like %s has won. Good game." % (self.player_to_str(player))
      print
      self.is_game_over = True
    elif self.is_board_full():
      self.display_game_board()
      print "Aw shucks! its a cats game. Lame"
      print
      self.is_game_over = True
  
  def ask_for_move(self):
    """
    returns int of move index
    """
    move = 0
    while True:
      move = raw_input("Choose your spot: ")
      try:
        move = int(move) - 1
      except ValueError:
        print "You must enter an integer, 1-9."
        continue

      if move < 0 or move > 8:
        print "That move is not even on the board."
      elif self.board[move] != 0:
        print "That spot is already taken."
      else:
        break

    return move

  def did_player_win(self, player):
    """
    check to see if the player just won. This should be called from make_move
    returns True if the player won and False otherwise
    """
    b = self.board
    p = player
    # brute force check all possible combos
    return ((b[0] == p and b[1] == p and b[2] == p) or # across the top
    (b[3] == p and b[4] == p and b[5] == p) or # across the middle
    (b[6] == p and b[7] == p and b[8] == p) or # across the bottom
    (b[0] == p and b[3] == p and b[6] == p) or # down the left side
    (b[1] == p and b[4] == p and b[7] == p) or # down the middle
    (b[2] == p and b[5] == p and b[8] == p) or # down the right side
    (b[0] == p and b[4] == p and b[8] == p) or # diagonal
    (b[2] == p and b[4] == p and b[6] == p)) # diagonal

  def is_board_full(self):
    """
    check to see if the board is full. AKA a cats game
    """
    for i in self.board:
      if i == 0:
        return False

    return True

  def display_game_board(self):
    print
    print
    print "  %s | %s | %s" % (self.disp_cell(0), self.disp_cell(1), self.disp_cell(2))
    print " ---+---+---  Move # %i" % (self.move_number)
    print "  %s | %s | %s" % (self.disp_cell(3), self.disp_cell(4), self.disp_cell(5))
    print " ---+---+---  %s's turn" % (self.player_to_str(self.current_player))
    print "  %s | %s | %s" % (self.disp_cell(6), self.disp_cell(7), self.disp_cell(8))
    print

  def disp_cell(self, index):
    if self.board[index] == 0:
      return index + 1
    return self.player_to_str(self.board[index])

  def player_to_str(self, player):
    if player == 1:
      return "X"
    elif player == -1:
      return "O"
    else:
      return " "

  def ai_make_move(self):
    # the most basic AI, make moves at random
    # Make a list of all possible moves
    open_move_index = []
    for i, val in enumerate(self.board):
      if val == 0:
        open_move_index.append(i)

    # randomly pick one of the possible valid moves
    move = open_move_index[randint(0,len(open_move_index) - 1)]
    self.make_move(self.current_player, move)
  
  def play(self):
    """
    method that handels game play
    """
    print
    print
    print
    print
    print "Welcome to pyTacToe. Learning Python via TicTacToe."

    while not self.is_game_over:
      self.display_game_board()
      if self.current_player == 1:
        move = self.ask_for_move()
        self.make_move(self.current_player, move)
      else:
        self.ai_make_move()

      self.current_player *= -1 # flip the current player

# start up the game
game = Game()
game.play()