# Sobre o Jogo

*The Farmer Was Replaced* é um jogo de programação: você escreve código numa linguagem parecida
com Python para dirigir um drone agrícola, e a árvore de pesquisa te entrega recursos da
linguagem — loops, variáveis, funções, listas — como itens a destravar. Esta página é o relato
curto e totalmente citado de quem construiu o jogo e do que se sabe (e do que não se sabe)
publicamente sobre como ele funciona.

> Tudo aqui vem de arquivos que o jogo shippa no disco ou da página dele na Steam. Onde algo não
> é publicado, esta página diz isso em vez de chutar — veja [Fontes](#fontes).

## Quem fez

O jogo é essencialmente um **projeto solo**. O `credits.md` shipado lista uma única pessoa em
programação, game design *e* arte:

| Papel | Pessoa |
|---|---|
| Programação, Game Design e Arte | **Timon Herzog** |
| Música e Efeitos Sonoros | **Floris Demandt** |
| Key Art | **Stephanie Stutz** |
| Publicado por | **Metaroot** — Andri Weidmann, Flurin Weidmann, Nathalie Weidmann |

A Steam lista a desenvolvedora como **Timon Herzog** e a publicadora como **Metaroot** e
**Timon Herzog**.

## Histórico de lançamento

| Marco | Data |
|---|---|
| Lançamento em Early Access | **10 de fevereiro de 2023** |
| Lançamento 1.0 | **10 de outubro de 2025** |

Ambas as datas são as declaradas na [página da Steam](https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/)
(app ID `2060160`) — o jogo passou cerca de dois anos e meio em Early Access.

## Engine e linguagem

O jogo é feito em **Unity**. Isso é visível direto no diretório de instalação, que tem o layout
padrão do Unity: `UnityPlayer.dll`, `UnityCrashHandler64.exe`, uma pasta de runtime
`MonoBleedingEdge/`, e uma pasta `TheFarmerWasReplaced_Data/` com `StreamingAssets/`.

A linguagem dentro do jogo é um **interpretador próprio** para um subconjunto de Python — não é
CPython embutido. Ela tem semântica própria, que este site documenta na seção
[Linguagem](../language/values-and-variables.md): todo número é float, módulos são *janelas* em
vez de arquivos, e loops infinitos são seguros porque o runtime coloca um atraso entre iterações.

!!! warning "O que **não** é público"
    **Não existe devlog, postmortem ou artigo técnico publicado** sobre como o interpretador é
    implementado. Além de "Unity, interpretador próprio", os internals não estão documentados em
    lugar nenhum público.

    É por isso que este repo documenta **comportamento, não implementação**. Todo mecanismo
    descrito no site é rastreado até a doc shipada, o stub `builtins.py`, ou um script que de fato
    rodou — nunca até um chute sobre o que o interpretador faz por baixo. Uma explicação plausível
    que se revela errada é pior do que nenhuma explicação, e esse modo de falha já mordeu este
    repo uma vez.

## A decisão de licenciar a doc em CC0

A coisa mais incomum que o desenvolvedor fez, do ponto de vista de documentação: **o jogo shippa
a documentação interna inteira no disco, em domínio público.**

```
…\steamapps\common\The Farmer Was Replaced\
  TheFarmerWasReplaced_Data\StreamingAssets\Languages\
```

- O `LICENSE` naquela pasta é **CC0 1.0 Universal** — uma dedicação a domínio público.
- Ela contém **47 arquivos markdown por idioma, em 14 idiomas**, incluindo português, mais um stub
  canônico `builtins.py` da API (51 definições).
- O `Languages/README.md` explica o layout e convida a correções, e o desenvolvedor mantém um
  **repositório público de tradução que aceita pull requests**:
  <https://github.com/Timiodon/TFWR-Translations>.

O que isso habilita é exatamente este projeto. Como a doc é CC0, ela pode legalmente ser citada,
traduzida, reorganizada e expandida — então este site consegue derivar uma
[referência da linguagem](../language/values-and-variables.md) e uma
[referência da API](../api/reference.md) de uma fonte primária, em vez de chutar a partir do jogo.
O desenvolvedor também admite naquele README que parte das traduções é feita por máquina e pede
correções, o que é uma porta aberta para contribuir de volta.

!!! note "Derivado, não copiado"
    CC0 torna copiar legal, mas repetir o texto oficial não acrescenta nada. O valor que este repo
    agrega é síntese, cross-linking, e a evidência em código na pasta
    [`farms/`](https://github.com/LucasCerattoRS/the-farmer-was-replaced-lab/tree/main/farms).

## Créditos completos

Reproduzidos do `EN/docs/credits.md` shipado (CC0).

**Programação, Game Design e Arte** — Timon Herzog
**Música e Efeitos Sonoros** — Floris Demandt
**Key Art** — Stephanie Stutz

**Publicado pela Metaroot** — Andri Weidmann · Flurin Weidmann · Nathalie Weidmann

**Allcorrect** — Maria Pavlova (russo) · Evgeniia Ushakova (russo) · Melanie Chen (chinês) ·
Siyoon Ji (coreano) · Mina Horiba-Maguire (japonês) · Danil Belousov (Account Manager) ·
Elizaveta Shevchenko (Team Lead) · Yulia Tregubova (Project Manager)

**Contribuidores da Tradução Comunitária** — HoshiyomiLusia · Liuxun · Davide Altamura ·
Milan Tuma · Ivan Bondar · Jimmy Sheep · Taigo Nakajima · НУІ

**Moderadores do Discord** — MrBlobfish · Josh Markey · danielrab · Jeff Siebold aka Noon Knight

**Agradecimentos Especiais** — Jonas Bornhöft · ThatMerlinGuy · Zoroark Zwart ·
Ramón Buchenberger · Swiss Game Hub

## Fontes

| Afirmação | Fonte |
|---|---|
| Créditos, papéis, nomes de tradutores e moderadores | `…\Languages\EN\docs\credits.md` (shipado, CC0) |
| A doc é domínio público | `…\Languages\LICENSE` — CC0 1.0 Universal |
| 47 docs × 14 idiomas, `builtins.py` canônico | A própria pasta `Languages\` |
| O repo de tradução aceita PRs; parte das traduções é de máquina | `…\Languages\README.md` |
| A engine é Unity | Diretório de instalação: `UnityPlayer.dll`, `UnityCrashHandler64.exe`, `MonoBleedingEdge/` |
| Datas de lançamento, desenvolvedora, publicadora | [Página da Steam](https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/), app `2060160` |
| Internals do interpretador | **Não publicados.** Não existe devlog nem postmortem. |

---

!!! note "Projeto de fã, não-oficial"
    Este site não tem vínculo com a desenvolvedora ou a publicadora. Todo o conteúdo do jogo
    pertence aos seus respectivos donos.
