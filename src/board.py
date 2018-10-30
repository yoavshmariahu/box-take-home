from utils import parse_location

class Board:
  def __init__(self):
    self.places = [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']]
    self.contained_pieces = set()
  def remove_piece(self, piece):
    pass