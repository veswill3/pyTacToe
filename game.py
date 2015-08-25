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