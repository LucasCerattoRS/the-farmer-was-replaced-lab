# Peculiaridades da Linguagem

A linguagem do jogo parece Python e quase sempre se comporta como Python — até não se
comportar. Todo item desta página é demonstrado por um arquivo real em
[`farms/basics/experiments/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/farms/basics/experiments),
a maioria com só algumas linhas. Eles são propositalmente minúsculos: cada um existe pra
provar exatamente uma coisa sobre o runtime.

## `import` recebe nome de janela, não caminho

Essa é a peculiaridade que surpreende todo mundo, e ela é invisível até você tentar.

Seu código mora em **janelas**, e o nome de uma janela *é* o nome do módulo dela. Não existe
estrutura de diretório de onde importar, então o `import` recebe o nome literal que você
digitou na aba da janela:

```python
# import_cycle_a.py — no jogo, esta janela se chama "ImportZyklus"
def f0():
    import ImportzyklusZubehör
    ImportzyklusZubehör.f1()
f0()
```

Repare no que isso significa para este repositório: os nomes curados aqui
(`import_cycle_a.py`, `import_cycle_b.py`) **não** são os nomes que o código importa. Os
imports ainda referenciam `ImportZyklus` / `ImportzyklusZubehör`, os nomes originais das
janelas no save. Copie esses arquivos pro seu jogo e o import quebra, a menos que suas janelas
tenham exatamente esses nomes — acentos e maiúsculas inclusive.

O mesmo vale pro `leaderboard_run`, cujo segundo argumento é um nome de janela. O repo até
guarda uma versão com o placeholder ainda lá:

```python
# launcher_v1.py
leaderboard_run(Leaderboards.Fastest_Reset, "NAME_OF_THE_WINDOW_WITH_THE_ABOVE_SCRIPT", 1000)
```

!!! warning "Renomeie uma janela, quebre todo import"
    Nada te avisa. Renomear uma janela invalida silenciosamente todo `import` e toda chamada de
    `leaderboard_run`/`simulate` que a referenciava, e você só descobre em runtime.

## Imports circulares

Duas janelas podem importar uma à outra. `import_cycle_a.py` e `import_cycle_b.py` são o caso
mínimo — A importa B, chama dentro dele, e B importa A de volta:

```python
# A
def f0():
    import ImportzyklusZubehör
    ImportzyklusZubehör.f1()
f0()

# B
def f1():
    import ImportZyklus
    ImportZyklus.f0()
```

Os dois imports ficam **dentro** das funções, não no topo do arquivo, e é isso que impede o
ciclo de se resolver no carregamento. Rode e você tem recursão mútua entre dois arquivos — o
que te joga direto na peculiaridade seguinte.

## Recursão tem limite de pilha

```python
# stack_overflow.py — o arquivo inteiro
def stack_overflow():
    stack_overflow()

stack_overflow()
```

Três linhas, um propósito: provar que o interpretador tem pilha de chamadas finita e te mostrar
como é bater nela. Vale saber antes de escrever um solver de labirinto recursivo — os solvers
DFS em `farms/mazes/` usam uma **pilha explícita numa lista** com loop iterativo em vez de
recursão, e é por isso.

O único lugar onde recursão é genuinamente idiomática aqui é retry em falha, onde a
profundidade fica minúscula:

```python
def unlock_tech(tech):
    ct = get_cost(tech)
    for c in ct:
        farm_item(c, ct[c])
    if not unlock(tech):
        unlock_tech(tech)   # profundidade 1–2 na pratica
```

## Nome indefinido falha em runtime, não antes

```python
# error_demo.py
while True:
    pet_the_piggy()
    do_a_flip()
    change_hat(Hats.Brown_Hat)
    Make_Error()
```

`Make_Error()` não existe. Nada pega isso até a execução chegar naquela linha — as três
chamadas antes dela rodam normalmente primeiro. Não há etapa de compilação nem linting, então
um typo num ramo que você raramente atinge fica ali quietinho até a única run em que importava.

Defesa prática: exercite todo ramo pelo menos uma vez sob
[`simulate()`](simulation.md) antes de confiar um script a uma tentativa de leaderboard.

## `spawn_drone` no teto devolve `None` — inofensivamente

```python
# hat_parade.py
def newHat():
    hats = [Hats.Gold_Hat, Hats.Golden_Cactus_Hat, Hats.Golden_Carrot_Hat,
            Hats.Golden_Sunflower_Hat, Hats.Golden_Tree_Hat]
    while True:
        move(North)
        change_hat(hats[get_pos_x() % 5])

while True:
    spawn_drone(newHat)
    move(East)
```

Esse `while True` externo nunca para de pedir drones. Uma vez atingido o teto, o
`spawn_drone` simplesmente devolve `None` toda vez e o loop segue girando sem erro.

Inofensivo aqui — mas no momento em que você **guarda** esses handles, deixa de ser:

```python
drones = []
for i in range(16):
    drones.append(spawn_drone(worker))   # pode dar append de None
...
for d in drones:
    wait_for(d)                          # wait_for(None) quebra
```

Confira o retorno, ou cheque `num_drones() < max_drones()` antes. É o item número um em
[Drones → armadilhas](drones.md#armadilhas-aprendidas-na-marra), e não por acaso.

## Closures são como se parametriza um drone

Uma função passada pro `spawn_drone` **não recebe argumentos**. Então como você diz a oito
drones pra começarem em oito colunas diferentes? Você constrói oito funções diferentes. O
`flip_party.py` é a demonstração mínima:

```python
def make_drone(offset):
    def drone_behavior():
        for step in range(offset):
            move(East)
        while True:
            do_a_flip()
    return drone_behavior

for i in range(number_of_drones):
    spawn_drone(make_drone(i))
```

`make_drone(i)` devolve uma função nova, de zero argumentos, que capturou o próprio `offset`.
Isso não é brinquedo — é exatamente o padrão que as farms de verdade usam:

- `criar_runner(col)` no `carrot_polyculture_32x32.py` (veja o
  [Tutorial 05](../tutorials/05-polyculture.md))
- `make_runner(col)` no `pumpkin_megafarm_v2.py` e no `sunflower_15petals.py`

A alternativa, usada com a mesma frequência, é o [truque de herança da posição de
spawn](drones.md#heranca-da-posicao-de-spawn): leve o spawner até o tile certo primeiro e deixe
o worker ler `get_pos_x()` na largada. Closures ganham quando o parâmetro não é uma posição.

## `clear()` é o botão de pânico

```python
# clear_only.py — o arquivo inteiro
clear()
```

Uma janela de uma linha cujo único trabalho é ser executada na mão quando a farm deu errado. O
`clear()` limpa a fazenda, devolve o drone pra `(0,0)` e reseta o chapéu — o que também
significa que ele é a saída de um minigame de dinossauro travado.

Mantê-lo como janela própria importa: quando as coisas estão quebradas, você quer clicar em uma
coisa, não editar código sob pressão.

!!! danger "Ele realmente apaga a fazenda"
    O `clear()` destrói um campo no meio de uma fusão ou de uma ordenação sem perguntar. O
    `set_world_size()` também, e todo upgrade de `Expand` também — veja
    [Progressão](../guides/progression.md#estagio-1-movimento-e-solo).

## Referência rápida

| Peculiaridade | Demonstrada por |
|---|---|
| `import` usa o nome da janela, não um caminho | `import_cycle_a.py`, `launcher_v1.py` |
| Imports circulares funcionam (imports dentro de funções) | `import_cycle_a.py` + `import_cycle_b.py` |
| Pilha de chamadas finita | `stack_overflow.py` |
| Nome indefinido só falha em runtime | `error_demo.py` |
| `spawn_drone` devolve `None` no teto | `hat_parade.py` |
| Closure factory parametriza workers | `flip_party.py` |
| `clear()` reseta fazenda, posição e chapéu | `clear_only.py` |

Veja também: [Primeiros Passos](../getting-started.md) para o básico da linguagem, e
[Drones](drones.md) para as primitivas de coordenação em que essas peculiaridades mais mordem.
