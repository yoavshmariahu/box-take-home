from utils import parse_location, coor_to_location
from functools import partial

# TODO: Promotions

class Piece:
  def __init__(self, player):
    self.player = player
    self.promoted = False
  def promote(self):
    self.promoted = True
  def demote(self):
    self.promoted = False

class King(Piece):
  def __init__(self, player):
    Piece.__init__(self, player)
    if player.name == 'lower':
      self.id = 'k'
    elif player.name == 'UPPER':
      self.id = 'K'
  def get_moves(self, location, other_pieces):
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
  def get_moves(self, location, other_pieces):
    #     return set of available moves for Rook instance
    coor = parse_location(location)
    coors = list()
    other_locs = set(parse_location(elem[1]) for elem in other_pieces)
    i = 1
    # top
    while coor[1] + i < 5:
      coors.append((coor[0], coor[1]+i))
      if (coor[0], coor[1]+i) in other_locs:
        break
      i += 1
    
    # bottom 
    i = 1
    while coor[1] - i >= 0:
      coors.append((coor[0] , coor[1]-i))
      if (coor[0], coor[1]-i) in other_locs:
        break
      i += 1
    # right
    i = 1
    while coor[0] + i < 5:
      coors.append((coor[0]+i , coor[1]))
      if (coor[0]+i, coor[1]) in other_locs:
        break
      i += 1
    # left
    i = 1
    while coor[0] - i >= 0:
      coors.append((coor[0]-i , coor[1]))
      if (coor[0]-i, coor[1]) in other_locs:
        break
      i += 1
    
    return set(map(coor_to_location, coors))


class Bishop(Piece):
  def __init__(self, player):
    Piece.__init__(self, player)
    if player.name == 'lower':
      self.id = 'b'
    elif player.name == 'UPPER':
      self.id = 'B'
  def get_moves(self, location, other_pieces):
    #     return set of available moves for Bishop instance
    coor = parse_location(location)
    other_locs = set(parse_location(elem[1]) for elem in other_pieces)
    coors = list()
    i = 1
    # upper left
    while coor[0] - i >= 0 and coor[1] - i >= 0:
      coors.append((coor[0]-i, coor[1]-i))
      if (coor[0]-i, coor[1]-i) in other_locs:
        break
      i += 1
    
    #  bottom left
    i = 1
    while coor[0] - i >= 0 and coor[1] + i < 5:
      coors.append((coor[0]-i , coor[1]+i))
      if (coor[0]-i, coor[1]+i) in other_locs:
        break
      i += 1
    # upper right
    i = 1
    while coor[0] + i < 5 and coor[1] - i >= 0:
      coors.append((coor[0]+i , coor[1]-i))
      if (coor[0]+i, coor[1]-i) in other_locs:
        break
      i += 1
    # bottom right
    i = 1
    while coor[0] + i < 5 and coor[1] + i < 5:
      coors.append((coor[0]+i , coor[1]+i))
      if (coor[0]+i, coor[1]+i) in other_locs:
        break
      i += 1
    return set(map(coor_to_location, coors))



class GoldGeneral(Piece):
  def __init__(self, player):
    Piece.__init__(self, player)
    if player.name == 'lower':
      self.id = 'g'
    elif player.name == 'UPPER':
      self.id = 'G'
  def get_moves(self, location, other_pieces):
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
  def get_moves(self, location, other_pieces):
    #     return set of available moves for SilverGeneral instance
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
  def get_moves(self, location, other_pieces):
    #     return set of available moves for Pawn instance
    coor = parse_location(location)
    coors = list()
    if self.id.islower() and coor[1] < 5:
      coors.append((coor[0], coor[1]+1))
    elif coor[1] > 0:
      coors.append((coor[0], coor[1]-1))
    return set(map(coor_to_location, coors))