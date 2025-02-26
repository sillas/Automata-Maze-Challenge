from pathfinder import run

if __name__ == '__main__':

  dataset = 'input2.txt'
  movementsDataset = 'output2.txt'

  # Procura o caminho mais curto, se possível.
  result = run(dataset, movementsDataset)

  if(not result):
    print("TABULEIRO SEM SOLUÇÃO!")
    exit()
  
  print("FIM!")