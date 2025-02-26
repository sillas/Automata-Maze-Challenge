from game import Game
from tree import Tree
import copy
import time

def run(dataset, movementsDataset):

  game = Game(dataset)
  tree = Tree() # path storage

  leaves = tree.leaves

  print("Buscando os caminhos...")
  step = 0

  add_new_particle = True
  paths = []

  while True:

    if( step >= 50_000 ):
      tree.clearDB()
      return False
    
    if( not leaves ):
      if( len(paths) == 0 ):
        print('paths esta vazio!')
        return False

      with open(movementsDataset, 'w', encoding="utf-8") as f:
        paths_txt = '\n'.join(paths)
        f.write(paths_txt)
      
      tree.clearDB()
      return True
    
    for leaf in copy.deepcopy(leaves):

      node = tree.leaves[leaf]
      position = node['position']
      
      stuck = True
      for direction in game.getCurrentScenario(position):

        if( direction['state'] in [0, 3, 4] ):
          stuck = False # Não estamos presos!

          position_allowed, new_position = tree.checkPosition(direction['dir'], position)
          x, y = new_position

          if(not position_allowed and game.board[y, x] != 4):
            continue # para a próxima direção

          _id = tree.addNode(leaf, direction['dir'], position, new_position)
          
          if( game.board[y, x] == 4 ):
            print("End Particle")
            add_new_particle = False
            paths.append(tree.getPathFrom(_id))
            tree.leaves[_id]['stop'] = True

          break # preferência para a direita e para baixo.

      if( stuck ):
        tree.leaves[leaf]['stop'] = True
    
    if( add_new_particle ):
      tree.addNewRoot(step)

    leaves = tree.getAllLeaves()
    game.updateBoard()
    step += 1


