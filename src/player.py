from pieces import King, Rook, Bishop, GoldGeneral, SilverGeneral, Pawn

class Player:
  def __init__(self, name):
    self.name = name
    self.pieces = [King(name), Rook(name), Bishop(name), GoldGeneral(name), SilverGeneral(name), Pawn(name)]
    self.captures = list()