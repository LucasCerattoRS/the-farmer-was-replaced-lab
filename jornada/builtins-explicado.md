# `__builtins__.py` explicado

Fonte: `Saves/pygame2/__builtins__.py` (2.321 linhas, lido em 2026-10-10).
Cada afirmação abaixo vem desse arquivo ou está marcada como **[não confirmado]**.

## 1. O que é esse arquivo (e o que NÃO é)

- É **só para o editor** (VS Code/Pylance): dá autocompletar, dicas de tipo e a documentação ao passar o mouse.
- **Não é executado pelo jogo.** O jogo tem as funções dele por dentro. O arquivo só descreve como elas são.
- A linguagem do jogo **não é Python de verdade**; o próprio cabeçalho diz que as definições são uma "aproximação".
- O jogo regenera o arquivo. Não edite.
- Todo corpo de função é `...`. Não há lógica ali, só assinatura + docstring.
- Se o editor não achar as funções, abra a **pasta inteira** do save. Em alguns editores é preciso `from __builtins__ import *`.

## 2. Ticks: a moeda de tempo do jogo

Quase toda docstring diz "takes N ticks". Isso é o custo de tempo do seu código.

| Tipo de ação | Custo |
|---|---|
| Ações que mexem no mundo e **deram certo** (`harvest`, `plant`, `till`, `move`, `swap`, `use_item`, `clear`, `change_hat`, `spawn_drone`, `unlock`) | **200 ticks** |
| A mesma ação **falhando** (não colheu, não andou, etc.) | **1 tick** |
| Consultas (`can_harvest`, `get_pos_x`, `get_entity_type`, `num_items`, `measure`, `can_move`…) | **1 tick** |
| `get_time()`, `get_tick_count()`, `quick_print()` | **0 ticks** |
| `print()`, `do_a_flip()`, `pet_the_piggy()` | **1 segundo** (não é afetado por upgrades de velocidade) |
| `set_execution_speed`, `set_world_size`, `simulate`, `leaderboard_run` | 200 ticks |

Consequência prática: **gastar ação à toa custa caro**. Checar `can_harvest()` (1 tick) antes de `harvest()` evita um `harvest` inútil, mas um que dá certo custa 200 de qualquer jeito.

## 3. Tipos e coleções (linhas 1–700)

- `Primitive` = `bool | int | float | string | None`.
- `Hashable` = o que pode ser chave de `dict` ou elemento de `set`: primitivos, tuplas, enums, `range`, `Drone`.
- `Any` = tudo que existe na linguagem do jogo: primitivos, `range`, funções, `tuple/list/set/dict`, enums, `Drone`.
- `string` é o nome do tipo `str` (por isso o `str(x)` do jogo devolve `string`). `range_class` é o tipo devolvido por `range()`.
- As classes `list`, `set` e `dict` com docstrings extras estão **comentadas** (linhas 140–446). É opcional ativar; se ativar, comente o `import` de `list, set, dict` lá em cima e use sempre `list()`, `dict()`, `set()` (nada de literais `[]`/`{}`).
- **Funções de coleção** (`add`, `append`, `insert`, `len`, `pop`, `remove`) valem **como método ou como função**:
  `lista.pop()` é o mesmo que `pop(lista)`.
  - `append`, `add`, `len`: 1 tick.
  - `insert`: `1 + len(lista) - índice` ticks.
  - `pop(lista, i)`: `len(lista) - i` ticks; sem índice ou em `dict`: 1 tick.
  - `remove`: em `set` 1 tick; em `list`, comparações + deslocamentos.
- `range(stop)`, `range(start, stop)`, `range(start, stop, step)`: 1 tick, devolve `range_class` (não é lista).
- `str(objeto)`: 1 tick.

## 4. Enums do jogo

**Direções** (`Direction`): `North` (cima), `East` (direita), `South` (baixo), `West` (esquerda).

**`Entities`** (o que pode estar numa casa):

