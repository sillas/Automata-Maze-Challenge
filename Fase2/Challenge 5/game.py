import helpers
import numpy as np

class Game:
  
  board = []
  board_w_pad = []

  def __init__(self, dataset_file):

    # Ler o arquivo contendo o tabuleiro.
    try:
      self.board = np.loadtxt(dataset_file, dtype=int)
      self.board_w_pad = helpers.pad_with_zeros(self.board)

    except Exception as e:
      print('ERRO ao ler o arquivo de tabuleiro: ', e)
      exit()

  def updateBoard(self):
    self.board, self.board_w_pad = helpers.matrixUpdate( self.board )
    
  def getCurrentScenario(self, position):
      '''
      Obtem o estado futuro para cada direção partindo da posição fornecida, no formato [x, y].
      Os estados possíveis são:
      3: Posição inicial imutável,
      4: Posição final imutável,
      1: GREEN
      0: WHITE
      None: fora da borda.
      '''
      x, y = position
      h, w = self.board.shape
      U, R, D, L = helpers.getNextStates(self.board_w_pad, x, y, h, w)

      return [
        {'dir': 'R', 'state': R},
        {'dir': 'D', 'state': D},
        {'dir': 'L', 'state': L},
        {'dir': 'U', 'state': U}
      ]
