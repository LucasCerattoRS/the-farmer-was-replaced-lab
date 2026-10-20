# 04 · Misturando plantas

## O que o jogo liberou
Nada de novo. Aqui você junta `for`, `till`, `plant` e `can_harvest` para cultivar **duas plantas
na mesma coluna**: cenoura nas pontas e bush no meio, ou o inverso.

## A ideia
Cenoura gasta Hay e Wood; o bush rende Wood. Misturar mantém o Wood chegando enquanto você
planta cenoura. O padrão é uma **coluna de 3 casas**: A, B e C.

O ponto que confunde: o padrão de 3 casas **já é** a coluna inteira. Então o `for i` (uma volta por
coluna) basta, e cada casa ganha o seu bloco de código.

## Fase 1: preparar e plantar (cenoura, bush, cenoura)

```python
for i in range(get_world_size()):
    till()                      # casa A: ara
    plant(Entities.Carrot)
    move(North)

    plant(Entities.Bush)        # casa B: bush cresce na grama, sem till
    move(North)

    till()                      # casa C: ara
    plant(Entities.Carrot)
    move(North)                 # 3 passos: o mapa dá a volta, volta para A

    move(East)                  # coluna pronta
```

Rastreando uma coluna (lado 3, a borda dá a volta):

| Passo | Casa | Faz |
|---|---|---|
| 1 | A | `till`, cenoura, anda |
| 2 | B | bush, anda |
| 3 | C | `till`, cenoura, anda e volta para A |
| 4 | A | `move(East)` vai para a coluna seguinte |

## Fase 2: colher e replantar a mesma coisa

```python
while True:
    for i in range(get_world_size()):
        if can_harvest():       # casa A
            harvest()
            plant(Entities.Carrot)
        move(North)

        if can_harvest():       # casa B
            harvest()
            plant(Entities.Bush)
        move(North)

        if can_harvest():       # casa C
            harvest()
            plant(Entities.Carrot)
        move(North)

        move(East)
```

Três regras sustentam isso:

1. **Cada casa é tratada uma vez por volta.**
2. **O `move` fica fora do `if`**, como no marco 01.
3. **Cada bloco replanta o que a casa tinha.** O código não "descobre" o padrão: ele o repete
   por posição, e é por isso que o padrão se mantém.

Para o inverso (bush nas pontas, cenoura no meio), troque os três blocos de lugar: bush em A e
C, `till` e cenoura em B.

## Erros comuns

- **Repetir o padrão num `for j`.** Dá 9 casas por coluna e desloca tudo (ver marco 02).
- **`till()` numa casa que já é solo.** Desfaz o solo (ver marco 03).
- **Rodar a fase 1 com a fazenda já arada.** Mesmo problema. Rode `clear()` antes: ✅ ele remove
  tudo, leva o drone a (0,0) e devolve o solo a grama.
- **Colher sem testar.** Cada casa precisa do próprio `if can_harvest()`.

## Limite: só funciona em lado 3
O padrão de 3 está escrito à mão. Em lado maior ele se desloca. Para qualquer tamanho, o código
precisa saber qual casa da coluna é a atual, o que pede comparar números. ⏳ Quando o jogo
liberar operadores, a ideia é `if j == 0: … elif j == 1: … else: …`, ou `j % 3`.

## Exercício
1. Monte a versão com bush nas pontas e cenoura no meio.
2. Rode a fase 2 por 1 minuto e anote o Wood antes e depois. ⏳ O rendimento do misto contra
   o de bush puro **ainda não foi medido**.
3. Explique, sem rodar, o que acontece se a fase 1 usar `till()` nas três casas.

Anterior: [Solo e cenoura](03-solo-e-cenoura.md).