| Entity | Pontos-chave do arquivo |
|---|---|
| `Grass` | cresce sozinho em grassland; colher dá `Hay`; ~0,5 s |
| `Bush` | dá `Wood`; ~4 s; grassland ou soil |
| `Tree` | mais `Wood` que o arbusto; demora mais se houver árvores vizinhas; ~7 s |
| `Carrot` | só em **soil**; ~6 s |
| `Pumpkin` | só em soil; ~2 s; abóboras vizinhas maduras se fundem; ~1 em 5 morre (`Dead_Pumpkin`); colher dá `Pumpkin` = (nº de abóboras da mega abóbora)³ |
| `Dead_Pumpkin` | inútil; `can_harvest()` é sempre `False`; some quando você planta outra coisa |
| `Sunflower` | só em soil; ~5 s; dá `Power`; bônus ×5 se tiver o máximo de pétalas **e** ≥10 girassóis |
| `Cactus` | só em soil; ~1 s; tamanhos 0–9; colher em ordem ordenada colhe os vizinhos em cadeia; dá cactus = (nº colhidos)² |
| `Dinosaur`, `Apple` | parte da cauda do chapéu de dinossauro / a maçã que ele come |
| `Hedge`, `Treasure` | partes do labirinto; o tesouro tem ouro = lado do labirinto |

**`Grounds`**: `Grassland` (padrão, grama nasce sozinha) e `Soil` (terra arada, necessária para cenoura, abóbora, girassol, cacto).

**`Items`**: `Hay`, `Wood`, `Carrot`, `Pumpkin`, `Cactus`, `Bone`, `Gold`, `Power`, `Water`, `Fertilizer`, `Weird_Substance`, `Piggy` (aposentado).
- `Power`: o drone usa sozinho para andar 2× mais rápido.
- `Fertilizer`: tira 2 s do tempo de crescimento.
- `Weird_Substance`: em arbusto cria labirinto; em outras plantas alterna "infecção".
- `Water`: `use_item(Items.Water)` rega.

**`Hats`**: 26 chapéus cosméticos (`Straw_Hat`, `Top_Hat`, `Dinosaur_Hat`, troféus…). `Dinosaur_Hat` tem função real (jogo do dinossauro); os demais, pelo arquivo, são visuais **[não confirmado se algum tem efeito além do dinossauro]**.

**`Leaderboards`**: placares por cultura (`Hay`, `Wood`, `Carrots`, `Pumpkins`, `Cactus`, `Sunflowers`, `Maze`, `Dinosaur`, `Fastest_Reset`) e versões `_Single`.

**`Unlocks`** (a árvore de progresso, em ordem alfabética no arquivo): `Expand`, `Speed`, `Plant`, `Senses`, `Loops`, `Variables`, `Operators`, `Functions`, `Lists`, `Dictionaries`, `Import`, `Utilities`, `Timing`, `Costs`, `Debug`, `Simulation`, `Hats`, `Grass`, `Trees`, `Carrots`, `Pumpkins`, `Sunflowers`, `Cactus`, `Dinosaurs`, `Mazes`, `Watering`, `Fertilizer`, `Polyculture`, `Megafarm`, `Leaderboard`, `Auto_Unlock`, `Top_Hat`, `The_Farmers_Remains`.
Importante: **o que você pode usar depende do que já desbloqueou**. O arquivo lista tudo, inclusive o que o seu save ainda não liberou. Funções de `Plant`, `Senses`, `Loops` etc. aparecem no autocompletar, mas **[não confirmado]** se o jogo recusa o uso antes do unlock (ver `save.json`, chave `unlocks`).

## 5. Funções por grupo

### Lavoura
| Função | O que faz |
|---|---|
| `harvest() -> bool` | colhe o que está sob o drone. **Se não estiver maduro, destrói.** |
| `can_harvest() -> bool` | há algo pronto para colher? |
| `plant(entity) -> bool` | gasta o custo e planta; falha se faltar recurso, solo errado ou já houver planta |
| `till()` | grassland → soil; se já é soil, **volta** a grassland |
| `swap(direction) -> bool` | troca a entidade daqui com a vizinha (funciona com `None`; não com todas) |
| `use_item(item, n=1) -> bool` | usa `Water`, `Fertilizer`, `Weird_Substance` |
| `clear()` | limpa o que está sob o drone |
| `change_hat(hat)` | troca o chapéu |

