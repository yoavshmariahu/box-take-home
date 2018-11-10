from utils import parse_location, coor_to_location
from functools import partial

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
        """
        Return a set of locations a King can move to given a string location
        and a dict of the other player's pieces. 
        
        The optional argument pieces is passed when checking if a player has 
        dropped a pawn to see if the drop has resulted in an immediate 
        checkmate, in which case the drop should not be made.

        >>> from player import Player
        >>> lower_player = Player('lower', [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']])
        >>> k = King(lower_player)
        >>> x = list(k.get_moves('c3', {}))
        >>> x.sort()
        >>> x
        ['b2', 'b3', 'b4', 'c2', 'c4', 'd2', 'd3', 'd4']
        >>> x = list(k.get_moves('e5', {}))
        >>> x.sort()
        >>> x
        ['d4', 'd5', 'e4']
        """
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
        """
        Return a set of locations a Rook can move to given a string location
        and a dict of the other player's pieces. Optional arugment pieces for 
        checkmate detection on Pawn drop.

        >>> from player import Player
        >>> lower_player = Player('lower', [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']])
        >>> r = Rook(lower_player)
        >>> x = list(r.get_moves('c3', {}))
        >>> x.sort()
        >>> x
        ['a3', 'b3', 'c1', 'c2', 'c4', 'c5', 'd3', 'e3']
        >>> r.promoted = True
        >>> x = list(r.get_moves('c3', {}))
        >>> x.sort()
        >>> x
        ['a3', 'b2', 'b3', 'b4', 'c1', 'c2', 'c4', 'c5', 'd2', 'd3', 'd4', 'e3']
        >>> x = list(r.get_moves('c1', {}))
        >>> x.sort()
        >>> x
        ['a1', 'b1', 'b2', 'c2', 'c3', 'c4', 'c5', 'd1', 'd2', 'e1']
        """
        if not pieces:
            pieces = self.player.pieces
        coor = parse_location(location)
        coors = list()
        other_locs = set(parse_location(loc) for loc in other_pieces if loc)
        self_locs = set(parse_location(loc) for loc in pieces if loc)
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
        """
        Return a set of locations a Bishop can move to given a string location
        and a dict of the other player's pieces. Optional arugment pieces for 
        checkmate detection on Pawn drop.

        >>> from player import Player
        >>> lower_player = Player('lower', [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']])
        >>> b = Bishop(lower_player)
        >>> x = list(b.get_moves('c3', {}))
        >>> x.sort()
        >>> x
        ['a1', 'a5', 'b2', 'b4', 'd2', 'd4', 'e1', 'e5']
        >>> x = list(b.get_moves('d2', {}))
        >>> x.sort()
        >>> x
        ['a5', 'b4', 'c1', 'c3', 'e1', 'e3']
        >>> b.promoted = True
        >>> x = list(b.get_moves('c3', {}))
        >>> x.sort()
        >>> x
        ['a1', 'a5', 'b2', 'b3', 'b4', 'c2', 'c4', 'd2', 'd3', 'd4', 'e1', 'e5']
        """
        if not pieces:
            pieces = self.player.pieces
        coor = parse_location(location)
        other_locs = set(parse_location(loc) for loc in other_pieces if loc)
        self_locs = set(parse_location(loc) for loc in pieces if loc)
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
        """
        Return a set of locations a GoldGeneral can move to given a string location
        and a dict of the other player's pieces. Optional arugment pieces for 
        checkmate detection on Pawn drop.

        >>> from player import Player
        >>> lower_player = Player('lower', [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']])
        >>> upper_player = Player('UPPER', [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']])
        >>> g = GoldGeneral(lower_player)
        >>> G = GoldGeneral(upper_player)
        >>> x = list(g.get_moves('c3', {}))
        >>> x.sort()
        >>> x
        ['b3', 'b4', 'c2', 'c4', 'd3', 'd4']
        >>> x = list(G.get_moves('c3', {}))
        >>> x.sort()
        >>> x
        ['b2', 'b3', 'c2', 'c4', 'd2', 'd3']
        """
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
        """
        Return a set of locations a SilverGeneral can move to given a string location
        and a dict of the other player's pieces. Optional arugment pieces for 
        checkmate detection on Pawn drop.

        >>> from player import Player
        >>> lower_player = Player('lower', [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']])
        >>> upper_player = Player('UPPER', [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']])
        >>> s = SilverGeneral(lower_player)
        >>> S = SilverGeneral(upper_player)
        >>> x = list(s.get_moves('c3', {}))
        >>> x.sort()
        >>> x
        ['b2', 'b4', 'c4', 'd2', 'd4']
        >>> s.promoted = True
        >>> x = list(s.get_moves('c3', {}))
        >>> x.sort()
        >>> x
        ['b3', 'b4', 'c2', 'c4', 'd3', 'd4']
        >>> x = list(S.get_moves('c3', {}))
        >>> x.sort()
        >>> x
        ['b2', 'b4', 'c2', 'd2', 'd4']
        """
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
        """
        Return a set of locations a Pawn can move to given a string location
        and a dict of the other player's pieces. Optional arugment pieces for 
        checkmate detection on Pawn drop.

        >>> from player import Player
        >>> lower_player = Player('lower', [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']])
        >>> upper_player = Player('UPPER', [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']])
        >>> p = Pawn(lower_player)
        >>> P = Pawn(upper_player)
        >>> x = list(p.get_moves('c3', {}))
        >>> x.sort()
        >>> x
        ['c4']
        >>> x = list(p.get_moves('d5', {}))
        >>> x.sort()
        >>> x
        [None]
        >>> p.promoted = True
        >>> x = list(p.get_moves('c3', {}))
        >>> x.sort()
        >>> x
        ['b3', 'b4', 'c2', 'c4', 'd3', 'd4']
        >>> x = list(P.get_moves('c3', {}))
        >>> x.sort()
        >>> x
        ['c2']
        """
        if self.promoted:
            return GoldGeneral.get_moves(self, location, other_pieces)
        coor = parse_location(location)
        coors = list()
        if self.id.islower() and coor[1] < 5:
            coors.append((coor[0], coor[1]+1))
        elif coor[1] > 0:
            coors.append((coor[0], coor[1]-1))
        return set(map(coor_to_location, coors))