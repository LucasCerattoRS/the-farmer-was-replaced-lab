# Valores & Variáveis

A linguagem do jogo é um subconjunto de Python com as baterias removidas: a sintaxe é a do
Python, mas você só ganha as peças que a árvore de pesquisa já destravou. Esta seção documenta
esse subconjunto do chão pra cima. Comece por aqui — é o que é um valor, como os nomes os
seguram, e as duas coisas que pegam a galera de surpresa (todo número é float; coleções são
compartilhadas por referência).

> Derivado da documentação oficial `scripting/` do jogo (CC0) e conferido contra os scripts em
> [`farms/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/farms).

## Tudo numérico é float

Existe exatamente um tipo numérico e ele é de ponto flutuante. `2`, `5`, `-125` são todos
floats. A doc oficial de operadores afirma isso sem rodeios, e muda como você escreve código:

- `/` sempre devolve um float: `5 / 2` é `2.5`, nunca `2`. Quando você quer o inteiro arredondado
  pra baixo — um índice de lista, um número de coluna — use `//` (`5 // 2` é `2`).
- Contadores de loop, coordenadas e índices são floats que por acaso guardam valores inteiros.
  `range()` e a indexação de listas os aceitam porque o valor é inteiro, não porque exista um
  tipo `int` separado.

Os valores não-numéricos que você vai encontrar: booleanos (`True` / `False`), os enums
constantes (`Entities.Pumpkin`, `Items.Hay`, `North` — catalogados na
[referência da API](../api/reference.md)), a string ocasional (quase sempre um nome de janela
para `import` / `leaderboard_run`), e as [coleções](collections.md).

## Atribuição liga um nome a um valor

`=` guarda o valor à sua direita sob o nome à sua esquerda:

```python
a = 5
b = can_harvest()      # guarda o que a chamada devolveu
```

`=` atribui; `==` compara e devolve um bool. Confundir os dois é o bug clássico de estreia, e a
doc oficial cita isso pelo nome.

A atribuição aumentada atualiza um nome a partir do seu próprio valor atual — o motor de todo
contador feito à mão:

```python
i = 0
while i < a:
    do_a_flip()
    i += 1             # exatamente i = i + 1
```

Todos os `+= -= *= /= %=` existem. Os operadores de atribuição exigem o unlock **Variables**.

## Um nome é declarado ao atribuí-lo

Não há palavra-chave de declaração separada. A primeira atribuição cria o nome. Ler um nome que
nunca foi atribuído é um erro de **runtime** — não há etapa de compilação para pegar isso antes,
o que é uma [pegadinha](../mechanics/language-quirks.md#nome-indefinido-falha-em-runtime-nao-antes)
por si só. *Em qual* escopo um nome vive — uma função, ou o programa inteiro — é o assunto de
[Funções & Escopo](functions-and-scope.md).

## Semântica de referência morde nas coleções

Números e booleanos são copiados na atribuição. **Listas, dicts e sets não são** — atribuir uma
delas a um novo nome te dá um segundo nome para o *mesmo* objeto:

```python
a = [1, 2]
b = a
b.pop()
# a e b são AMBOS [1]
```

Isso não é uma armadilha a evitar, é o modelo a entender: é exatamente o que faz uma lista
compartilhada entre drones ser de fato compartilhada. O tratamento completo está em
[Coleções](collections.md); tuplas ficam de fora por serem imutáveis.

## Comentários, e o truque do tooltip

`#` inicia um comentário que vai até o fim da linha. Um caso especial vale decorar: **um
comentário na linha imediatamente acima de um `def` vira o tooltip de hover daquela função no
jogo.** Documentação embutida e de graça para os seus próprios ajudantes.

```python
# Varre uma coluna de cima a baixo, colhendo.
def sweep_column():
    ...
```

## Vendo valores: print vs quick_print

`print(x)` solta uma baforada de fumaça no ar acima do drone *e* uma linha na janela de Output;
custa ~1s. `quick_print(x)` pula o ar e só escreve no Output — use quando estiver despejando
muitos valores num loop. Junto com breakpoints e o modo passo a passo, esses são o depurador
inteiro.

---

Próximo: [Operadores](operators.md) — como esses valores se combinam ·
[Controle de Fluxo](control-flow.md) — como a execução ramifica e repete.
