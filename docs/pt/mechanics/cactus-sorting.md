# Ordenação de Cactos

Cactos são o momento "algoritmo importa" mais claro do jogo: o mesmo campo de cactos
crescidos paga ordens de magnitude a mais se você ordenar antes.

## A regra da colheita em cadeia

Um cacto tem tamanho `0`–`9`, legível com `measure()` (ou `measure(direction)` para um
vizinho). Colher um cacto sozinho e desordenado paga `tamanho²`. Mas se o campo — ou uma
região dele — estiver ordenado de forma que **todo vizinho ao Norte e Leste seja ≥ o
tamanho dele, e todo vizinho ao Sul/Oeste seja ≤**, colher *qualquer um* dos cactos daquele
bloco ordenado **colhe o bloco inteiro em cadeia**, numa ação só. Um campo 32×32 totalmente
ordenado paga como se os 1024 cactos tivessem sido colhidos um a um, no tempo de uma única
chamada de `harvest()`.

A primitiva que torna a ordenação possível é `swap(direction)`: ela troca a entidade sob o
drone com a vizinha na direção dada, e funciona mesmo se um dos lados estiver vazio
(`None`). Combinada com `measure()`, um campo de cactos vira um array ordenável in-place
numa grade 2-D.

## Três algoritmos (todos neste repo)

### 1. Insertion sort por linha — `cactus_insertion_sort.py`

Varre cada linha e coluna e, sempre que o tile de trás for maior que o atual, dá `swap()`
para trás até ficar no lugar — insertion sort clássico, aplicado uma vez por linha e depois
uma vez por coluna:

```python
def insertion_sort_row_step():
    while get_pos_x() > 0:
        if measure() < measure(West):
            swap(West)
            move(West)
        else:
            break
```

Simples, e barato num campo **quase ordenado** (poucas trocas por passada) — mas cada linha
cria um drone novo por passada (`plant_and_sort_all_rows`), e depois uma segunda leva por
coluna, então o overhead de coordenação é real.

### 2. Cocktail / shaker sort — `cactus_shaker_sort.py`

Borbulha nos dois sentidos por passada, com um limite `last_swap` que **encolhe o trecho
percorrido** a cada passada — assim que um sufixo/prefixo para de produzir trocas, ele é
excluído da passada seguinte:

```python
while x_curr < right:
    if measure() < measure(East):
        swap(East)
        loc_last_swap = x_curr
    move(East)
    x_curr += 1
right = loc_last_swap   # a próxima passada não anda além daqui
```

É o algoritmo por trás da run de leaderboard em
[`farms/leaderboards/cactus_cocktail_sort.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/leaderboards/cactus_cocktail_sort.py)
(meta do board `Cactus`: 33.554.432 cactos). O `pro_swap()` dele também se recusa a trocar a
menos que um dos lados esteja genuinamente fora de ordem *e* o drone não esteja na borda do
campo, evitando chamadas de `swap()` desperdiçadas no limite.

### 3. "Teoria do vácuo" — `cactus_vacuum_sort.py`

Trata tiles vazios como tamanho **−1** em vez de pulá-los, então toda comparação empurra os
buracos para um canto, exatamente como faria com um cacto normal:

```python
def medir_com_vazio(direcao):
    val = measure(direcao) if direcao != None else measure()
    return -1 if val == None else val
```

Isso faz com que cactos recém-plantados (tamanho 0) e buracos vazios derivem na mesma
direção conforme a ordenação avança — ideal para **farming contínuo**, em que o campo é
replantado e ordenado ao mesmo tempo, em vez de ordenado uma vez e colhido.

## Comparação de complexidade

| Algoritmo | Melhor caso | Pior caso | Melhor para |
|---|---|---|---|
| Insertion sort (por linha) | Quase linear em linhas quase ordenadas | Quadrático em linhas ordenadas ao contrário | Campos que ficam quase ordenados entre colheitas |
| Cocktail / shaker sort | Passadas com limite que encolhe cortam comparações desperdiçadas | Quadrático no pior caso, igual ao bubble sort | Runs de leaderboard — determinístico, sem contabilidade extra |
| Vácuo (buraco = "−1") | Mesma assintótica de insertion/shaker | Igual | Campos que replantam continuamente em vez de reencher em lote |

Nenhum dos três scripts publica uma alegação formal de complexidade — esta tabela reflete o
padrão de caminhada que cada um implementa (comparar-e-trocar em tiles adjacentes), que é
fundamentalmente da família insertion/bubble, independentemente da variante; a diferença
está em quanta caminhada *desperdiçada* cada variante evita.

## Ordenação multi-drone com barreiras

Linhas podem ser ordenadas em paralelo (um drone por linha), mas a passada por coluna
seguinte toca tiles que todo drone de linha acabou de escrever — ordene todas as linhas,
**sincronize**, aí ordene todas as colunas:

```python
drones = []
for _ in range(world_size - 1):
    drones.append(spawn_drone(shake_row))
    move(North)
shake_row()          # este drone ordena a última linha ele mesmo
wait_for_drones(drones)   # barreira: toda linha tem que terminar antes
```

O `sort_all_columns()` em `cactus_cocktail_sort.py`/`cactus_insertion_sort.py` repete a mesma
barreira spawn-e-`wait_for` para as colunas. Pular a barreira — começar a ordenar colunas
antes de toda linha terminar — reintroduz desordem no meio da ordenação, já que uma troca de
coluna pode desfazer uma linha que ainda não foi visitada nessa passada.

## Regra de bolso para colher

Não colha a toda oportunidade. Deixe o campo encher e ordenar por completo, aí colha uma vez
— o rendimento escala com `tamanho²` e com o comprimento da cadeia, então paciência compõe.
Veja [Culturas & Economia](crops.md#cactos-rendimento-regra-de-cadeia) para a fórmula de
rendimento e [Drones](drones.md) para as primitivas de barreira/sincronização usadas acima.
