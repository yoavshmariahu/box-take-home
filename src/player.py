from pieces import King, Rook, Bishop, GoldGeneral, SilverGeneral, Pawn
from utils import parse_location, loc_occupied

class Player:
  def __init__(self, name, board):
    self.name = name
    self.captures = list()
    self.pieces = list()
    self.available_locations = {'a1', 'b1', 'c1', 'd1', 'e1',
                                'a2', 'b2', 'c2', 'd2', 'e2',
                                'a3', 'b3', 'c3', 'd3', 'e3',
                                'a4', 'b4', 'c4', 'd4', 'e4',
                                'a5', 'b5', 'c5', 'd5', 'e5'}
    self.board = board
  def insert_piece(self, piece, location):
    coor = parse_location(location)
    self.board[coor[0]][coor[1]] = piece.id
    for elem in self.pieces:
      if elem[0] is piece:
        elem[1] = location
    
  def remove_piece(self, location, other=None):
    coor = parse_location(location)
    self.board[coor[0]][coor[1]] = ''
    if not other:
      for i in range(len(self.pieces)):
        if self.pieces[i][1] == location:
          self.pieces[i][1] = None
          return
    for i in range(len(other.pieces)):
      if other.pieces[i][1] == location:
        temp = other.pieces.pop(i)
        return temp[0]
    
  def move_piece(self, other, piece, loc_from, loc_to):
    if loc_occupied(loc_to, self.board):
      self.add_to_cap(self.remove_piece(loc_to, other))
    self.remove_piece(loc_from)
    self.insert_piece(piece, loc_to)
  
  def add_to_cap(self, piece):
    if self.name == 'lower':
      piece.id = piece.id.lower()
    elif self.name == 'UPPER':
      piece.id = piece.id.upper()
    self.captures.append(piece)
  
  def add_piece(self, piece, location=None):
    self.pieces[piece] = location

  def start_game_pieces(self):
    if self.name == 'lower':
      self.pieces = [
        [King(self), 'a1'],
        [Rook(self), 'e1'],
        [Bishop(self), 'd1'],
        [GoldGeneral(self), 'b1'],
        [SilverGeneral(self), 'c1'],
        [Pawn(self), 'a2']
      ]
      
    elif self.name == 'UPPER':
      self.pieces = [
        [King(self), 'e5'],
        [Rook(self), 'a5'],
        [Bishop(self), 'b5'],
        [GoldGeneral(self), 'd5'],
        [SilverGeneral(self), 'c5'],
        [Pawn(self), 'e4']
      ]
    for piece in self.pieces:
      self.insert_piece(piece[0], piece[1])