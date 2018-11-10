"""
MiniShogi Game

Objective: capture the other player's king

Rules:
- Lower_player always moves first
- Players can jump the other players pieces and capture them
- Players can drop its captured pieces back onto the board
- Each player gets up to 200 turns
- If no player has won after taking 200 turns it is a Tie game
- Players trying to make an illegal move immediately lose
- Players can promote their pieces by getting them to the promotion zone

Illegal Moves:
- Moving a piece to location out of its range
- Moving a piece onto its own player's pieces
- Dropping a piece on an occupied location
- Dropping a Pawn in a player's promotion zone or immediate checkmate
- Dropping a Pawn onto in a column where the player has an unpromoted pawn
"""


from utils import _stringifySquare, stringifyBoard, parseTestCase, loc_occupied, parse_location
from player import Player
import sys
import os

assert len(sys.argv) > 1 and (sys.argv[1] == '-i' or sys.argv[1] == '-f'), 'Must specify game mode with appropriate flag:\n\t-i\t\tInteractive Mode\n\t-f <filePath>\tFile Mode'

TURNS_LIMIT = 200

def dispatch_turn(command, player, other, board):
    #   dispatch player's actions
    if command[0] == 'move':
        if len(command) > 3 and command[3] == 'promote':
        #   before performing move, check if promotion is being called
        #   check if piece being moved can be promoted
            player.can_promote(command[1])
        player.move_piece(other, command[1], command[2])
        if len(command) > 3 and command[3] == 'promote':
            #   after move is performed, now we can promote the piece
            #   ensured to be legal since can_promote was called
            player.promote(command[2], command[1])
        elif len(command) > 3:
            raise Exception(player.name, 'illegal move', 'Unidentified command')
    elif command[0] == 'drop':
        player.drop_piece(other, command[1], command[2])
    else:
        raise Exception(player.name, 'illegal move', 'Unidentified command') 

def game_state(board, upper_player, lower_player):
    # print board and players' captures
    print(stringifyBoard(board))
    print('Captures UPPER: {0}'.format(upper_player.stringify_captures()))
    print('Captures lower: {0}\n'.format(lower_player.stringify_captures()))

def interactive_mode():
    """ 
    Two Player Mode
    """
    
    board = [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']]
    lower_player = Player('lower', board)
    upper_player = Player('UPPER', board)
    lower_player.start_game_pieces()
    upper_player.start_game_pieces()
    turns = 0
    player = lower_player
    other = upper_player
    while turns < TURNS_LIMIT * 2:
        try:
            game_state(board, upper_player, lower_player) 
            if player.in_check(player.pieces, other.pieces):
                possible_moves = player.avoid_checkmate(other)
                if len(possible_moves) > 0:
                    possible_moves.sort()
                    print('{0} player is in check!\nAvailable moves:'.format(player.name))
                    for move in possible_moves:
                        print(move)
                else:
                    print('{0} player wins. Checkmate.'.format(other.name))
                    quit()
            player_move = input('{0}> '.format(player.name))
            print('{0} player action: {1}'.format(player.name, player_move))
            player_command = player_move.split()
            dispatch_turn(player_command, player, other, board)
            player, other = other, player
            turns += 1
        except Exception as e:
            if e.args[0] == 'no king':
                quit()
            if e.args[1] == 'illegal move':
                if e.args[0].islower():
                    print('\nUPPER player wins.  Illegal move.')
                    quit()
                elif e.args[0].isupper():
                    print('\nlower player wins.  Illegal move.')
                    quit()
    # end game for too many turns
    print('\nTie game.  Too many moves.')


def file_mode(path):
    game = parseTestCase(path)
    board = [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']]
    lower_player = Player('lower', board)
    upper_player = Player('UPPER', board)
    for elem in game['initialPieces']:
        if elem['piece'].islower():
            lower_player.create_piece(elem['piece'], elem['position'])
        elif elem['piece'].isupper():
            upper_player.create_piece(elem['piece'], elem['position'])
    for elem in game['lowerCaptures']:
        lower_player.make_captured_piece(elem)
    for elem in game['upperCaptures']:
        upper_player.make_captured_piece(elem)

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
                    quit()
                elif e.args[0].isupper():
                    print('lower player wins.  Illegal move.')
                    quit()
    print('{0} player action: {1}'.format(other.name, game['moves'][i-1]))
    game_state(board, upper_player, lower_player)
    if player.in_check(player.pieces, other.pieces):
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
        file_mode(sys.argv[2])

main()



    # board = [['a1','a2','a3','a4','a5'],
    #          ['b1','b2','b3','b4','b5'],
    #          ['c1','c2','c3','c4','c5'],
    #          ['d1','d2','d3','d4','d5'],
    #          ['e1','e2','e3','e4','e5']]

