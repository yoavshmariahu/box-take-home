import os    

def parse_location(location):
    """
    Return corresponding coordinates of board given string location.

    >>> parse_location('a1')
    (0, 0)
    >>> parse_location('c2')
    (2, 1)
    >>> parse_location('e5')
    (4, 4)
    """
    assert isinstance(location, str)
    return (ord(location[0]) - ord('a'), int(location[1])-1)

def coor_to_location(coor):
    """
    Return string location of board given coordinates for the board.

    >>> coor_to_location((1, 0))
    'b1'
    >>> coor_to_location((3, 4))
    'd5'
    >>> coor_to_location((0, 4))
    'a5'
    """
    if coor[0] < 0 or coor[0] > 4 or coor[1] < 0 or coor[1] > 4:
        return None
    return chr(coor[0] + ord('a')) + str(coor[1]+1)

def stringify_captures(player):
    """
    Return string of captured pieces formatted for spec output
    """
    cap_str = ''
    for piece in player.captures:
        cap_str += piece.id + ' '
    return cap_str

def get_available_locations(board):
    """
    Return list of string locations that are not occuppied by any pieces on board.
    Used in Player.avoid_checkmate() to try dropping pieces at all open locations.
    """
    locs = list()
    for i in range(len(board)):
        for j in range(len(board[i])):
            loc = coor_to_location((i, j))
            if not loc_occupied(loc, board):
                locs.append(loc)
    return locs

def loc_occupied(location, board):
    """
    Determine if location on board is occupied.
    """
    coor = parse_location(location)
    if board[coor[0]][coor[1]] == '':
        return False
    return True

def stringify_square(sq):
    if type(sq) is not str or len(sq) > 2:
        raise ValueError('Board must be an array of strings like "", "P", or "+P"')
    if len(sq) == 0:
        return '__|'
    if len(sq) == 1:
        return ' ' + sq + '|'
    if len(sq) == 2:
        return sq + '|'

def stringify_board(board):
    s = ''
    for row in range(len(board) - 1, -1, -1):
        s += '' + str(row + 1) + ' |'
        for col in range(0, len(board[row])):
            s += stringify_square(board[col][row])
        s += os.linesep
    s += '    a  b  c  d  e' + os.linesep
    return s

def parse_test_case(path):
    f = open(path)
    line = f.readline()
    initial_board_state = []
    while line != '\n':
        piece, position = line.strip().split(' ')
        initial_board_state.append(dict(piece=piece, position=position))
        line = f.readline()
    line = f.readline().strip()
    upper_captures = [x for x in line[1:-1].split(' ') if x != '']
    line = f.readline().strip()
    lower_captures = [x for x in line[1:-1].split(' ') if x != '']
    line = f.readline()
    line = f.readline()
    moves = []
    while line != '':
        moves.append(line.strip())
        line = f.readline()

    return dict(initialPieces=initial_board_state, upperCaptures=upper_captures, lowerCaptures=lower_captures, moves=moves)
