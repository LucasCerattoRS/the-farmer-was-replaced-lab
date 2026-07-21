# Peculiaridades da Linguagem

A linguagem do jogo parece Python e quase sempre se comporta como Python — até não se
comportar. Todo item desta página é demonstrado por um arquivo real em
[`farms/basics/experiments/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/farms/basics/experiments),
a maioria com só algumas linhas. Eles são propositalmente minúsculos: cada um existe pra
provar exatamente uma coisa sobre o runtime.

## Módulos são arquivos, e arquivos são janelas

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

## Importar um arquivo o *executa*

Essa é a que de fato custa recursos. O primeiro `import` de um arquivo **executa o arquivo
inteiro**. Se esse arquivo chama `harvest()`, importá-lo colhe. Importe de novo e nada acontece
na segunda vez — o módulo fica em cache desde a primeira execução.

O guard é o mesmo que o Python usa. `__name__` vale `"__main__"` quando o arquivo roda direto, e
o próprio nome do arquivo quando ele é alcançado por um `import`:

```python
a_global_variable = "global"

def main():
    a_local_variable = "local"
    # do things

if __name__ == "__main__":
    main()
```

Tudo que você não quer disparar na importação vai dentro desse bloco. A própria documentação do
jogo recomenda essa estrutura, e é por isso que a maioria dos arquivos que valem a pena importar
define suas globais no topo e esconde todo o resto atrás de `main()`.

## Import circular funciona — com `import`, não com `from`

Dois arquivos importando um ao outro funciona, e vale entender por quê, porque a *outra* forma
quebra.

Com `import` simples, o arquivo `b` recebe uma **referência ao módulo `a` ainda em
carregamento**. Quando algo de fato chama nele, `a` já terminou de carregar e a referência
resolve:

```python
# arquivo a
import b
x = 0

# arquivo b
import a
def f():
    print(a.x)
```

Rodar `import a` percorre: `a` começa → bate em `import b` → `b` começa → bate em `import a`,
acha o módulo parcialmente carregado e guarda uma *referência* a ele → `b` define `f` → `a`
retoma e faz `x = 0`. Chamar `b.f()` depois imprime `0`, porque `a` já está completo a essa
altura.

Troque por `from a import *` e o mesmo percurso quebra:

```python
# arquivo a
from b import *
x = 0

# arquivo b
from a import *
def f():
    print(x)
```

Agora `b` **desempacota um retrato** do que `a` contém naquele instante — que é nada, porque `a`
ainda não chegou no `x = 0`. Não há referência viva, então `x` nunca aparece e `b.f()` falha.

!!! tip "A regra que evita tudo isso"
    Fique no `import arquivo` em vez de `from arquivo import`, e envolva tudo que não é uma
    definição global em `if __name__ == "__main__":`. A forma `from` ainda deixa uma colisão de
    nomes sobrescrever silenciosamente suas próprias variáveis.

`import_cycle_a.py` e `import_cycle_b.py` neste repo são um ciclo executável — com os imports
colocados dentro das funções, então chamar neles produz recursão mútua entre dois arquivos, o
que te leva à próxima peculiaridade.

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

Toda farm desta coleção parametriza um worker **construindo uma função nova**, nunca passando
argumentos. O stub gerado pelo save que esses scripts usam declara `spawn_drone(function)`, sem
parâmetros extras, então pra dizer a oito drones pra começarem em oito colunas diferentes você
constrói oito funções diferentes. O `flip_party.py` é a demonstração mínima:

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

O jogo atual também aceita `spawn_drone(task, *args)` e copia os argumentos extras pro worker —
a doc oficial mostra `spawn_drone(harvest_column, i)`. Os scripts desta coleção não usam essa
forma, mas ela é uma terceira opção quando é só um valor simples que você precisa passar.

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
| Importar um arquivo o executa (uma vez — depois fica em cache) | `scripting/import.md` oficial |
| Import circular funciona com `import`, quebra com `from … import *` | `import_cycle_a.py` + `import_cycle_b.py` |
| Pilha de chamadas finita | `stack_overflow.py` |
| Nome indefinido só falha em runtime | `error_demo.py` |
| `spawn_drone` devolve `None` no teto | `hat_parade.py` |
| Closure factory parametriza workers | `flip_party.py` |
| `clear()` reseta fazenda, posição e chapéu | `clear_only.py` |

Veja também: [Primeiros Passos](../getting-started.md) para o básico da linguagem, e
[Drones](drones.md) para as primitivas de coordenação em que essas peculiaridades mais mordem.
