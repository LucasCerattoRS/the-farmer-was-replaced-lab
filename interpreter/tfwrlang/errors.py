"""Errors and the Unspecified registry.

The whole point of this package is to model the *documented* behaviour of the TFWR language
and to be loud wherever the official sources say nothing. That loudness lives here.

`Unspecified` is raised where the game's own docs decline to define an outcome. Every place we
raise it is catalogued in `UNSPECIFIED_CATALOG`, from which `interpreter/UNSPECIFIED.md` is
generated. A raised `Unspecified` is not a bug in the model — it is a Track 2 experiment waiting
to be run.
"""


class TfwrError(Exception):
    """Base class for everything this package raises."""


class TfwrSyntaxError(TfwrError):
    """The source is not valid TFWR syntax."""

    def __init__(self, message, line=None, col=None):
        self.message = message
        self.line = line
        self.col = col
        where = "" if line is None else f" (line {line}" + (f", col {col})" if col is not None else ")")
        super().__init__(message + where)


class NotSupported(TfwrError):
    """The source uses a construct that is outside the *documented* subset.

    This is deliberately distinct from a syntax error: it means "the parser understood you, but
    this feature is not part of the language the `language/` pages describe." Hitting it on a
    curated script is a finding — either the docs are incomplete or the script reaches past the
    documented subset.
    """


class TfwrRuntimeError(TfwrError):
    """A runtime fault the docs *do* define (e.g. reading an unassigned name)."""


class TfwrNameError(TfwrRuntimeError):
    """A name was read before it was ever assigned — a runtime error per `scopes.md`."""


# --------------------------------------------------------------------------------------------
# Unspecified: the catalogue of holes the official sources leave open.
# --------------------------------------------------------------------------------------------

UNSPECIFIED_CATALOG = {
    "truthiness": (
        "Truthiness of non-boolean values. operators.md only defines booleans in conditions and "
        "explicitly does not promise what a non-boolean means in `if`/`while`/`and`/`or`/`not`. "
        "The model refuses non-booleans in boolean context instead of borrowing Python's rules."
    ),
    "boolean-short-circuit": (
        "Whether `and`/`or` skip evaluating their second operand. operators.md does not state "
        "that short-circuit evaluation happens. The model evaluates left-to-right and skips the "
        "second operand, but records the choice here because it is observable when the skipped "
        "side has side effects."
    ),
    "call-stack-limit": (
        "The maximum recursion depth. language-quirks.md says the call stack is finite, but the "
        "actual limit is unmeasured (a Track 2 item). The model makes it a parameter and never "
        "invents a number."
    ),
    "grow-time": (
        "How long each entity takes to grow. crops.md asserts approximate seconds (~0.5s / ~4s / "
        "~7s ...) that were never measured. The world model refuses to advance growth unless a "
        "grow-time model is injected."
    ),
    "pumpkin-death-rate": (
        "The probability a pumpkin dies while growing. crops.md says 'about 1 in 5', unmeasured. "
        "The world model requires the rate to be injected."
    ),
    "sunflower-petals": (
        "The distribution of sunflower petal counts. Assumed 1-15, uniform, unverified. The world "
        "model requires the distribution to be injected."
    ),
    "drone-scheduling": (
        "How multiple drones are interleaved. Inter-drone ordering is the least documented part "
        "of the game. The model refuses `spawn_drone`/`wait_for` rather than invent a scheduler."
    ),
    "module-by-window-name": (
        "`import` resolves a module by the game window's name, not a file path. There is no "
        "file-system model for that here, so `import` is refused rather than faked."
    ),
    "default-arg-eval-time": (
        "When a default-argument expression is evaluated (at `def` time or at call time). The "
        "docs call `def` an assignment but never pin this down. The model evaluates defaults at "
        "call time and records the choice."
    ),
}


class Unspecified(TfwrError):
    """Raised where the official sources define no behaviour.

    `topic` must be a key in `UNSPECIFIED_CATALOG`.
    """

    def __init__(self, topic, detail=""):
        if topic not in UNSPECIFIED_CATALOG:
            raise KeyError(f"unknown Unspecified topic: {topic!r}")
        self.topic = topic
        self.detail = detail
        msg = f"[{topic}] {UNSPECIFIED_CATALOG[topic]}"
        if detail:
            msg += f"\n  -> {detail}"
        super().__init__(msg)


class Registry:
    """Records which Unspecified topics were reached during a run.

    Recording is distinct from raising: some holes (short-circuit, default-arg timing) get a
    modelled default *and* a recorded note, so a run can proceed while still surfacing the hole.
    """

    def __init__(self):
        self.hits = {}

    def record(self, topic, detail=""):
        if topic not in UNSPECIFIED_CATALOG:
            raise KeyError(f"unknown Unspecified topic: {topic!r}")
        self.hits.setdefault(topic, set())
        if detail:
            self.hits[topic].add(detail)

    def raise_(self, topic, detail=""):
        self.record(topic, detail)
        raise Unspecified(topic, detail)

    def topics(self):
        return sorted(self.hits)
