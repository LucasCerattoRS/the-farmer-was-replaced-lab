# 03 · Solo e cenoura

## O que o jogo liberou
`till()` e `plant(Entities.Carrot)`.

## A ideia
Cenoura só cresce em **solo arado**. Você ara a casa com `till()`. Plantar custa itens: **1 Hay
e 1 Wood** por cenoura, descontados no momento do `plant`.

- 📖 Crescimento: entre 4,8 e 7,2 segundos.
- ✅ Casa vazia é grama; depois do `till()`, vira solo.

## A armadilha: `till()` alterna

```python
till()   # grama -> solo
till()   # solo  -> grama  (desfez!)
```

Chamar `till()` numa casa que já é solo a **devolve para grama**. O `harvest()` da cenoura deixa
o solo arado, então a casa não precisa de `till()` de novo. O erro clássico é arar a cada colheita:

```python
# ERRADO: na volta 2 a casa já é solo, o till desfaz, o plant falha
if can_harvest():
    harvest()
    till()
    plant(Entities.Carrot)
```

Sintoma: a casa fica alternando entre grama e cenoura.

## A solução: duas fases

```python
# Fase 1: ara e planta, uma vez por casa
for i in range(get_world_size()):
    for j in range(get_world_size()):
        till()
        plant(Entities.Carrot)
        move(North)
    move(East)

# Fase 2: colhe e replanta, sem till
while True:
    for i in range(get_world_size()):
        for j in range(get_world_size()):
            if can_harvest():
                harvest()
                plant(Entities.Carrot)
            move(North)
        move(East)
```

!!! warning "Rodar a fase 1 duas vezes estraga"
    Como o `till()` alterna, uma segunda execução devolve a grama as casas já aradas. ✅ O
    `clear()` remove tudo, leva o drone a (0,0) e devolve o solo a grama; use-o para recomeçar.

## "Por que a colheita fica irregular?"

Você roda a fase 2 e o drone colhe a 1ª casa, pula a 2ª e a 3ª, e na volta seguinte pega as
que ficaram. Não é erro de código. ✅ Cada cenoura sorteia seu tempo entre 4,8 e 7,2 s, então
algumas ainda não estão prontas quando o drone passa, e ele anda do mesmo jeito. O `move`
fora do `if` faz exatamente isso.

⏳ Dá para forçar o drone a esperar na casa com `while True` e `break`, trocando o desencontro
por tempo parado. Não medimos qual rende mais.

## Economia
Wood vem do bush; Hay vem da grama colhida. A cenoura gasta os dois. Transformar a fazenda
inteira em cenoura derruba a produção do que ela consome, então um **misto** (cenoura nas
casas do meio, bush nos cantos, ou o inverso) mantém o Wood chegando. ⏳ Qual proporção rende
mais não foi medido.

## Exercício
1. Reproduza o erro (`till()` dentro do `if`) e veja a casa alternar. Depois corrija.
2. Faça uma coluna cenoura, bush, cenoura em lado 3. Dica: o padrão cabe num único `for i`.
3. Meça: anote o Wood antes e depois de 1 minuto da fase 2. Quanto rendeu?

Anterior: [`for` e a grade](02-for-e-a-grade.md) · Próximo: [Misturando plantas](04-misturando-plantas.md).
