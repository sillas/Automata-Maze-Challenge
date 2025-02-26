from pathfinder import run

if __name__ == '__main__':

  dataset = 'input1.txt'
  movementsDataset = 'output1.txt'

  # Procura o caminho mais curto, se possível.
  result = run(dataset, movementsDataset)

  if(not result):
    print("TABULEIRO SEM SOLUÇÃO!")
    exit()
  
  print("FIM!")