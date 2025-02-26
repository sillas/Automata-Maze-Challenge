import helpers as hlp
import numpy as np
import pymongo

class Tree:

  startNode = None
  tree = None
  leaves = {}
  current_id = 0

  def __init__(self):

    client = pymongo.MongoClient("mongodb://localhost:27017/") # MongoDB - cainho padrão
    mydb = client["tree"]
    self.tree = mydb["nodes"] 

    self.tree.create_index("leaf")
    self.tree.create_index("dist")
    self.clearDB()
    
    '''
    Inicia com o nó raiz na posição inicial.
    '''
    root = {
      "_id": '_0',
      "father": None,
      "direction": 'X',
      "position": [0, 0],
      "dist": 0,
      "lives": 1,
      "leaf": True
    }

    self.leaves['_0'] = root

  def newId(self):
    self.current_id += 1
    return f'_{self.current_id}'

  def node(self, _id):
    return self.leaves.get(_id, self.tree.find_one({"_id": _id}))

  def verifySameLeaf(self):

    check = set()
    leaves = []
    to_delete = []

    for _id in self.leaves:
      l = self.leaves[_id]

      if('stop' in l):
        to_delete.append(_id)

      elif(l['leaf']):
        x, y = l['position']

        if((x, y) in check):
          to_delete.append(_id)
          continue

        check.add((x, y))
        leaves.append(_id)

      else:
        self.tree.insert_one(l)
        to_delete.append(_id)
    
    for _id in to_delete:
      del self.leaves[_id]

    return leaves

  def addNode(self, father_id, direction, father_position, step):
    
    lives = self.leaves[father_id]["lives"]

    if( direction['state'] == 1 and step < 500 ): # decidi aplicar a "licença" a partir desse passo.
      return None, None

    if( direction['state'] == 1 and lives >= 6 ):
      return None, None

    if( direction['state'] == 1 ):
      lives += 1

    position = hlp.calcNextPosition(np.array(father_position), direction['dir'])
    dist = hlp.distanceCalc(position[0], position[1])

    new_id = self.newId()
    new_node = {
      "_id": new_id,
      "father": father_id, # id do pai.
      "direction": direction['dir'], # direção tomada do pai até aqui.
      "position": position,
      "dist": dist,
      "lives": lives,
      "leaf": True
    }
    
    self.leaves[new_id] = new_node
    self.leaves[father_id]["leaf"] = False # indica que o pai não é mais uma "folha".

    return position, new_id

  def pruneTheTree(self, distance=0):
    # obtem a folha mais distante
    maxi_id = max( self.leaves, key=lambda _id: self.leaves[_id]['dist'] )
    # elimina todas as folhas menores

    dist = self.leaves[maxi_id]["dist"]
    print("Max. dist.:", dist)

    for _id in self.leaves.copy():
      if( self.leaves[_id]['leaf'] and self.leaves[_id]['dist'] < dist-distance ):
        self.leaves[_id]['stop'] = True

  def clearDB(self):
    print('Limpando os dados no disco...')
    self.tree.delete_many({})

  def getPathFrom(self, node_id):
    '''
    percorre a árvore do nó (nodeId) até a raiz, montando o caminho.
    '''
    path = []

    while True:
      node = self.node( node_id )
      path.insert( 0, node['direction'] ) # adiciona o novo passo no início do array.

      if( not node["father"] ):
        print('Path size:', len(path) - 1)
        self.clearDB() # Apaga tudo.
        return ' '.join( path ).replace('X ', '')
        
      node_id = node["father"]
