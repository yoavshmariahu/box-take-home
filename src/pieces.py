class King:
  def __init__(self, player):
    if player == 'UPPER':
      self.id = 'K'
    else:
      self.ed = 'k'
  def get_moves(self):
    pass

class Rook:
  def __init__(self, player):
    if player == 'UPPER':
      self.id = 'R'
    else:
      self.ed = 'r'
  def get_moves(self):
    pass

class Bishop:
  def __init__(self, player):
    if player == 'UPPER':
      self.id = 'B'
    else:
      self.ed = 'b'
  def get_moves(self):
    pass

class GoldGeneral:
  def __init__(self, player):
    if player == 'UPPER':
      self.id = 'G'
    else:
      self.ed = 'g'
  def get_moves(self):
    pass

class SilverGeneral:
  def __init__(self, player):
    if player == 'UPPER':
      self.id = 'S'
    else:
      self.ed = 's'
  def get_moves(self):
    pass

class Pawn:
  def __init__(self, player):
    if player == 'UPPER':
      self.id = 'P'
    else:
      self.ed = 'p'
  def get_moves(self):
    pass