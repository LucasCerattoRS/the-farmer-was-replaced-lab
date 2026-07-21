# Estratégias de Leaderboard

Táticas por board, tiradas dos scripts em
[`farms/leaderboards/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/farms/leaderboards).
Para o que cada board *é* — metas, regras single vs. multi, como o `leaderboard_run()` se
comporta — comece em [Leaderboards](../mechanics/leaderboards.md). Esta página é sobre como
de fato ir bem neles.

## Ensaie antes de gastar uma run

O hábito de maior alavancagem: **nunca depure dentro de uma run real.** O `simulate()` existe
justamente pra você não precisar.

```python
run_time = simulate("f1", Unlocks, {Items.Carrot: 10000, Items.Hay: 50}, {"a": 13}, 0, 64)
```

Ele recebe os unlocks iniciais, os itens iniciais, as globais iniciais, uma `seed` e um
`speedup` — e **devolve o tempo que a run levou**. Esse retorno é o ponto inteiro: transforma
"esse algoritmo é melhor?" num número que dá pra comparar.

Duas consequências que vale internalizar:

- **Fixe a `seed` e você tem um A/B justo.** Layout de labirinto, morte de abóbora e sorteio
  de pétalas são todos semeados. Comparar dois algoritmos de ordenação em seeds diferentes
  compara sorte; comparar na mesma seed compara código.
- **Varie a `seed` e você tem a variância.** Uma estratégia que ganha na seed 0 e morre na
  seed 7 é uma estratégia que uma hora vai morrer no leaderboard. Passe por um punhado de
  seeds antes de confiar num número.

Detalhes e ressalvas em [Simulação](../mechanics/simulation.md#casos-de-uso); note em especial
os [limites](../mechanics/simulation.md#limites).

## O padrão launcher

Mantenha o launcher e a run em **arquivos separados**. O
[`launcher.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/leaderboards/launcher.py)
deste repo tem uma linha só, e essa é a ideia inteira:

```python
leaderboard_run(Leaderboards.Fastest_Reset, "leaderboard_run", 1000)
```

O script da run nunca se edita pra trocar de board ou de speedup; o launcher é o único botão.
Isso mantém o arquivo da run byte a byte idêntico entre um ensaio no `simulate()` e a
tentativa real — então o que você mediu é o que você rodou.

!!! warning "Proteja seu script de run contra o seu save vivo"
    Um script de `Fastest_Reset` assume estado limpo. Apontado pra um save real, ele vai
    alegremente dar `clear()` na sua fazenda e começar a recomprar tecnologia. O
    `leaderboard_run.py` termina com uma guarda que se recusa a rodar se a árvore não estiver
    realmente vazia:

    ```python
    if num_unlocked(Unlocks.Speed) == 0 and num_unlocked(Unlocks.Plant) == 0:
        slowest_automation()
    else:
        print("You need to call this script")
        print("from a 'leaderboard_run' or 'simulate'")
    ```

    Coloque isso no fim de todo arquivo de run do zero que você escrever.

!!! tip "Mire um número que você nunca vai alcançar"
    Tanto `power_collector.py` quanto `bone_collector.py` são chamados com `1000000000000` como
    alvo. Isso não é uma meta — é "infinito na prática". A meta do próprio board é o que para o
    cronômetro, então o script simplesmente farma até a run acabar. Um caso de borda a menos
    pra errar.

## `Fastest_Reset`

