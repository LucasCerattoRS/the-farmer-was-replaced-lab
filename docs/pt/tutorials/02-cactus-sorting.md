# Tutorial 02 · Ordenação de Cactos (colheita em cadeia = tamanho²)

**Objetivo:** colher um campo inteiro de cactos no tempo de um clique.
**Requer:** unlock de Cactus, Senses (`measure`), swap.

## Por que ordenar?

Um cacto colhido sozinho dá `tamanho²` cactos — mas se **todo vizinho ao Norte e Leste for
≥ o tamanho dele e todo vizinho ao Sul/Oeste for ≤** (ou seja, o campo inteiro ordenado nos
dois sentidos), colher *um* cacto colhe **todos eles** em cadeia. Um campo 32×32 ordenado
paga centenas de milhares por colheita.

## A primitiva: `swap(direction)`

`measure()` devolve o tamanho do cacto sob o drone; `measure(North)` mede o vizinho.
`swap(North)` troca os dois. É só disso que você precisa — o resto é um algoritmo de
ordenação numa grade 2-D.

## Três algoritmos, três trade-offs (todos neste repo)

### 1. Insertion sort por linha — `farms/crops/cactus_insertion_sort.py`
Marche para Leste; enquanto o cacto atrás de você for maior, troque para trás. Simples,
poucos movimentos desperdiçados em campos quase ordenados.

### 2. Cocktail / shaker sort — `farms/crops/cactus_shaker_sort.py`
Borbulha nos dois sentidos com um limite `last_swap` que encolhe o trecho percorrido a cada
passada. É o algoritmo por trás da run de leaderboard em
`farms/leaderboards/cactus_cocktail_sort.py` (meta: 33.554.432 cactos).

```python
def shake_row(y):
    last = get_world_size() - 1
    while last > 0:
        new_last = 0
        for x in range(last):
            if measure() > measure(East):
                swap(East)
                new_last = x
            move(East)
        last = new_last
        # volta para Oeste fazendo o mesmo com a comparação '<'
```

### 3. "Teoria do vácuo" — `farms/crops/cactus_vacuum_sort.py`
Tiles vazios são tratados como tamanho **−1**, então os buracos são empurrados para um canto
e cactos recém-plantados sempre entram pelo lado ordenado. Melhor para farming contínuo, em
que você replanta enquanto ordena.

## Ordenação multi-drone

Linhas podem ser ordenadas em paralelo (um drone por faixa de linha), mas as passadas por
coluna tocam tiles compartilhados — sincronize com `wait_for()` entre as fases:
ordena todas as linhas → barreira → ordena todas as colunas → repete até não haver mais troca.

## Regra de bolso para colher

Não colha a toda oportunidade. Deixe o campo encher e ordenar por completo, aí colha uma vez
só — o rendimento escala com tamanho², então paciência literalmente compõe.
