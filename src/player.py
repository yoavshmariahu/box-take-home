from pieces import King, Rook, Bishop, GoldGeneral, SilverGeneral, Pawn
from utils import parse_location, loc_occupied

# TODO: Check Detection, Checkmate Detection

class Player:
  def __init__(self, name, board):
    self.name = name
    self.captures = list()
    self.pieces = list()
    self.board = board

  def insert_piece(self, piece, location):
    coor = parse_location(location)
    self.board[coor[0]][coor[1]] = piece.id
    for elem in self.pieces:
      if elem[0] is piece:
        elem[1] = location
    
  def remove_piece(self, location, other=None):
    if not loc_occupied(location, self.board):
      raise Exception(self.name, 'illegal move')
    coor = parse_location(location)
    self.board[coor[0]][coor[1]] = ''
    if not other:
      for i in range(len(self.pieces)):
        if self.pieces[i][1] == location:
          self.pieces[i][1] = None
          return self.pieces[i][0]
    for i in range(len(other.pieces)):
      if other.pieces[i][1] == location:
        temp = other.pieces.pop(i)
        return temp[0]
    
  def drop_piece(self, piece_id, location):
    if loc_occupied(location, self.board):
      raise Exception(self.name, 'illegal move')
    if self.name == 'UPPER':
      piece_id = piece_id.upper()
    for i in range(len(self.captures)):
      if self.captures[i].id == piece_id:
        piece = self.captures.pop(i)
        self.insert_piece(piece, location)
        self.pieces.append([piece, location])

  def move_piece(self, other, loc_from, loc_to):
    # TODO: check if the move is legal
    #       - loc_from must be occupied by one of self's pieces
    #       - loc_to must not be occupied by one of self's pieces
    #       - loc_to must be in the pieces range
    piece = self.remove_piece(loc_from)
    if not loc_to in piece.get_moves(loc_from, other.pieces) or self.get_piece(loc_to):
      raise Exception(self.name, 'illegal move')
    if loc_occupied(loc_to, self.board):
      self.add_to_cap(self.remove_piece(loc_to, other))
    self.insert_piece(piece, loc_to)
  
  def get_piece(self, location):
    for elem in self.pieces:
      if elem[1] == location:
        return elem[0]
    return None

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