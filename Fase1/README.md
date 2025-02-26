# Stone-Automata-Maze-Challenge

O funcionamento do script é semelhante ao de um raio. O script parte em todas as direções viáveis, e o primeiro caminho que chegar ao destino, mata todos os demais e retorna a solução.
Além disso, para cada passo, se dois caminhos chegam a uma mesma célula, um deles é eliminado. Já que a partir daí, o passo seguinte é idêntico.

## Conteúdo enviado:

- game.py: Script contendo a lójica do jogo e a exibição em tela usando o Pygame. Pode ser utilizado de forma independente para executar o caminho encontrado.
- tree.py: Classe para armazenar e tratar os caminhos durante a fase de busca;
- pathfinder.py: Script de busca de um caminho. Deve ser executado para se encontrar uma solução.
- input.txt: Dataset contendo a configuração inicial do tabuleiro (fornecida pelo desafio).
- result.txt: Arquivo contendo o caminho encontrado no formato especificado pelas regras do desafio.
- README.md: Este arquivo, contendo as instruções de execução.

## Atenção:

> **Para execução correta dos scripts, todos os arquivos devem estar localizados no mesmo diretório.** > **E durante a execução, deve-se evitar clicar fora da janela de visualização, pois ela pode travar. Embora, se isto acontecer, o script continuará rodando normalmente até o final** (mesmo não influenciando no resultado do script, infelizmente não tive tempo suficiente para tratar este problema)**.**

## Instruções para execução:

1.  Instalar o Python 3.11+: https://www.python.org/downloads/ ;
2.  Instalar o Pygame: https://www.pygame.org/wiki/GettingStarted ;
3.  Descompactar o conteúdo em um diretório;
4.  Abrir um terminal nesse diretório;
5.  Executar a busca de um caminho, e em seguida, a solução encontrada:

    > python pathfinder.py

    O script irá buscar um caminho até que ele seja encontrado. Se não houver uma solução, então será encerrado. Logo que um caminho for encontrado, a tela de visualização do Pygame será fechada, e será exibido o caminho no terminal. O caminho também será salvo no arquivo

    **result.txt**, de onde pode ser consultado. Uma vez terminado a busca, pode-se teclar **[ENTER]**, pode-se executar o caminho encontrado. Se teclar **n** então encerra-se a execução.

6.  Para executar apenas a resposta, pode-se usar diretamente o script game.py:

    > python game.py
