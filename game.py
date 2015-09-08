import os
from random import randint

def clear_screen():
  """ http://stackoverflow.com/questions/517970/how-to-clear-python-interpreter-console """
  os.system(['clear','cls'][os.name == 'nt'])

### Game - handles game related info and mechanics
class Game(object):

  def __init__(self, playerX, playerO):
    self.playerX = playerX
    self.current_player = playerX # X always starts
    self.playerO = playerO
    self.board = ["", "", "", "", "", "", "", "", ""]
    self.is_game_over = False
    self.winner = None # nobody yet
    self.move_number = 0

  def play_game(self):
    self.playerX.player_letter = "X"
    self.playerO.player_letter = "O"
    # main game loop
    while not self.is_game_over:
      # take turns
      if self.current_player == self.playerX:
        self.make_move(self.playerX.get_move(self))
      else:
        self.make_move(self.playerO.get_move(self))
    else:
      self.playerX.game_over_callback(self)
      self.playerO.game_over_callback(self)
      return self.winner # game is now over

  def make_move(self, move):
    """ Take current_player's turn by choosing a move.

    Args:
      move (int): index of the move on the board, 0-8

    Raises:
      TypeError: If move is not of type int
      IndexError: If move is out of bounds for the board
      ValueError: If the move is not valid (not on board or space is taken)
    """
    # make sure move is valid (int, 0-8, and space is open)
    if type(move) is not int:
      raise TypeError("move must be an int")

    if move < 0 or move > 8:
      raise IndexError("move must be 0-8")

    if self.board[move] != "":
      raise ValueError("move cannot point to a filled space")

    # update the board
    self.board[move] = self.current_player.player_letter
    self.move_number += 1

    # check if player just won, or if it was a cats game
    if self.did_player_win():
      self.winner = self.current_player
      self.is_game_over = True
    elif self.is_board_full():
      self.is_game_over = True

    # flip the current player
    if self.current_player == self.playerX:
      self.current_player = self.playerO
    else:
      self.current_player = self.playerX

  def did_player_win(self):
    """ Check if the current_player has won.
    Returns:
      bool: True if the current_player has won and False otherwise.
    """
    b = self.board
    p = self.current_player.player_letter
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
    """ Check if the board is full.
    Returns:
      bool: True if the board is full (AKA cats game) and False otherwise.
    """
    for i in self.board:
      if i == "":
        return False

    return True

  def display_game_board(self):
    """ print the game board to the console in human readable form """

    # insert the space number in empty spaces so making moves is easy
    b = []
    for i, v in enumerate(self.board):
      if v == "":
        if not self.is_game_over:
          b.append(str(i + 1))
        else:
          b.append(" ") # keep the spacing when we dont displat number helpers
      else:
        b.append(v)

    clear_screen()
    print("  %s | %s | %s" % (b[0], b[1], b[2]))
    print(" ---+---+---  Move # %i" % self.move_number)
    print("  %s | %s | %s" % (b[3], b[4], b[5]))
    if not self.is_game_over:
      print(" ---+---+---  %s's turn" % self.current_player.player_letter)
    else:
      print(" ---+---+---")
    print("  %s | %s | %s" % (b[6], b[7], b[8]))


### Player and subclasses - handles game time decisions and record keeping
class Player(object):
  """A player in a Game of tic tac toe"""

  def get_move(self, game):
    """Return an int 0-8 representing a valid move on the game board"""
    raise NotImplementedError("Subclasses should implement this!")

  def game_over_callback(self, game):
    """Subclasses may override this for special end game functions"""
    pass


class HumanPlayer(Player):
  """A type of player that will ask for human input to indicate a move"""

  def get_move(self, game):
    game.display_game_board()
    while True:
      print("")
      move = input("Choose your spot: ")
      # ensure we get a valid move
      try:
        move = int(move) - 1 # shift down to zero based
      except ValueError:
        print("You must enter an integer, 1-9.")
        continue

      if move < 0 or move > 8:
        print("That move is not even on the board.")
      elif game.board[move] != "":
        print("That spot is already taken.")
      else:
        break

    return move

  def game_over_callback(self, game):
    # If both players are human, make sure we only print this message once (only when player is X)
    if isinstance(game.playerX, HumanPlayer) and isinstance(game.playerO, HumanPlayer) and game.playerO == self:
      return

    # redisplay the game so the user can see the end result
    game.display_game_board()
    # Print end game messages
    # ASCII art courtesy of http://patorjk.com/software/taag/
    if game.winner == None:
      # cats game
      print("   _____        _                ")
      print("  / ____|      | |   _           ")
      print(" | |      __ _ | |_ | )___       ")
      print(" | |     / _` || __||// __|      ")
      print(" | |____| (_| || |_   \__ \      ")
      print("  \_____|\__,_| \__|  |___/      ")
      print("   __ _   __ _  _ __ ___    ___  ")
      print("  / _` | / _` || '_ ` _ \  / _ \ ")
      print(" | (_| || (_| || | | | | ||  __/ ")
      print("  \__, | \__,_||_| |_| |_| \___| ")
      print("   __/ |                         ")
      print("  |___/                          ")
      print("")
    else:
      if game.winner == game.playerX:
        print(" __   __            _              _ ")
        print(" \ \ / /           (_)            | |")
        print("  \ V /  __      __ _  _ __   ___ | |")
        print("   > <   \ \ /\ / /| || '_ \ / __|| |")
        print("  / . \   \ V  V / | || | | |\__ \|_|")
        print(" /_/ \_\   \_/\_/  |_||_| |_||___/(_)")
        print("")
      else:
        print("   ____              _              _ ")
        print("  / __ \            (_)            | |")
        print(" | |  | | __      __ _  _ __   ___ | |")
        print(" | |  | | \ \ /\ / /| || '_ \ / __|| |")
        print(" | |__| |  \ V  V / | || | | |\__ \|_|")
        print("  \____/    \_/\_/  |_||_| |_||___/(_)")
        print("")


class RandomPlayer(Player):
  """A type of player that will make moves at random"""
  def get_move(self, game):
    # Make a list of all possible moves
    open_move_index = []
    for i, val in enumerate(game.board):
      if val == "":
        open_move_index.append(i)

    # randomly pick one of the possible valid moves
    move = open_move_index[randint(0,len(open_move_index) - 1)]
    return move


class NeuralnetPlayer(Player):
  """A type of player that will make moves that a neural network chooses"""
  def __init__(self, network, individual=None):
    self.network = network
    self.individual = individual

  def get_move(self, game):
    # adjust the game board so that 1 represent this player,
    # 0 for blanks, and -1 for the opponent
    a = []
    for i in game.board:
      if i == self.player_letter:
        a.append(1)
      elif i == "":
        a.append(0)
      else:
        a.append(-1)
    # ask the network what it wants to do
    o = self.network.feedforward(a)
    # find best valid move
    max_val = -1000
    move = 0
    for i, val in enumerate(o):
      if val > max_val and a[i] == 0:
        max_val = val
        move = i

    return move

  def game_over_callback(self, game):
    if self.individual is not None:
      # incriment the individuals stats
      winner = game.winner
      if winner is None:
        self.individual.ties += 1
      elif winner == self:
        self.individual.wins += 1
      else:
        self.individual.losses += 1
