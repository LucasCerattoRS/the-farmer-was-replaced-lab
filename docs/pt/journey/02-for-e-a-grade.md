# 02 · `for` e a grade

## O que o jogo liberou
`for`, `range()`, `get_world_size()`. A fazenda deixou de ser uma fila e virou um quadrado,
então só `move(North)` não alcança mais todas as casas.

## A ideia: um `for` dentro do outro

O `for` roda o corpo **uma vez por elemento**. Ele não testa condição, como faz o `while`.
`for i in range(3)` roda 3 vezes, com `i` valendo 0, 1 e 2.

Para percorrer o quadrado, pense num prédio. O `for` de fora (`i`) é o **andar**; o de dentro
(`j`) são as **portas** daquele andar:

```python
for i in range(get_world_size()):        # uma volta por coluna
    for j in range(get_world_size()):    # uma volta por casa da coluna
        harvest()
        move(North)
    move(East)                           # coluna acabou: vai para a seguinte
```

A regra que resolve a confusão: **o `for` de dentro roda inteiro a cada volta do de fora, e
recomeça do zero.** Para lado 3, o corpo de dentro roda 3 × 3 = 9 vezes.

A **indentação** diz quando cada linha roda:

- dentro do `j`: a cada casa;
- fora do `j`, mas dentro do `i`: a cada coluna (aqui, o `move(East)`).

Se o `move(East)` ficasse dentro do `j`, o drone andaria para o lado a cada casa e não
faria coluna nenhuma.

## Para repetir para sempre: `while` por fora

```python
while True:
    for i in range(get_world_size()):
        for j in range(get_world_size()):
            if can_harvest():
                harvest()
            move(North)
        move(East)
```

O `for` percorre a fazenda **uma vez**; o `while True` repete isso. Ao contrário, um `while`
dentro do `for` prenderia o drone na primeira casa. E como o `get_world_size()` é lido a cada
volta, o código continua certo quando a fazenda crescer.

## O erro mais comum: repetir o padrão duas vezes

Quer plantar o padrão cenoura, bush, cenoura numa coluna de 3 casas. A tentação:

```python
# ERRADO
for i in range(get_world_size()):
    for j in range(get_world_size()):
        # ...tratamento das 3 casas A, B e C aqui dentro...
    move(East)
```

O corpo já trata **3 casas**, e o `for j` o repete 3 vezes: são 9 casas por coluna. Pior, se o
corpo termina sem andar, a volta seguinte começa na casa onde a anterior parou, e o resultado
sai deslocado.

Quando o padrão já cobre a coluna inteira, **o `for i` sozinho basta**: um bloco para cada casa
e um `move(North)` depois de cada um.

!!! info "Limite de agora"
    Esse padrão escrito à mão só vale para fazenda de **lado 3**. Para qualquer lado, o código
    precisa saber "qual casa da coluna é esta", ou seja, comparar `j` com um número. Isso exige
    operadores (`==`, `%`), que o jogo ainda não liberou nesta etapa.

## Exercício
1. Faça o drone colher a fazenda inteira e voltar à casa inicial.
2. Sem rodar: com lado 4, quantas vezes o corpo do `j` roda? E o `move(East)`?
3. Rode a versão com o `move(East)` dentro do `j` e descreva o caminho do drone.

Anterior: [Colher e repetir](01-colher-e-repetir.md) · Próximo: [Solo e cenoura](03-solo-e-cenoura.md).
