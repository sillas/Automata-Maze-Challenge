import numpy as np
from numba import njit

@njit
def calcNextPosition(current_position, direction):
    x, y = current_position
    moves = {'U': (0, -1), 'R': (1, 0), 'D': (0, 1), 'L': (-1, 0)}
    dx, dy = moves.get(direction, (0, 0))
    return [x + dx, y + dy]

@njit
def getNextState(board_window):
    cl = board_window[1, 1]
    adj = np.sum(board_window) - cl
    
    if( cl ):
        test = 3 < adj < 6
    else:
        test = 1 < adj < 5

    return 1 if test else 0

@njit
def getNextStates(board_w_pad, x, y, h, w):

  return [
    getNextState(board_w_pad[y-1:y+2, x:x+3]) if y > 0 else None,
    getNextState(board_w_pad[y:y+3, x+1:x+4]) if x < w - 1 else None,
    getNextState(board_w_pad[y+1:y+4, x:x+3]) if y < h - 1 else None,
    getNextState(board_w_pad[y:y+3, x-1:x+2]) if x > 0 else None
  ]

@njit
def pad_with_zeros(board):
    c, r = board.shape
    padded_board = np.zeros((c+2, r+2), dtype=board.dtype)
    padded_board[1:-1, 1:-1] = board
    padded_board[1, 1] = 0
    padded_board[-2, -2] = 0
    return padded_board

@njit
def matrixUpdate(board):

  c, r = board.shape

  board_w_pad = pad_with_zeros(board)
  result = np.array([[getNextState(board_w_pad[i:i+3, j:j+3]) for j in range(r)] for i in range(c)])
  
  result[0, 0] = 3
  result[-1,-1] = 4
  
  return result, pad_with_zeros(result)

@njit
def distanceCalc(x, y):
    return np.sqrt(x**2 + y**2)