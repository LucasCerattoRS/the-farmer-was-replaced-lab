# Dinossauros

Equipar `Hats.Dinosaur_Hat` — *"Equipe para começar o jogo do dinossauro"* — transforma o
drone na cabeça de uma criatura tipo cobra: conforme ele anda, arrasta atrás de si uma cauda
de segmentos `Entities.Dinosaur`, preenchendo todo tile por onde já passou.

## O minigame

- `change_hat(Hats.Dinosaur_Hat)` inicia a run.
- `Entities.Dinosaur` — *"Um pedaço da cauda do chapéu de dinossauro. Usando o chapéu de
  dinossauro, a cauda é arrastada atrás do drone preenchendo os tiles já percorridos."*
  Tempo médio de crescimento ~0,2s, cresce em Grassland ou Soil.
- A cauda ocupa os tiles atrás do drone, então um `move()` que pisaria na própria cauda
  **falha** — essa falha é como todo script deste repo detecta "a run acabou" ou "preciso
  limpar um tile".
- `change_hat(Hats.Straw_Hat)` (ou qualquer outro chapéu) encerra o minigame e devolve o drone
  ao cultivo normal.

## Mecânica das maçãs e o `measure()`

`Entities.Apple` — *"Dinossauros amam, aparentemente."* Uma maçã nasce em algum lugar do
tabuleiro; chegar no tile dela e coletar é o loop-objetivo do minigame (cauda mais longa =
mais quadrados "ocupados" = mais valor na run).

A docstring geral de `measure()` lista Sunflower (pétalas), Maze (posição do tesouro), Cactus
(tamanho) e Dinosaur ("o número correspondente ao tipo") como as entidades com comportamento
especial. Na prática, `farms/dinosaur/apple_solver.py` chama `measure()` puro enquanto o
minigame roda e trata o resultado como a **posição `(x, y)` da maçã atual**:

```python
apple_pos = measure()
...
def measure_apple():
    global apple_pos, squares_occupied
    apple_pos = measure()
    squares_occupied += 1
```

Isso é confirmado pelo comportamento do script, não pela docstring geral — se você for
escrever seu próprio solver, verifique com um `print(measure())` no começo do jogo em vez de
assumir que o formato da tupla de posição está documentado em outro lugar.

## A rota "ondulada" em dois estágios do `apple_solver.py`

O solver roda em dois estágios alternados que varrem o tabuleiro a partir de cantos opostos:

- O **Estágio 1** varre de baixo (`apple_pos_y == 0` é a condição de contorno) para cima,
  perseguindo a coluna da maçã enquanto marca `offlimit_columns_stage2` pra que o *outro*
  estágio não cruze de novo tiles que este já reivindicou com a cauda.
- O **Estágio 2** espelha isso de cima para baixo, marcando `offlimit_columns_stage1`.
- Os dois se passam a bola (`transition_to_stage_1/2`) sempre que a maçã sai da região
  alcançável do estágio atual, ou quando a cauda está prestes a encurralar o drone.

Assim que o tabuleiro fica denso o bastante para que continuar perseguindo maçãs individuais
arrisque um beco sem saída (`squares_occupied > (world_size_minus_one) * 4 - 4` no script), ele
abandona a perseguição de vez e muda para uma **rota fixa de cobertura "ondulada"**
(`move_to_right_col_wavy`), que garante cobrir o resto do tabuleiro sem se encurralar,
usando `game_complete` (um `move()` que falhou) como condição natural de fim.

## Comportamento da cauda numa farm mais simples

O `farms/dinosaur/bone_snake_solo.py` faz o oposto: em vez de rotear ao redor da própria
cauda, ele trata um `move()` bloqueado como "limpa este tile e tenta de novo":

```python
def limpar_e_mover(direcao):
    if not move(direcao):
        if can_harvest():
            harvest()
        move(direcao)
```

Um único drone faz zigue-zague num campo 32×32 (serpentina: sobe nas colunas pares, desce nas
ímpares), colhendo segmentos da cauda (ossos) pelo caminho e limpando qualquer tile que o
bloqueie antes de tentar o movimento de novo. Muito mais simples que o solver de maçã em dois
estágios, e com um drone só — o trade-off é throughput: é uma farm de ossos "solo e confiável",
não uma maximizada.

## Rendimento de ossos

`Items.Bone` — *"Os ossos de uma criatura ancestral."* A meta do leaderboard `Dinosaur` é
**33.488.928 ossos** (multi-drone) — veja [Leaderboards](leaderboards.md). A fórmula exata de
pagamento não é publicada no stub da API; o `farms/leaderboards/fastest_reset.py` estima
internamente o custo em maçãs necessário para atingir uma meta de ossos com uma fórmula que
depende do tamanho do mundo e do nível de `Unlocks.Dinosaurs` (`farm_bones`), o que é uma
aproximação do lado do script para fins de automação, não uma constante documentada do jogo —
encare como "o rendimento escala com o tamanho do mundo e o nível do unlock `Dinosaurs`", não
como um número exato em que confiar.

Veja também: [Leaderboards](leaderboards.md) para a meta do board `Dinosaur`, e
[Estratégias de Leaderboard](../guides/leaderboard-strategies.md) para como o `bone_collector.py`
adapta o padrão de cobra para uma run de competição.
