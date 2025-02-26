from game import Game
from tree import Tree
import copy

def run(dataset, movementsDataset):

  tree = Tree() # path storage
  game = Game(dataset)
  leaves = tree.leaves # Apenas as folhas da árvore.

  print("Buscando o caminho mais curto...")
  step = 1
  while True:

    if( step >= 50_000):
      print('LIMITE DE PASSOS:', step)
      tree.clearDB()
      return False
    
    if( not leaves ): # Se não há mais folhas, não há solução.
      tree.clearDB()
      return False

    for leaf in copy.deepcopy(leaves):
      
      node = tree.node(leaf)
      position = node['position']

      stuck = True
      for direction in game.getCurrentScenario( position ):

        if( direction['state'] != None ): # não pode sair do tabuleiro.
          new_position, _id = tree.addNode(leaf, direction, position, step)

          if( _id == None ):
            continue

          stuck = False # Não estamos presos!
          
          x, y = new_position
          if( game.board[y, x] == 4 ): # Se uma das posições for 4, encerra aqui mesmo.
            print("FINISH")
            path = tree.getPathFrom(_id) # Percorre a árvore até a raiz para obter o caminho.
            print(path)

            with open(movementsDataset, 'w', encoding="utf-8") as f:
              f.write(path)
              
            return True

      if( stuck ): # Se não houve direção viável, esta folha ficou presa, e é "terminada".
        tree.leaves[leaf]['stop'] = True

    # Poda as folhas mais próximas da origem.
    if(step > 59 and not step % 10):
      print(step)
      tree.pruneTheTree(11)
      
    # Se no mesmo passo, duas folhas estão na mesma célula, apenas uma é necessária.
    leaves = tree.verifySameLeaf()
    game.updateBoard()

    step += 1

  print('Steps:', step)
  return False
