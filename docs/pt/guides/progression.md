# Progressão (início → fim)

A árvore de tecnologia é o verdadeiro eixo de progressão do jogo. Todo o resto — fazendas
maiores, mais drones, culturas exóticas — é consequência do que você destravou e de quão
rápido seu drone roda. Este guia é o roteiro: o que comprar, em que ordem, e *por que* cada
passo é o que destrava o seguinte.

## Como o unlock funciona de verdade

Três funções embutidas fazem todo o trabalho (assinaturas completas na
[Referência da API](../api/reference.md#economia-pesquisa)):

- `get_cost(tech)` — um dict mapeando `Items.*` para a quantidade exigida.
- `unlock(tech)` — tenta a compra; devolve se deu certo.
- `num_unlocked(tech)` — quantas vezes você comprou (`0` significa "ainda não").

O padrão seguro, tirado direto de
[`farms/leaderboards/leaderboard_run.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/leaderboards/leaderboard_run.py):

```python
def unlock_tech(tech):
    ct = get_cost(tech)
    for c in ct:
        farm_item(c, ct[c])
    if not unlock(tech):
        unlock_tech(tech)   # os preços escalam — releia o custo e tente de novo
```

!!! warning "Por que o retry importa"
    O `get_cost()` é lido **antes** de você farmar, mas os preços escalam conforme você compra.
    Quando um loop longo de farming termina, o custo cotado pode estar velho e o `unlock()`
    devolve falso. Nunca assuma que a compra passou — teste o retorno e recorra.

## Dois tipos de unlock

| Tipo | Exemplos | Comportamento |
|---|---|---|
| **Linguagem / ferramental** | `Variables`, `Operators`, `Loops`, `Functions`, `Lists`, `Dictionaries`, `Utilities`, `Import`, `Senses`, `Costs`, `Debug`, `Debug_2`, `Timing`, `Simulation`, `Auto_Unlock` | Capacidade de uma vez só. Comprar `Functions` te deixa escrever `def`; não há o que melhorar. |
| **Conteúdo / upgrade** | `Plant`, `Grass`, `Trees`, `Carrots`, `Pumpkins`, `Sunflowers`, `Cactus`, `Dinosaurs`, `Mazes`, `Expand`, `Watering`, `Fertilizer`, `Speed`, `Megafarm`, `Polyculture`, `Leaderboard` | Repetível. A primeira compra destrava a coisa; toda compra depois é um upgrade — geralmente *"aumenta o rendimento e o custo"*. |
| **Cosmético** | `Hats`, `Top_Hat`, `The_Farmers_Remains` | Diversão pura. `change_hat()` não custa nada que você precise. |

Essa divisão orienta a estratégia inteira: **unlocks de linguagem são pré-requisitos, unlocks
de conteúdo são investimentos.** Você compra os primeiros assim que aparecem, porque eles
limitam o que você consegue expressar; os segundos, quando o seu gargalo atual mandar.

## Os estágios

### Estágio 0 — um tile, sem movimento

Você tem um único tile de grama e um loop `while True:`. Colher grama é renda de graça e a
única renda. O estágio inteiro é sobre tirar a linguagem da jaula — `Variables`, `Loops`,
`Functions`, aí `Senses` pro drone saber o que tem embaixo dele, e `Plant` pra ele conseguir
botar algo ali.

```python
while True:
    if can_harvest():
        harvest()
```

### Estágio 1 — movimento e solo

`Expand` é o unlock decisivo do começo: a descrição dele diz *"Expande a terra da fazenda e
destrava o movimento."* Até você comprar, o drone é um tile só com um programa preso nele.

!!! danger "`Expand` limpa a fazenda"
    Todo **upgrade** de `Expand` apaga o campo. Isso é tranquilo quando é um passo roteirizado,
    mas significa que você nunca deve comprar `Expand` no meio de uma fusão longa ou de uma
    ordenação — você vai destruir o campo que estava prestes a colher. Scripts que expandem
    (veja o `unlock_tech()` acima) releem `get_world_size()` logo em seguida.

Com o movimento vêm `Carrots` (sua primeira cultura de solo, precisa de `till()`) e
`Watering`. Água é um nível por tile lido com `get_water()`; mantê-la acima de ~0,5 é o
multiplicador de crescimento mais barato do jogo — veja
[Água & Fertilizante](../mechanics/crops.md#agua-fertilizante).

### Estágio 2 — madeira e velocidade pura

`Trees` destrava a planta de madeira melhor, e `Grass` melhora o rendimento de feno. Os dois
alimentam os custos de unlock de tudo que vem depois. Intercalado com tudo isso: **`Speed`**,
que é comprado mais vezes que qualquer outra tecnologia numa run de reset real (cinco vezes
antes do leaderboard). Velocidade compõe com todo loop que você vai escrever, então raramente
está errado.

!!! tip "Árvores brigam entre si"
    Árvores crescem **mais devagar quando adjacentes a outras árvores**. O `farm_trees()` do
    `leaderboard_run.py` planta elas num xadrez `(get_pos_x() + get_pos_y()) % 2` exatamente
    por isso — veja [Culturas & Economia](../mechanics/crops.md#a-lista-completa).

### Estágio 3 — abóboras e fertilizante

`Pumpkins` é o primeiro rendimento **não-linear** do jogo: abóboras maduras adjacentes se
fundem, e a colheita paga o número de abóboras fundidas **ao cubo**. `Fertilizer` (−2 s do
tempo restante, por tile) é o que faz um campo grande terminar antes da sua paciência — ele é
comprado quatro vezes na run de reset de referência.

Este também é o primeiro estágio em que *paciência ganha de pressa*: colher cedo trava um
rendimento pequeno e linear. Mecânica completa, incluindo a taxa de ~1 em 5 mortes que deixa
bloqueios de `Dead_Pumpkin`, em [Fusão de abóboras](../mechanics/crops.md#fusao-de-aboboras).

### Estágio 4 — `Megafarm`: o salto de throughput

`Megafarm` — *"Destrava múltiplos drones e funções de gerenciamento de drones"* — é o maior
salto isolado do jogo. Um drone varrendo um campo 32×32 é um loop serial; dezesseis drones
dividindo por coluna é o mesmo loop dividido por dezesseis.

Tudo sobre herança de posição de spawn, divisão por colunas e o padrão drone-chefe está em
[Drones](../mechanics/drones.md#o-padrao-de-divisao-por-colunas), e o
[Tutorial 01](../tutorials/01-multi-drone.md) percorre isso do começo ao fim. Leia as
[armadilhas](../mechanics/drones.md#armadilhas-aprendidas-na-marra) antes da sua primeira farm
multi-drone, não depois.

### Estágio 5 — as culturas não-lineares

Agora as regras de rendimento começam a premiar esperteza em vez de escala:

| Unlock | O que isso realmente te compra |
|---|---|
| `Cactus` | `tamanho²` por cacto, e a **regra de colheita em cadeia** — um campo totalmente ordenado paga como se tudo tivesse sido colhido de uma vez. Isso transforma cultivo num problema de ordenação: [Ordenação de Cactos](../mechanics/cactus-sorting.md#a-regra-da-colheita-em-cadeia). |
| `Sunflowers` | `Items.Power`, o recurso que abastece a duplicação de velocidade — mais o bônus de 5× com 15 pétalas explorado pelo `sunflower_15petals.py` ([pétalas](../mechanics/crops.md#girassois-power-petalas)). |
| `Polyculture` | `get_companion()` — plantio com companheiras para bônus de rendimento. Só vale depois que você consegue rotear drones por companheira; veja [quando ganha da monocultura](../mechanics/polyculture.md#quando-policultura-ganha-da-monocultura). |

### Estágio 6 — labirintos e dinossauros

`Mazes` transforma Weird Substance em ouro via labirintos de cerca-viva com um tesouro no
centro; `Dinosaurs` transforma maçãs em ossos através de um minigame estilo cobrinha. Os dois
são *economias de re-roll* — a jogada vencedora é throughput de tentativas pequenas, não
perfeição numa só:

- [Economia do re-roll](../mechanics/mazes.md#economia-do-re-roll) e
  [por que muitos labirintos pequenos ganham de um grande](../mechanics/mazes.md#escala-muitos-labirintos-pequenos-ganham-de-um-grande).
- [Rendimento de ossos](../mechanics/dinosaurs.md#rendimento-de-ossos) e a
  [mecânica de maçã/`measure()`](../mechanics/dinosaurs.md#mecanica-das-macas-e-o-measure).

### Estágio 7 — `Leaderboard`

*"Entre no leaderboard do reset mais rápido."* Esta é a linha de chegada de uma run de reset e
o ingresso para toda a meta-camada do end-game —
[Leaderboards](../mechanics/leaderboards.md) e
[Estratégias de Leaderboard](leaderboard-strategies.md).

## O caminho mínimo canônico

O `slowest_automation()` no
[`leaderboard_run.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/leaderboards/leaderboard_run.py)
é um caminho funcional, do zero até `Leaderboard`, em **32 compras** distribuídas em 13
tecnologias. Como é um script de `Fastest_Reset`, ele toma a rota *mínima* — um piso útil pra
entender o que a progressão de fato exige:

| Tecnologia | Vezes comprada | Leitura |
|---|---|---|
| `Speed` | 5 | Comprada mais que qualquer outra; compõe com todo loop. |
| `Fertilizer` | 4 | Tempo de crescimento é o gargalo assim que os campos crescem. |
| `Carrots` / `Watering` / `Trees` / `Expand` | 3 cada | Terra, água e as duas culturas-base de renda. |
| `Pumpkins` / `Grass` / `Cactus` / `Dinosaurs` | 2 cada | Um unlock + um upgrade. |
| `Plant` / `Mazes` / `Leaderboard` | 1 cada | Portões puros. |

A ordem em que ele compra (`Speed` → `Plant` → `Carrots` → `Speed` → `Watering` → `Trees` →
`Speed` → `Expand` ×2 → …) vale a leitura completa: ela alterna **capacidade** e
**throughput**, sem nunca deixar um dos dois ficar muito à frente do outro.

!!! note "O que o caminho mínimo pula"
    O `slowest_automation()` nunca compra `Megafarm`, `Sunflowers`, `Polyculture` nem nenhuma
    tecnologia de linguagem — e mesmo assim o script usa funções, dicts e `global` à vontade.
    Uma run de `Fastest_Reset` reseta a árvore *de cultivo*, não sua capacidade de escrever
    código. Num save normal você vai querer todas elas; numa run de reset, são custo puro.

## Onde os scripts deste repo se encaixam

| Estágio | Scripts para ler |
|---|---|
| início / meio | `basics/plant_helpers.py`, `basics/pumpkin_solo.py` |
| meio | `crops/sunflower_power_simple.py`, `crops/cactus_basic_22x22.py`, `crops/cactus_bubble_22x22.py` |
| meio / fim | `crops/pumpkin_megafarm.py`, `crops/sunflower_farm.py`, os três ordenadores de cacto |
| fim | `crops/*_polyculture.py`, `crops/sunflower_15petals.py`, `mazes/treasure_wall_follower.py`, `dinosaur/*` |
| end-game | `mazes/maze_gold_dfs.py`, `mazes/maze_gold_16drones_bfs.py`, `mazes/gold_25drones.py`, tudo em `leaderboards/` |

Índice anotado completo em [`farms/README.md`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/README.md).

Veja também: [Simulação](../mechanics/simulation.md#casos-de-uso) — ensaie uma ordem de unlocks
headless com `sim_unlocks` antes de gastar horas nela, e
[Estratégias de Leaderboard](leaderboard-strategies.md) para o que fazer depois que a árvore acabar.
