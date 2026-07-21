# Tutorial 06 · Caça a Seeds com `simulate()`

**Objetivo:** parar de adivinhar se uma mudança deixou sua farm mais rápida, e começar a medir.
**Requer:** unlock de Simulation, Dictionaries.

A superfície da API está documentada em [Simulação](../mechanics/simulation.md). Esta página é
o *método* — como transformar o `simulate()` num instrumento de medição.

## Por que isso existe

`simulate()` é a única função do jogo que te devolve um **número que dá pra otimizar**:

```python
run_time = simulate(filename, sim_unlocks, sim_items, sim_globals, seed, speedup)
```

Todo o resto te conta sobre o mundo agora. Esta te conta quanto tempo uma estratégia *levou*.
Isso a torna uma função de fitness, e uma função de fitness transforma "acho que dividir em 4
colunas é melhor" num experimento.

## Regra 1 — seed fixa compara código, seed aleatória compara sorte

Layout de labirinto, morte de abóbora e sorteio de pétalas são todos guiados pela `seed`. Rode
dois algoritmos em duas seeds diferentes e o número mais rápido pode ser só o tabuleiro mais
sortudo:

```python
SEED = 12345

a = simulate("shaker_sort",    Unlocks, {}, {}, SEED, 64)
b = simulate("insertion_sort", Unlocks, {}, {}, SEED, 64)

quick_print("shaker:", a, " insertion:", b)
```

Mesma seed, mesmos unlocks iniciais, mesmos itens — a única diferença é o arquivo. Agora a
comparação significa alguma coisa.

## Regra 2 — depois varie a seed, porque um número não é um resultado

Uma estratégia que ganha na seed 12345 e morre na seed 7 uma hora vai morrer no leaderboard.
Varra um punhado e olhe a dispersão, não só o melhor:

```python
seeds = [1, 2, 3, 5, 8, 13, 21]
total = 0
pior = 0

for s in seeds:
    t = simulate("shaker_sort", Unlocks, {}, {}, s, 64)
    total += t
    if t > pior:
        pior = t
    quick_print("seed", s, "->", t)

quick_print("media:", total / len(seeds), " pior:", pior)
```

!!! tip "Otimize o pior caso, não a média"
    Uma run de leaderboard é uma tentativa **única**. Uma estratégia com ótima média e péssimo
    pior caso é uma estratégia que vai te entregar esse pior caso justo na run que valia. Quando
    dois candidatos têm médias parecidas, fique com o de dispersão menor.

## Regra 3 — `sim_globals` parametriza sem editar o arquivo

Esta é a parte que passa batido. O `sim_globals` injeta valores direto no escopo global do
script alvo, então dá pra varrer um parâmetro **sem tocar no script entre as runs**:

```python
melhor_tempo = None
melhor_cols = 0

for cols in [2, 4, 8]:
    t = simulate("sunflower_farm", Unlocks, {}, {"cols_per_drone": cols}, 999, 64)
    quick_print(cols, "colunas ->", t)
    if melhor_tempo == None or t < melhor_tempo:
        melhor_tempo = t
        melhor_cols = cols

quick_print("melhor:", melhor_cols, "colunas em", melhor_tempo)
```

O script alvo só precisa ler `cols_per_drone` como global em vez de fixar `4` no código.
Manter o arquivo byte a byte idêntico em todas as runs é o que torna a comparação honesta — e
é o mesmo motivo pelo qual o launcher de leaderboard é um arquivo separado de uma linha, veja
[o padrão launcher](../guides/leaderboard-strategies.md#o-padrao-launcher).

## Caça a seeds de verdade

Tudo acima ajusta *o seu código*. Caça a seeds é o caminho inverso: segure o código parado e
procure um **tabuleiro favorável**.

```python
BOM_O_BASTANTE = 300.0
achadas = []

for s in range(1, 200):
    t = simulate("full_run", Unlocks, {}, {}, s, 256)
    if t < BOM_O_BASTANTE:
        achadas.append((s, t))
        quick_print("seed candidata", s, "->", t)
```

Duas ressalvas honestas:

- **`seed` precisa ser um inteiro positivo** — não existe modo sem semente. Toda simulação é
  reprodutível por construção, que é exatamente o que faz isso funcionar.
- **Uma seed sortuda para um script não é sortuda em geral.** Você está achando um tabuleiro
  que serve às premissas *desta* estratégia. Mude a estratégia e a busca vira nula.

## Encaixando numa tentativa de leaderboard

`simulate()` e `leaderboard_run()` recebem o mesmo formato de `filename`/estado de propósito.
O fluxo que sai disso:

1. Escreva o script da run com a guarda contra o save vivo (veja
   [Estratégias de Leaderboard](../guides/leaderboard-strategies.md#o-padrao-launcher)).
2. Rode no `simulate()` com seed fixa enquanto você itera no algoritmo.
3. Varra seeds pra achar o pior caso, e conserte ele.
4. Varra `sim_globals` pra afinar os parâmetros que você deixou variáveis.
5. Só então gaste um `leaderboard_run()` de verdade.

Os passos 2–4 não custam nada além de ticks. O passo 5 é aquele em que você é julgado.

## Limites que vale conhecer antes de confiar num número

`simulate()` devolve **só** o tempo decorrido — sem traço, sem estado intermediário. Se você
precisa saber *por que* uma variante foi mais lenta, instrumente o próprio script alvo com
`quick_print` (que é de graça) ou passe uma flag por `sim_globals`. Veja
[Simulação → Limites](../mechanics/simulation.md#limites).
