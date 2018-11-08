from utils import parse_location, coor_to_location
from functools import partial

# TODO: Promotions

class Piece:
  def __init__(self, player):
    self.id = None
    self.player = player
    self.promoted = False
  def __repr__(self):
    return self.player.name + ' ' + self.id

class King(Piece):
  def __init__(self, player):
    Piece.__init__(self, player)
    if player.name == 'lower':
      self.id = 'k'
    elif player.name == 'UPPER':
      self.id = 'K'
  def get_moves(self, location, other_pieces, pieces=None):
    #     return set of available moves for King instance
    coor = parse_location(location)
    coors = [(coor[0]-1, coor[1]-1), (coor[0], coor[1]-1), (coor[0]+1, coor[1]-1),
              (coor[0]-1, coor[1]), (coor[0]+1, coor[1]),
              (coor[0]-1, coor[1]+1), (coor[0], coor[1]+1), (coor[0]+1, coor[1]+1)]
    coors = filter(lambda x: x[0] > -1 and x[0] < 5 and x[1] > -1 and x[1] < 5, coors)
    return set(map(coor_to_location, coors))
    

class Rook(Piece):
  def __init__(self, player):
    Piece.__init__(self, player)
    if player.name == 'lower':
      self.id = 'r'
    elif player.name == 'UPPER':
      self.id = 'R'
  def get_moves(self, location, other_pieces, pieces=None):
    #     return set of available moves for Rook instance
    if not pieces:
      pieces = self.player.pieces
    coor = parse_location(location)
    coors = list()
    other_locs = set(parse_location(loc) for loc in other_pieces.values() if loc)
    self_locs = set(parse_location(loc) for loc in pieces.values() if loc)
    i = 1
    # top
    while coor[1] + i < 5:
      if (coor[0], coor[1]+i) in self_locs:
        break
      coors.append((coor[0], coor[1]+i))
      if (coor[0], coor[1]+i) in other_locs:
        break
      i += 1
    
    # bottom 
    i = 1
    while coor[1] - i >= 0:
      if (coor[0], coor[1]-i) in self_locs:
        break
      coors.append((coor[0] , coor[1]-i))
      if (coor[0], coor[1]-i) in other_locs:
        break
      i += 1
    # right
    i = 1
    while coor[0] + i < 5:
      if (coor[0]+i, coor[1]) in self_locs:
        break
      coors.append((coor[0]+i , coor[1]))
      if (coor[0]+i, coor[1]) in other_locs:
        break
      i += 1
    # left
    i = 1
    while coor[0] - i >= 0:
      if (coor[0]-i, coor[1]) in self_locs:
        break
      coors.append((coor[0]-i , coor[1]))
      if (coor[0]-i, coor[1]) in other_locs:
        break
      i += 1
    
    rook_moves = set(map(coor_to_location, coors))
    if self.promoted:
      return rook_moves.union(King.get_moves(self, location, other_pieces))
    return rook_moves


class Bishop(Piece):
  def __init__(self, player):
    Piece.__init__(self, player)
    if player.name == 'lower':
      self.id = 'b'
    elif player.name == 'UPPER':
      self.id = 'B'
  def get_moves(self, location, other_pieces, pieces=None):
    #     return set of available moves for Bishop instance
    if not pieces:
      pieces = self.player.pieces
    coor = parse_location(location)
    other_locs = set(parse_location(loc) for loc in other_pieces.values() if loc)
    self_locs = set(parse_location(loc) for loc in pieces.values() if loc)
    coors = list()
    i = 1
    # upper left
    while coor[0] - i >= 0 and coor[1] - i >= 0:
      if (coor[0]-i, coor[1]-i) in self_locs:
        break
      coors.append((coor[0]-i, coor[1]-i))
      if (coor[0]-i, coor[1]-i) in other_locs:
        break
      i += 1
    
    #  bottom left
    i = 1
    while coor[0] - i >= 0 and coor[1] + i < 5:
      if (coor[0]-i, coor[1]+i) in self_locs:
        break
      coors.append((coor[0]-i , coor[1]+i))
      if (coor[0]-i, coor[1]+i) in other_locs:
        break
      i += 1
    # upper right
    i = 1
    while coor[0] + i < 5 and coor[1] - i >= 0:
      if (coor[0]+i, coor[1]-i) in self_locs:
        break
      coors.append((coor[0]+i , coor[1]-i))
      if (coor[0]+i, coor[1]-i) in other_locs:
        break
      i += 1
    # bottom right
    i = 1
    while coor[0] + i < 5 and coor[1] + i < 5:
      if (coor[0]+i, coor[1]+i) in self_locs:
        break
      coors.append((coor[0]+i , coor[1]+i))
      if (coor[0]+i, coor[1]+i) in other_locs:
        break
      i += 1

    bish_moves = set(map(coor_to_location, coors))
    if self.promoted:
      return bish_moves.union(King.get_moves(self, location, other_pieces))
    return bish_moves



class GoldGeneral(Piece):
  def __init__(self, player):
    Piece.__init__(self, player)
    if player.name == 'lower':
      self.id = 'g'
    elif player.name == 'UPPER':
      self.id = 'G'
  def get_moves(self, location, other_pieces, pieces=None):
    #     return set of available moves for GoldGeneral instance
    coor = parse_location(location)
    coors = [(coor[0], coor[1]-1),
              (coor[0]-1, coor[1]), (coor[0]+1, coor[1]),
              (coor[0], coor[1]+1)]
    if self.id.islower():
      coors.extend([(coor[0]-1, coor[1]+1), (coor[0]+1, coor[1]+1)])
    else:
      coors.extend([(coor[0]-1, coor[1]-1), (coor[0]+1, coor[1]-1)])
    coors = filter(lambda x: x[0] > -1 and x[0] < 5 and x[1] > -1 and x[1] < 5, coors)
    return set(map(coor_to_location, coors))
    
class SilverGeneral(Piece):
  def __init__(self, player):
    Piece.__init__(self, player)
    if player.name == 'lower':
      self.id = 's'
    elif player.name == 'UPPER':
      self.id = 'S'
  def get_moves(self, location, other_pieces, pieces=None):
    #     return set of available moves for SilverGeneral instance
    if self.promoted:
      return GoldGeneral.get_moves(self, location, other_pieces)
    coor = parse_location(location)
    coors = [(coor[0]-1, coor[1]-1), (coor[0]+1, coor[1]-1),
              (coor[0]-1, coor[1]+1), (coor[0]+1, coor[1]+1)]
    if self.id.islower():
      coors.append((coor[0], coor[1]+1))
    else:
      coors.append((coor[0], coor[1]-1))
    coors = filter(lambda x: x[0] > -1 and x[0] < 5 and x[1] > -1 and x[1] < 5, coors)
    return set(map(coor_to_location, coors))



class Pawn(Piece):
  def __init__(self, player):
    Piece.__init__(self, player)
    if player.name == 'lower':
      self.id = 'p'
    elif player.name == 'UPPER':
      self.id = 'P'
  def get_moves(self, location, other_pieces, pieces=None):
    #     return set of available moves for Pawn instance
    if self.promoted:
      return GoldGeneral.get_moves(self, location, other_pieces)
    coor = parse_location(location)
    coors = list()
    if self.id.islower() and coor[1] < 5:
      coors.append((coor[0], coor[1]+1))
    elif coor[1] > 0:
      coors.append((coor[0], coor[1]-1))
    return set(map(coor_to_location, coors))