# Números Medidos

A maior parte deste site descreve *como* o jogo se comporta. Esta página é sobre **quais são os
números de fato** — e ela é deliberada quanto à diferença entre um número que veio de uma fonte
primária e um número que alguém supôs.

Dois status aparecem abaixo:

| Status | Significado |
|---|---|
| ✅ **Com fonte** | Tirado do `builtins.py` canônico que o jogo shippa. Confiável agora. |
| ⏳ **Pendente** | Uma afirmação que o site faz hoje e que **nunca foi medida**. O script que vai medi-la já existe em [`farms/research/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/farms/research); o número entra aqui depois de uma batelada rodada no jogo. |

> Nada nesta página é estimado. Se um número ainda não foi medido, ele fica com ⏳ e vazio em vez
> de ganhar um chute plausível — as
> [regras de base](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/ROADMAP.md)
> do repo existem porque uma resposta errada dita com confiança já foi publicada aqui uma vez.

## ✅ Custos em ticks, completo

Todo custo abaixo é transcrito do **`builtins.py` canônico** shipado com a doc oficial CC0 (51
definições) — não do stub menor gerado pelo save. Esta é a primeira vez que a tabela de custos
aparece inteira, num lugar só, no site.

**De graça — 0 ticks**

| Função | Nota |
|---|---|
| `get_tick_count()` | O próprio instrumento de medição é grátis, então uma diferença `t1 - t0` é exata. |
| `get_time()` | Veja a [divergência entre os stubs](#os-dois-stubs-discordam-sobre-get_time) abaixo. |
| `quick_print(*x)` | O motivo de preferi-la ao `print` dentro de loops. |

**1 tick — sensores, inventário e built-ins baratos**

`can_harvest()` · `can_move(dir)` · `get_pos_x()` · `get_pos_y()` · `get_world_size()` ·
`get_entity_type()` · `get_ground_type()` · `get_water()` · `num_items(item)` ·
`get_companion()` · `measure(dir)` · `has_finished(drone)` · `max_drones()` · `num_drones()` ·
`get_cost(thing)` · `num_unlocked(thing)` · `random()` · `abs(x)` · `len(x)` · `str(x)` ·
`range(...)` · `list.append(x)` · `set.add(x)`

**200 ticks — sempre, sem caminho barato**

`till()` · `clear()` · `change_hat(hat)` · `set_execution_speed(s)` · `set_world_size(n)` ·
`simulate(...)` · `leaderboard_run(...)`

**200 ticks no sucesso, 1 tick caso contrário** — o grupo de dois preços. É por isso que um
`if can_move(d): move(d)` com guarda não é automaticamente mais barato que um `move(d)` puro que
falha.

| Função | Custa 200 quando… |
|---|---|
| `harvest()` | uma entidade foi de fato removida |
| `plant(entity)` | o plantio deu certo |
| `swap(direction)` | a troca deu certo |
| `use_item(item, n)` | um item foi de fato usado |
| `move(direction)` | o drone de fato se moveu |
| `spawn_drone(task)` | um drone foi de fato criado (`1` no teto) |
| `unlock(unlock)` | a compra deu certo |

**Custo variável**

| Função | Custo |
|---|---|
| `list.insert(i, x)` | `1 + len(list) - i` ticks |
| `list.pop(i)` / `dict.pop(key)` | `1` tick sem índice, ou para um dict |
| `set.remove(x)` | `1` tick |
| `wait_for(drone)` | `1 +` os ticks restantes na tarefa daquele drone |

**Medidos em segundos, não em ticks**

`print(*x)` · `do_a_flip()` · `pet_the_piggy()` — cada um custa **1 segundo**. É por isso que o
`quick_print` existe.

Veja a [Referência da API](../api/reference.md#colecoes-listas-dicts-sets) para os métodos de
coleção em forma de assinatura.

## Os dois stubs discordam sobre `get_time()`

Uma inconsistência concreta que vale conhecer, achada ao montar a tabela acima:

| Fonte | Custo alegado de `get_time()` |
|---|---|
| `builtins.py` canônico (shipado com a doc oficial, 2321 linhas) | **0 ticks** |
| `farms/lib/__builtins__.py` gerado pelo save (1307 linhas) | **1 tick** |

O stub canônico é a autoridade — é o artefato oficial e maior, e o mesmo arquivo está certo sobre
os cinco métodos de coleção que o stub do save omite por completo. Esta página, portanto, lista
`get_time()` como grátis, e o `tick_costs.py` mede isso explicitamente para desempatar na prática.

Na prática quase não muda nada — mas significa que um loop de cronometragem construído sobre
`get_time()` não perturba o orçamento de ticks que ele está medindo, o que é conveniente para o
[`grow_times.py`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/farms/research/grow_times.py).

## O kit de medição

Cinco scripts em [`farms/research/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/farms/research).
Cada um imprime uma tabela limpa na janela de Output e nada mais — são instrumentos, não fazendas.

