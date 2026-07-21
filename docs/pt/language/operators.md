# Operadores

Três famílias, todas tiradas do Python, todas limitadas pela
[regra do só-float](values-and-variables.md#tudo-numerico-e-float). A referência oficial as
lista; esta página adiciona a precedência, as lacunas honestas, e os operadores em que este repo
de fato se apoia.

## Aritméticos: `+ - * / // % **`

Como todo número é de ponto flutuante, a divisão é a que pega as pessoas:

| Operador | Exemplo | Resultado | Nota |
|---|---|---|---|
| `+` `-` `*` | `2 * 3` | `6` | soma, subtração, multiplicação |
| `/` | `5 / 2` | `2.5` | **sempre um float** |
| `//` | `5 // 2` | `2` | divisão arredondada pra baixo — o que você quer para índices e colunas |
| `%` | `5 % 2` | `1` | resto; `-2 % 6` dobra os negativos de volta pra faixa |
| `**` | `2 ** 10` | `1024` | potência; `(-5) ** 3` é `-125` (os parênteses importam) |

`%` justifica seu salário pelo repo afora: `hats[get_pos_x() % 5]` cicla chapéus por coluna em
`hat_parade.py`, e toda implantação multi-drone mapeia um índice de drone para uma faixa do campo
com `//` e `%`.

## Comparação: `== != < <= > >=`

Cada um devolve `True` ou `False`. `==` e `!=` comparam **quaisquer** valores, enums incluídos —
`get_entity_type() == Entities.Pumpkin` é a espinha dorsal de todo loop de sentir-e-agir. As
quatro ordenações (`< <= > >=`) são definidas **só para números**.

## Lógicos: `not and or`

Combinação booleana padrão: `not` inverte, `and` é verdadeiro só se ambos os lados forem, `or`
é verdadeiro se qualquer um dos lados for.

!!! warning "Duas coisas que a doc oficial *não* promete"
    **Avaliação em curto-circuito não é especificada.** O Python pula o lado direito de `a and b`
    quando `a` é falso; a doc do jogo nunca afirma que ele faz o mesmo. Não escreva
    `can_move(d) and move(d)` assumindo que `move` é pulado — trate ambos os lados como avaliados
    até confirmar o contrário dentro do jogo.

    **A veracidade (truthiness) de não-booleanos não é especificada.** Fique com condições
    booleanas de verdade (`n > 0`, `x in s`) em vez de depender de `if alguma_lista:` significar
    "não-vazia".

    Quando um mecanismo não é documentado, a regra deste repo é *não* depender dele — veja as
    [regras de base do projeto](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/blob/main/ROADMAP.md).

## Precedência

A doc oficial descreve a linguagem como um subconjunto de Python mas não imprime uma tabela de
precedência. Ela bate com a do Python: `**` liga mais forte, depois o `-` unário, depois
`* / // %`, depois `+ -`, depois as comparações, depois `not`, depois `and`, depois `or`. O
próprio exemplo `(-5) ** 3` da doc mostra por que você parenteza na dúvida — sem os parênteses o
`-` e o `**` brigam pelo `5`.

---

Próximo: [Controle de Fluxo](control-flow.md) — pondo condições para trabalhar · volta para
[Valores & Variáveis](values-and-variables.md).
