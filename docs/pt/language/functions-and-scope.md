# Funções & Escopo

Funções dão nome a um bloco de código; escopo decide quais nomes aquele bloco enxerga. Estão numa
página só porque os padrões interessantes — closures, globais deliberados — vivem exatamente onde
as duas ideias se encontram.

## Definindo e chamando

```python
def move_n(n, direction):
    for _ in range(n):
        move(direction)

move_n(10, North)
move_n(2, West)
```

`def name(params):` liga uma função a `name`; `()` a chama. Parâmetros viram variáveis locais
segurando os argumentos. **`def` é uma atribuição** — a doc oficial é explícita em que você deve
ler `def f():` como `f = <uma função nova>`. Como qualquer atribuição, ela precisa rodar *antes*
da chamada: chamar uma função acima do próprio `def` dela é um erro de runtime.

## Valores de retorno, e retornar vários

`return` devolve um valor. Para devolver mais de um, retorne uma **tupla** e desempacote
([Coleções](collections.md#tuplas)):

```python
def bounds():
    return get_pos_x(), get_pos_y()

x, y = bounds()
```

## Argumentos padrão

```python
def flip(times = 1):
    for _ in range(times):
        do_a_flip()

flip()      # 1
flip(5)     # 5
```

Um parâmetro com valor padrão não pode ser seguido por um sem — mesma regra do Python.

## Funções são valores

Uma função é só mais um valor, então você pode guardá-la, passá-la ou devolvê-la. Isso não é
curiosidade — é o mecanismo por trás de [`spawn_drone(task)`](../mechanics/drones.md), que recebe
uma função para rodar, e por trás da fábrica de closures abaixo.

```python
def repeat10(action, arg):
    for _ in range(10):
        action(arg)

repeat10(move, North)
repeat10(use_item, Items.Fertilizer)
```

## Closures parametrizam um trabalhador

Uma função definida dentro de outra **captura** as variáveis da função externa. É assim que este
repo entrega a cada drone sua própria coluna de partida quando a tarefa em si não tem argumento a
gastar:

```python
def make_runner(col):
    def run():
        while get_pos_x() < col:
            move(East)
        # ... trabalha esta coluna para sempre
    return run

for c in range(0, size, cols_per_drone):
    spawn_drone(make_runner(c))
```

`make_runner(c)` devolve uma função de zero argumentos, novinha, que capturou o seu próprio `c`.
Instâncias reais: `criar_runner(col)` em `carrot_polyculture_32x32.py`, `make_runner(col)` em
`pumpkin_megafarm.py` e `sunflower_15petals.py`, e o mínimo
[`flip_party.py`](../mechanics/language-quirks.md#closures-sao-como-se-parametriza-um-drone).
(O jogo atual *também* aceita `spawn_drone(task, *args)`; os scripts daqui usam closures — a
página de quirks tem a história completa.)

## Escopo: local por padrão

Existe um escopo global, e toda chamada de função ganha seu próprio escopo local. Atribuir um
nome dentro de uma função o cria **localmente**, mesmo quando existe um global de mesmo nome:

```python
x = 0
def f():
    x = 1      # um x local NOVO, sem relação com o global
f()
# o x global continua 0
```

Esse isolamento é uma feature: um ajudante não consegue atropelar um global só por reusar um nome
comum.

## A palavra-chave `global`

Para *escrever* no global de dentro de uma função, declare-o:

```python
WORLD_SIZE = 0
def setup():
    global WORLD_SIZE
    WORLD_SIZE = get_world_size()
```

É assim que a config compartilhada em `cactus_insertion_sort.py` (`global WORLD_SIZE`,
`MAX_DRONES`) e os mapas de desejo da policultura em `carrot_polyculture.py`
(`global companion_mapping`, `tree_mapping`) são preenchidos uma vez e lidos em todo lugar. Use
com parcimônia — a doc oficial avisa que se apoiar em globais é "o primeiro passo rumo ao código
espaguete", e num programa multi-drone um global compartilhado é compartilhado entre os drones.

## Loops e ramos não criam escopo

Só *funções* introduzem um escopo. Um `for`/`while`/`if` não, então os nomes que eles atribuem
sobrevivem:

```python
for i in range(3):
    pass
# i é 2 aqui
```

Prático para "achar o último índice que casou", surpreendente se você esperava a variável do loop
sumir.

---

Próximo: [Coleções](collections.md) — os dados compartilhados e mutáveis que essas funções passam
adiante · [Módulos & Imports](modules-and-imports.md) — escalar para além de um arquivo.