| Script | Alvo | Método | N padrão |
|---|---|---|---|
| `tick_costs.py` | A tabela acima | Envolve cada operação em `get_tick_count()` e compara com o custo documentado. Prepara um estado de tile conhecido antes, por causa do grupo de dois preços. | 1 cada |
| `grow_times.py` | As figuras `~0,5s / ~4s / ~7s` em [Culturas](crops.md#a-lista-completa) | Cronometra `plant()` → `can_harvest()` com `get_time()`, num tile isolado, água acima de 0,9 | 10 por entidade |
| `pumpkin_death_rate.py` | "cerca de 1 em 5 abóboras morre" em [Culturas](crops.md#fusao-de-aboboras) | Uma abóbora por vez num tile solitário (sem fusão para corromper a contagem); resolve em `Dead_Pumpkin` ou `can_harvest()` | 200 |
| `sunflower_petals.py` | Se o sorteio de pétalas é uniforme | `measure()` em cada girassol recém-plantado, agrupado num histograma | 300 |
| `cactus_chain.py` | A regra `tamanho²` e a regra da cadeia | Parte 1 cacto isolado vs `tamanho²`; Parte 2 pontua a ordenação do campo e compara o payout com o teto somado de `tamanho²` | 8 campos |

!!! note "Por que os tamanhos de amostra diferem"
    O `tick_costs.py` precisa de N=1 porque custos em ticks são determinísticos. As perguntas de
    taxa e distribuição precisam de centenas de amostras antes de o número significar alguma
    coisa — uma amostra de 20 abóboras facilmente mostra "1 em 4" para uma taxa real de 1 em 5.

## ⏳ Perguntas abertas esperando números

Estas são afirmações vivas neste site, ainda sem nenhuma medição por trás.

| Afirmação | Onde é afirmada | Status |
|---|---|---|
| Grass ~0,5s, Bush ~4s, Tree ~7s, Carrot ~6s, Pumpkin ~2s, Sunflower ~5s, Cactus ~1s | [Culturas & Economia](crops.md#a-lista-completa) | ⏳ |
| "Cerca de 1 em 5 abóboras morre ao crescer" | [Culturas & Economia](crops.md#fusao-de-aboboras) | ⏳ |
| Contagem de pétalas vai de 1 a 15, implicitamente uniforme | [Culturas & Economia](crops.md#girassois-power-petalas) | ⏳ |
| Um cacto sozinho rende `tamanho²` | [Ordenação de Cactos](cactus-sorting.md) | ⏳ |
| Um campo ordenado paga como se tivesse sido colhido inteiro | [Ordenação de Cactos](cactus-sorting.md) | ⏳ |
| Árvores crescem mais devagar ao lado de outras árvores | [Culturas & Economia](crops.md#a-lista-completa) | ⏳ ainda sem script |
| Fertilizante tira exatamente 2s do tempo restante de crescimento | [Culturas & Economia](crops.md#agua-fertilizante) | ⏳ ainda sem script |

**Quando uma medição contradisser uma dessas páginas, a página é corrigida** e a correção fica
registrada no roadmap — igual às correções do Track 0.

## Uma segunda fonte de perguntas abertas: o interpretador de referência

O [Interpretador de Referência](../language/reference-interpreter.md) gera sua própria lista de
lacunas. Sempre que o modelo executável precisa consultar um número que as fontes oficiais nunca
deram, ele recusa — e cada recusa dessas está catalogada em
[`interpreter/UNSPECIFIED.md`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/interpreter/UNSPECIFIED.md).
Alguns coincidem com a tabela acima (tempo de crescimento, morte de abóbora, pétalas); outros o
modelo revelou por conta própria — por exemplo a **quantidade colhida**, para a qual as docs dão um
*tipo* mas nunca uma quantidade base. Trate esse arquivo como uma segunda fonte de itens ⏳,
derivada do código, ao lado de `farms/research/`.

## Rodando a batelada

Os scripts só rodam **dentro do jogo** — a linguagem é um interpretador próprio, então não há
como executá-los de um shell. A batelada é curta:

1. Abra o jogo e crie uma janela por script (o nome da janela é o nome do módulo — veja
   [Módulos & Imports](../language/modules-and-imports.md)).
2. Cole um script, aperte **Execute** e deixe terminar. O `pumpkin_death_rate.py` e o
   `sunflower_petals.py` são os lentos; ambos imprimem resultados parciais no caminho, então dá
   para parar antes e ainda ter um N utilizável.
3. Copie o conteúdo da janela de Output.
4. Os números substituem as linhas ⏳ acima, cada um com seu método, tamanho de amostra e o script
   que o produziu.

!!! warning "Estes scripts chamam `clear()` e `set_world_size()`"
    Eles limpam a fazenda e redimensionam o mundo de propósito, para partir de um estado
    conhecido. **Não rode num save com que você se importa** — use um save de rascunho, ou aceite
    que o campo será resetado. O `clear()` está documentado em
    [Peculiaridades da Linguagem](language-quirks.md#clear-e-o-botao-de-panico).

## Fontes

| Fato | Fonte |
|---|---|
| Todo custo em ticks da tabela acima | `builtins.py` canônico, `…\Languages\builtins.py` (shipado, CC0, 2321 linhas, 51 defs) |
| A divergência de `get_time()` | O mesmo arquivo vs. `farms/lib/__builtins__.py` neste repo |
| Métodos de medição | Os próprios scripts, em `farms/research/` |
