import os    

def parse_location(location):
      # return coordinates given a string location e.g. e4 returns (4, 3)
      assert isinstance(location, str)
      return (ord(location[0]) - ord('a'), int(location[1])-1)

def loc_occupied(location, board):
    coor = parse_location(location)
    if board[coor[0]][coor[1]] == '':
        return False
    return True

def coor_to_location(coor):
    if coor[0] < 0 or coor[0] > 4 or coor[1] < 0 or coor[1] > 4:
        return None
    return chr(coor[1] + ord('a')) + str(coor[0]+1)

def _stringifySquare(sq):

    if type(sq) is not str or len(sq) > 2:
        raise ValueError('Board must be an array of strings like "", "P", or "+P"')

    if len(sq) == 0:
        return '__|'
    if len(sq) == 1:
        return ' ' + sq + '|'
    if len(sq) == 2:
        return sq + '|'


def stringifyBoard(board):

    s = ''

    for row in range(len(board) - 1, -1, -1):
        
        s += '' + str(row + 1) + ' |'
        for col in range(0, len(board[row])):
            s += _stringifySquare(board[col][row])

        s += os.linesep

    s += '    a  b  c  d  e' + os.linesep

    return s

def parseTestCase(path):
    f = open(path)
    line = f.readline()
    initialBoardState = []
    while line != '\n':
        piece, position = line.strip().split(' ')
        initialBoardState.append(dict(piece=piece, position=position))
        line = f.readline()
    line = f.readline().strip()
    upperCaptures = [x for x in line[1:-1].split(' ') if x != '']
    line = f.readline().strip()
    lowerCaptures = [x for x in line[1:-1].split(' ') if x != '']
    line = f.readline()
    line = f.readline()
    moves = []
    while line != '':
        moves.append(line.strip())
        line = f.readline()

    return dict(initialPieces=initialBoardState, upperCaptures=upperCaptures, lowerCaptures=lowerCaptures, moves=moves)
