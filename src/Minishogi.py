from utils import _stringifySquare, stringifyBoard, parseTestCase, loc_occupied, parse_location
from player import Player
import sys
import os

assert len(sys.argv) > 1 and (sys.argv[1] == '-i' or sys.argv[1] == '-f'), 'Must specify game mode with appropriate flag:\n\t-i\t\tInteractive Mode\n\t-f <filePath>\tFile Mode'

def dispatch_turn(command, player, other, board):
  #     dispatch player's actions
  #     catch signs of an end game
  if command[0] == 'move':
    if len(command) > 3 and command[3] == 'promote':
      player.can_promote(command[1])
    player.move_piece(other, command[1], command[2])
    if len(command) > 3 and command[3] == 'promote':
      player.promote(command[1], command[2])
    elif len(command) > 3:
      raise Exception(player.name, 'illegal move', 'Unidentified command')
  elif command[0] == 'drop':
    player.drop_piece(other, command[1], command[2])
  else:
    raise Exception(player.name, 'illegal move', 'Unidentified command') 

def game_state(board, upper_player, lower_player):
  # print board and captures
  print(stringifyBoard(board))
  print('Captures UPPER: {0}'.format(upper_player.stringify_captures()))
  print('Captures lower: {0}\n'.format(lower_player.stringify_captures()))

def interactive_mode():
  #     Two Player Mode
  #     Initialize all values and prepare to start game
  board = [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']]
  lower_player = Player('lower', board)
  upper_player = Player('UPPER', board)
  lower_player.start_game_pieces()
  upper_player.start_game_pieces()
  turns = 0

  while turns < 200:
    try:
      #-----------START lower player's turn-----------

      game_state(board, upper_player, lower_player) 
      #   TODO: Check/Checkmate detection
      if lower_player.in_check(lower_player.pieces, upper_player.pieces):
        # TODO: get list of moves to get out of check
        possible_moves = lower_player.avoid_checkmate(upper_player)
        if len(possible_moves) > 0:
          possible_moves.sort()
          print('lower player is in check!\nAvailable moves:')
          for move in possible_moves:
            print(move)
        else:
          print('UPPER player wins. Checkmate.')
          quit()
      lower_move = input('lower> ')
      print('lower player action: {0}'.format(lower_move))
      lower_command = lower_move.split()
      #     ACTION: lower player
      dispatch_turn(lower_command, lower_player, upper_player, board)
      

      #-----------END lower player's turn-----------

      #-----------START upper player's turn-----------
      game_state(board, upper_player, lower_player) 
      #   TODO: Check/Checkmate detection
      if upper_player.in_check(upper_player.pieces, lower_player.pieces):
        # TODO: get list of moves to get out of check
        possible_moves = upper_player.avoid_checkmate(lower_player)
        if len(possible_moves) > 0:
          possible_moves.sort()
          print('lower player is in check!\nAvailable moves:')
          for move in possible_moves:
            print(move)
        else:
          print('lower player wins. Checkmate.')
          quit()
      upper_move = input('UPPER> ')
      print('UPPER player action: {0}'.format(upper_move))
      upper_command = upper_move.split()
      #     ACTION: upper player
      dispatch_turn(upper_command, upper_player, lower_player, board)

      #-----------END upper player's turn-----------
      turns += 1
    except Exception as e:
      if e.args[0] == 'no king':
        quit()
      if e.args[1] == 'illegal move':
        if e.args[0].islower():
          print('\nUPPER player wins. Illegal move.')
        elif e.args[0].isupper():
          print('\nlower player wins. Illegal move.')
        quit()

  
  # end game for too many turns
  print('\nTie game. Too many moves.')


def file_mode(path):
  game = parseTestCase(path)
  board = [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']]
  lower_player = Player('lower', board)
  upper_player = Player('UPPER', board)
  for elem in game['initialPieces']:
    if elem['piece'].islower():
      lower_player.make_piece(elem['piece'], elem['position'])
    elif elem['piece'].isupper():
      upper_player.make_piece(elem['piece'], elem['position'])
  for elem in game['lowerCaptures']:
    lower_player.make_captured_piece(elem)
  for elem in game['upperCaptures']:
    upper_player.make_captured_piece(elem)

  # play moves
  i = 0
  player = lower_player
  other = upper_player
  while i < 400 and i < len(game['moves']):
    try:
      command = game['moves'][i].split()
      dispatch_turn(command, player, other, board)
      player, other = other, player
      i += 1
    except Exception as e:
      if e.args[0] == 'no king':
        quit()
      if e.args[1] == 'illegal move':
        print('{0} player action: {1}'.format(player.name, game['moves'][i]))
        game_state(board, upper_player, lower_player)
        if e.args[0].islower():
          print('UPPER player wins.  Illegal move.')
        elif e.args[0].isupper():
          print('lower player wins.  Illegal move.')
        quit()
  print('{0} player action: {1}'.format(other.name, game['moves'][i-1]))
  game_state(board, upper_player, lower_player)
  if player.in_check(player.pieces, other.pieces):
    # TODO: get list of moves to get out of check
    possible_moves = player.avoid_checkmate(other)
    if len(possible_moves) > 0:
      possible_moves.sort()
      print('{0} player is in check!\nAvailable moves:'.format(player.name))
      for move in possible_moves:
        print(move.lower())
      print(player.name + '>')
    else:
      print('{0} player wins.  Checkmate.'.format(other.name))  
  elif i < 400:      
    print(player.name + '>')
  else:
    print('Tie game.  Too many moves.')

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

