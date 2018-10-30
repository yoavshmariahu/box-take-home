from utils import parse_location

class Board:
  def __init__(self):
    self.places = [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']]
  def start_game(self):
    self.places = [['k','p','','','R'],['g','','','','B'],['s','','','','S'],['b','','','','G'],['r','','','P','K']]
  def add_piece(self, piece, location):
    coor = parse_location(location)
    self.places[coor[0]][coor[1]] = piece.id
  def remove_piece(self, piece):
    pass