### Movimento
- `move(direction) -> bool`: anda 1 casa. **A borda dá a volta** (sai por um lado, entra pelo outro).
- `can_move(direction) -> bool`
- `get_pos_x()`, `get_pos_y()`, `get_world_size()` (lado do grid).

### Sentidos
- `get_entity_type()` → `Entity` ou `None` se vazio.
- `get_ground_type()` → `Ground`.
- `get_water()` → número de 0 a 1.
- `num_items(item)` → quantidade no inventário.
- `get_companion()` → `(entidade, (x, y))` ou `None` (plantio companheiro / Polyculture).
- `measure(direction=None)`: girassol → pétalas; cacto → tamanho; dinossauro → número do tipo; labirinto → posição do tesouro; outras → `None`.

### Megafazenda (vários drones)
- `spawn_drone(função, *args) -> Drone` (ou `None` se já estão todos criados). Recebe uma função **sem chamar** (`spawn_drone(f)`, não `spawn_drone(f())`).
- `wait_for(drone)` espera e devolve o retorno da função do drone.
- `has_finished(drone)`, `max_drones()`, `num_drones()`.

### Depuração e teste
- `get_time()` (segundos desde o início), `get_tick_count()`.
- `set_execution_speed(v)`: `1` = velocidade base; `0` ou negativo = volta ao máximo.
- `set_world_size(n)`: mínimo 3; **limpa a fazenda e reposiciona o drone**.
- `simulate(...)`: roda um arquivo numa fazenda simulada com unlocks/itens/seed definidos; devolve o tempo. Precisa do unlock `Simulation`.
- `leaderboard_run(leaderboard, nome_arquivo, speedup)`.

### Auto unlock
- `get_cost(coisa, nivel=None)` → dict de custos ou `None`.
- `unlock(unlock) -> bool`: compra o desbloqueio por código.
- `num_unlocked(coisa)`: nível atual (1 + upgrades) ou 0/1.

### Matemática e utilidades
- `random()` (0 a 1), `min(*args)`, `max(*args)`, `abs(x)` (os três últimos exigem `Utilities`).
- `print(...)`: escreve em fumaça sobre o drone, **1 s** de espera. `quick_print(...)`: 0 ticks (use para depurar sem custo).
- `do_a_flip()`, `pet_the_piggy()`: 1 s, só diversão.

## 6. Armadilhas para quem vem do Python

1. **Não é Python:** o Pylance pode marcar erro em código que o jogo aceita (e o contrário). Quem manda é o jogo.
2. `from typing import ...` **quebra no jogo** (o arquivo avisa). Dicas de tipo só para o editor.
3. `harvest()` em planta verde **destrói** a planta.
4. `till()` é um interruptor, não só "arar".
5. `move()` dá a volta no mapa: `get_pos_x()` nunca passa de `get_world_size()-1`.
6. Falhar custa 1 tick, acertar custa 200: loops que tentam sem checar gastam pouco, mas loops que agem sem necessidade gastam muito.
7. `print()` custa 1 segundo reais; para investigar, use `quick_print()`.

## 7. Primeiros experimentos sugeridos (quando você começar o `main.py`)

Só com o que o save já libera (grass, soil, harvest, pass, tap…, ver `save.json`):
1. `harvest()` num laço e observar o `Hay` subir.
2. Medir quantos ticks um ciclo gasta com `get_tick_count()` antes e depois.
3. Anotar na nota da sessão qualquer comportamento que **contradiga** esta página.

*Lacunas: não li as docstrings completas dos `Unlocks` (custos e níveis) nem o texto de cada `Hat`; o arquivo não traz custos de `plant`/`unlock` (para isso, `get_cost`).*
