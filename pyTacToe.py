from random import randint
import os

# Shim to make sure input works in python v 2 and 3
try:
  input = raw_input
except NameError:
  pass
# end python v 2 and 3 input shim

class Game(object):
  def __init__(self):
    self.board = ["", "", "", "", "", "", "", "", ""]
    self.is_game_over = False
    self.winner = "" # nobody yet
    self.current_player = "X" # x always starts
    self.move_number = 0

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
    self.board[move] = self.current_player
    self.move_number += 1

    # check if player just won, or if it was a cats game
    if self.did_player_win():
      self.winner = self.current_player
      self.is_game_over= True
    elif self.is_board_full():
      self.is_game_over = True

    # flip the current player
    if self.current_player == "X":
      self.current_player = "O"
    else:
      self.current_player = "X"

  def did_player_win(self):
    """ Check if the current_player has won.
    Returns:
      bool: True if the current_player has won and False otherwise.
    """
    b = self.board
    p = self.current_player
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

def clear_screen():
  """ http://stackoverflow.com/questions/517970/how-to-clear-python-interpreter-console """
  os.system(['clear','cls'][os.name == 'nt'])

def display_game_board(game):
  """ print the game board to the console in human readable form """

  # insert the space number in empty spaces so making moves is easy
  b = []
  for i, v in enumerate(game.board):
    if v == "":
      if not game.is_game_over:
        b.append(str(i + 1))
      else:
        b.append(" ") # keep the spacing when we dont displat number helpers
    else:
      b.append(v)

  clear_screen()
  print("  %s | %s | %s" % (b[0], b[1], b[2]))
  print(" ---+---+---  Move # %i" % game.move_number)
  print("  %s | %s | %s" % (b[3], b[4], b[5]))
  if not game.is_game_over:
    print(" ---+---+---  %s's turn" % game.current_player)
  else:
    print(" ---+---+---")
  print("  %s | %s | %s" % (b[6], b[7], b[8]))

def ask_human_for_move(game):
  while True:
    print("")
    move = input("Choose your spot: ")
    try:
      move = int(move) - 1
    except ValueError:
      print("You must enter an integer, 1-9.")
      continue

    if move < 0 or move > 8:
      print("That move is not even on the board.")
    elif game.board[move] != "":
      print("That spot is already taken.")
    else:
      break

  game.make_move(move)

def random_move_ai(game):
  """ The most basic AI, make moves at random """
  # Make a list of all possible moves
  open_move_index = []
  for i, val in enumerate(game.board):
    if val == "":
      open_move_index.append(i)

  # randomly pick one of the possible valid moves
  move = open_move_index[randint(0,len(open_move_index) - 1)]
  game.make_move(move)

def get_player_func(player_letter):
  while True:
    print("")
    print("Choose type for player %s" % player_letter)
    print("    1: Human")
    print("    2: Random move AI (stupid easy)")

    choice = input("Choice: ").lower()
    if choice == "1" or choice[0] == "h":
      return ask_human_for_move
    elif choice == "2" or choice[0] == "r":
      return random_move_ai
    else:
      print("Invalid choice, try again.")

# create a new game instance
game = Game()

# print a greeting
clear_screen()
print("Welcome to pyTacToe. Learning Python via TicTacToe.")

# setup opponent preferences (human vs computer)
playerXfunc = get_player_func("X")
playerOfunc = get_player_func("O")

# main game loop
while not game.is_game_over:
  display_game_board(game)

  # take turns
  if game.current_player == "X":
    playerXfunc(game)
  else:
    playerOfunc(game)
else:
  # redisplay the game so the user can see the end result
  display_game_board(game)

  # ASCII art courtesy of http://patorjk.com/software/taag/
  if game.winner == "":
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
    if game.winner == "X":
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