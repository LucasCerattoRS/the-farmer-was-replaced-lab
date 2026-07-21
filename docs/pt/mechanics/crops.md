# Culturas & Economia

Cada entidade plantável, direto de [`farms/lib/__builtins__.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/lib/__builtins__.py),
mais as notas de economia que caem por terra ao jogar isso em escala.

## A lista completa

| Entidade | Solo | Tempo médio | Rende | Notas |
|---|---|---|---|---|
| `Entities.Grass` | Grassland ou Soil | ~0,5s | `Items.Hay` | Cresce sozinha em Grassland; colher é manutenção opcional. |
| `Entities.Bush` | Grassland ou Soil | ~4s | `Items.Wood` | A planta de madeira básica; mais barata e rápida que `Tree`. |
| `Entities.Tree` | Grassland ou Soil | ~7s | `Items.Wood` (mais que Bush) | Cresce **mais devagar com outras árvores adjacentes** — espace ou aceite a penalidade (veja o xadrez `(x + y) % 2` em `farm_trees()`, no `leaderboard_run.py`). |
| `Entities.Carrot` | Soil | ~6s | `Items.Carrot` | Rendimento fixo, sem fusão — o bônus de companheira na policultura é o que torna isso interessante no late-game. |
| `Entities.Pumpkin` | Soil | ~2s | `Items.Pumpkin` = n³ | Veja [fusão de abóboras](#fusao-de-aboboras) abaixo. |
| `Entities.Sunflower` | Soil | ~5s | `Items.Power` | Veja [girassóis & pétalas](#girassois-power-petalas) abaixo. |
| `Entities.Cactus` | Soil | ~1s | `Items.Cactus` = n² | Colhe em cadeia quando o campo está ordenado — mecânica completa na página de [Ordenação de Cactos](cactus-sorting.md). |
| `Entities.Dead_Pumpkin` | — | — | nada | `can_harvest()` é sempre `False`; some quando algo novo é plantado por cima. |

## Água & Fertilizante

- `get_water()` devolve um nível `0`–`1` sob o drone; `use_item(Items.Water)` completa. Mais água acelera o crescimento — a maioria das farms de end-game mantém a água acima de `0,5`–`0,75` como piso.
- `Items.Fertilizer`: `use_item(Items.Fertilizer)` corta na hora **2 segundos** do tempo restante de crescimento da planta sob o drone. Barato o suficiente pra usar sem dó em culturas de alto valor (abóboras, maçãs), onde cada segundo de crescimento é throughput.
- Os dois são efeitos por tile; um drone varrendo o campo só rega/aduba o tile onde está pisando.

## Fusão de abóboras

Abóboras **se fundem com abóboras adjacentes já crescidas** numa única mega-abóbora. Colher isso rende `Items.Pumpkin` igual ao **número de abóboras fundidas, ao cubo** (n³) — é por isso que megafarms existem: um campo 32×32 totalmente fundido (1024 abóboras) faz qualquer coisa que um drone sozinho colhesse tile a tile parecer piada.

O porém: **cerca de 1 em cada 5 abóboras morre** ao crescer, deixando uma `Dead_Pumpkin`. Abóboras mortas são inúteis, bloqueiam a fusão e precisam ser limpas (plantar algo novo por cima resolve). Tanto `farms/crops/pumpkin_megafarm.py` quanto `pumpkin_megafarm_v2.py` rodam um **drone-chefe** que confere o tamanho da mega-abóbora em `(0,0)` via `measure()` enquanto os drones operários só replantam tiles mortos — veja [Drones](drones.md) para o padrão.

!!! tip "Dimensionando a colheita"
    O `pumpkin_megafarm.py` limita a meta em 1.000.000 de abóboras (`ALVO_COLHEITA`) como gatilho conservador, em vez de esperar uma fusão teórica do campo inteiro — uma colheita menor e confiável ganha de uma gigante que às vezes falha.

## Girassóis, Power & pétalas

Girassóis viram `Items.Power` ao serem colhidos — o recurso que o drone queima automaticamente pra dobrar a própria velocidade. Cada girassol também tem uma **contagem de pétalas**; `measure()` num girassol devolve isso. Se você colher um girassol **no máximo de pétalas, e existirem pelo menos 10 girassóis**, você ganha um **bônus de 5×** naquela colheita.

O `farms/crops/sunflower_15petals.py` explora isso direto: fica replantando e remedindo cada girassol novo, matando (colhendo) qualquer um que não seja um sorteio de 15 pétalas, e só deixa amadurecer a planta de 15 — transformando toda colheita do campo num pagamento de 5× em vez de apostar que o bônus aconteça naturalmente.

## Cactos (rendimento & regra de cadeia)

Cactos vêm em **10 tamanhos (0–9)**. Uma colheita isolada dá `tamanho²` cactos. O pagamento de verdade é a **regra de colheita em cadeia**: colher um cacto colhe recursivamente todo cacto adjacente que esteja em ordem em relação a ele (crescendo ao Norte/Leste, decrescendo ao Sul/Oeste). Um campo totalmente ordenado paga como se você tivesse colhido cada cacto dele numa ação só. Mecânica completa, os três algoritmos de ordenação e a coordenação multi-drone estão em [Ordenação de Cactos](cactus-sorting.md).

## Notas de economia

- **Tempo de crescimento vs. densidade de rendimento** define qual cultura farmar em qual fase: grama/feno é quase de graça e serve pra bootstrapar tudo; cenoura e abóbora são o feijão com arroz do mid-game; cacto e girassol só compõem depois que você tem os unlocks (`Cactus`, `Polyculture`) e o throughput multi-drone pra explorar as regras de rendimento não-linear deles.
- Mecânicas de fusão/cadeia (abóbora n³, cacto n²) significam que **paciência ganha de pressa**: colher cedo trava um rendimento pequeno e linear. Deixar o campo encher e colher só uma vez maximiza o expoente.
- Plantio com companheiras (`get_companion()`) muda a conta ainda mais — veja [Policultura](polyculture.md) para quando isso ganha de uma monocultura pura.

Veja também: [Drones](drones.md) para o padrão de farming multi-drone usado por todo script de cultura acima, e [Simulação](simulation.md) para testar estratégias de rendimento sem tocar num campo real.
