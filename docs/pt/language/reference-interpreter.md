# Interpretador de Referência

!!! warning "Isto **não** é uma reimplementação do interpretador do jogo"
    O interpretador do próprio jogo é fechado — não há devlog, postmortem ou código-fonte
    publicados sobre ele (veja [Sobre o Jogo](../about/the-game.md)). Isto é um **modelo do
    comportamento documentado**: as mesmas afirmações que as páginas desta seção *Linguagem* fazem
    em prosa, numa forma que pode ser *executada e testada*. É deliberadamente pequeno, e nunca
    deve ser descrito como "como o jogo funciona por dentro" — apenas como "como a linguagem
    documentada se comporta."

Todas as outras páginas aqui escrevem o que a linguagem faz. Esta torna essa escrita
**executável**. Um pequeno interpretador tree-walking do subconjunto documentado de TFWR vive em
[`interpreter/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/interpreter)
— um lexer, um parser, um avaliador puro e um modelo de mundo — para que a prosa ganhe uma segunda
vida como código que ou concorda com as docs ou falha um teste.

## Por que fazer isso, se as docs já existem

Porque a prosa pode esconder um chute e o código não. O design transforma isso numa regra
mecânica:

> **Onde as fontes oficiais são silenciosas, o modelo levanta `Unspecified` em vez de silenciosamente
> herdar a resposta do Python.**

Isso inverte o risco de sempre. Num port comum para Python, cada canto indocumentado
silenciosamente faria *o que o CPython faz* — e você nunca perceberia que o modelo inventou uma
resposta. Aqui cada canto desses é **barulhento**: ele para e se nomeia. Todo `Unspecified` que o
modelo pode levantar está catalogado em
[`interpreter/UNSPECIFIED.md`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/interpreter/UNSPECIFIED.md),
e cada entrada é um experimento de [Números Medidos](../mechanics/measured-numbers.md) esperando
para ser rodado. Medir um deles transforma uma recusa num número documentado.

## O que ele cobre

| Camada | Arquivo | O que modela |
|---|---|---|
| **Front end** | `lexer.py`, `parser.py`, `nodes.py` | Blocos por indentação, a gramática completa de expressões, precedência de [Operadores](operators.md) |
| **Avaliador** | `interp.py` | Valores, operadores, `if`/`while`/`for`, `def`/chamada/`return`, escopo + `global` + closures, coleções |
| **Mundo** | `world.py`, `builtins.py` | Uma grade **toro** N×N, ground/entity/água, inventário, o contador de ticks, e os verbos documentados |

O front end é checado contra todo o corpus curado: `parse_corpus.py` faz o parse de **45 de 46**
scripts em [`farms/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/farms)
sem erros. O único que resiste — `maze_gold_dfs.py` — usa slicing de lista `a[i:j]`, que nenhuma
página desta seção documenta. Isso é registrado como um **finding**, não remendado: ou a linguagem
tem slicing e as docs estão incompletas, ou ela não tem e o script foi além do subconjunto. Até
ser medido no jogo, o estado honesto é "não documentado."

## O que ele recusa, e por quê

As recusas são o ponto, não uma falha. Cada uma cita a página que se recusa a definir o
comportamento:

- **Verdade de não-booleanos.** [Operadores](operators.md) define booleanos numa condição e nunca
  diz o que um não-booleano significa, então `if 5:` levanta `Unspecified('truthiness')` em vez de
  chutar que `5` é verdadeiro.
- **Ordenar não-números.** `< <= > >=` sobre não-números é um erro em tempo de execução —
  operators.md define ordenação apenas sobre números.
- **Os quatro números não medidos do jogo** — tempo de crescimento, taxa de morte de abóbora,
  distribuição de pétalas de girassol e quantidade colhida — são *injetados* no mundo. Seus padrões
  levantam `Unspecified` no instante em que são consultados, para que um script não possa rodar
  silenciosamente sobre um número chutado. Injete um modelo concreto e o mesmo script roda do
  início ao fim.
- **Drones.** `spawn_drone` / `wait_for` / `has_finished` levantam `Unspecified('drone-scheduling')`.
  A ordem entre drones é a parte menos documentada do jogo ([Drones](../mechanics/drones.md)), e não
  pode ser encontrada em fonte alguma — então uma recusa documentada *é* a entrega, não um
  escalonador inventado.

## Como rodar

Tudo roda a partir da raiz do repositório. Nenhum jogo é necessário — isto é Python puro.

```bash
# 1. Faz o parse de todo o corpus curado (front end)
python interpreter/parse_corpus.py

# 2. Roda os testes de comportamento — um por afirmação que as páginas de Linguagem fazem
pip install pytest
python -m pytest interpreter/tests/

# 3. Regenera o catálogo de comportamentos não especificados a partir do código
python interpreter/gen_unspecified.py          # escreve interpreter/UNSPECIFIED.md
python interpreter/gen_unspecified.py --check   # modo CI: falha se saiu de sincronia
```

A suíte de testes é a especificação tornada executável: cada teste nomeia a página cuja afirmação
ele fixa — que loops e ramificações não abrem escopo, que closures capturam, que a regra de tick de
dois preços vale, e que cada número não medido recusa em alto e bom som.

Usando o modelo de mundo diretamente, com números concretos injetados para um script poder rodar:

```python
import sys; sys.path.insert(0, "interpreter")
from tfwrlang import world as W
from tfwrlang.builtins import make_world_interpreter

models = W.ModelSet(grow=lambda e, elapsed: True, yield_=lambda e, size: 1.0)
interp, world = make_world_interpreter(world=W.World(size=8, models=models))
interp.run_source("""
for i in range(get_world_size()):
    if can_harvest():
        harvest()
    plant(Entities.Grass)
    move(East)
""")
print(world.ticks, world.num_items("Hay"))
```

## Deliberadamente fora do escopo

Nenhuma VM de bytecode, nenhum otimizador, nenhum back end de compilador — tree-walking é o ponto.
Nenhuma tentativa de reproduzir o timing real do jogo além dos custos de tick documentados, e
nenhuma reprodução do texto das mensagens de erro. Isto nunca vira um jeito headless de jogar: um
script curado rodando do início ao fim é um bônus, nunca um requisito.

## Fontes

| Afirmação | Fonte |
|---|---|
| O subconjunto da linguagem e sua semântica | As páginas desta seção *Linguagem*, cada uma derivada das docs oficiais CC0 `scripting/` |
| Cada custo de tick que o mundo cobra | A tabela ✅ com fonte em [Números Medidos](../mechanics/measured-numbers.md) |
| O toro, os verbos e as constantes | [Drones](../mechanics/drones.md), [Referência da API](../api/reference.md) |
| O que *não* é público sobre o interpretador real | [Sobre o Jogo](../about/the-game.md) |