O board mais prestigiado: automatizar de um canteiro só até destravar os leaderboards de
novo. A implementação de referência é o
[`leaderboard_run.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/leaderboards/leaderboard_run.py),
e a arquitetura dele vale ser copiada inteira:

| Peça | Função |
|---|---|
| `slowest_automation()` | O roteiro — 32 chamadas de `unlock_tech()` numa ordem fixa. Veja [Progressão](progression.md#o-caminho-minimo-canonico). |
| `unlock_tech(tech)` | Farma exatamente o que `get_cost()` pede, compra, e **tenta de novo se falhar**, porque os preços mudam. |
| `farm_item(item, num)` | Tabela de despacho: cada tipo de item vai pro seu próprio loop de cultivo. |
| `get_resources_for(item, nb)` | Compra insumos em lote antes da hora — `nb = max(ws**2, nb)` — pra um campo ser plantado numa passada só, em vez de travar no meio da fileira. |
| `sow_tile(to_harvest, water, entity)` | A primitiva cavalo-de-batalha. |

O `sow_tile()` merece atenção. Ele é **idempotente** — "faça este tile virar esta planta",
seja qual for o estado inicial:

```python
def sow_tile(to_harvest, water, entity):
    if (to_harvest and can_harvest()) or get_entity_type() != entity:
        harvest()
    if get_ground_type() != get_ground(entity):
        till()
    if water and num_unlocked(Unlocks.Watering) > 0 and get_ground_type() == Grounds.Soil:
        while get_water() < 0.5 and num_items(Items.Water) > 0:
            use_item(Items.Water)
    if get_entity_type() != entity:
        plant(entity)
```

Todo loop de cultivo do arquivo vira então um corpo de duas linhas: mover, `sow_tile(...)`.
Nenhum loop precisa saber o que o tile era antes. Construa essa primitiva primeiro e o resto
de uma run de reset se escreve sozinho.

!!! note "Duas cópias neste repo"
    O [`fastest_reset.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/leaderboards/fastest_reset.py)
    e o `leaderboard_run.py` são quase-duplicatas. O `leaderboard_run.py` é a cópia de trabalho
    mais recente: ele acrescenta uma caminhada explícita de volta pra `(0, 0)` antes do loop do
    dinossauro (o padrão fixo de movimento só funciona a partir da origem) e reescreve a busca
    no labirinto pra usar `while get_entity_type() != Entities.Treasure` em vez de detecção de
    cerca-viva. Compare os dois — a diferença é um estudo de caso enxuto dos dois bugs que
    essas runs realmente cometem.

## `Cactus` — 33.554.432

O [`cactus_cocktail_sort.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/leaderboards/cactus_cocktail_sort.py)
satura o teto de drones em **duas fases**, e a barreira entre elas é o truque inteiro:

```python
while num_items(Items.Cactus) < 33554432:
    for i in range(max_drones()-1):
        spawn_drone(pro_cactus_vertical)
        move(East)
    pro_cactus_vertical()
    move_to(0, get_pos_y())
    while num_drones() > 1:
        pass                      # ← barreira: toda coluna terminou

    for i in range(max_drones()-1):
        spawn_drone(pro_cactus_gorizontal)
        move(North)
    pro_cactus_gorizontal()
    while num_drones() > 1:
        pass                      # ← barreira: toda linha terminou
    harvest()
```

Por que a barreira é obrigatória: ordenar colunas e depois linhas só produz um campo
globalmente ordenado se **toda** coluna terminar antes de **qualquer** linha começar. Um drone
que inicia a passada de linha cedo lê dados meio ordenados e corrompe a ordenação de forma
permanente. Veja
[ordenação multi-drone com barreiras](../mechanics/cactus-sorting.md#ordenacao-multi-drone-com-barreiras).

E repare na linha do pagamento: um **único `harvest()`** no fim. A
[regra de colheita em cadeia](../mechanics/cactus-sorting.md#a-regra-da-colheita-em-cadeia)
cascateia pelo campo ordenado inteiro, então uma chamada coleta tudo. Ordenar *é* o cultivo.

## `Sunflowers` — 10.000 de Power

O [`power_collector.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/leaderboards/power_collector.py)
usa um **spawn em cascata** em vez de um loop spawner central. Cada drone deriva a própria
identidade de `num_drones()` e cria o próximo:

```python
def drone_worker():
    current_drone_id = num_drones()

    if current_drone_id != 1 and get_pos_x() != initial_world_size - 1:
        move(East)
    if current_drone_id != max_drones() and get_pos_x() != initial_world_size - 1:
        spawn_drone(drone_worker)

    while num_items(Items.Power) < target_quantity:
        if can_harvest():
            harvest()
        prepare_soil_and_plant(Entities.Sunflower)
        apply_fertilizer_and_water(False, False, True)
        move(North)
```

