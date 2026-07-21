# Tutorial 04 · O Solver da Maçã do Dinossauro

**Objetivo:** sobreviver o máximo possível no minigame do dinossauro, coletando toda maçã que der.
**Requer:** unlock de Dinosaurs, Senses (`measure`), Hats, Dictionaries.

Mecânica completa em [Dinossauros](../mechanics/dinosaurs.md); esta página é sobre como o
`farms/dinosaur/apple_solver.py` de fato joga o jogo.

## Coletar é implícito

Não existe `collect()`. Você **pisa na maçã** e ela é sua — a única coisa que você precisa
fazer é perguntar onde está a próxima:

```python
def move_and_check_apple(direction):
    if not move(direction):
        return False
    if (get_pos_x(), get_pos_y()) == apple_pos:
        measure_apple()
    return True
```

Duas tarefas numa primitiva só, e as duas importam:

- Ela remede **só quando você cai em cima da maçã**, então `apple_pos` é sempre o alvo *atual*.
- Ela devolve `False` quando o `move()` falha — o que neste minigame significa que **você bateu
  na própria cauda**. Todo chamador propaga esse `False` pra cima em vez de seguir às cegas.

O `measure_apple()` também incrementa `squares_occupied`, a estimativa do script de quanto do
tabuleiro a cauda já ocupa. É esse contador que uma hora encerra a perseguição.

## Perseguição: um caminhador, dois modos

Mover até uma coordenada é um par de funções só, e elas recebem uma flag que troca a própria
função de passo:

```python
def move_to_col(target_x_pos, do_measure=True):
    curr_x = get_pos_x()
    direction = West
    if curr_x < target_x_pos:
        direction = East

    for x in range(abs(target_x_pos - curr_x)):
        this_check = move
        if do_measure:
            this_check = move_and_check_apple
        if not this_check(direction):
            return False
    return True
```

`this_check = move` versus `this_check = move_and_check_apple` — funções são valores, então
"anda vigiando a maçã" e "só anda" são o mesmo caminho de código. A rota de cobertura do fim
passa `do_measure=False`, porque a essa altura não há nada sendo perseguido, e pular a
comparação de posição a cada passo é velocidade de graça.

## Dois estágios que não se atropelam

O tabuleiro é varrido por dois estágios alternados: o **estágio 1** sobe pela metade de baixo,
o **estágio 2** espelha isso descendo do topo. O perigo é evidente — a cauda que um estágio
deixa pra trás é parede para o outro.

A solução são dois dicionários, `offlimit_columns_stage1` e `offlimit_columns_stage2`, que
registram *até onde uma coluna já foi reivindicada*. O estágio 1 desiste na hora se a maçã
estiver onde ele não pode ir:

```python
apple_pos_x, apple_pos_y = apple_pos
if apple_pos_y == 0 or apple_pos_x in edge_positions or (
    apple_pos_x in offlimit_columns_stage1
    and apple_pos_y <= offlimit_columns_stage1[apple_pos_x]
):
    return transition_to_stage_2()
```

Três condições de desistência: a maçã está na linha de fronteira, numa coluna de borda, ou
dentro do território que o *outro* estágio já reivindicou.

E quando um estágio pega uma maçã, ele reivindica um **par** de colunas pra si:

```python
offlimit_columns_stage2[target_x_pos] = apple_pos_y
offlimit_columns_stage2[target_x_pos + 1] = apple_pos_y
```

Esse pareamento é o motivo de a coluna-alvo ser encaixada num limite par/ímpar antes
(`target_x_pos = apple_pos_x - 1` quando a coluna da maçã é par). O tabuleiro é consumido de
duas em duas colunas, então os dois estágios se intercalam limpo em vez de fragmentá-lo.

## Saber a hora de parar de perseguir

Esta é a decisão mais importante do script inteiro:

```python
if squares_occupied > (world_size_minus_one) * 4 - 4:
    break
```

Passada essa densidade, perseguir uma maçã individual é como você se encurrala — a cauda está
longa o bastante para que um desvio te sele num bolso sem saída. Então o script para de
otimizar por maçãs e passa a otimizar por **sobrevivência**.

!!! tip "A lição geral"
    Uma estratégia gulosa que está certa no começo costuma ser fatal no fim. Escreva a condição
    de virada *antes* de afinar a parte gulosa — é ela que decide se sua run termina com 60% do
    tabuleiro coberto ou 100%.

## A rota ondulada de cobertura

Depois da virada, o drone percorre uma serpentina fixa que sabe o que a perseguição já consumiu:

```python
def move_to_right_col_wavy():
    for x in range(world_size):
        if x % 2:
            target_y = 1
            if x in offlimit_columns_stage1:
                target_y = offlimit_columns_stage1[x] + 1
            while get_pos_y() != target_y:
                move(South)
            move(East)
        else:
            while get_pos_y() != world_size_minus_one:
                move(North)
            move(East)
```

Colunas ímpares descem, pares sobem — mas uma coluna ímpar para em
`offlimit_columns_stage1[x] + 1` em vez da linha 1, porque tudo abaixo disso já é cauda. Os
dicionários montados durante a perseguição são *reaproveitados* como mapa do tabuleiro.

Dali em diante o script roda um bustrofédon simples até um `move()` finalmente falhar,
travando o resultado pra que uma única falha encerre a run inteira de forma limpa:

```python
game_complete = not move_to_row(world_size_minus_one, False)
game_complete = game_complete or not move(East)
game_complete = game_complete or not move_to_row(1, False)
```

`change_hat(Hats.Straw_Hat)` no finzinho tira o chapéu e devolve o drone ao cultivo normal.

## Quer algo mais simples antes?

O `farms/dinosaur/bone_snake_solo.py` é a filosofia oposta: em vez de rotear ao redor da
própria cauda, ele trata um movimento bloqueado como "colhe este tile e tenta de novo". Muito
menos código, muito menos throughput — um bom aquecimento antes deste. Veja
[Dinossauros](../mechanics/dinosaurs.md#comportamento-da-cauda-numa-farm-mais-simples).

Para a versão de competição do farming de ossos, veja
[Estratégias de Leaderboard](../guides/leaderboard-strategies.md#dinosaur-33488928-ossos).
