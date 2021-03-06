"""
Modeled after https://github.com/fewf/curtsies_2048
The 'original': https://github.com/gabrielecirulli/2048
"""

import random, time

import sturm

def main():
    with sturm.cbreak_mode():
        play(make_board())

heading = "Use the arrow keys, U to undo (and forfeit), or Q to quit.\n\n"

def play(board):
    forfeit = False
    history = []
    while True:
        score = ("You lose!"    if is_lost(board) else
                 "You forfeit." if forfeit        else
                 "You win!"     if is_won(board)  else "")
        frame(board, score)
        key = sturm.get_key()
        if key.upper() == 'Q':
            break
        elif key.upper() == 'U':
            if history:
                board = history.pop()
                forfeit = True
        elif key in arrows:
            sliding = list(arrows[key](board))
            if sliding:
                history.append(board)
                animate(sliding, score)
                board = plop(sliding[-1], 2 if random.random() < .9 else 4)

def frame(board, score):
    sturm.render(heading, view(board), score)

def animate(boards, score):
    for board in boards:
        frame(board, score)
        time.sleep(1./25)

# A board is a tuple of 4 rows;
# a row is a tuple of 4 values;
# a value is 0 for empty, or a positive number.

def make_board(): return plop(plop(empty_board, 2), 2)

empty_board = ((0,)*4,)*4

def view(board):
    for row in board:
        for v in row:
            yield ' '; yield tiles[v] if v in tiles else S.bold(str(v))
        yield '\n\n'

S = sturm
tiles = {   0:                                         '  . ',
            2: S.on_blue(S.white(                      '  2 ')),
            4: S.on_red(S.black(                       '  4 ')),
            8: S.white(S.on_magenta(                   '  8 ')),
           16: S.black(S.on_cyan(                      ' 16 ')),
           32: S.black(S.on_green(                     ' 32 ')),
           64: S.black(S.on_yellow(                    ' 64 ')),
          128: S.black(S.on_white(                     '128 ')),
          256: S.bold(S.blue(S.on_black(               '256 '))),
          512: S.bold(S.magenta(S.on_black(            '512 '))),
         1024: S.underlined(S.bold(S.red(S.on_black(   '1024')))),
         2048: S.underlined(S.bold(S.yellow(S.on_black('2048'))))}

def is_won(board):
    return any(any(2048 <= v for v in row)
               for row in board)

def is_lost(board):
    return not any(list(move(board)) for move in arrows.values())

# Pre: board is not full.
def plop(board, v):
    return update(board, random_empty_square(board), v)

def random_empty_square(board):
    return random.choice([(r,c)
                          for r, row in enumerate(board)
                          for c, v in enumerate(row)
                          if v == 0])

def update(board, pos, new_v):
    return tuple(tuple(new_v if (r,c) == pos else v
                       for c, v in enumerate(row))
                 for r, row in enumerate(board))

def flipd(board): return tuple(zip(*board))                # diagonal flip
def fliph(board): return tuple(row[::-1] for row in board) # horizontal

# Arrow-key actions. Each returns an iterable of boards animating
# the move, an empty iterable if there's no move in that direction.
def up(board):    return map(flipd, left( flipd(board)))
def down(board):  return map(flipd, right(flipd(board)))
def right(board): return map(fliph, left( fliph(board)))
def left(board):
    states = tuple(slide(0, row) for row in board)
    while any(lo < 4 for lo,_ in states):
        yield tuple(row for _,row in states)
        states = tuple(slide(lo, row) for lo,row in states)

def slide(lo, row):
    """Slide row one place leftward, leaving fixed any places left of lo.
    Advance lo past merging or completion."""
    for i in range(lo+1, 4):
        if (row[i-1] == 0) != (row[i-1] == row[i]):
            if row[i-1] == row[i]: lo = i
            return lo, row[:i-1] + (row[i-1]+row[i],) + row[i+1:] + (0,)
    return 4, row

arrows = dict(up=up, down=down, right=right, left=left)


# Let's test sliding:
def test_left(row):
    for row, in left((row,)):
        print(row)

## test_left((0, 0, 0, 0))
## test_left((2, 4, 2, 2))
#. (2, 4, 4, 0)
## test_left((2, 2, 2, 2))
#. (4, 2, 2, 0)
#. (4, 4, 0, 0)
## test_left((0, 2, 0, 2))
#. (2, 0, 2, 0)
#. (2, 2, 0, 0)
#. (4, 0, 0, 0)
## test_left((2, 0, 2, 0))
#. (2, 2, 0, 0)
#. (4, 0, 0, 0)
## test_left((2, 0, 0, 2))
#. (2, 0, 2, 0)
#. (2, 2, 0, 0)
#. (4, 0, 0, 0)
## test_left((0, 0, 0, 2))
#. (0, 0, 2, 0)
#. (0, 2, 0, 0)
#. (2, 0, 0, 0)
## test_left((0, 2, 4, 4))
#. (2, 4, 4, 0)
#. (2, 8, 0, 0)
## test_left((0, 2, 2, 4))
#. (2, 2, 4, 0)
#. (4, 4, 0, 0)
## test_left((2, 2, 2, 4))
#. (4, 2, 4, 0)
## test_left((2, 2, 4, 4))
#. (4, 4, 4, 0)
#. (4, 8, 0, 0)


if __name__ == '__main__':
    main()
