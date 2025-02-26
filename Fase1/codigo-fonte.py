import pygame
import time

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

    except:
      print(f'\nERRO: Arquivo "{movement_file}" não encontrado!\n')

    try:
      with open(dataset_file, 'r') as f:
        dataset = f.readlines()
        self.board = [[ int(cell) for cell in line.replace('\n', '').split(' ')] for line in dataset]
        self.shape = [ len(self.board[0]), len( self.board ) ] # [X, Y]

    except:
      print(f'\nERRO: Arquivo "{dataset_file}" não encontrado!\n')
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
      time.sleep(0.1)

      if( self.finish ):
        return self.win
    
    return False

class Tree:
  startNode = None
  tree = {}
  lastId = -1

  def __init__ (self):

    '''
    Inicia com o nó raiz na posição inicial.
    '''
    self.tree['root'] = {
      "father": None,
      "direction": 'X',
      "position": [0, 0],
      "children": [],
      "stop": False
    }

  def calcNextPosition (self, current_position, direction):
    '''
    Dada uma posição [x, y] e uma direção (U|R|D|L), calcula a nóva célula.
    '''
    x, y = current_position

    if( direction == 'U' ):
      return [x, y - 1]
    
    if( direction == 'R' ):
      return [x + 1, y]
    
    if( direction == 'D' ):
      return [x, y + 1]
    
    if( direction == 'L' ):
      return [x - 1, y]
    
    return current_position # se não for possível, permanece na celula atual.

  def newId(self):
    '''
    Apenas um gerador de id único, curto e simples.
    '''

    self.lastId += 1
    return f"id_{ self.lastId }"

  def node(self, id):
    return self.tree[id]

  def verifySameLeaf(self):
    '''
    Retorna as folhas excluindo as repetidas
    Apenas uma em cada célula, e no mesmo passo é permitido.
    '''
    check = {}
    leaves = []

    for id in self.getAllLeaves():

      node = self.tree[id]
      x, y = node['position']
      pos_id = f"{x},{y}"

      if( pos_id in check ):
        node["stop"] = True # fim deste caminho!
        continue

      check[ pos_id ] = True
      leaves.append(id)
    
    return leaves

  def addNode(self, father, direction_to_here, father_position):
    
    position = self.calcNextPosition(father_position, direction_to_here)
    node_id = self.newId()

    self.tree[ node_id ] = {
      "father": father, # id do pai.
      "direction": direction_to_here, # direção tomada do pai até aqui.
      "position": position,
      "children": [],
      "stop": False # False = ainda é um caminho válido.
    }

    self.tree[father]['children'].append( node_id ) # indica que o pai não é mais uma "folha".
    return [position, node_id]

  def getPathFrom(self, nodeId):
    '''
    percorre a árvore do nó (nodeId) até a raiz, montando o caminho. 
    '''
    path = []

    while True:
      node = self.tree[ nodeId ]
      path.insert( 0, node['direction'] ) # adiciona o novo passo no início do array.

      if( not node["father"] ):
        print('Path size:', len(path) - 1)
        return ' '.join( path ).replace('X ', '')
        
      nodeId = node["father"]

  def getAllLeaves(self):
    '''
    Obtém todas as folhas, excluindo as que foram "terminadas".
    '''
    leaves = []

    for id in self.tree:
      leaf = self.tree[id]

      if( len( leaf["children"]) == 0 and not leaf["stop"] ):
        leaves.append(id)
    
    return leaves

def pathfinder(dataset, movementsDataset):
  '''
  O funcionamento do script é semelhante ao de um raio. O script parte em todas as direções viáveis, e o primeiro caminho que chegar ao destino, mata todos os demais.
  Além disso, para cada passo, se dois caminhos chegam a uma mesma célula, um deles é eliminado. Já que a partir daí, o passo seguinte é idêntico.
  '''

  tree = Tree() # path storage
  game = Game(dataset)

  x_win = game.shape[0] - 1
  y_win = game.shape[1] - 1
  
  game.displayBoard()

  positions_to_display = [[0,0]] # inicia com a célula [0, 0], a "raiz" da árvore.
  leaves = tree.getAllLeaves() # Apenas as folhas da árvore.

  print("Buscando...")

  while True:

    if( len(leaves) == 0 ): # Se não há mais folhas, não há solução.
      game.terminate()
      return False

    game.displayBoard(positions_to_display) # mostra apenas as folhas no tabuleiro.
    positions_to_display = [] # reinicia para o próximo passo.

    for leaf in leaves:
      node = tree.node(leaf)
      position = node['position']

      directions = game.getCurrentScenario( position )
      stuck = True

      for direction in directions:

        if( direction['state'] in [0, 3, 4] ): # é permitido voltar à célula inicial.

          stuck = False # Não estamos presos!

          new_position, id = tree.addNode(leaf, direction['dir'], position)
          positions_to_display.append(new_position) # apenas para visualização no tabuleiro.

          if( direction['state'] == 4 ): # Se uma das posições for 4, encerra aqui mesmo.
            print("FINISH")
            path = tree.getPathFrom(id) # Percorre a árvore até a raiz para obter o caminho.
            print(path)

            with open(movementsDataset, 'w') as f:
              f.write(path)
              
            game.terminate()
            return True

      if( stuck ): # Se não houve direção viável, este nó ficou preso, e é "terminado".
        node['stop'] = True

    # Se no mesmo passo, duas folhas estão na mesma célula, apenas uma é necessária.
    # A outra é "terminada".
    leaves = tree.verifySameLeaf() 
    game.updateBoardOnly()

  game.terminate()
  return False

if __name__ == '__main__':
  dataset = 'input.txt'
  movements_dataset = 'result.txt'

  # Procura o caminho mais curto, se possível.
  result = pathfinder(dataset, movements_dataset)

  if(not result):
    print("TABULEIRO SEM SOLUÇÃO!")
    exit()
  
  choice = input('Caminho encontrado. Experimentar? [enter] ou [n]: ')
  if(choice == 'n'):
    exit()
  
  # executa o caminho encontrado.
  game = Game(dataset, movements_dataset)
  game.start()

  print( "Vitória!" if game.win else "Derrota." )