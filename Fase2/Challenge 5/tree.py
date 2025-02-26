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
    self.clearDB()
    
    '''
    Inicia com o nó raiz na posição inicial.
    '''
    self.addNewRoot(0)

  def newId(self):
    self.current_id += 1
    return f'_{self.current_id}'

  def addNewRoot(self, step):
    _id = self.newId()

    self.leaves[_id] = {
      "_id": _id,
      "father": None,
      "direction": 'X',
      "position": [0, 0],
      "leaf": True,
      "step": step
    }

  def node(self, _id):
    return self.leaves.get(_id, self.tree.find_one({"_id": _id}))

  def getAllLeaves(self):

    to_delete = []
    leaves = []

    for _id in self.leaves:
      l = self.leaves[_id]

      if('stop' in l):
        # to_delete.append(_id)
        continue
      
      if(l['leaf']):
        leaves.append(_id)
      
      else:
        self.tree.insert_one(l)
        to_delete.append(_id)
    
    for _id in to_delete:
      del self.leaves[_id]
    
    return leaves

  def verifySameLeaf(self, position):
    x1, y1 = position

    for _id in self.leaves:
      l = self.leaves[_id]

      if('stop' in l):
        continue

      if(l['leaf']):
        x2, y2 = l['position']
        
        if(x1 == x2 and y1 == y2):
          return False

    return True

  def checkPosition(self, direction_to_here, father_position):
    position = hlp.calcNextPosition(np.array(father_position), direction_to_here)
    return self.verifySameLeaf(position), position

  def addNode(self, father_id, direction_to_here, father_position, new_position):
    
    new_id = self.newId()
    new_node = {
      "_id": new_id,
      "father": father_id, # id do pai.
      "direction": direction_to_here, # direção tomada do pai até aqui.
      "position": new_position,
      "leaf": True
    }

    self.leaves[new_id] = new_node
    self.leaves[father_id]["leaf"] = False # indica que o pai não é mais uma "folha".

    return new_id

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

      if(not node):
        print('ERRO! Node nao encontrado:', node_id)

      path.insert( 0, node['direction'] ) # adiciona o novo passo no início do array.

      if( not node["father"] ):
        return f"{node.get('step')} {' '.join( path ).replace('X ', '')}"
        
      node_id = node["father"]
