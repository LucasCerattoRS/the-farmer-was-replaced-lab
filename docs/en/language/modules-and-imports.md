# Modules & Imports

One file gets unmanageable fast. `import` pulls functions and globals in from another file —
but the game's module system has real teeth, and getting it wrong costs harvests. This is the
canonical account; the [Language Quirks](../mechanics/language-quirks.md) page keeps only the
one-line surprises and points back here.

## A module is a file, and its name is a window name

Your code lives in **windows**, and a window's name *is* its module name. There's no directory
tree to path into, so `import` takes the literal name on the window's tab:

```python
import module2
module2.print_x()      # reach into it with the . operator
```

Because the name is the window title, the curated files in this repo import `ImportZyklus` /
`ImportzyklusZubehör` — the original save window names, not the tidy filenames on disk. The same
is true of the second argument to `leaderboard_run` / `simulate`. **Rename a window and every
`import` and `leaderboard_run` that referenced it breaks silently, at runtime.**

## Importing a file *runs* it

The first `import` of a file **executes the entire file**, then hands you the names it defined.
If that file calls `harvest()`, importing it harvests. Import it again and nothing re-runs — the
module is **cached** from the first execution.

So imports have side effects, and the guard against unwanted ones is `__name__`: it's
`"__main__"` when a file is run directly, and the file's own name when it's reached through
`import`. The recommended structure — straight from the official docs — puts anything that
should only run on direct execution behind the guard:

```python
a_global_variable = "global"

def main():
    a_local_variable = "local"
    # do things

if __name__ == "__main__":
    main()
```

Define your importable globals at top level; hide the run-it-now behaviour inside `main()`.

## `import file` vs `from file import`

`from module2 import *` copies the other file's globals **into your own scope** instead of
namespacing them under `module2`. The official docs recommend against it for two reasons: it
breaks under import cycles (next section), and a name collision can silently overwrite one of
your own variables. **Prefer `import file` and reach in with the dot.**

## Import cycles: fine with `import`, broken with `from`

Two files importing each other works — as long as you use plain `import`. Say `a` imports `b`
and `b` imports `a`, and someone runs `import a`:

```python
# file a
import b
x = 0

# file b
import a
def f():
    print(a.x)
```

`a` starts → hits `import b` → `b` starts → hits `import a`, finds the **half-loaded** module `a`
and stores a *reference* to it → `b` defines `f` → `a` resumes and sets `x = 0`. Later, `b.f()`
prints `0`, because the reference now points at the finished module.

Swap in `from a import *` and the same walk breaks:

```python
# file a
from b import *
x = 0

# file b
from a import *
def f():
    print(x)
```

Now `b` **unpacks a snapshot** of `a` at the moment it's reached — and `a` hasn't run `x = 0`
yet, so nothing is copied. There's no live reference to catch up later, so `b.f()` fails on a
missing `x`. This is the concrete reason the docs steer you away from `from … import *`.

## The repo's cycle demo

`import_cycle_a.py` and `import_cycle_b.py` are a runnable cycle with the imports placed *inside*
the functions, so calling across them produces mutual recursion between two files — which runs
straight into the [finite call stack](../mechanics/language-quirks.md#recursion-has-a-stack-limit).

---

Back to [Functions & Scope](functions-and-scope.md), or the surprising-subset summary on
[Language Quirks](../mechanics/language-quirks.md).
