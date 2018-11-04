from utils import parse_location, coor_to_location

class Piece:
  def __init__(self, player, location='captured'):
    self.location = location
    self.player = player
    if location != 'captured':
      self.player.available_locations.remove(self.location)

class King(Piece):
  def __init__(self, player, location='captured'):
    Piece.__init__(self, player, location)
    if player.name == 'lower':
      self.id = 'k'
    elif player.name == 'UPPER':
      self.id = 'K'
  def get_moves(self):
    if self.location != 'captured':
      coor = parse_location(self.location)
      coors = [(coor[0]-1, coor[1]-1), (coor[0], coor[1]-1), (coor[0]+1, coor[1]-1),
               (coor[0]-1, coor[1]), (coor[0]+1, coor[1]),
               (coor[0]-1, coor[1]+1), (coor[0], coor[1]+1), (coor[0]+1, coor[1]+1)]
      coors = filter(lambda x: x[0] > -1 and x[0] < 5 and x[1] > -1 and x[1] < 5, coors)
      locs = set(map(coor_to_location, coors))
      return locs.intersection(self.player.available_locations)
    

class Rook(Piece):
  def __init__(self, player, location='captured'):
    Piece.__init__(self, player, location)
    if player.name == 'lower':
      self.id = 'r'
    elif player.name == 'UPPER':
      self.id = 'R'
  def get_moves(self):
    if self.location != 'captured':
      coor = parse_location(self.location)
      pass

class Bishop(Piece):
  def __init__(self, player, location='captured'):
    Piece.__init__(self, player, location)
    if player.name == 'lower':
      self.id = 'b'
    elif player.name == 'UPPER':
      self.id = 'B'
  def get_moves(self):
    if self.location != 'captured':
      pass

class GoldGeneral(Piece):
  def __init__(self, player, location='captured'):
    Piece.__init__(self, player, location)
    if player.name == 'lower':
      self.id = 'g'
    elif player.name == 'UPPER':
      self.id = 'G'
  def get_moves(self):
    if self.location != 'captured':
      pass
class SilverGeneral(Piece):
  def __init__(self, player, location='captured'):
    Piece.__init__(self, player, location)
    if player.name == 'lower':
      self.id = 's'
    elif player.name == 'UPPER':
      self.id = 'S'
  def get_moves(self):
    if self.location != 'captured':
      pass
class Pawn(Piece):
  def __init__(self, player, location='captured'):
    Piece.__init__(self, player, location)
    if player.name == 'lower':
      self.id = 'p'
    elif player.name == 'UPPER':
      self.id = 'P'
  def get_moves(self):
    if self.location != 'captured':
      pass