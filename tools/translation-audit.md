# Official pt-BR translation audit

Audit of the game's shipped Portuguese localisation against the English original, done
2026-07-21 as Track 4 of the [roadmap](../ROADMAP.md).

**Source under audit:** `…\StreamingAssets\Languages\PT\` vs `…\Languages\EN\` (CC0).
**Upstream repo:** <https://github.com/Timiodon/TFWR-Translations> — accepts pull requests.

## Why this audit exists

The upstream `Languages/README.md` says, in the developer's own words:

> Some of the translations are still machine translations though many have been revised or remade
> by translators. They are reasonably good, but there are sometimes errors, especially in the
> shorter strings.

This repo had just written ~1500 lines of careful pt-BR on exactly this subject matter (Track 1),
so it was well placed to check.

## Scope

| Area | Audited? | Why |
|---|---|---|
| `PT/docs/scripting/` (16 files) | ✅ yes | The language reference — this repo's area of expertise |
| `PT/Strings/` (14 files) | ✅ yes | Where the README says errors concentrate |
| `PT/docs/` root (`getting_started`, `output`, `backup`, …) | ✅ yes | Small and stable |
| `PT/docs/unlocks/` | ❌ **deliberately skipped** | The README states these files are likely to change and "there is no point in improving the current translations for those files" |

## Method

Mechanical checks first, then a semantic read of the technical pages.

1. **Structural** — every `@Key` marker in each `Strings/*.txt` compared EN vs PT.
2. **Placeholder integrity** — every `{0}` / `{{ something }}` compared. Breaking these breaks
   the game, so this was checked exhaustively.
3. **Numeric consistency** — all numbers extracted per string block and compared. A tick count or
   yield number that drifts in translation is a factual bug.
4. **Code-span consistency** — all `` `backtick` `` spans compared as multisets. Per the upstream
   guidelines, code must not be translated, so drift here is a strong error signal.
5. **Semantic read** — `scopes`, `sets`, `tuples`, `operators`, `variables` and others read
   line-by-line against the English.

Scripts used: `audit_pt.py` and `audit_docs.py` (throwaway, run from a scratch dir).

## Result: the translation is in good shape

This is the honest headline. The mechanical checks came back **completely clean**:

| Check | Result |
|---|---|
| Missing `@Key` entries in PT | **0** (only `languages.txt` is EN-only, which is by design) |
| Broken/missing placeholders | **0** |
| Numeric drift EN → PT | **0** |
| Code spans altered | **0 in `Strings/`** |
| Whole files missing | **0** |

The `code_tooltips.txt` line-count difference (EN 633 / PT 629) is wrapping, not missing content.

Code-span differences in `docs/` were all **translated comments and string literals inside
examples** (`#do something` → `#faça algo`, `"this is never printed"` →
`"isso nunca é impresso"`). That is correct, pedagogically desirable localisation — not an error,
and not proposed for change.

## Concrete errors found (2)

### 1. `PT/docs/scripting/operators.md:9` — an unlock name is translated

```
EN  For assignment operators you need to unlock the "Variables" unlock.
PT  Para operadores de atribuição, você precisa desbloquear o desbloqueio "Variáveis".
```

`Variables` is an **unlock name** (`Unlocks.Variables`), and the upstream guidelines are explicit:

> Names of items, entities, grounds, unlocks and leaderboards cannot be translated either,
> because things like 'Items.Carrot' are also a part of the code.

A player reading this looks for **"Variáveis"** in the research tree and finds **"Variables"**.
Secondary issue: *"desbloquear o desbloqueio"* repeats itself awkwardly in Portuguese.

**Proposed:** `Para operadores de atribuição, você precisa desbloquear "Variables".`

### 2. `PT/docs/scripting/tuples.md:26` — backticks on the wrong token

```
EN  `prints` (4,5)
PT  `imprime` (4,5)
```

The backticks sit on the verb instead of on the value, so **"imprime" renders as code**. The same
file gets it right eleven lines earlier — line 16 reads ``imprime `2` ``.

**Proposed:** ``imprime `(4,5)` `` — consistent with line 16.

*(The English original has the same misplaced backticks. The PT fix is worth making regardless,
since a Portuguese verb rendered as code is more obviously wrong than an English one.)*

## Deliberately **not** proposed

Judgment calls where changing upstream would be presumptuous:

- **`Sets` → "Conjuntos", `Dictionaries` → "Dicionários", `Lists` → "Listas"** as page titles and
  prose. The upstream guideline says code elements "such as 'dictionary' and 'while'" should stay
  untranslated even outside code blocks, which arguably makes these violations too. But the choice
  is applied **consistently across the entire pt-BR translation**, so reverting it is a large,
  opinionated stylistic PR nobody asked for. Flagging it here instead. Note the guideline *is*
  respected where it matters most: `while`, `for`, `break`, `global`, `True`/`False` are all
  correctly left in English.
- **Translated comments and strings inside code examples** — correct localisation, see above.
- **`scopes.md`** adding quotes around *"código espaguete"* where the English has none — a
  stylistic improvement, if anything.

## Terminology cross-check (both directions)

Checked whether this site should adopt the official terms, per the roadmap item.

| Term | Official pt-BR | This site | Verdict |
|---|---|---|---|
| scope | escopo | escopo | ✅ aligned |
| loop | loop (kept) | loop (kept) | ✅ aligned |
| statement / branch | declaração / desvio | instrução / ramo | Both fine; no change |
| unpack | desempacotar | desempacotar | ✅ aligned |
| truthiness | *(not covered)* | veracidade | Ours; official has no term |
| set / dict | Conjuntos / Dicionários | set / dict (kept in English) | **Ours is closer to the upstream guideline** — kept |

No changes to this site were required.

## Outcome

Both fixes submitted upstream as **[Timiodon/TFWR-Translations#32](https://github.com/Timiodon/TFWR-Translations/pull/32)**
(2026-07-21) — 2 files, +2/−2, mergeable clean. Credited to Lucas Ceratto (@LucasCerattoRS).
The audit found the PT localisation to be in good shape overall; these were the only two concrete
in-scope errors.