A recursão se limita sozinha por duas condições — teto de `max_drones()` atingido, ou borda
leste alcançada — então o campo enche exatamente uma vez, sem aritmética pra errar. Ele se
apoia na [herança de posição de spawn](../mechanics/drones.md#heranca-da-posicao-de-spawn): o
filho começa onde o pai está, então "anda pro leste, aí cria" distribui os drones um por coluna.

!!! tip "`Sunflowers` e `Sunflowers_Single` dividem a mesma meta"
    Os dois querem 10.000 de Power — o único par de boards que não escala o alvo para a versão
    multi-drone. Isso torna a variante *single* a colocação genuinamente mais difícil, e é onde
    o bônus de 5× com 15 pétalas deixa de ser um luxo: veja
    [girassóis & pétalas](../mechanics/crops.md#girassois-power-petalas) e o
    `crops/sunflower_15petals.py`.

## `Dinosaur` — 33.488.928 ossos

O [`bone_collector.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/leaderboards/bone_collector.py)
é o script mais intrincado da coleção. Duas coisas o fazem funcionar:

**Ele se alimenta sozinho.** Maçãs custam cacto, então a run repõe o próprio insumo antes de
cada tentativa em vez de assumir um inventário abastecido:

```python
required_cacti = apple_cost[Items.Cactus] * (initial_world_size * initial_world_size)
if num_items(Items.Cactus) < required_cacti:
    collect_cactus_solo(required_cacti)
```

**Ele replaneja conforme a cauda cresce.** O `stage1()` vai atrás da próxima maçã (localizada
com `measure()`); o `stage2()` cai numa varredura em serpentina. Um `offset` corrente amplia a
margem de segurança conforme `length` cresce, e o script troca de perseguição direcionada para
serpentina pura assim que a cauda fica longa o bastante para que caçar maçãs arrisque
autocolisão:

```python
if length > (threshold - 8) + (offset * (initial_world_size - 2)):
    offset += 1
if offset < initial_world_size / 16:
    stage1()
else:
    stage2()
```

O `change_hat(Hats.Dinosaur_Hat)` entra no minigame; a run acaba quando `move()` devolve
`False` — você bateu na própria cauda — o que o código trava na variável `close`. Mecânica em
[Dinossauros](../mechanics/dinosaurs.md#mecanica-das-macas-e-o-measure).

## `Maze` — 9.863.168 de ouro

Não há script de leaderboard dedicado aqui, mas os solvers de end-game em
[`farms/mazes/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/farms/mazes)
são o material — o
[`gold_25drones.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/mazes/gold_25drones.py)
é o mais próximo de uma run de board, com 25 drones numa grade 5×5 de labirintos.

O ponto estratégico é econômico, não algorítmico: ouro vem de labirintos *completados*, então
throughput de labirintos pequenos ganha de profundidade em grandes, e re-rolar um layout ruim
costuma ser mais barato que resolvê-lo. Leia
[economia do re-roll](../mechanics/mazes.md#economia-do-re-roll) e
[por que muitos labirintos pequenos vencem](../mechanics/mazes.md#escala-muitos-labirintos-pequenos-ganham-de-um-grande)
antes de otimizar seu solver — um wall-follower melhor no tamanho certo de labirinto ganha de
um BFS perfeito no tamanho errado.

## Os boards `_Single` são programas diferentes

Toda categoria `_Single` roda numa **fazenda 8×8 fixa com exatamente um drone**. Nenhum dos
padrões acima sobrevive a isso: nada de spawn em cascata, nada de barreiras, nada de divisão
por colunas. Você está escrevendo um programa genuinamente diferente, que precisa ordenar *e*
colher em cadeia, ou rotear *e* coletar, de forma serial num tabuleiro pequeno. Reserve tempo
pra isso em vez de tentar degradar um script multi-drone — veja
[regras single vs. multi](../mechanics/leaderboards.md#regras-single-vs-multi).

## Checklist antes de uma tentativa

1. Rode sob `simulate()` numa **seed fixa**, depois em várias seeds.
2. Confirme que o arquivo da run tem uma guarda pra não encostar no seu save vivo.
3. Confirme que o launcher é um one-liner separado e que o arquivo da run não mudou desde a medição.
4. Defina o alvo como algo inalcançável e deixe a meta do board encerrar a run.
5. Confira os joins de drone: toda leva de `spawn_drone()` precisa de um
   `while num_drones() > 1: pass` (ou `wait_for()`) correspondente antes da fase seguinte.

Veja também: [Progressão](progression.md) para destravar a árvore em primeiro lugar, e
[Drones](../mechanics/drones.md#armadilhas-aprendidas-na-marra) para os bugs de coordenação que
mais custam runs.
