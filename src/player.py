from pieces import King, Rook, Bishop, GoldGeneral, SilverGeneral, Pawn

class Player:
  def __init__(self, name, captures=[]):
    self.name = name
    self.pieces = list()
    self.captures = captures
  def add_pieces(self, pieces):
    self.pieces.extend(pieces)
  def start_game_pieces(self):
    self.pieces = [King(), Rook(), Bishop(), GoldGeneral(), SilverGeneral(), Pawn()]
    if self.name == 'lower':
      for piece in self.pieces:
        piece.id = piece.id.lower()