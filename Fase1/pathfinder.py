from game import Game
from tree import Tree
import time

def run(dataset, movementsDataset):
  '''
  Este script é inspirado no comportamento de um ráio ou no de um formiguéiro quando procura por comida.
  Vários caminhos são disparados em todas as direções possíveis. E o primeiro que encontrar o destino,
  anula os demais. Assim, ele retorna obrigatoriamente o menor caminho possível.

  Este script não é indicado para tabuleiros extremamete grandes, pois a complexidade cresce rapidamente. 
  Para cada célula, temos quatro caminhos prováveis, e o script percorre cada um deles, se possível, até chegar ao final, ou até todos eles ficarem presos.

  Para o tabuleiro proposto neste desafio, o tempo de busca e de menos de 1 minuto, nos meus testes, desde a inicialização até o fim da busca. Devo dizer que pode ser possível pensar em um script mais rápido. Mas isso me demandaria mais tempo do que disponho no momento.
  '''

  tree = Tree() # path storage
  game = Game(dataset)

  x_win = game.shape[0] - 1
  y_win = game.shape[1] - 1
  
  game.displayBoard()

  positions_to_display = [[0,0]] # inicia com a célula [0, 0], a "raiz" da árvore.
  leaves = tree.getAllLeaves() # Apenas as folhas da árvore.

  print("Buscando o caminho mais curto...")

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
  movementsDataset = 'result.txt'

  # Procura o caminho mais curto, se possível.
  result = run(dataset, movementsDataset)

  if(not result):
    print("TABULEIRO SEM SOLUÇÃO!")
    exit()
  
  choice = input('Caminho encontrado. Experimentar? [enter] ou [n]')
  if(choice == 'n'):
    exit()
  
  # executa o caminho encontrado.
  game = Game(dataset, movementsDataset)
  game.start()

  print( "Vitória!" if game.win else "Derrota." )
