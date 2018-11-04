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
      raise Exception(self.name, 'illegal move', 'Referenced location with no piece')
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
      raise Exception(self.name, 'illegal move', 'Dropped piece on an occupied location')
    for i in range(len(self.captures)):
      if self.captures[i].id == piece_id:
        piece = self.captures.pop(i)
        if isinstance(piece, Pawn):
          coor = parse_location(location)
          if (self.name.islower() and coor[1] == 4) \
              or (self.name.isupper() and coor[1] == 0):    # TODO: add case to check if immediate checkmate
              raise Exception(self.name, 'illegal move', 'Dropped pawn in promotion zone or immediate checkmate')
          for loc in self.board[coor[0]]:
            if (loc == 'p' and self.name.islower()) or (loc == 'P' and self.name.isupper):
              raise Exception(self.name, 'illegal move', 'Dropped pawn in same column as another unpromoted pawn')
        self.insert_piece(piece, location)
        self.pieces.append([piece, location])

  def move_piece(self, other, origin, destination):
    # TODO: check if the move is legal
    #       - origin must be occupied by one of self's pieces
    #       - destination must not be occupied by one of self's pieces
    #       - destination must be in the pieces range
    piece = self.remove_piece(origin)
    if not destination in piece.get_moves(origin, other.pieces) or self.get_piece(destination):
      raise Exception(self.name, 'illegal move', 'Destination not in range of piece')
    if loc_occupied(destination, self.board):
      self.add_to_cap(self.remove_piece(destination, other))
    self.insert_piece(piece, destination)
  
  def get_piece(self, location):
    for elem in self.pieces:
      if elem[1] == location:
        return elem[0]
    return None

  def add_to_cap(self, piece):
    if piece.promoted:
      piece.id = piece.id[1]
      piece.promoted = False
    if self.name == 'lower':
      piece.id = piece.id.lower()
    elif self.name == 'UPPER':
      piece.id = piece.id.upper()
    self.captures.append(piece)
  
  def stringify_captures(self):
    cap_str = ''
    for piece in self.captures:
      cap_str += piece.id + ' '
    return cap_str

  def promote(self, location):
    piece = self.get_piece(location)
    if isinstance(piece, King) or isinstance(piece, GoldGeneral):
      raise Exception(piece.id, 'illegal move', 'Promoted unpromotable piece')
    if not piece.promoted:
      coor = parse_location(location)
      if (piece.id.islower() and coor[1] == 4) \
         or (piece.id.isupper() and coor[1] == 0):
        piece.promoted = True
        piece.id = '+' + piece.id
        self.board[coor[0]][coor[1]] = piece.id

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