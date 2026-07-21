# Controle de Fluxo

Ramificar e repetir — o formato de todo loop de fazenda. Todas as quatro construções (`if`,
`while`, `for`, e o par `break`/`continue`) se comportam como em Python, com uma reviravolta
específica do jogo: **loops infinitos são de boa.**

## `if` / `elif` / `else`

Roda um bloco só quando uma condição é `True`; a doc descreve `if` como "um loop `while` que não
repete". `elif` é açúcar sintático para um `else: if` aninhado.

```python
if can_harvest():
    harvest()
elif get_entity_type() == None:
    plant(Entities.Carrot)
else:
    move(North)
```

## `while` — e por que loops infinitos são seguros aqui

O loop `while` repete seu corpo enquanto a condição valer. Ao contrário de um runtime Python
normal, **um loop infinito não vai travar o jogo**: existe um atraso entre iterações, então
`while True:` apenas roda até você apertar Execute de novo. Isso não é um bug a evitar — é o
formato padrão de topo de um trabalhador persistente:

```python
while True:
    if can_harvest():
        harvest()
    plant(Entities.Grass)
    move(North)
```

Os loops de spawn em `farms/` são todos `while True: ... spawn_drone(...)`, e o
[`hat_parade.py`](../mechanics/language-quirks.md#spawn_drone-no-teto-devolve-none-inofensivamente)
se apoia exatamente nisso para ficar pedindo drones para sempre.

## `for` e `range`

O loop `for` itera uma sequência, ligando uma variável a cada elemento. Um **range** é a
sequência de contagem fixa de sempre; listas, tuplas, dicts e sets também são todos iteráveis
(veja [Coleções](collections.md)).

```python
for i in range(get_world_size()):
    harvest()
    move(North)
```

`range(stop)`, `range(start, stop)` e `range(start, stop, step)` todos existem. Limitar uma
varredura por `range(get_world_size())` em vez de por uma checagem de movimento é o hábito mais
importante em código multi-drone — o mundo é um toro, então `while can_move(...)` entra direto na
faixa do próximo drone. Essa cilada está detalhada em
[Drones](../mechanics/drones.md#armadilhas-aprendidas-na-marra).

## `break` e `continue`

`break` sai do loop mais interno imediatamente; `continue` pula para a próxima iteração daquele
loop. Ambos agem **apenas** no loop mais interno.

```python
while True:
    if can_harvest():
        break          # para de esperar, segue em frente
```

Um `while not can_harvest(): pass` diz a mesma coisa — a doc oficial dá exatamente essa
equivalência.

## Loops não criam escopo

Uma variável atribuída dentro de um `for` ou `while` continua visível depois do loop — ramos e
loops **não** introduzem seu próprio escopo. Depois de `for i in range(3): pass`, `i` é `2`. Isso
importa o suficiente para viver em
[Funções & Escopo](functions-and-scope.md#loops-e-ramos-nao-criam-escopo), onde escopo é coberto
direito.

## Sem recursão para travessias profundas

`for`/`while` são iterativos por natureza, o que é deliberado aqui: a pilha de chamadas é finita
(a [pegadinha do limite de pilha](../mechanics/language-quirks.md#recursao-tem-limite-de-pilha)),
então os solucionadores de labirinto em `farms/mazes/` rodam sua busca em profundidade com uma
**pilha explícita numa lista** e um loop `while`, em vez de recursão.

---

Próximo: [Funções & Escopo](functions-and-scope.md) — dar nome a blocos disto e controlar o que
eles enxergam.
