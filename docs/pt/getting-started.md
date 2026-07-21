# Primeiros Passos

## O que é The Farmer Was Replaced?

Você controla um **drone** numa fazenda em grade — mas não com as mãos. Você escreve
programas numa linguagem parecida com Python, e o drone executa: mover, plantar, regar,
colher, destravar tecnologia nova e, lá na frente, comandar dezenas de drones ao mesmo
tempo. A progressão é limitada por uma árvore de pesquisa paga com os recursos que você
cultiva.

A genialidade do jogo: **seu código é seu save.** Algoritmo melhor significa, literalmente,
progresso mais rápido — e o late game vira um parquinho puro de otimização, com
leaderboards globais.

## A linguagem

Parece Python e se comporta quase como Python, com algumas viradas:

- Sem classes suas; um conjunto curado de funções embutidas (veja a [Referência da API](api/reference.md)).
- Toda chamada que mexe no mundo custa **ticks** — `harvest()` leva tempo, `quick_print()` é
  de graça. Velocidade de execução é um recurso que você destrava e melhora.
- Cada janela de código aberta é um arquivo; arquivos podem se `import`ar depois que você
  destrava **Import**.
- `while True:` é o normal — farms rodam para sempre.

## Sua primeira farm

```python
while True:
    if can_harvest():
        harvest()
    move(North)
```

Só isso já cultiva grama para sempre na coluna 0 (o mundo dá a volta nas bordas — é um
toro). Daí o jogo escala: arar o solo, regar, comprar melhorias com `unlock()`, medir
plantas com `measure()`, trocar entidades de lugar com `swap()` e criar drones extras com
`spawn_drone()`.

## Onde o jogo guarda seu código (Windows)

```text
%USERPROFILE%\AppData\LocalLow\TheFarmerWasReplaced\TheFarmerWasReplaced\Saves\<nome-do-save>\
```

Cada janela do jogo é um arquivo `.py` ali, mais o `__builtins__.py` (o stub da API que o
jogo gera) e o `save.json` (progresso). Este repositório espelha um save real de end-game
via [`tools/sync_save.ps1`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/tools/sync_save.ps1).

## Ordem de leitura sugerida

1. [Culturas & Economia](mechanics/crops.md) — o que cada planta faz e rende.
2. [Guia de progressão](guides/progression.md) — o que destravar, em que ordem, e por quê.
3. [Tutorial 01 · Farming Multi-Drone](tutorials/01-multi-drone.md) — o maior salto de throughput do jogo.
