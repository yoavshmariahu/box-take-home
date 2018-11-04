from utils import _stringifySquare, stringifyBoard, parseTestCase
from player import Player
import sys
import os

assert len(sys.argv) > 1 and (sys.argv[1] == '-i' or sys.argv[1] == '-f'), 'Must specify game mode with appropriate flag:\n\t-i\t\tInteractive Mode\n\t-f <filePath>\tFile Mode'

def dispatch_turn(command, player, other, board):
  #     dispatch player's actions
  #     catch signs of an end game
  try:
    if command[0] == 'move':
      player.move_piece(other, command[1], command[2])
    if command[0] == 'drop':
      player.drop_piece(command[1], command[2])
  except Exception as e:
    if e.args[1] == 'illegal move':
      if e.args[0] == 'lower':
        print('\nUPPER player wins.  Illegal move.')
      elif e.args[0] == 'UPPER':
        print('\nlower player wins.  Illegal move.')
      quit()

def game_output(board, upper_captures_str, lower_captures_str):
  # print board and captures
  print(stringifyBoard(board))
  print('Captures UPPER: {0}'.format(upper_captures_str))
  print('Captures lower: {0}'.format(lower_captures_str))

def interactive_mode():
  #     Initialize all values and prepare to start game
  board = [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']]
  lower_player = Player('lower', board)
  lower_player.start_game_pieces()
  upper_player = Player('UPPER', board)
  upper_player.start_game_pieces()
  upper_captures_str = ''
  lower_captures_str = ''
  turns = 0

  while turns < 200:
    #-----------START lower player's turn-----------

    game_output(board, upper_captures_str, lower_captures_str) 
    lower_move = input('\nlower> ')
    print('lower player action: {0}'.format(lower_move))
    lower_command = lower_move.split()
    #     ACTION: lower player
    dispatch_turn(lower_command, lower_player, upper_player, board)
    #     update lower player's capture string
    lower_captures_str = ''
    for piece in lower_player.captures:
      lower_captures_str += piece.id + ' '

    #-----------END lower player's turn-----------

    #-----------START upper player's turn-----------
    game_output(board, upper_captures_str, lower_captures_str) 
    upper_move = input('\nUPPER> ')
    print('UPPER player action: {0}'.format(upper_move))
    upper_command = upper_move.split()
    #     ACTION: upper player
    dispatch_turn(upper_command, upper_player, lower_player, board)
    
    #     update upper player's capture string
    upper_captures_str = ''
    for piece in upper_player.captures:
      upper_captures_str += piece.id + ' '
    #-----------END upper player's turn-----------
    turns += 1
  
  # end game for too many turns
  print('\nTie game. Too many moves.')
def file_mode(path):
  # open(path, 'r').readline()
  pass

def main():
  # Dispatch program according to flags
  if sys.argv[1] == '-i':
    interactive_mode()
  elif sys.argv[1] == '-f':
    path = sys.argv[2]
    file_mode(path)

main()


# board = [['a1','a2','a3','a4','a5'],
#          ['b1','b2','b3','b4','b5'],
#          ['c1','c2','c3','c4','c5'],
#          ['d1','d2','d3','d4','d5'],
#          ['e1','e2','e3','e4','e5']]

