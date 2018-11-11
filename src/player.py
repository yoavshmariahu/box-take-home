from pieces import *
from utils import parse_location, loc_occupied, get_available_locations

class Player:
    def __init__(self, name, board):
        self.name = name
        self.captures = list()
        self.pieces = dict()
        self.board = board

    #-------------CREATION METHODS-------------

    def create_piece(self, piece_id, piece_location):
        """
        Used in File Mode

        Create piece given input read from files and calls insert_piece
        with arguments piece and location.

        >>> board = [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']]
        >>> lower_player = Player('lower', board)
        >>> lower_player.create_piece('k', 'a1')
        >>> lower_player.create_piece('+p', 'e2')
        >>> board
        [['k', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '', '', '', ''], ['', '+p', '', '', '']]
        """
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
        """
        Used for File Mode

        Create piece given input read from files and add_to_cap to add
        piece to player's list of captured pieces.

        >>> board = [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']]
        >>> lower_player = Player('lower', board)
        >>> upper_player = Player('UPPER', board)
        >>> lower_player.make_captured_piece('r')
        >>> lower_player.make_captured_piece('g')
        >>> lower_player.make_captured_piece('s')
        >>> lower_player.make_captured_piece('p')
        >>> upper_player.make_captured_piece('p')
        >>> upper_player.make_captured_piece('r')
        >>> lower_player.captures
        [lower r, lower g, lower s, lower p]
        >>> upper_player.captures
        [UPPER P, UPPER R]
        """

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

    #-------------GAME ACTION METHODS-------------

    def insert_piece(self, piece, location):
        """
        Updates the player's pieces dict to map location to piece instance.
        Modifies the Board to reflect the insertion.

        >>> board = [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']]
        >>> lower_player = Player('lower', board)
        >>> upper_player = Player('UPPER', board)
        >>> k = King(lower_player)
        >>> K = King(upper_player)
        >>> lower_player.insert_piece(k, 'a1')
        >>> upper_player.insert_piece(K, 'e5')
        >>> lower_player.pieces['a1']
        lower k
        >>> upper_player.pieces['e5']
        UPPER K
        """
        self.pieces[location] = piece
        coor = parse_location(location)
        if isinstance(piece, Pawn):
            """    force Pawn promotion     
                   see details in promote() about the missing argument    """
            if self.name.islower() and coor[1] == 4:
                self.promote(location)
            elif self.name.isupper() and coor[1] == 0:
                self.promote(location)
        self.board[coor[0]][coor[1]] = piece.id

    def move_piece(self, other, origin, destination):
        """
        Executes move action by player to move piece at location origin to
        locaiton destination, meanwhile checking validity of the move.
        If the destination is occupied by the other player's piece that piece
        will be captured by the player.

        >>> board = [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']]
        >>> lower_player = Player('lower', board)
        >>> upper_player = Player('UPPER', board)
        >>> upper_player.create_piece('K', 'a4')
        >>> upper_player.create_piece('+R', 'c4')
        >>> lower_player.create_piece('+b', 'e2')
        >>> lower_player.create_piece('k', 'e1')
        >>> upper_player.create_piece('K', 'a4')
        >>> lower_player.move_piece(upper_player, 'e2', 'c4')
        >>> lower_player.pieces['c4']
        lower +b
        >>> lower_player.captures
        [lower r]
        """
        temp_pieces, temp_other_pieces = self.simulate_move(other, origin, destination)
        if self.in_check(temp_pieces, temp_other_pieces):
            raise Exception(self.name, 'illegal move', 'Moved self to check')
        piece = self.remove_piece(origin)
        if not destination in piece.get_moves(origin, other.pieces) or destination in self.pieces:
            self.insert_piece(piece, origin)
            raise Exception(self.name, 'illegal move', 'Destination not in range of piece')
        if loc_occupied(destination, self.board):
            self.add_to_cap(other.pieces.pop(destination))
        self.insert_piece(piece, destination)

    def remove_piece(self, location):
        """ 
        Helper function for move_piece

        Clear board at location and returns the piece which was previously
        at that location.
        """
        if not loc_occupied(location, self.board):
            raise Exception(self.name, 'illegal move', 'Referenced location with no piece')
        coor = parse_location(location)
        self.board[coor[0]][coor[1]] = ''
        return self.pieces.pop(location)
        
    def add_to_cap(self, piece):
        """
        Mutate the piece so that its attributes reflect that it is owned 
        by the player. Unpromote the piece if it was promoted, then add
        the piece to the player's list of captured pieces.
        """
        if piece.promoted:
            piece.id = piece.id[1]
            piece.promoted = False
        if self.name == 'lower':
            piece.id = piece.id.lower()
        elif self.name == 'UPPER':
            piece.id = piece.id.upper()
        piece.player = self
        self.captures.append(piece)

    def drop_piece(self, other, piece_id, location):
        """
        Execute drop action of player. Remove piece from list of captured
        pieces and ensure that the drop is legal.
        - Piece can only be dropped on an unoccupied space
        - If piece being dropped is a Pawn:
            (1) The drop cannot result in an immediate checkmate
            (2) The pawn cannot be dropped in the promotion zone
            (3) The pawn cannot be dropped in the same column where
                another one of a player's unpromoted pawns exists
        
        >>> board = [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']]
        >>> lower_player = Player('lower', board)
        >>> upper_player = Player('UPPER', board)
        >>> upper_player.create_piece('K', 'a4')
        >>> upper_player.create_piece('+R', 'c4')
        >>> lower_player.create_piece('+b', 'e2')
        >>> lower_player.create_piece('k', 'e1')
        >>> upper_player.create_piece('K', 'a4')
        >>> lower_player.move_piece(upper_player, 'e2', 'c4')
        >>> lower_player.pieces['c4']
        lower +b
        >>> lower_player.captures
        [lower r]
        >>> lower_player.drop_piece(upper_player, 'r', 'b2')
        >>> lower_player.captures
        []
        >>> lower_player.pieces['b2']
        lower r
        """
        if loc_occupied(location, self.board):
            raise Exception(self.name, 'illegal move', 'Dropped piece on an occupied location')
        for i in range(len(self.captures)):
            if self.captures[i].id.lower() == piece_id:
                piece = self.captures[i]
                if isinstance(piece, Pawn):
                    #   handle special cases for pawn drop
                    coor = parse_location(location)
                    temp = self.pieces.copy()
                    self.pieces = self.simulate_drop(other, piece, location)
                    if not other.avoid_checkmate(self):
                        #   case 1: immediate checkmate
                        self.pieces = temp
                        raise Exception(self.name, 'illegal move', 'Dropped pawn in immediate checkmate location')
                    elif (self.name.islower() and coor[1] == 4) \
                        or (self.name.isupper() and coor[1] == 0):
                        #   case 2: drop in promotion zone
                        raise Exception(self.name, 'illegal move', 'Dropped pawn in promotion zone')
                    for loc in self.board[coor[0]]:
                        if (loc == 'p' and self.name.islower()) or (loc == 'P' and self.name.isupper):
                            #   case 3: same column as another unpromoted pawn
                            raise Exception(self.name, 'illegal move', 'Dropped pawn in same column as another unpromoted pawn')
                self.captures.pop(i)
                self.insert_piece(piece, location)
                return
        raise Exception(self.name, 'illegal move', 'No such piece \"{0}\" in captures'.format(piece_id))  

    def can_promote(self, location):
        """
        Check if piece at location can be promoted.
        Raise Exception if player's piece can not be promoted -> illegal move
        Ensures legal promotion in Minishogi.dispatch_turns()
        """
        piece = self.pieces[location]
        if isinstance(piece, King) or isinstance(piece, GoldGeneral) or piece.promoted:
            raise Exception(self.name, 'illegal move', 'Cannot promote {0}'.format(piece))

    def promote(self, destination, origin=None):
        """
        Executes promote action on piece while it is moving from origin to destination.
        The piece can be promoted if it's origin or destination are in promotion zones.
        No value is passed to origin when forcing a pawn promotion through insert_piece().

        >>> board = [['','','','',''],['','','','',''],['','','','',''],['','','','',''],['','','','','']]
        >>> lower_player = Player('lower', board)
        >>> upper_player = Player('UPPER', board)
        >>> lower_player.create_piece('b', 'e4')
        >>> upper_player.create_piece('K', 'a4')
        >>> lower_player.create_piece('k', 'e1')
        >>> lower_player.move_piece(upper_player, 'e4', 'd5')
        >>> lower_player.promote('d5')
        >>> lower_player.pieces['d5']
        lower +b
        """
        piece = self.pieces[destination]
        if isinstance(piece, King) or isinstance(piece, GoldGeneral):
            raise Exception(piece.id, 'illegal move', 'Promoted unpromotable piece')
        if not piece.promoted:
            coor_dest = parse_location(destination)
            if origin:
                coor_orig = parse_location(origin)
            else:
                coor_orig = coor_dest
            if (piece.id.islower() and (coor_orig[1] == 4 or coor_dest[1] == 4)) \
                or (piece.id.isupper() and (coor_orig[1] == 0 or coor_dest[1] == 0)):
                piece.promoted = True
                piece.id = '+' + piece.id
            self.board[coor_dest[0]][coor_dest[1]] = piece.id

    def start_game_pieces(self):
        """
        Used in Interactive Mode

        Set up board and player to have its proper initial state at the
        beginning of the game.
        """
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

    #-------------CHECKMATE METHODS-------------

    def get_king_location(self, pieces):
        """        
        Return location of player's king
        """
        for loc in pieces:
            if isinstance(pieces[loc], King):
                return loc
        raise Exception('no king')

    def in_check(self, pieces, other_pieces):
        """
        Searches through other_pieces checking if any piece can capture the king in pieces

        Note: this function does not search directly through a player's pieces dict because
              in_check() is used for two functions:
              (1) To check if a player is in check before each turn
              (2) To determine if making a simulated move will result in the player staying
                  in check or not.
        """
        king_loc = self.get_king_location(pieces)
        for loc, other_piece in other_pieces.items():
            if king_loc in other_piece.get_moves(loc, pieces, other_pieces):
                return True
        return False

    def simulate_move(self, other, origin, destination):
        """
        Copy self.pieces and other.pieces and return a modified version of both
        where the player moved their piece from origin to destination.
        """
        if destination in self.pieces:
            return self.pieces, other.pieces
        temp_self = self.pieces.copy()
        temp_other = other.pieces.copy()
        if origin in temp_self:
            temp_self.pop(origin)
        if destination in temp_other:
            temp_other.pop(destination)
        temp_self[destination] = self.pieces[origin]
        return temp_self, temp_other

    def simulate_drop(self, other, piece, location):
        """
        Copy self.pieces and other.pieces and return a modified version of both
        where the player dropped piece in location.
        """
        temp_pieces = self.pieces.copy()
        if isinstance(piece, Pawn):
            if (self.name.islower() and parse_location(location)[1] == 4) \
                or (self.name.isupper() and parse_location(location)[1] == 0):
                return temp_pieces
        temp_pieces[location] = piece
        return temp_pieces

    def avoid_checkmate(self, other):
        """
        Return a list of all legal moves and drops that get the player out of check.
        List is empty when the player is in checkmate.

        Uses simulate_move() and simulate_drop() to determine which legal moves get
        the player out of check.
        """
        possible_moves = list()
        for loc, piece in self.pieces.items():
            for move in piece.get_moves(loc, other.pieces):
                temp_self, temp_other = self.simulate_move(other, loc, move)
                if not self.in_check(temp_self, temp_other):
                    possible_moves.append('move {0} {1}'.format(loc, move))
        for cap in self.captures:
            for loc in get_available_locations(self.board):
                temp_self = self.simulate_drop(other, cap, loc)
                if not self.in_check(temp_self, other.pieces):
                    possible_moves.append('drop {0} {1}'.format(cap.id, loc))
        return possible_moves
