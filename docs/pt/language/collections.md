# Coleções

Quatro tipos de contêiner, cada um atrás do seu próprio unlock de pesquisa: **listas**,
**dicionários**, **sets** e **tuplas**. Listas, dicts e sets compartilham a
[semântica de referência](values-and-variables.md#semantica-de-referencia-morde-nas-colecoes) que
torna os dados compartilháveis entre drones; tuplas são a exceção imutável.

Assinaturas de método e custos em ticks estão na
[referência da API](../api/reference.md#colecoes-listas-dicts-sets); esta página é sobre *quando e
por que* recorrer a cada uma.

## Listas

Ordenadas, indexadas do zero, mutáveis e iteráveis:

```python
entities = [Entities.Tree, Entities.Carrot, Entities.Pumpkin]
plant(entities[1])                 # Carrot

total = 0
for n in [4, 7, 2, 5]:
    total += n                     # 18
```

Os métodos de mutação — `append`, `insert`, `pop`, `remove` — são chamados no estilo de método e
cada um custa ticks (`insert`/`pop` custam mais quanto mais longe do fim você mexe). `len(list)`
dá o comprimento.

!!! note "Slicing funciona, mas as docs oficiais nunca mencionam"
    O interpretador do jogo aceita slices no estilo Python — o `maze_gold_dfs.py` inverte sua
    lista de direções com `ALL_DIRECTIONS[::-1]`, e ele roda. Mas slicing não aparece em **lugar
    nenhum** das fontes oficiais: `lists.md` documenta acesso por índice único (`entities[1]`) e os
    quatro métodos de mutação, e a classe `list` do `builtins.py` canônico expõe apenas `append` /
    `insert` / `pop` / `remove` / `len` / `__getitem__`. Nenhum `[start:stop:step]` em canto algum.
    Então é uma verdadeira **lacuna de documentação**, não uma limitação do jogo — registrada aqui
    porque o corpus é nossa evidência de que é suportado. O
    [Interpretador de Referência](reference-interpreter.md), que modela só o subconjunto
    *oficialmente documentado*, recusa slicing de propósito (`NotSupported`); essa recusa foi
    justamente o que revelou esta lacuna.

!!! warning "Semântica de referência — e mutar enquanto itera"
    `b = a` dá a `a` e `b` a **mesma** lista, então `b.pop()` esvazia `a` também. Duas
    consequências vivas neste repo: uma lista construída por um drone e lida por outro é de fato
    compartilhada, e iterar uma lista enquanto remove dela pula elementos — a fila de pedidos da
    policultura contorna isso iterando sobre uma *cópia* enquanto drena a original (veja o
    [Tutorial 05](../tutorials/05-polyculture.md)).

## Dicionários

Mapeiam chaves a valores, com busca rápida:

```python
rightOf = {North: East, East: South, South: West, West: North}
turn = rightOf[South]              # West
```

Adicione ou sobrescreva com `dict[key] = value` (chaves são únicas), delete com `dict.pop(key)`,
e teste pertencimento com `key in dict` — a guarda barata antes de uma busca. Iterar um dict
devolve suas **chaves**, sem ordem garantida:

```python
for key in dict:
    value = dict[key]
```

Dicionários são estruturais pelo repo afora: os mapas de direção (`rightOf`/`leftOf`/`oppositeOf`)
em `fastest_reset.py` giram uma orientação sem um `if`, e `get_cost(thing)` *devolve* um dict de
item → quantidade que o código de auto-unlock percorre com `for c in cost: farm_item(c, cost[c])`.

## Sets

Um dicionário com chaves mas sem valores — uma coleção não-ordenada de elementos únicos:

```python
seen = set()          # {} seria um DICT vazio, não um set
seen.add(North)
if North in seen:
    ...
```

`add` / `remove` para mudá-lo, `in` para testar pertencimento — e para testes de pertencimento
em muitos elementos, o `in` de um set é **bem mais rápido que o de uma lista**. Adicionar um
duplicado é um no-op porque os elementos são únicos. `maze_gold_16drones_bfs.py` usa um mapa
`visited` exatamente assim para impedir que sua busca re-pise em tiles.

## Tuplas

Grupos imutáveis de valores, criados por vírgula e desmontados por desempacotamento:

```python
point = 1, 2          # uma tupla
a, b = point          # desempacotada: a=1, b=2
```

Elas indexam como listas (`point[1]` é `2`) mas não podem ser alteradas após a criação —
`point[0] = 3` é um erro. Essa imutabilidade compra duas coisas que listas não podem oferecer:

- **Elas podem ser chaves de dicionário** — que é por que mapas coordenada → valor como
  `{(x, y): get_entity_type()}` funcionam.
- **São o jeito limpo de retornar vários valores** de uma função
  ([Funções & Escopo](functions-and-scope.md#valores-de-retorno-e-retornar-varios)), que é como
  `measure()` devolve um `(x, y)` para um tesouro ou alvo de labirinto.

---

Próximo: [Módulos & Imports](modules-and-imports.md) — dividir código entre arquivos sem
surpresas · volta para [Funções & Escopo](functions-and-scope.md).
