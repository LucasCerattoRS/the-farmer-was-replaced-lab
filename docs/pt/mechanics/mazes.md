# Labirintos & Ouro

Labirintos são a fonte de ouro dedicada do jogo: plante um arbusto, aplique Weird Substance,
e o que cresce de volta é um labirinto de cercas-vivas escondendo um tesouro.

## Cultivando um labirinto

```python
plant(Entities.Bush)
substance = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
use_item(Items.Weird_Substance, substance)
```

Esse bloco de 3 linhas ([`farms/mazes/make_maze_snippet.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/mazes/make_maze_snippet.py))
aparece, literalmente ou quase, no começo de todo script de labirinto do repo. A dose de
Weird Substance escala com o **tamanho do campo** e com o **nível do unlock `Mazes`** — cada
nível de `Mazes` dobra a dose (e, pela descrição dele, o ouro lá dentro).
`use_item(Items.Weird_Substance, n)` é a forma em lote de `use_item`: gasta `n` unidades numa
chamada só, em vez de repetir `use_item()` uma de cada vez.

## Sensores dentro do labirinto

- `can_move(direction)` — o sensor de parede. Devolve `False` se uma `Hedge` bloqueia aquela
  direção, `True` se o tile está livre (`move()` vai funcionar ali).
- `get_entity_type() == Entities.Treasure` — como todo solver reconhece que chegou.
- `measure()` — num `Treasure`, devolve a posição `(x, y)` dele e, segundo o stub da API,
  funciona **de qualquer lugar do labirinto**, não só em cima do tile do tesouro. É isso que
  transforma "vagar até achar" em "rotear direto para um destino conhecido" nos solvers mais
  avançados abaixo.

## Economia do re-roll

Depois que um tesouro é colhido, reaplicar Weird Substance no mesmo canteiro **re-rola tudo
num labirinto novo**, em vez de exigir um arbusto do zero — o campo em si não precisa ser
limpo e replantado entre tesouros. O `farms/mazes/gold_25drones.py` explora isso direto: cada
um dos 25 drones fica numa grade 5×5 de labirintos compartilhada e roda
`colher → use_item(Weird_Substance, 160) → repetir`, contando os re-rolls e só chamando o
(mais caro) `harvest()` na *45ª* passada:

```python
if get_entity_type() == Entities.Treasure:
    use_item(Items.Weird_Substance, 160)
    treasure_count += 1
    if treasure_count == 45:
        harvest()
```

A lógica: re-rolar é barato e o ouro por tesouro é fixado pelo lado do labirinto, então
juntar ~45 re-rolls antes da chamada de `harvest()` (que custa ticks) dilui o overhead da
colheita entre muitos tesouros, em vez de pagar ele toda vez.

## Wall-follower vs. DFS vs. BFS

### Wall-follower (memória zero) — `treasure_wall_follower.py`

O clássico da regra da mão direita: tente virar para o seu lado preferido; se estiver
bloqueado, gire até aparecer uma abertura; mova; repita. Garantido que acha o tesouro
eventualmente, sem estado além da direção atual. O `treasure_hunt_worker()` cria 8 drones com
direções iniciais e preferências de giro diferentes (4 horário, 4 anti-horário) pra eles não
seguirem todos a mesma parede.

### DFS iterativo com pilha de caminho — `maze_gold_dfs.py`

Mantém uma `path_stack` explícita de `(direção_tomada, próxima_direção_a_tentar)` pra poder
**voltar** em vez de vagar de novo: o `explore_option_iterative()` empilha um quadro novo toda
vez que entra num ramo não visitado, e desempilha + refaz o caminho quando um ramo dá em
beco. Vários drones rodam o mesmo labirinto com **ordens de direção permutadas**, definidas
por `drone_id % 2 / 3 / 5`, pra que drones paralelos se espalhem por ramos diferentes em vez
de convergir no mesmo caminho:

```python
if drone_id % 2:
    ALL_DIRECTIONS = ALL_DIRECTIONS[::-1]
if drone_id % 3:
    ALL_DIRECTIONS[0], ALL_DIRECTIONS[1] = ALL_DIRECTIONS[1], ALL_DIRECTIONS[0]
```

### BFS com mapa primeiro, guiado por `measure()` — `maze_gold_16drones_bfs.py`

Explora uma vez pra montar um mapa de adjacência completo do labirinto (`get_moves()` registra
toda direção aberta de toda célula visitada), repete essa rota fixa várias vezes pra farmar
os *primeiros* 200 tesouros barato, e aí muda para roteamento guiado por `measure()`: dado o
`(x, y)` do tesouro atual, o `path_move()` procura no mapa registrado um caminho até lá e
anda direto, em vez de reexplorar. Com uma grade 4×4 de labirintos 8×8 e 16 drones, essa é a
estratégia por trás da meta do leaderboard `Maze` (9.863.168 de ouro).

## Escala: muitos labirintos pequenos ganham de um grande

O tempo de resolução (wall-follower ou DFS) cresce de forma **super-linear** com o lado do
labirinto, enquanto o ouro por tesouro só cresce linearmente com ele. Esse trade-off favorece
saturar uma fazenda com muitos labirintos pequenos e rápidos de limpar em vez de um labirinto
gigante: o `gold_25drones.py` roda 25 drones numa grade 5×5 de canteiros em vez de 1 drone
num labirinto 32×32, e o `maze_gold_16drones_bfs.py` ladrilha 16 labirintos 8×8 separados em
vez de um 32×32.

## Outros scripts de labirinto neste repo

- `gold_25drones_alt.py` — uma variante da farm de re-roll com 25 drones, com limiar de re-roll
  diferente; compare com o `gold_25drones.py` pra ver o quanto a taxa de ouro é sensível a essa
  única constante.
- `maze_5x5_25drones.py` — a versão mínima: 25 drones estáticos numa grade 5×5, cada um
  resolvendo o próprio canteiro sem estado compartilhado nenhum. O mais fácil de ler entre os
  scripts de labirinto.
- `treasure_hunt_8drones_buy.py` — um wall-follower que **compra os próprios insumos**, chamando
  `get_cost()` e cultivando a Weird Substance de que precisa em vez de assumir um inventário
  abastecido. Útil se você quer uma farm de labirinto que rode sozinha.

Veja também: [Simulação](simulation.md) para ensaiar a contagem de re-rolls/taxa de ouro de uma
estratégia antes de rodar pra valer, e [Leaderboards](leaderboards.md) para as metas exatas de
`Maze` / `Maze_Single`.
