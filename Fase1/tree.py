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

if __name__ == '__main__':
  '''
  TESTE
  '''
  tree = Tree()

  id1 = tree.addNode('root', 'A', [0, 0])
  id2 = tree.addNode(id1[1], 'B', [1, 0])
  id3 = tree.addNode(id1[1], 'C', [0, 1])
  id4 = tree.addNode(id3[1], 'D', [2, 0])
  id5 = tree.addNode(id3[1], 'E', [1, 1])
  id6 = tree.addNode(id2[1], 'F', [1, 1])
  id7 = tree.addNode(id5[1], 'G', [3, 1])

  path = tree.getPathFrom(id7[1])

  print(path)
  print(tree.tree)