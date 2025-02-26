import pygame
from time import sleep, time

class Game:
  WHITE = 0
  GREEN = 1
  BLACK = 2
  FINISH = 4  

  COLORS = [
    (255, 255, 255),
    (0, 255, 0),
    (0, 0, 0),
    (0, 0, 255),
    (255, 0, 0)
  ]
  
  window = None
  board = []
  shape = [0, 0] # [X, Y]
  position = [0, 0]
  finish = False
  win = False
  movement = None

  def __init__(self, dataset_file, movement_file = None):

    try:
      if( movement_file ):
        with open(movement_file, 'r') as f:
          self.movement = f.read().replace('\n', '').split(' ')

    except Exception as e:
      print('ERRO ao ler o arquivo de movimentos: ', e)

    try:
      with open(dataset_file, 'r') as f:
        dataset = f.readlines()
        self.board = [[ int(cell) for cell in line.replace('\n', '').split(' ')] for line in dataset]
        self.shape = [ len(self.board[0]), len( self.board ) ] # [X, Y]

    except Exception as e:
      print(e)
      exit()
    
    w, h = self.shape
    window_width = (w * 10) + (w - 1)
    window_height = (h * 10) + (h - 1)

    pygame.init()
    self.window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Autômato')
  
  def getCurrentScenario(self, position = None):
    '''
    Obtem o estado futuro para cada direção, partindo da posição fornecida no formato array [x, y].
    Os estados possíveis são:
    
    3: Posição inicial imutável,
    4: Posição final imutável,
    1: self.GREEN
    0: self.WHITE
    None: fora da borda.

    Parâmetro:
    position: [x, y] | None

    return: dict
    '''
    x, y = position if position else self.position
    w, h = self.shape

    U = self.getNextState(x, y - 1, withCurrent = True) if y > 0 else None
    R = self.getNextState(x + 1, y, withCurrent = True) if x < w - 1 else None
    D = self.getNextState(x, y + 1, withCurrent = True) if y < h - 1 else None
    L = self.getNextState(x - 1, y, withCurrent = True) if x > 0 else None

    return [
      {'dir': 'U', 'state': U},
      {'dir': 'R', 'state': R},
      {'dir': 'D', 'state': D},
      {'dir': 'L', 'state': L}
    ]
 
  def cell(self, x, y):
    '''
    Método auxiliar.
    Apenas retorna o valor de uma célula na posição x, y. 
    '''    
    return self.board[y][x]

  def getNextState(self, cellX, cellY, withCurrent = False):
    '''
    Dado a posição de uma célula, calcula qual o seu próximo estado.

    retorna self.GREEN ou self.WHITE ou -1, caso não haja alteração.
    Caso 'withCurrent' seja verdadeiro e a célula não mude de estado,
    retorna o valor corrente, ao invez de -1.
    '''

    adj_green_count = 0

    y = -1
    for n in range(9):
      if( n == 4 ):
        continue

      x = ( n%3 ) - 1
      
      update = True
      if( (cellY + y) < 0 or (cellX + x) < 0):
        update = False
      
      elif( (cellX + x) >= self.shape[0] or (cellY + y) >= self.shape[1]):
        update = False
      
      if( update ):
        cell_state = self.cell(cellX + x, cellY + y)
        adj_green_count += 0 if cell_state > 1 else cell_state

      y += int( x == 1 )

    color = self.cell(cellX, cellY)

    if( color == self.WHITE and
     adj_green_count in [2,3,4]):
      return self.GREEN
    
    elif( color == self.GREEN and
     not adj_green_count in [4, 5] ):
      return self.WHITE
    
    return color if withCurrent else -1
    
  def updateBoardOnly(self):
    '''
    Atualiza o tabuleiro com os novos estados 
    sem verificações adicionais de vitória ou derrota.
    É utilizado como auxiliar na execução normal, e também na etapa de 
    calculo de rotas, quando as posições são calculadas externamente.
    '''
    tempBoard = [] # para isolar os novos estados dos estados antigos.

    for l in self.board: # "deep copy" 
      tempBoard.append(l.copy())

    for i in range(self.shape[0]):
      for j in range(self.shape[1]):
        tempBoard[j][i] = self.getNextState( i, j, withCurrent = True )
    
    self.board = [] # "deep copy" 
    for l in tempBoard:
      self.board.append(l.copy())

  def updateBoardAndVerify(self):
    '''
    Atualiza o tabuleiro, verificando se houve vitória ou derrota.
    '''
    self.updateBoardOnly()

    x, y = self.position

    color = self.cell(x, y)
    if( color == self.GREEN ): # posiçao em uma célula "verde": Derrota!
      self.finish = True

    if( color == self.FINISH ): # posiçao em uma célula "4": Vitória!
        self.finish = True
        self.win = True

  def displayBoard(self, itens = None):
    '''
    Exibe o tabuleiro na tela usando o PyGame
    '''
    if(not itens):
      itens = [self.position]

    self.window.fill((255, 255, 255))

    for i, line in enumerate(self.board):
      for j, value in enumerate(line):
        x = j * 11
        y = i * 11

        color = self.COLORS[value]

        if( [j, i] in itens ):
          color = self.COLORS[self.BLACK]
        
        pygame.draw.rect(self.window, color, (x, y, 10, 10))
    pygame.display.update()

  def moveTo(self, direction):
    '''
    Recebe uma direção (U|R|D|L) e calcula a nova posição.
    '''

    if( self.finish ):
      return False

    x, y = self.position

    if( direction == 'U' ):
      y -= 1
    elif( direction == 'D' ):
      y += 1
    elif( direction == 'L' ):
      x -= 1
    elif( direction == 'R' ):
      x += 1
    else:
      return False # Comando inválido!
    
    # Se a próxima posição está fora do tabuleiro, não faz nada.
    if( x < 0 or y < 0 or x >= self.shape[0] or y >= self.shape[1] ):
      return True

    self.position = [x, y]
    self.updateBoardAndVerify()
    self.displayBoard()

    return True

  def terminate(self):
    pygame.quit()

  def start(self):
    '''
    Se um caminho foi fornecido de um arquivo, executa-o. 
    '''
    if( not self.movement ):
      return False

    x = y = 0

    self.displayBoard()

    count = 1

    for step in self.movement:

      self.moveTo( step )
      self.displayBoard()

      print('step ', step, count)
      count += 1
      sleep(0.1)

      if( self.finish ):
        return self.win
    
    return False


if __name__ == '__main__':
  # TESTE
  dataset = 'input.txt'
  path_dataset = 'result.txt'

  game = Game(dataset, path_dataset) 
  game.start()

  print( "Vitória!" if game.win else "Derrota." )
  sleep(3)
  game.terminate()
  