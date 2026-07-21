# Módulos & Imports

Um arquivo só fica ingerenciável rápido. `import` traz funções e globais de outro arquivo — mas o
sistema de módulos do jogo tem dentes de verdade, e errar nele custa colheitas. Este é o relato
canônico; a página de [Peculiaridades da Linguagem](../mechanics/language-quirks.md) guarda só as
surpresas de uma linha e aponta de volta pra cá.

## Um módulo é um arquivo, e o nome dele é um nome de janela

Seu código vive em **janelas**, e o nome de uma janela *é* o nome do módulo dela. Não há árvore de
diretórios para percorrer, então `import` recebe o nome literal na aba da janela:

```python
import module2
module2.print_x()      # alcance dentro dele com o operador .
```

Como o nome é o título da janela, os arquivos curados neste repo importam `ImportZyklus` /
`ImportzyklusZubehör` — os nomes de janela originais do save, não os nomes limpos de arquivo em
disco. O mesmo vale para o segundo argumento de `leaderboard_run` / `simulate`. **Renomeie uma
janela e todo `import` e `leaderboard_run` que a referenciava quebra silenciosamente, em
runtime.**

## Importar um arquivo o *executa*

O primeiro `import` de um arquivo **executa o arquivo inteiro**, e então te entrega os nomes que
ele definiu. Se aquele arquivo chama `harvest()`, importá-lo colhe. Importe de novo e nada
re-roda — o módulo fica **em cache** a partir da primeira execução.

Então imports têm efeitos colaterais, e a guarda contra os indesejados é `__name__`: ela é
`"__main__"` quando um arquivo é rodado diretamente, e o próprio nome do arquivo quando ele é
alcançado por `import`. A estrutura recomendada — direto da doc oficial — põe qualquer coisa que
só deveria rodar em execução direta atrás da guarda:

```python
a_global_variable = "global"

def main():
    a_local_variable = "local"
    # faz coisas

if __name__ == "__main__":
    main()
```

Defina seus globais importáveis no nível de topo; esconda o comportamento de rode-agora dentro de
`main()`.

## `import file` vs `from file import`

`from module2 import *` copia os globais do outro arquivo **para o seu próprio escopo** em vez de
namespaceá-los sob `module2`. A doc oficial recomenda contra por dois motivos: quebra sob imports
circulares (próxima seção), e uma colisão de nome pode silenciosamente sobrescrever uma das suas
próprias variáveis. **Prefira `import file` e alcance dentro com o ponto.**

## Imports circulares: de boa com `import`, quebrado com `from`

Dois arquivos importando um ao outro funciona — desde que você use `import` puro. Digamos que `a`
importa `b` e `b` importa `a`, e alguém roda `import a`:

```python
# arquivo a
import b
x = 0

# arquivo b
import a
def f():
    print(a.x)
```

`a` começa → bate em `import b` → `b` começa → bate em `import a`, encontra o módulo `a`
**meio-carregado** e guarda uma *referência* a ele → `b` define `f` → `a` retoma e faz `x = 0`.
Depois, `b.f()` imprime `0`, porque a referência agora aponta para o módulo terminado.

Troque por `from a import *` e a mesma caminhada quebra:

```python
# arquivo a
from b import *
x = 0

# arquivo b
from a import *
def f():
    print(x)
```

Agora `b` **desempacota um snapshot** de `a` no momento em que é alcançado — e `a` ainda não rodou
`x = 0`, então nada é copiado. Não há referência viva para se atualizar depois, então `b.f()`
falha num `x` inexistente. Esta é a razão concreta pela qual a doc te afasta de `from … import *`.

## O demo de ciclo do repo

`import_cycle_a.py` e `import_cycle_b.py` são um ciclo executável com os imports colocados
*dentro* das funções, então chamar entre eles produz recursão mútua entre dois arquivos — o que
corre direto na [pilha de chamadas finita](../mechanics/language-quirks.md#recursao-tem-limite-de-pilha).

---

Volta para [Funções & Escopo](functions-and-scope.md), ou o resumo do subconjunto-surpreendente
em [Peculiaridades da Linguagem](../mechanics/language-quirks.md).
