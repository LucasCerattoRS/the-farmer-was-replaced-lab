# Tutorial 03 · Farmando Ouro em Labirintos

**Objetivo:** ouro em escala industrial. **Requer:** unlock de Mazes, Weird Substance, de preferência Megafarm.

## Como labirintos funcionam

1. Plante um **arbusto** e use `Items.Weird_Substance` nele → o arbusto vira um labirinto de
   cercas-vivas com um **tesouro** dentro. O tesouro paga `ouro = lado do labirinto`.
2. Dentro de um labirinto, `can_move(dir)` diz se uma cerca-viva te bloqueia — esse é seu
   sensor de parede.
3. `measure()` na região do tesouro devolve o `(x, y)` dele — você sabe *para onde* ir, só
   não *como*.
4. Reaplicar Weird Substance num tesouro já resolvido **re-rola tudo num labirinto novo**,
   então um mesmo canteiro pode ser farmado repetidamente antes de sacar.

## Nível 1: wall-follower (memória zero)

O clássico da regra da mão direita — sempre tente virar no sentido horário a partir da sua
última direção:

```python
def solve():
    d = East
    while get_entity_type() != Entities.Treasure:
        d = next_ccw(d)          # comece tentando virar para um lado
        while not can_move(d):
            d = next_cw(d)       # gire até aparecer uma abertura
        move(d)
```

Garantido que acha o tesouro. Lento, mas perfeito como primeiro solver.
Repo: `farms/mazes/treasure_wall_follower.py` (8 drones, um labirinto cada).

## Nível 2: DFS iterativo com pilha de caminho

Lembre de onde você veio; só explore ramos não visitados; volte desempilhando. Vários drones
podem rodar o mesmo labirinto com **ordens de direção diferentes** (definidas por
`drone_id % 2/3/5`), então eles se espalham em vez de seguir uns aos outros.
Repo: `farms/mazes/maze_gold_dfs.py`.

## Nível 3: BFS com mapa primeiro (guiado por `measure()`)

Mapeie as aberturas de cada célula uma vez, depois calcule o caminho mais curto até a
posição medida do tesouro e ande direto. Com uma grade 4×4 de labirintos 8×8 e 16 drones,
essa é a estratégia do `farms/mazes/maze_gold_16drones_bfs.py` — e a espinha dorsal do
leaderboard `Maze` (9.863.168 de ouro).

## Economia de escala

- O custo do labirinto escala com a dose de Weird Substance; re-rolar um labirinto resolvido
  ~45 vezes antes de colher (veja `farms/mazes/gold_25drones.py`) multiplica o ouro por canteiro.
- 25 drones numa grade 5×5 de labirintos ganham de 1 drone num labirinto gigante: o tempo de
  resolução cresce de forma super-linear com o tamanho, então **muitos labirintos pequenos vencem**.
