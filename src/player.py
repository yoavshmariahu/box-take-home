from pieces import King, Rook, Bishop, GoldGeneral, SilverGeneral, Pawn
from utils import parse_location, loc_occupied, stringifyBoard, get_available_locations

# TODO: Check Detection, Checkmate Detection

class Player:
  def __init__(self, name, board):
    self.name = name
    self.captures = list()
    self.pieces = dict()
    self.board = board

  def insert_piece(self, piece, location):
    self.pieces[piece] = location
    coor = parse_location(location)
    if isinstance(piece, Pawn):
      #    force Pawn promotion
      if self.name.islower() and coor[1] == 4:
        self.promote('a1', location)
      elif self.name.isupper() and coor[1] == 0:
        self.promote('a1', location)
    self.board[coor[0]][coor[1]] = piece.id

  def can_promote(self, location):
    piece = self.get_piece(location)
    if isinstance(piece, King) or isinstance(piece, GoldGeneral) or piece.promoted:
      raise Exception(self.name, 'illegal move', 'Cannot promote {0}'.format(piece))

  def make_piece(self, piece_id, piece_location):
    promoted = False
    if piece_id[0] == '+':
      promoted = True
      piece_id = piece_id[1]
    if piece_id.lower() == 'k':
      piece = King(self)
    elif piece_id.lower() == 'r':
      piece = Rook(self)
    elif piece_id.lower() == 'b':
      piece = Bishop(self)
    elif piece_id.lower() == 'g':
      piece = GoldGeneral(self)
    elif piece_id.lower() == 's':
      piece = SilverGeneral(self)
    elif piece_id.lower() == 'p':
      piece = Pawn(self)
    if promoted:
      piece.id = '+' + piece_id
      piece.promoted = True
    self.insert_piece(piece, piece_location)

  def make_captured_piece(self, piece_id):
    if piece_id.lower() == 'k':
      self.add_to_cap(King(self))
    elif piece_id.lower() == 'r':
      self.add_to_cap(Rook(self))
    elif piece_id.lower() == 'b':
      self.add_to_cap(Bishop(self))
    elif piece_id.lower() == 'g':
      self.add_to_cap(GoldGeneral(self))
    elif piece_id.lower() == 's':
      self.add_to_cap(SilverGeneral(self))
    elif piece_id.lower() == 'p':
      self.add_to_cap(Pawn(self))

  def remove_piece(self, location, sim=False):
    if not loc_occupied(location, self.board):
      if sim:
        return None
      raise Exception(self.name, 'illegal move', 'Referenced location with no piece')
    coor = parse_location(location)
    self.board[coor[0]][coor[1]] = ''
    #     moving a player's own piece
    for piece in self.pieces:
      if self.pieces[piece] == location:
        self.pieces[piece] = None
        return piece

  def jump_piece(self, location, other):
      # for i in range(len(self.pieces)):
      #   if self.pieces[i][1] == location:
      #     self.pieces[i][1] = None
      #     return self.pieces[i][0]
    #     removing other player's piece
    for piece in other.pieces:
      if other.pieces[piece] == location:
        other.pieces.pop(piece)
        self.add_to_cap(piece)
        return
    
  def drop_piece(self, other, piece_id, location):
    if loc_occupied(location, self.board):
      raise Exception(self.name, 'illegal move', 'Dropped piece on an occupied location')
    for i in range(len(self.captures)):
      if self.captures[i].id.lower() == piece_id:
        piece = self.captures[i]
        if isinstance(piece, Pawn):
          coor = parse_location(location)
          temp = self.pieces.copy()
          self.pieces = self.simulate_drop(other, piece, location)
          if not other.avoid_checkmate(self):
            self.pieces = temp
            raise Exception(self.name, 'illegal move', 'Dropped pawn in immediate checkmate location')
          elif (self.name.islower() and coor[1] == 4) \
              or (self.name.isupper() and coor[1] == 0):    # TODO: add case to check if immediate checkmate
              raise Exception(self.name, 'illegal move', 'Dropped pawn in promotion zone')
          for loc in self.board[coor[0]]:
            if (loc == 'p' and self.name.islower()) or (loc == 'P' and self.name.isupper):
              raise Exception(self.name, 'illegal move', 'Dropped pawn in same column as another unpromoted pawn')
        self.captures.pop(i)
        self.insert_piece(piece, location)
        return
    raise Exception(self.name, 'illegal move', 'No such piece \"{0}\" in captures'.format(piece_id))

  def move_piece(self, other, origin, destination):
    # TODO: check if the move is legal
    #       - origin must be occupied by one of self's pieces
    #       - destination must not be occupied by one of self's pieces
    #       - destination must be in the pieces range
    temp_pieces, temp_other_pieces = self.simulate_move(other, origin, destination)
    if self.in_check(temp_pieces, temp_other_pieces):
      raise Exception(self.name, 'illegal move', 'Moved self to check')
    piece = self.remove_piece(origin)
    if not destination in piece.get_moves(origin, other.pieces) or self.get_piece(destination):
      self.insert_piece(piece, origin)
      raise Exception(self.name, 'illegal move', 'Destination not in range of piece')
    if loc_occupied(destination, self.board):
      self.jump_piece(destination, other)
    self.insert_piece(piece, destination)
      
  
  def get_piece(self, location):
    for piece in self.pieces:
      if self.pieces[piece] == location:
        return piece
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

  def promote(self, origin, destination):
    piece = self.get_piece(destination)
    if isinstance(piece, King) or isinstance(piece, GoldGeneral):
      raise Exception(piece.id, 'illegal move', 'Promoted unpromotable piece')
    if not piece.promoted:
      coor1 = parse_location(origin)
      coor2 = parse_location(destination)
      if (piece.id.islower() and (coor1[1] == 4 or coor2[1] == 4)) \
         or (piece.id.isupper() and (coor1[1] == 0 or coor2[1] == 0)):
        piece.promoted = True
        piece.id = '+' + piece.id
        self.board[coor2[0]][coor2[1]] = piece.id

  def add_piece(self, piece, location=None):
    self.pieces[piece] = location

  def start_game_pieces(self):
    if self.name == 'lower':
      self.insert_piece(King(self), 'a1')
      self.insert_piece(Rook(self), 'e1')
      self.insert_piece(Bishop(self), 'd1')
      self.insert_piece(GoldGeneral(self), 'b1')
      self.insert_piece(SilverGeneral(self), 'c1')
      self.insert_piece(Pawn(self), 'a2')
      
    elif self.name == 'UPPER':
      self.insert_piece(King(self), 'e5')
      self.insert_piece(Rook(self), 'a5')
      self.insert_piece(Bishop(self), 'b5')
      self.insert_piece(GoldGeneral(self), 'd5')
      self.insert_piece(SilverGeneral(self), 'c5')
      self.insert_piece(Pawn(self), 'e4')

  def get_king_location(self, pieces):
    for piece in pieces:
      if isinstance(piece, King):
        return pieces[piece]
    raise Exception('no king')

  def in_check(self, pieces, other_pieces):
    king_loc = self.get_king_location(pieces)
    for other_piece, loc in other_pieces.items():
      if king_loc in other_piece.get_moves(loc, pieces, other_pieces):
        return True
    return False

  def simulate_move(self, other, origin, destination):
    for piece in self.pieces:
      if self.pieces[piece] == destination:
        return self.pieces, other.pieces
    temp_self = self.get_temp_removed(origin)
    temp_other = other.get_temp_removed(destination)
    temp_self = self.get_temp_inserted(self.get_piece(origin), destination)
    return temp_self, temp_other

  def get_temp_inserted(self, piece, location):
    temp_pieces = self.pieces.copy()
    temp_pieces[piece] = location
    return temp_pieces

  def get_temp_removed(self, location):
    #   return temp dict of pieces where the piece at location is removed
    temp_pieces = self.pieces.copy()
    for piece in temp_pieces:
      if temp_pieces[piece] == location:
        temp_pieces.pop(piece)
        return temp_pieces
    return temp_pieces

  def simulate_drop(self, other, piece, location):
    temp_pieces = self.pieces.copy()
    if isinstance(piece, Pawn):
      if (self.name.islower() and parse_location(location)[1] == 4) \
         or (self.name.isupper() and parse_location(location)[1] == 0):
         return temp_pieces
    temp_pieces[piece] = location
    return temp_pieces

  def avoid_checkmate(self, other):
    possible_moves = list()
    for piece, loc in self.pieces.items():
      for move in piece.get_moves(loc, other.pieces):
        temp_self, temp_other = self.simulate_move(other, loc, move)
        # if loc == 'e5' and move == 'e4':
        #   print(temp_self)
        #   for piece in temp_other:
        #     print(piece)
        #     print(piece.get_moves(temp_other[piece], temp_self, temp_other))
        if not self.in_check(temp_self, temp_other):
          possible_moves.append('move {0} {1}'.format(loc, move))
    for cap in self.captures:
      for loc in get_available_locations(self.board):
        temp_self = self.simulate_drop(other, cap, loc)
        if not self.in_check(temp_self, other.pieces):
          possible_moves.append('drop {0} {1}'.format(cap.id, loc))
    return possible_moves
