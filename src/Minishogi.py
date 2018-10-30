from utils import _stringifySquare, stringifyBoard, parseTestCase
from player import Player
from board import Board
import sys
import os

assert len(sys.argv) > 1 and (sys.argv[1] == '-i' or sys.argv[1] == '-f'), 'Must specify game mode with appropriate flag:\n\t-i\t\tInteractive Mode\n\t-f <filePath>\tFile Mode'

def interactive_mode():
  lower_player = Player('lower')
  lower_player.start_game_pieces()
  upper_player = Player('UPPER')
  upper_player.start_game_pieces()
  board = Board()
  board.start_game()
  print(stringifyBoard(board.places))
def file_mode(path):
  # open(path, 'r').readline()
  pass




if sys.argv[1] == '-i':
  interactive_mode()
elif sys.argv[1] == '-f':
  path = sys.argv[2]
  file_mode(path)




# board = [['a1','a2','a3','a4','a5'],
#          ['b1','b2','b3','b4','b5'],
#          ['c1','c2','c3','c4','c5'],
#          ['d1','d2','d3','d4','d5'],
#          ['e1','e2','e3','e4','e5']]

