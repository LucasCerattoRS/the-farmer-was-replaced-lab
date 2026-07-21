# Collections

Four container types, each behind its own research unlock: **lists**, **dictionaries**,
**sets** and **tuples**. Lists, dicts and sets share the [reference semantics](values-and-variables.md#reference-semantics-bite-with-collections)
that make data sharable between drones; tuples are the immutable exception.

Method signatures and tick costs are in the [API reference](../api/reference.md#collections-lists-dicts-sets);
this page is about *when and why* to reach for each.

## Lists

Ordered, index-from-zero, mutable, and iterable:

```python
entities = [Entities.Tree, Entities.Carrot, Entities.Pumpkin]
plant(entities[1])                 # Carrot

total = 0
for n in [4, 7, 2, 5]:
    total += n                     # 18
```

The mutation methods — `append`, `insert`, `pop`, `remove` — are called method-style and each
costs ticks (`insert`/`pop` cost more the further from the end you touch). `len(list)` gives the
length.

!!! warning "Reference semantics — and mutating while iterating"
    `b = a` gives `a` and `b` the **same** list, so `b.pop()` empties `a` too. Two live
    consequences in this repo: a list built by one drone and read by another is genuinely
    shared, and iterating a list while removing from it skips elements — the polyculture order
    queue works around this by looping over a *copy* while it drains the original
    (see [Tutorial 05](../tutorials/05-polyculture.md)).

## Dictionaries

Map keys to values, with fast lookup:

```python
rightOf = {North: East, East: South, South: West, West: North}
turn = rightOf[South]              # West
```

Add or overwrite with `dict[key] = value` (keys are unique), delete with `dict.pop(key)`, and
test membership with `key in dict` — the cheap guard before a lookup. Iterating a dict yields
its **keys**, in no guaranteed order:

```python
for key in dict:
    value = dict[key]
```

Dictionaries are load-bearing across the repo: the direction maps
(`rightOf`/`leftOf`/`oppositeOf`) in `fastest_reset.py` turn a heading without a branch, and
`get_cost(thing)` *returns* a dict of item → amount that the auto-unlock code walks with
`for c in cost: farm_item(c, cost[c])`.

## Sets

A dictionary with keys but no values — an unordered collection of unique elements:

```python
seen = set()          # {} would be an empty DICT, not a set
seen.add(North)
if North in seen:
    ...
```

`add` / `remove` to change it, `in` to test membership — and for membership tests on many
elements, a set's `in` is **much faster than a list's**. Adding a duplicate is a no-op because
elements are unique. `maze_gold_16drones_bfs.py` uses a `visited` map exactly this way to keep
its search from re-treading tiles.

## Tuples

Immutable groups of values, created by comma and taken apart by unpacking:

```python
point = 1, 2          # a tuple
a, b = point          # unpacked: a=1, b=2
```

They index like lists (`point[1]` is `2`) but can't be changed after creation — `point[0] = 3`
is an error. That immutability buys two things lists can't offer:

- **They can be dictionary keys** — which is why coordinate → value maps like
  `{(x, y): get_entity_type()}` work.
- **They're the clean way to return several values** from a function
  ([Functions & Scope](functions-and-scope.md#return-values-and-returning-several)), which is
  how `measure()` hands back an `(x, y)` for a treasure or maze target.

---

Next: [Modules & Imports](modules-and-imports.md) — splitting code across files without
surprises · back to [Functions & Scope](functions-and-scope.md).
