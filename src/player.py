from pieces import King, Rook, Bishop, GoldGeneral, SilverGeneral, Pawn
from utils import parse_location

class Player:
  def __init__(self, name, captures=[]):
    self.name = name
    self.captures = captures
    self.available_locations = {'a1', 'b1', 'c1', 'd1', 'e1',
                                'a2', 'b2', 'c2', 'd2', 'e2',
                                'a3', 'b3', 'c3', 'd3', 'e3',
                                'a4', 'b4', 'c4', 'd4', 'e4',
                                'a5', 'b5', 'c5', 'd5', 'e5'}
  def insert_piece(self, piece, location, board):
    # this function will be complicated
    coor = parse_location(location)
    if board.places[coor[1]][coor[0]] == '':
      board.places[coor[1]][coor[0]] = piece.id
      board.contained_pieces.add(piece)
      piece.location = location
      self.available_locations.remove(location)
  def remove_piece(self, piece, board):
    pass