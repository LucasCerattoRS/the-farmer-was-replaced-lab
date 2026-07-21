# Referência da API

Tudo abaixo vem do stub `__builtins__.py` gerado pelo jogo
([mantido no repo](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/lib/__builtins__.py) para autocomplete na IDE).
As funções custam tempo de jogo ("ticks") salvo quando indicado.

## Movimento & sensores

| Função | Retorna | Resumo |
|---|---|---|
| `move(direction)` | `bool` | Move um tile; o mundo dá a volta (toro). |
| `can_move(direction)` | `bool` | Se dá pra mover naquela direção (paredes de labirinto!). |
| `get_pos_x()` / `get_pos_y()` | `int` | Coordenadas do drone. |
| `get_world_size()` | `int` | Lado da grade (quadrada). |
| `get_entity_type()` | `Entity \| None` | O que está sob o drone. |
| `get_ground_type()` | `Ground` | `Grounds.Grassland` ou `Grounds.Soil`. |
| `get_water()` | `float` | Nível de água 0–1 sob o drone. |
| `measure(direction=None)` | varia | Girassol → pétalas; tesouro/labirinto → coordenadas; cacto → tamanho; dinossauro → tipo. |

## Farming

| Função | Retorna | Resumo |
|---|---|---|
| `harvest()` | `bool` | Colhe a entidade sob o drone. |
| `can_harvest()` | `bool` | Se a planta está totalmente crescida. |
| `plant(entity)` | `bool` | Paga o custo e planta sob o drone. |
| `till()` | `None` | Alterna Soil ↔ Grassland. |
| `swap(direction)` | `bool` | Troca a entidade sob o drone com a vizinha — a chave da ordenação de cactos. |
| `use_item(item, n=1)` | `bool` | Usa `Items.Water`, `Items.Fertilizer` ou `Items.Weird_Substance`. |
| `get_companion()` | `(Entity, (x, y)) \| None` | O pedido de policultura da planta: qual entidade ela quer e onde. |

## Economia & pesquisa

| Função | Retorna | Resumo |
|---|---|---|
| `num_items(item)` | `float` | Quantidade no inventário. |
| `get_cost(thing, level=None)` | `dict \| None` | Custo de plantar/destravar algo. |
| `unlock(unlock)` | `bool` | Compra um nó da árvore de pesquisa pelo código. |
| `num_unlocked(thing)` | `int` | 1 + nível de upgrade (ou 1/0 para não-melhoráveis). |

## Drones

| Função | Retorna | Resumo |
|---|---|---|
| `spawn_drone(function)` | handle | Inicia outro drone rodando `function`; `None` se estiver no teto. |
| `wait_for(drone)` | valor | Bloqueia até aquele drone terminar; devolve o retorno dele. |
| `has_finished(drone)` | `bool` | Checagem que não bloqueia. |
| `max_drones()` / `num_drones()` | `int` | Teto de drones / ativos agora. |

## Leaderboards & simulação

| Função | Retorna | Resumo |
|---|---|---|
| `leaderboard_run(leaderboard, file_name, speedup)` | `None` | Inicia uma run cronometrada e isolada de um arquivo. |
| `simulate(filename, sim_unlocks, sim_items, sim_globals, seed, speedup)` | `float` | Roda uma simulação headless e devolve o tempo — perfeito pra testar estratégia. |
| `get_time()` | `float` | Segundos desde o início do jogo. |
| `get_tick_count()` | `int` | Ticks desde o início da execução (chamada gratuita). |

## Utilidades & diversão

| Função | Resumo |
|---|---|
| `print(*x)` | Baforada de fumaça acima do drone (custa 1s) — `quick_print(*x)` é a de graça. |
| `random()` | Float em `[0, 1)`. |
| `len` / `range` / `str` / `min` / `max` / `abs` | Os suspeitos de sempre (alguns atrás de **Utilities**). |
| `set_execution_speed(speed)` / `set_world_size(size)` | Limitadores de debug (mundo mín. 3; redimensionar limpa a fazenda). |
| `clear()` | Limpa a fazenda, volta pra (0,0), reseta o chapéu. |
| `change_hat(hat)` | Cosmético — mas `Hats.Dinosaur_Hat` realmente inicia o minigame do dino. |
| `do_a_flip()` / `pet_the_piggy()` | Essenciais. |

## Classes de constantes

- **`Items`** — `Hay`, `Wood`, `Carrot`, `Pumpkin`, `Cactus`, `Bone`, `Gold`, `Power`,
  `Water`, `Fertilizer` (−2s de crescimento), `Weird_Substance` (transforma um arbusto em
  labirinto), `Piggy`.
- **`Entities`** — `Grass` (~0,5s → Hay), `Bush` (~4s → Wood), `Tree` (~7s, mais madeira,
  cresce mais devagar perto de outras árvores), `Carrot` (~6s), `Pumpkin` (~2s, funde com
  vizinhas, rendimento n³, 1/5 morre), `Dead_Pumpkin`, `Sunflower` (~5s → Power; bônus 5× no
  máximo de pétalas com ≥ 10), `Cactus` (~1s, tamanhos 0–9, colheita em cadeia quando
  ordenado, rendimento n²), `Hedge`, `Treasure` (ouro = lado do labirinto), `Apple`,
  `Dinosaur`.
- **`Grounds`** — `Grassland`, `Soil`.
- **`Unlocks`** — a árvore de pesquisa: `Loops`, `Variables`, `Operators`, `Functions`,
  `Lists`, `Dictionaries`, `Senses`, `Speed`, `Expand`, `Grass`, `Trees`, `Carrots`,
  `Pumpkins`, `Watering`, `Fertilizer`, `Sunflowers`, `Cactus`, `Mazes`, `Dinosaurs`,
  `Polyculture`, `Megafarm` (multi-drone), `Import`, `Simulation`, `Leaderboard`,
  `Auto_Unlock`, `Costs`, `Timing`, `Utilities`, `Debug`, `Debug_2`, `Hats`, `Top_Hat`,
  `The_Farmers_Remains`.
- **`Hats`** — cosméticos, incl. troféu e chapéus `Golden_*`; `Dinosaur_Hat` é gameplay.
- **`Leaderboards`** — boards por categoria com metas fixas, ex.: `Cactus` (33.554.432),
  `Cactus_Single` (131.072 em 8×8), `Maze` (9.863.168 de ouro), `Maze_Single` (616.448),
  `Dinosaur` (33.488.928 ossos), `Fastest_Reset` (automação completa do zero — o board de prestígio).
- **`Direction`** — `North`, `East`, `South`, `West` (globais).
