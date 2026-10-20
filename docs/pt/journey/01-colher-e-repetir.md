# 01 · Colher e repetir

## O que o jogo liberou
`while`, `if`/`else`, `can_harvest()`, `harvest()`, `move()` com `North`/`East`/`South`/`West`,
`plant()` com `Entities.Bush`.

## A ideia
Seu drone só executa o que está no script, e o script roda uma vez e acaba. Para a fazenda
trabalhar sozinha, o código fica dentro de um `while True:`, que repete para sempre.

Dentro dele, a pergunta é sempre a mesma: **"a planta desta casa está pronta?"**

```python
while True:
    if can_harvest():
        harvest()
        plant(Entities.Bush)
    move(North)
```

Leia assim: repita sempre; se a planta está pronta, colha e replante; **depois** ande, tendo
colhido ou não.

## Três fatos que importam

- ✅ **Casa vazia é grama.** `plant(Entities.Bush)` funciona nela sem preparar o solo.
- ✅ **A borda dá a volta.** Andar `North` na última linha leva você à primeira. Numa fazenda
  de lado 3, três passos para o norte trazem o drone ao ponto de partida.
- 📖 **Loop infinito é seguro.** O jogo coloca um atraso entre as repetições, então o
  `while True` não trava nada. Você para apertando Execute de novo.

## O erro mais comum: o `move` dentro do `if`

```python
# ERRADO
while True:
    if can_harvest():
        harvest()
        plant(Entities.Bush)
        move(North)      # só anda quando colheu
```

Se a casa não está pronta, o `if` falha, o drone **não anda** e fica parado esperando. Pode
até ser o que você quer em uma casa, mas num caminho com várias casas ele trava na primeira
planta que demora. O `move` fica **fora** do `if`: o drone anda sempre, colhendo só onde dá.

## Exercício
1. Faça o drone colher e replantar bush em uma coluna, sem parar.
2. Troque o `plant` por nada (só `harvest`) e observe: a casa volta a ser grama sozinha.
3. ⏳ Pergunta em aberto: com a fazenda de lado 3, o bush chega a crescer entre uma volta e a
   seguinte? Anote quantas vezes o `can_harvest()` deu falso e conte você mesmo.

!!! warning "Colher cedo destrói"
    ✅ Colher uma planta que ainda não está pronta a destrói. Por isso o `if can_harvest()`
    não é enfeite.

Próximo: [`for` e a grade](02-for-e-a-grade.md).
